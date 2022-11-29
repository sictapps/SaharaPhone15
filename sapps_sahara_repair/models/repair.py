from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.float_utils import float_is_zero


class Repair(models.Model):
    _inherit = 'repair.order'

    transfer_material_count = fields.Integer(compute='_compute_transfer_material_count')
    transfer_product_count = fields.Integer(compute='_compute_transfer_product_count')

    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        readonly=True, required=True, states={'order': [('readonly', False)]})

    invoice_method = fields.Selection([
        ("none", "No Invoice"),
        ("b4repair", "Before Repair"),
        ("after_repair", "After Repair")], string="Invoice Method",
        default='after_repair', index=True, readonly=True, required=True,
        states={'order': [('readonly', False)]},
        help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.')

    product_qty = fields.Float(
        'Product Quantity',
        default=1.0, digits='Product Unit of Measure',
        readonly=True, required=True, states={'order': [('readonly', False)]})

    operations = fields.One2many(
        'repair.line', 'repair_id', 'Parts',
        copy=True, readonly=True, states={'confirmed': [('readonly', False)]})

    product_uom = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        readonly=True, required=True, states={'order': [('readonly', False)]},
        domain="[('category_id', '=', product_uom_category_id)]")

    state = fields.Selection([
        ('order', 'draft'),
        ('draft', 'Quotation'),
        ('cancel', 'Cancelled'),
        ('confirmed', 'Confirmed'),
        ('under_repair', 'Under Repair'),
        ('ready', 'Ready to Repair'),
        ('2binvoiced', 'To be Invoiced'),
        ('invoice_except', 'Invoice Exception'),
        ('done', 'Repaired')], string='Status',
        copy=False, default='order', readonly=True, tracking=True,
        help="* The \'Draft\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Ready to Repair\' status is used to start to repairing, user can start repairing only after repair order is confirmed.\n"
             "* The \'To be Invoiced\' status is used to generate the invoice before or after repairing done.\n"
             "* The \'Done\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order.")

    create_if_not_exists = fields.Boolean(string='Create If Not Exists')
    new_lot_if_not_exists = fields.Char(string='New Lot')
    is_internal = fields.Boolean(string='Internal')

    def _default_stock_location(self):
        default_location_id = self.env['ir.config_parameter'].sudo().get_param('repair.default_location')
        default_location = self.env["stock.location"].search([('id', '=', default_location_id)], limit=1)
        if default_location:
            return default_location.id
        return False

    location_id = fields.Many2one(
        'stock.location', 'Location',
        default=_default_stock_location,
        index=True, readonly=True, required=True,
        help="This is the location where the product to repair is located.",
        states={'order': [('readonly', False)], 'draft': [('readonly', True)]})

    def _prepare_if_not_exits_transfer(self, lot_id):
        stock_picking_type = self.env['ir.config_parameter'].sudo().get_param('repair.receipt_new_serial')
        pick_type_id = self.env['stock.picking.type'].search([('id', '=', stock_picking_type)], limit=1)
        move_lines = []
        # for move in self.operations:
        move_line = {
            'product_id': self.product_id.id,
            'product_uom': self.product_uom.id,
            'product_uom_qty': self.product_qty,
            'name': self.product_id.name,
            'company_id': self.company_id.id,
            'location_id': pick_type_id.default_location_src_id.id,
            'location_dest_id': pick_type_id.default_location_dest_id.id,
            'partner_id': self.partner_id.id,
        }

        move_lines.append(move_line)
        vals = [{'picking_type_id': pick_type_id.id,
                 'location_id': pick_type_id.default_location_src_id.id,
            'location_dest_id': pick_type_id.default_location_dest_id.id,
                 'origin': self.name,
                 'partner_id': self.partner_id.id,
                 'move_ids_without_package': move_lines,
                 'product_repair_id': self.id,
                 'owner_id': self.partner_id.id
                 }]
        picking = self.with_context(from_repair=True).env['stock.picking'].create(vals)
        picking.action_confirm()
        picking.action_assign()
        for line in picking.move_line_ids:
            line.write({'lot_id': lot_id.id})


    def action_confirm_quot(self):
        self.ensure_one()
        self.state = 'draft'

        if self.create_if_not_exists:
            exists = self.sudo().env['stock.production.lot'].search_count([('name', '=', self.new_lot_if_not_exists)])
            if exists:
                raise UserError(_("Already Exists"))
            lot_id = self.sudo().env['stock.production.lot'].create([{'name': self.new_lot_if_not_exists,
                                                               'product_id': self.product_id.id,
                                                               'company_id': self.env.company.id}])
            self.sudo()._prepare_if_not_exits_transfer(lot_id=lot_id)
            self.sudo().lot_id = lot_id
        else:
            stock_picking_type = self.env['ir.config_parameter'].sudo().get_param('repair.transfer_product_op')
            pick_type_id = self.env['stock.picking.type'].search([('id', '=', stock_picking_type)], limit=1)
            if self.is_internal:
                move_lines = []
                location_from = self.env['stock.warehouse'].search([], limit=1).lot_stock_id
                location_dest = int(self.env['ir.config_parameter'].sudo().get_param('repair.repair_area'))
                # for move in self.operations:
                move_line = {
                    'product_id': self.product_id.id,
                    'product_uom': self.product_uom.id,
                    'product_uom_qty': self.product_qty,
                    'name': self.product_id.name,
                    'company_id': self.company_id.id,
                    'location_id': location_from.id,
                    'location_dest_id': location_dest,
                }
                move_lines.append(move_line)
                vals = [{'picking_type_id': pick_type_id.id,
                         'location_id': location_from.id,
                         'location_dest_id': location_dest,
                         'origin': self.name,
                         'move_ids_without_package': move_lines,
                         'product_repair_id': self.id,
                         }]

            else:
                move_lines = []
                # for move in self.operations:
                move_line = {
                    'product_id': self.product_id.id,
                    'product_uom': self.product_uom.id,
                    'product_uom_qty': self.product_qty,
                    'name': self.product_id.name,
                    'company_id': self.company_id.id,
                    'location_id': pick_type_id.default_location_src_id.id,
                    'location_dest_id': pick_type_id.default_location_dest_id.id,
                    'partner_id': self.partner_id.id
                }
                move_lines.append(move_line)
                vals = [{'picking_type_id': pick_type_id.id,
                         'location_id': pick_type_id.default_location_src_id.id,
                         'location_dest_id': pick_type_id.default_location_dest_id.id,
                         'origin': self.name,
                         'partner_id': self.partner_id.id,
                         'move_ids_without_package': move_lines,
                         'product_repair_id': self.id,
                         'owner_id': self.partner_id.id
                         }]

            picking = self.with_context(from_repair=True).env['stock.picking'].create(vals)
            picking.action_confirm()
            picking.action_assign()
            for move_line in picking.move_line_ids:
                move_line.lot_id = self.lot_id

    @api.model
    def create(self, vals_list):
        res = super(Repair, self).create(vals_list)
        for item in res:
            service_product_id = self.env['ir.config_parameter'].sudo().get_param('repair.repair_service_product')
            if not service_product_id:
                raise UserError(_('Please Contact Administrator to Specify Repair Product Service'))
            service_product = self.env['product.product'].search([('id', '=', int(service_product_id))])
            fees = self.env['repair.fee'].sudo().new({
                                        'name': service_product.product_tmpl_id.name,
                                       'product_id':service_product.id,
                                        'repair_id': res.id,
                                        'price_unit': service_product.list_price,
                                        'product_uom': service_product.uom_id.id
                                    })
            item.sudo().fees_lines = fees
            item.state = 'order'
        return res

    def button_transfer_materials(self):
        self.ensure_one()
        stock_picking_type = self.env['ir.config_parameter'].sudo().get_param('repair.operation_type')
        pick_type_id = self.env['stock.picking.type'].search([('id', '=', stock_picking_type)], limit=1)
        move_lines = []
        for move in self.operations:
            move_line = {'product_id': move.product_id.id, 'product_uom': move.product_uom.id,
                         'product_uom_qty': move.product_uom_qty, 'name': move.name,
                         'company_id': self.company_id.id, 'location_id': pick_type_id.default_location_src_id.id,
                         'location_dest_id': pick_type_id.default_location_dest_id.id,
                         }

            move_lines.append(move_line)
        v_view_id = self.env['ir.ui.view'].search([('name', '=', 'stock.view_picking_form')]).id
        return {
            'type': 'ir.actions.act_window',
            'name': 'transfer',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(v_view_id, 'form')],
            'context': {'default_picking_type_id': pick_type_id.id, 'default_origin': self.name,
                        # 'default_location_src_id':  self.feed_location_src_id.id,
                        # 'default_location_dest_id': self.location_src_id.id,
                        # 'default_move_lines': [(0,0,mv) for mv in move_lines],
                        # 'default_partner_id': self.partner_id.id,
                        'default_move_ids_without_package': move_lines,
                        'from_repair': True,
                        'default_material_repair_id': self.id
                        }
        }

    def action_repair_invoice_create(self):
        super(Repair, self.with_context(repair=True)).action_repair_invoice_create()

    def action_repair_end(self):
        res = super(Repair, self).action_repair_end()
        return res

    @api.onchange('operations')
    def sapps_onchange_operations(self):
        for rec in self.operations:
            if rec.product_id:
                rec.price_unit = rec.product_id.standard_price

    def action_repair_start(self):
        # check if raw material is not in repair location
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        if self.filtered(lambda repair: any(op.product_uom_qty < 0 for op in repair.operations)):
            raise UserError(_("You can not enter negative quantities."))
        if self.product_id.type == 'consu':
            return self.action_repair_confirm()

        owner_id = self.partner_id
        if self.is_internal:
            owner_id = False
        for op in self.operations:
            available_qty_owner = self.env['stock.quant']._get_available_quantity(op.product_id, op.location_id,
                                                                                  owner_id=owner_id, strict=True)
            available_qty_noown = self.env['stock.quant']._get_available_quantity(op.product_id, op.location_id,
                                                                                  strict=False)
            # for available_qty in [available_qty_owner, available_qty_noown]:
            if float_compare(available_qty_noown, self.product_qty, precision_digits=precision) < 0:
                raise UserError(_("There isn't enough repair materials"))
        return super(Repair, self).action_repair_start()

    def button_transfer_product(self):
        self.ensure_one()
        stock_picking_type = self.env['ir.config_parameter'].sudo().get_param('repair.transfer_product_op2')
        pick_type_id = self.env['stock.picking.type'].search([('id', '=', int(stock_picking_type))], limit=1)
        move_lines = []
        # for move in self.operations:
        repair_area = self.env['ir.config_parameter'].sudo().get_param('repair.repair_area')
        repair_area_id = self.env["stock.location"].search([('id', '=', repair_area)], limit=1)
        move_line = {
            'product_id': self.product_id.id,
            'product_uom': self.product_uom.id,
            'product_uom_qty': self.product_qty,
            'name': self.product_id.name,
            'company_id': self.company_id.id,
            'location_id': pick_type_id.default_location_src_id.id ,
            'location_dest_id': pick_type_id.default_location_dest_id.id,
            'partner_id': self.partner_id.id
        }

        move_lines.append(move_line)
        v_view_id = self.env['ir.ui.view'].search([('name', '=', 'stock.view_picking_form')]).id
        return {
            'type': 'ir.actions.act_window',
            'name': 'transfer',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(v_view_id, 'form')],
            'context': {'default_picking_type_id': pick_type_id.id, 'default_origin': self.name,
                        # 'default_location_src_id':  self.feed_location_src_id.id,
                        # 'default_location_dest_id': self.location_src_id.id,
                        # 'default_move_lines': [(0,0,mv) for mv in move_lines],
                        'default_partner_id': self.partner_id.id,
                        'default_move_ids_without_package': move_lines,
                        'from_repair': True,
                        'default_product_repair_id': self.id,
                        'default_owner_id': self.partner_id.id
                        }
        }

    def action_validate(self):
        self.ensure_one()
        # check if product to repair is in repair area
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        repair_area = self.env['ir.config_parameter'].sudo().get_param('repair.repair_area')
        repair_area_id = self.env["stock.location"].search([('id', '=', repair_area)], limit=1)
        if self.is_internal:
            qty = self.env['stock.quant']._get_available_quantity(self.product_id, repair_area_id, lot_id=self.lot_id)
        else:
            qty = self.env['stock.quant']._get_available_quantity(self.product_id, repair_area_id, lot_id=self.lot_id, owner_id=self.partner_id)
        if float_compare(qty, self.product_qty, precision_digits=precision) < 0:
            raise UserError(_('Product is not in repair location'))

        self.action_repair_confirm()

    def action_view_transfer_materials(self):
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        # remove default filters
        action["context"] = {}
        lines = self.env['stock.picking'].search([('material_repair_id', '=', self.id)])
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = lines.id
        return action

    def action_view_transfer_products(self):
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        # remove default filters
        action["context"] = {}
        lines = self.env['stock.picking'].search([('product_repair_id', '=', self.id)])
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = lines.id
        return action

    def _compute_transfer_material_count(self):
        for rec in self:
            rec.transfer_material_count = len(self.env['stock.picking'].search([('material_repair_id', '=', rec.id)]))

    def _compute_transfer_product_count(self):
        for rec in self:
            rec.transfer_product_count = len(self.env['stock.picking'].search([('product_repair_id', '=', rec.id)]))

    def action_repair_done(self):
        """ Creates stock move for operation and stock move for final product of repair order.
        @return: Move ids of final products

        """
        if self.filtered(lambda repair: not repair.repaired):
            raise UserError(_("Repair must be repaired in order to make the product moves."))
        res = {}
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        Move = self.env['stock.move']
        for repair in self:
            # Try to create move with the appropriate owner
            if self.is_internal:
                owner_id = False
            else:
                owner_id = self.partner_id
            available_qty_owner = self.env['stock.quant']._get_available_quantity(repair.product_id, repair.location_id, repair.lot_id, owner_id=owner_id, strict=False)

            moves = self.env['stock.move']
            consumption_value = 0
            for operation in repair.operations:
                move = Move.create({
                    'name': repair.name,
                    'product_id': operation.product_id.id,
                    'product_uom_qty': operation.product_uom_qty,
                    'product_uom': operation.product_uom.id,
                    'location_id': operation.location_id.id,
                    'location_dest_id': operation.location_dest_id.id,
                    'move_line_ids': [(0, 0, {'product_id': operation.product_id.id,
                                           'lot_id': operation.lot_id.id,
                                           'product_uom_qty': 0,  # bypass reservation here
                                           'product_uom_id': operation.product_uom.id,
                                           'qty_done': operation.product_uom_qty,
                                           'package_id': False,
                                           'result_package_id': False,
                                           'location_id': operation.location_id.id, #TODO: owner stuff
                                           'location_dest_id': operation.location_dest_id.id,})],
                    'repair_id': repair.id,
                    'origin': repair.name,
                })
                moves |= move
                operation.write({'move_id': move.id, 'state': 'done'})
                consumption_value = consumption_value + operation.price_subtotal

            stock_picking_type = self.env['ir.config_parameter'].sudo().get_param('repair.transfer_product_op')
            pick_type_id = self.env['stock.picking.type'].search([('id', '=', int(stock_picking_type))], limit=1)
            wharehouse_location_id = self.env['stock.warehouse'].search([], limit=1).lot_stock_id
            move = Move.create({
                'name': repair.name,
                'product_id': repair.product_id.id,
                'product_uom': repair.product_uom.id or repair.product_id.uom_id.id,
                'product_uom_qty': repair.product_qty,
                'partner_id': repair.address_id.id,
                'location_id': pick_type_id.default_location_dest_id.id,
                'location_dest_id': pick_type_id.default_location_src_id.id if not self.is_internal else wharehouse_location_id.id,
                'move_line_ids': [(0, 0, {'product_id': repair.product_id.id,
                                           'lot_id': repair.lot_id.id,
                                           'product_uom_qty': 0,  # bypass reservation here
                                           'product_uom_id': repair.product_uom.id or repair.product_id.uom_id.id,
                                           'qty_done': repair.product_qty,
                                           'package_id': False,
                                           'result_package_id': False,
                                           'owner_id': owner_id.id if owner_id else False,
                                           'location_id': pick_type_id.default_location_dest_id.id, #TODO: owner stuff
                                           'location_dest_id': pick_type_id.default_location_src_id.id if not self.is_internal else wharehouse_location_id.id
                                          })],
                'repair_id': repair.id,
                'origin': repair.name,
            })
            consumed_lines = moves.mapped('move_line_ids')
            produced_lines = move.move_line_ids
            moves |= move
            moves._action_done()
            produced_lines.write({'consume_line_ids': [(6, 0, consumed_lines.ids)]})
            res[repair.id] = move.id

            #TODO put put the stock interm
            if len(self.operations) and self.is_internal:
                new_std_price = ((self.product_id.standard_price * self.product_id.qty_available) + consumption_value)/self.product_id.qty_available
                counterpart_account_id = self.operations[0].product_id.categ_id.property_stock_account_output_categ_id.id
                self.product_id.sudo().change_std_price_enhanced(new_std_price,
                                                                            counter_part_account_id=counterpart_account_id)
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def change_std_price_enhanced(self, new_price, counter_part_account_id=False):
        if self.filtered(lambda p: p.valuation == 'real_time') and not self.env[
            'stock.valuation.layer'].check_access_rights('read', raise_exception=False):
            raise UserError(_(
                "You cannot update the cost of a product in automated valuation as it leads to the creation of a journal entry, for which you don't have the access rights."))

        svl_vals_list = []
        company_id = self.env.company
        for product in self:
            if product.cost_method not in ('standard', 'average'):
                continue
            quantity_svl = product.sudo().quantity_svl
            if float_is_zero(quantity_svl, precision_rounding=product.uom_id.rounding):
                continue
            diff = new_price - product.standard_price
            value = company_id.currency_id.round(quantity_svl * diff)
            if company_id.currency_id.is_zero(value):
                continue

            svl_vals = {
                'company_id': company_id.id,
                'product_id': product.id,
                'description': _('Product value manually modified (from %s to %s)') % (
                    product.standard_price, new_price),
                'value': value,
                'quantity': 0,
            }
            svl_vals_list.append(svl_vals)
        stock_valuation_layers = self.env['stock.valuation.layer'].sudo().create(svl_vals_list)

        # Handle account moves.
        product_accounts = {product.id: product.product_tmpl_id.get_product_accounts() for product in self}
        am_vals_list = []
        for stock_valuation_layer in stock_valuation_layers:
            product = stock_valuation_layer.product_id
            value = stock_valuation_layer.value

            if product.type != 'product' or product.valuation != 'real_time':
                continue

            # Sanity check.
            if not product_accounts[product.id].get('expense'):
                raise UserError(_('You must set a counterpart account on your product category.'))
            if not product_accounts[product.id].get('stock_valuation'):
                raise UserError(_(
                    'You don\'t have any stock valuation account defined on your product category. You must define one before processing this operation.'))

            if value < 0:
                debit_account_id = counter_part_account_id if counter_part_account_id else product_accounts[product.id]['expense'].id
                credit_account_id = product_accounts[product.id]['stock_valuation'].id
            else:
                debit_account_id = product_accounts[product.id]['stock_valuation'].id
                credit_account_id = counter_part_account_id if counter_part_account_id else product_accounts[product.id]['expense'].id

            move_vals = {
                'journal_id': product_accounts[product.id]['stock_journal'].id,
                'company_id': company_id.id,
                'ref': product.default_code,
                'stock_valuation_layer_ids': [(6, None, [stock_valuation_layer.id])],
                'move_type': 'entry',
                'line_ids': [(0, 0, {
                    'name': _(
                        '%(user)s changed cost from %(previous)s to %(new_price)s - %(product)s',
                        user=self.env.user.name,
                        previous=product.standard_price,
                        new_price=new_price,
                        product=product.display_name
                    ),
                    'account_id': debit_account_id,
                    'debit': abs(value),
                    'credit': 0,
                    'product_id': product.id,
                }), (0, 0, {
                    'name': _(
                        '%(user)s changed cost from %(previous)s to %(new_price)s - %(product)s',
                        user=self.env.user.name,
                        previous=product.standard_price,
                        new_price=new_price,
                        product=product.display_name
                    ),
                    'account_id': credit_account_id,
                    'debit': 0,
                    'credit': abs(value),
                    'product_id': product.id,
                })],
            }
            am_vals_list.append(move_vals)

        account_moves = self.env['account.move'].sudo().create(am_vals_list)
        if account_moves:
            account_moves._post()
        product.standard_price = new_price