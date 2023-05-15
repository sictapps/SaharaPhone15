# -*- coding: utf-8 -*-
from ast import literal_eval

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custody_location = fields.Many2one('stock.location',domain="[('usage', '=', 'internal')]",string="Custody location", config_parameter='asset.custody_location')
    receiving_custody_picking_id = fields.Many2one('stock.picking.type',string="Assignment Custody Operation",domain="[('default_location_dest_id', '=', custody_location),('code','=','internal')]",config_parameter='asset.custody_Receiving')
    delivering_custody_picking_id = fields.Many2one('stock.picking.type', string="Return Custody Operation",
                                                   domain="[('default_location_src_id', '=', custody_location),('code','=','internal')]",
                                                   config_parameter='asset.custody_delivering')

    Maintenance_picking_ids = fields.Many2many('stock.picking.type',relation='maintenance_picking', string="Capital Internal Maintenance Operations",
                                               compute="_compute_pls_fields",inverse="_inverse_pls_fields_str")

    locked_location = fields.Boolean(compute='_compute_locked',default=False)
    Maintenance_picking_ids_str = fields.Char(string='Lead Scoring Frequency Fields in String',
                                                     config_parameter='asset.Maintenance_picking_ids')



    @api.depends('Maintenance_picking_ids_str')
    def _compute_pls_fields(self):
        """ As config_parameters does not accept m2m field,
            we get the fields back from the Char config field, to ease the configuration in config panel """
        for setting in self:
            if setting.Maintenance_picking_ids_str:
                names = setting.Maintenance_picking_ids_str.split(',')
                fields = self.env['stock.picking.type'].search([('sequence_code', 'in', names)])
                setting.Maintenance_picking_ids = fields
            else:
                setting.Maintenance_picking_ids = None

    def _inverse_pls_fields_str(self):
        """ As config_parameters does not accept m2m field,
            we store the fields with a comma separated string into a Char config field """
        for setting in self:
            if setting.Maintenance_picking_ids:
                setting.Maintenance_picking_ids_str = ','.join(
                    setting.Maintenance_picking_ids.mapped('sequence_code'))
            else:
                setting.Maintenance_picking_ids_str = ''



    def _compute_locked(self):
        if not self.custody_location:
            self.locked_location=False
        else:
            res= self.env['stock.picking'].search_count([('location_dest_id', '=',self.custody_location.id)])
            if res>0:
                self.locked_location = False
            else:
                self.locked_location = True
class ProductCategory(models.Model):
    _inherit = "product.category"

    is_asset_category = fields.Boolean(string="Is Fixed Asset")
class ProductTemplate(models.Model):
    _inherit = "product.template"

    can_be_asset = fields.Boolean(string="Can be Asset" ,default=False)
    show_asset_property = fields.Boolean(compute='_compute_check',default=False)

    @api.depends('categ_id','tracking','type')
    def _compute_check(self):
        for product in self:
            show_asset_property =False
            if product.categ_id.is_asset_category== True and product.tracking == 'serial' and product.type == 'product':
                show_asset_property=True
                product.can_be_asset=True
            product.show_asset_property=show_asset_property

    @api.model
    def create(self, values):
        result = super(ProductTemplate, self).create(values)
        if result.categ_id.is_asset_category == True:
            if result.tracking != 'serial' or result.type != 'product':
                raise UserError(_("Fixed Asset Product must be tracking by serial and it's type must be Storable Product "))
            else:
                result.can_be_asset = True


        return result

    @api.model
    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if self.categ_id.is_asset_category == True:
            if self.tracking != 'serial' or self.type != 'product':
                raise UserError(
                    _("Fixed Asset Product must be tracking by serial and his type must be Storable Product "))


        return result
