from num2words import num2words
from odoo import fields, api, models, _

from odoo import tools


class TextAccountMove(models.Model):
    _inherit = "account.move"

    invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,
                               default=lambda self: fields.Datetime.now(), states={'draft': [('readonly', False)]})
    sapps_text_amount = fields.Char(string="Total In Words", required=False, compute="amount_to_words")
    order_payment_method = fields.Char(string="payment type", required=False, compute="get_payment_type")
    #  order_discount = fields.Integer(string="discount", required=False,compute="get_order_discount")
    discount_total = fields.Monetary("Discount Total", compute='total_discount')
    #  salesperson_id = fields.Many2one('hr.employee', string='Salesperson',compute="get_order_line_salesperson_id")

    actual_vendor = fields.Many2one('res.partner', string='Actual Vendor', readonly=False)

    #    sahara_purchase_invoice_price_total = fields.Float(string="sahara purchase total price", required=False, compute="get_purchase_total_price" )

    #    @api.depends('amount_residual')
    #    def get_purchase_total_price(self):
    #        for rec in self:
    #             rec.sahara_purchase_invoice_price_total = (rec.amount_residual-((4.761*rec.amount_residual)/100)+((5*rec.amount_residual)/100))

    @api.depends('amount_total')
    def amount_to_words(self):
        for rec in self:
            rec.sapps_text_amount = num2words(rec.amount_total).upper()

    def get_order_line_salespersos(self, line):
        salespersons = []
        for rec in self:
            move_id = self.id
            pos_order = self.env['pos.order'].search([('account_move', '=', self.id)])
            pos_order_lines = self.env['pos.order.line'].search([('order_id', '=', pos_order.id)])
            if pos_order_lines:
                pos_order_line = pos_order_lines[0]
                salespersons.append({
                    'id': pos_order_line.salesperson_id,
                    'name': pos_order_line.salesperson_id.name
                })
        return salespersons

    @api.depends('pos_payment_ids')
    def get_payment_type(self):
        for rec in self:
            accountMoveInv = self.env['account.move'].search([('id', '=', (rec.id) + 1)])
            rec.order_payment_method = "-"
            for pos_payment_id in accountMoveInv.pos_payment_ids:
                if pos_payment_id.payment_method_id:
                    rec.order_payment_method = pos_payment_id.payment_method_id.name
                else:
                    rec.order_payment_method = "-"
        #    if rec.order_payment_method == "-":
        #         for item in rec._get_reconciled_info_JSON_values():
        #              rec.order_payment_method = item['journal_name']

    #  def get_order_discount(self):
    #     result = 0
    #     for rec in self.invoice_line_ids:
    #         result = result + rec.discount
    #     return result

    @api.depends('invoice_line_ids.quantity', 'invoice_line_ids.price_unit', 'invoice_line_ids.discount')
    def total_discount(self):
        for invoice in self:
            total_price = 0
            discount_amount = 0
            final_discount_amount = 0
            if invoice:
                for line in invoice.invoice_line_ids:
                    if line:
                        total_price = line.quantity * line.price_unit
                        if total_price:
                            discount_amount = total_price - line.price_subtotal
                            if discount_amount:
                                final_discount_amount = final_discount_amount + discount_amount
                invoice.update({'discount_total': final_discount_amount})

    def check_tax_amount(self, line):
        result = 0
        for rec in self:
            result = line.price_total / line.quantity
        return result

    def get_line_lots(self, line):
        lot_values = []
        move_id = line.move_id.id
        pos_order = self.env['pos.order'].search([('account_move', '=', line.move_id.id)])
        pos_order_line = self.env['pos.order.line'].search(
            [('order_id', '=', pos_order.id), ('product_id', '=', line.product_id.id)])
        lots = pos_order_line.pack_lot_ids or False
        if lots:
            for lot in lots:
                lot_values.append({
                    'product_name': lot.product_id.name,
                    'quantity': line.qty if lot.product_id.tracking == 'lot' else 1.0,
                    'uom_name': line.product_uom_id.name,
                    'lot_name': lot.lot_name,
                })
        if lot_values == []:
            move_id = line.move_id.id
            account_move = self.env['account.move'].search([('id', '=', line.move_id.id)])
            order_lines = self.env['stock.move.line'].search(
                [('picking_id', 'in', account_move.invoice_line_ids.sale_line_ids.order_id.picking_ids.ids),
                 ('product_id', '=', line.product_id.id)])
            if order_lines:
                for lot in order_lines:
                    obj = {
                        'product_name': lot.product_id.name,
                        'quantity': line.qty if lot.product_id.tracking == 'lot' else 1.0,
                        'uom_name': line.product_uom_id.name,
                        'lot_name': lot.lot_id.name,
                    }
                    if not obj in lot_values:
                        lot_values.append(obj)
        if lot_values == []:
            move_id = line.move_id.id
            account_move = self.env['account.move'].search([('id', '=', line.move_id.id)])
            stock_move = self.env['stock.move'].search([('purchase_line_id', '=', line.purchase_line_id.id)])
            order_lines = self.env['stock.move.line'].search(
                [('move_id', 'in', stock_move.ids), ('product_id', '=', line.product_id.id)])
            if order_lines:
                for lot in order_lines:
                    obj = {
                        'product_name': lot.product_id.name,
                        'quantity': line.qty if lot.product_id.tracking == 'lot' else 1.0,
                        'uom_name': line.product_uom_id.name,
                        'lot_name': lot.lot_id.name,
                    }
                    if not obj in lot_values:
                        lot_values.append(obj)

        return lot_values