class StockProductionAssetInherited(models.Model):
    _inherit = 'stock.production.lot'

    asset_id = fields.Many2many('account.asset',relation='product_asset', string="Related Assets")

    book_value = fields.Monetary(string='Book Value', readonly=True, compute='_compute_book_value')

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True ,compute='_compute_currency')
    has_asset = fields.Boolean(default=False, compute='_compute_has_asset')

    employee_id= fields.Many2one('res.users',string="assigned to",readonly=True )
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    tcp_operation = fields.Monetary(string='TCO/Operation Value', readonly=True, compute='_compute_operation_value')
    tcp_capital = fields.Monetary(string='TCO/Capital Value', readonly=True, compute='_compute_capital_value')

    classification_id = fields.Many2one('assetcalsification', string="asset classification")


    @api.depends('asset_id.book_value','asset_id.product_serials')
    def _compute_book_value(self):
        for record in self:
            value=0
            for asset in record.asset_id:
                x=len(asset.product_serials)
                value+= asset.book_value/x
            record.book_value = value

    @api.depends('asset_id.book_value', 'asset_id.product_serials')
    def _compute_capital_value(self):
        for record in self:
            book_value = 0
            orginal_value = 0
            for asset in record.asset_id:
                x = len(asset.product_serials)
                book_value += asset.book_value / x
                orginal_value+=asset.original_value / x

            record.tcp_capital = orginal_value-book_value


    def _compute_operation_value(self):
        for record in self:
            value = 0
            if record.analytic_account_id:
                items = self.env['account.analytic.line'].search([('account_id','=',record.analytic_account_id.id)])
                value = sum(sml.amount for sml in items)
            record.tcp_operation = value

    @api.depends('asset_id')
    def _compute_has_asset(self):
        for record in self:
            has_asset=False
            if record.asset_id:
               has_asset=True
            record.has_asset = has_asset



    def _compute_currency(self):
        for record in self:
            currency= False
            for asset in record.asset_id:
                currency = asset.currency_id
            record.currency_id = currency
class AccountAsset(models.Model):
    _inherit = 'account.asset'
    _description = 's-apps-asset-management.s-apps-asset-management'

    product_serials = fields.Many2many('stock.production.lot',relation='product_asset',
                                       domain="[('product_id.can_be_asset', '=', True)]",
                                       string="Related Product Serials")

    def force_delete(self):
        for asset in self:

            for mv in asset.depreciation_move_ids:
                mv.button_draft()
                mv.with_context(force_delete=True).unlink()
            asset.write({'state':'draft'})

            super(AccountAsset, self).unlink()