class SaharaAccountPayment(models.Model):
    _inherit = "account.payment"

    duedate = fields.Date(string='Due Date', readonly=False)
    getDueDate = fields.Date(string='get Due Date', readonly=False, compute="computeDueDate")

    @api.depends('duedate')
    def computeDueDate(self):
        for rec in self:
            if rec.duedate:
                rec.getDueDate = self.duedate
            else:
                rec.getDueDate = self.date

    def _check_build_page_info(self, i, p):
        res = super(SaharaAccountPayment, self)._check_build_page_info(i, p)
        # res.getDueDate = '01/01/2022'
        for rec in self:
            # res.update(getDueDate= '01/01/2025'+str(rec.getDueDate))
            res.update(getDueDate=rec.getDueDate)
        return res

    @api.onchange('duedate')
    def onchange_duedate(self):
        self.getDueDate = self.duedate

    def _check_fill_line(self, amount_str):
        return amount_str or ''


class SaharaQrCode(models.Model):
    _inherit = 'res.company'

    qrcode = fields.Binary('qrcode', readonly=False)


class SaharaScannedEmirateId(models.Model):
    _inherit = 'res.partner'

    scannedEmirateId = fields.Binary('scannedEmirateId', readonly=False)
    scannedEmirateIdsecond = fields.Binary('scannedEmirateIdSecond', readonly=False)


# class saharaaccountmoveline(models.Model):
#     _inherit = 'account.move.line'

#     sahara_purchase_invoice_price = fields.Float(string="sahara purchase line price", required=False, compute="get_purchase_line_price" )

#     @api.depends('price_total')
#     def get_purchase_line_price(self):
#        for rec in self:
#             rec.sahara_purchase_invoice_price = (rec.price_total-((4.761*rec.price_total)/100)+((5*rec.price_total)/100))


class PosOrderSalesPersonReport(models.Model):
    _name = "report.pos.order.salesperson"
    _description = "Point of Sale Orders sales person Report"
    _auto = False
    _order = 'date desc'

    date = fields.Datetime(string='Order Date', readonly=True)
    order_id = fields.Many2one('pos.order', string='Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    state = fields.Selection(
        [('draft', 'New'), ('paid', 'Paid'), ('done', 'Posted'),
         ('invoiced', 'Invoiced'), ('cancel', 'Cancelled')],
        string='Status')
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    price_total = fields.Float(string='Total Price', readonly=True)
    price_sub_total = fields.Float(string='Subtotal w/o discount', readonly=True)
    total_discount = fields.Float(string='Total Discount', readonly=True)
    average_price = fields.Float(string='Average Price', readonly=True, group_operator="avg")
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    nbr_lines = fields.Integer(string='Sale Line Count', readonly=True)
    product_qty = fields.Integer(string='Product Quantity', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal')
    delay_validation = fields.Integer(string='Delay Validation')
    product_categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    invoiced = fields.Boolean(readonly=True)
    config_id = fields.Many2one('pos.config', string='Point of Sale', readonly=True)
    pos_categ_id = fields.Many2one('pos.category', string='PoS Category', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', readonly=True)
    session_id = fields.Many2one('pos.session', string='Session', readonly=True)
    margin = fields.Float(string='Margin', readonly=True)
    sales_person_id = fields.Many2one('hr.employee', string='sales person', readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(l.id) AS id,
                COUNT(*) AS nbr_lines,
                s.date_order AS date,
                SUM(l.qty) AS product_qty,
                SUM(l.qty * l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_sub_total,
                SUM(ROUND((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END, cu.decimal_places)) AS price_total,
                SUM((l.qty * l.price_unit) * (l.discount / 100) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS total_discount,
                CASE
                    WHEN SUM(l.qty * u.factor) = 0 THEN NULL
                    ELSE (SUM(l.qty*l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)/SUM(l.qty * u.factor))::decimal
                END AS average_price,
                SUM(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') AS INT)) AS delay_validation,
                s.id as order_id,
                s.partner_id AS partner_id,
                s.state AS state,
                s.user_id AS user_id,
                s.company_id AS company_id,
                s.sale_journal AS journal_id,
                l.product_id AS product_id,
                pt.categ_id AS product_categ_id,
                p.product_tmpl_id,
                ps.config_id,
                pt.pos_categ_id,
                s.pricelist_id,
                s.session_id,
                s.account_move IS NOT NULL AS invoiced,
                SUM(l.price_subtotal - l.total_cost / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS margin,
                l.salesperson_id As sales_person_id
        """

    def _from(self):
        return """
            FROM pos_order_line AS l
                INNER JOIN pos_order s ON (s.id=l.order_id)
                LEFT JOIN product_product p ON (l.product_id=p.id)
                LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                LEFT JOIN uom_uom u ON (u.id=pt.uom_id)
                LEFT JOIN pos_session ps ON (s.session_id=ps.id)
                LEFT JOIN res_company co ON (s.company_id=co.id)
                LEFT JOIN res_currency cu ON (co.currency_id=cu.id)
        """

    def _group_by(self):
        return """
            GROUP BY
                s.id, s.date_order, s.partner_id,s.state, pt.categ_id,
                s.user_id, s.company_id, s.sale_journal,
                s.pricelist_id, s.account_move, s.create_date, s.session_id,
                l.product_id,
                pt.categ_id, pt.pos_categ_id,
                p.product_tmpl_id,
                ps.config_id,
                l.salesperson_id
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._group_by())
                         )