class asset(models.TransientModel):
    _name = 'asset'




    def force_delete(self):
        active_ids = self._context.get('active_ids', []) or []
        for asset in self.env['account.asset'].browse(active_ids):
            asset.force_delete()
        return {
            'name': _('Assets'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.asset',
            'view_id': False,
            'type': 'ir.actions.act_window',


        }
class AccountMove(models.Model):
    _inherit = 'account.move'


    def button_draft(self):
        super(AccountMove, self).button_draft()
        self._depreciate_resset()


    def _depreciate_resset(self):
        for move in self.filtered(lambda m: m.asset_id):
            asset = move.asset_id
            if asset.state in ('open', 'pause'):
                asset.value_residual += abs(sum(move.line_ids.filtered(lambda l: l.account_id == asset.account_depreciation_id).mapped('balance')))
            elif asset.state == 'close':
                asset.value_residual += abs(sum(move.line_ids.filtered(lambda l: l.account_id != asset.account_depreciation_id).mapped('balance')))
            else:
                raise UserError(_('You cannot post a depreciation on an asset in this state: %s') % dict(self.env['account.asset']._fields['state'].selection)[asset.state])
class assetStockPicking(models.Model):
    _inherit = "stock.picking"


    employee_id= fields.Many2one('hr.employee',string="assigned to")
    is_cusdoty_r = fields.Boolean(default=False)
    is_cusdoty_d = fields.Boolean( default=False)
    is_cusdoty = fields.Boolean( default=False)
    is_Maintenance = fields.Boolean( default=False)
    asset_model= fields.Many2one('account.asset',string="Asset Model",domain="[('state', '=', 'model')]")
    asset_serial= fields.Many2one('stock.production.lot',string="Asset Serial",domain="[('product_id.can_be_asset', '=', True)]")
    product_ids = fields.One2many('product.product', compute='_compute_product_ids')
    lots_ids = fields.One2many('stock.production.lot', compute='_compute_serial_ids')

    @api.onchange('picking_type_id','employee_id')
    def _compute_product_ids(self):
        Maintenance =False
        self.product_ids = False
        params = self.env['ir.config_parameter'].sudo()
        if params.get_param('asset.Maintenance_picking_ids'):
            Maintenance=params.get_param('asset.Maintenance_picking_ids').split(',')

        custody_Receiving = params.get_param('asset.custody_delivering')

        if self.picking_type_id.id == int(custody_Receiving) and self.employee_id:



            self.product_ids = self.env['custody'].search([('employee_id','=',self.employee_id.id)]).mapped('product_id')

        else:
            if Maintenance:
                if self.picking_type_id.sequence_code in Maintenance:
                    self.product_ids = self.env['product.product'].search([('can_be_asset','=',False)])
                else:
                    self.product_ids = self.env['product.product'].search([])
            else:
                self.product_ids= self.env['product.product'].search([])

    @api.onchange('picking_type_id', 'employee_id')
    def _compute_serial_ids(self):
        self.lots_ids = False
        params = self.env['ir.config_parameter'].sudo()
        custody_Receiving = params.get_param('asset.custody_delivering')

        if self.picking_type_id.id == int(custody_Receiving) and self.employee_id:


            self.lots_ids = self.env['custody'].search([('employee_id', '=', self.employee_id.id)]).mapped('serial_id')
        else:
            self.lots_ids = self.env['stock.production.lot'].search([])


    def _domain_desct_id(self):

        params = self.env['ir.config_parameter'].sudo()

        custody_location = params.get_param('asset.custody_delivering')

        return [('id', '!=', int(custody_location))]


    def _domain_rec_id(self):


        params = self.env['ir.config_parameter'].sudo()

        custody_location = params.get_param('asset.custody_location')

        return [('id', '!=', int(custody_location))]



    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_src_id,
        check_company=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]},domain=_domain_desct_id)
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_dest_id,
        check_company=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]},domain=_domain_rec_id)


    @api.onchange('location_id','location_dest_id','picking_type_id')
    def _compute_locked(self):
        Maintenance =False
        params = self.env['ir.config_parameter'].sudo()
        custody_delivering = params.get_param('asset.custody_delivering')
        custody_Receiving = params.get_param('asset.custody_Receiving')
        if params.get_param('asset.Maintenance_picking_ids'):
            Maintenance = params.get_param('asset.Maintenance_picking_ids').split(',')


        if  self.picking_type_id.id==int(custody_delivering) :
            self.is_cusdoty=True
            self.is_cusdoty_d = True
            self.is_cusdoty_r = False
        if self.picking_type_id.id==int(custody_Receiving):
            self.is_cusdoty=True
            self.is_cusdoty_r = True
            self.is_cusdoty_d = False
        if self.picking_type_id.id!= int(custody_delivering) and self.picking_type_id.id!=int(custody_Receiving):
            self.is_cusdoty=False
            self.is_cusdoty_d = False
            self.is_cusdoty_r = False


        if Maintenance:
            if self.picking_type_id.sequence_code in Maintenance:
                self.is_Maintenance =True
            else:
                self.is_Maintenance = False

        else:
            self.is_Maintenance =False

    def _action_done(self):


        if self.is_Maintenance:
            o_value=0
            mod=self.asset_model
            for line in self.move_ids_without_package.move_line_ids:
                o_value += line.product_id.standard_price * line.qty_done
            asset=self.env['account.asset'].create({
                'name':mod.name+' '+ self.asset_serial.name,
                'original_value':o_value,
                'method':mod.method,
                'method_period':mod.method_period,
                'method_number':mod.method_number,
                'company_id':mod.company_id.id,
                'account_asset_id':mod.account_asset_id.id,
                'account_depreciation_id':mod.account_depreciation_id.id,
                'account_depreciation_expense_id':mod.account_depreciation_expense_id.id,
                'journal_id':mod.journal_id.id,
                'asset_type': 'purchase',
                'product_serials':self.asset_serial


            })

        super(assetStockPicking, self)._action_done()
        if self.is_cusdoty_r:
            for line in self.move_ids_without_package.move_line_ids:
                res= self.env['custody'].search([('employee_id','=',self.employee_id.id),('product_id','=',line.product_id.id)])
                if len(res)>0:
                    res.write({'qty':res.qty+line.qty_done})
                else:
                    self.env['custody'].create(
                        {
                            'employee_id':self.employee_id.id,
                            'product_id':line.product_id.id,
                            'serial_id':line.lot_id.id,
                            'qty':line.qty_done
                        }
                    )
        if self.is_cusdoty_d:
            for line in self.move_ids_without_package.move_line_ids:
                res= self.env['custody'].search([('employee_id','=',self.employee_id.id),('product_id','=',line.product_id.id)])
                if len(res)>0:
                    if res.qty==line.qty_done:
                        res.unlink()
                    else:

                        res.write({'qty':res.qty-line.qty_done})
    def button_validate(self):


        if self.is_cusdoty_d:
            for line in self.move_ids_without_package.move_line_ids:
                res= self.env['custody'].search([('employee_id','=',self.employee_id.id),('product_id','=',line.product_id.id),
                                                 ('serial_id','=',line.lot_id.id)])

                if len(res)==0:

                    raise UserError(_("Product %s not assigned to %s") %(line.product_id.name,self.employee_id.name))
                if len(res)>0 and sum(l.qty for l in res)<line.product_uom_qty:
                    raise UserError(_("This number of product %s are not assigned to %s") % (line.product_id.name, self.employee_id.name))

        return super().button_validate()

    def action_assign(self):


        if self.is_cusdoty_d:
            for line in self.move_ids_without_package.move_line_ids:
                res= self.env['custody'].search([('employee_id','=',self.employee_id.id),('product_id','=',line.product_id.id),
                                                 ('serial_id','=',line.lot_id.id)])
                if len(res)==0:
                    raise UserError(_("Product %s not assigned to %s") %(line.product_id.name,self.employee_id.name))
                if len(res)>0 and sum(l.qty for l in res)<line.product_uom_qty:
                    raise UserError(_("This number of product %s are not assigned to %s") % (line.product_id.name, self.employee_id.name))

        return super().action_assign()


    @api.model
    def create(self, vals):
        res = super(assetStockPicking, self).create(vals)
        params = self.env['ir.config_parameter'].sudo()
        custody_delivering = params.get_param('asset.custody_delivering')
        custody_Receiving = params.get_param('asset.custody_Receiving')
        custody_location = params.get_param('asset.custody_location')

        if res.picking_type_id.id !=int(custody_Receiving) and res.picking_type_id.id !=int(custody_delivering):
            if res.location_id.id == int(custody_location) or res.location_dest_id.id == int(custody_location):
                raise UserError(
                    _("Custody Location Allowed To use in custody operation type only"))
        return res
class Cusdoty(models.Model):
    _name = "custody"

    employee_id= fields.Many2one('hr.employee',string="assigned to")
    product_id = fields.Many2one('product.product',"Product")
    serial_id = fields.Many2one('stock.production.lot',striing="Serial")
    qty = fields.Integer(string="Qty")
class assetcalsification(models.Model):
    _name = "assetcalsification"


    name = fields.Char(string="name")
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def action_get_custody(self):
        self.ensure_one()
        action_ref = self.env.ref('s-apps-asset-management.action_custody')
        if not action_ref:
            return False
        action_data = action_ref.read()[0]

        action_data['domain'] = [('employee_id', '=', self.id)]
        return action_data
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    is_cusdoty = fields.Boolean(compute='_check_custody')

    @api.depends('location_id')
    def _check_custody(self):
        for line in self:
            params = self.env['ir.config_parameter'].sudo()
            custody_location = params.get_param('asset.custody_location')
            if line.location_id.id == int(custody_location) or line.location_id.is_custody:
                line.is_cusdoty=True
            else:
                line.is_cusdoty = False
class Location(models.Model):
    _inherit = 'stock.location'

    employee_id= fields.Many2one('hr.employee',string="assigned to")
    is_custody = fields.Boolean( default=False)


















