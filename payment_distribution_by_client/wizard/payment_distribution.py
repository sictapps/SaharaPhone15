# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError

class PaymentDistributionByClient(models.Model):
    _name = 'payment.distribution.by.client'
    _description = 'Payment Distribution'

    @api.model
    def _default_journal(self):
        journal = self.env['account.journal'].search([('type', 'in', ['bank', 'cash'])], limit=1)
        return journal.id if journal else False

    def _pre_payment(self):
        invoices = []
        res = {'invoice': 'out_invoice', 'bills': 'in_invoice', 'credit_note': 'in_refund', 'debit_note': 'out_refund'}
        domain = [('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                  ('invoice_user_id', 'in', self.partner_id.ids), ('payment_state', '=', 'not_paid')]
        invoice_ids = self.env['account.move'].search(domain).order_by('id')
        vv = self.env['account.move'].read_group(domain,
                                                 fields=['partner_id', 'amount_residual', 'currency_id:array_agg'],
                                                 groupby=['partner_id'], lazy='false')

    partner_id = fields.Many2one('res.users', string='Salesperson', required=True)
    payment_date = fields.Date("Payment Date", default=fields.Date.context_today)
    reference = fields.Char('Reference')
    payment_amount = fields.Float(string='Total Amount',compute='_compute_name', readonly=True)
    min_amount = fields.Float(string='min amount due',default=1000)
    distribution_line_ids = fields.One2many('payment.distribution.line.by.client', 'distribution_id', string='Partial Inovice Line')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type', 'in', ['cash', 'bank'])], default=_default_journal)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled')
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    is_posted = fields.Boolean(string="posted", default=False)
    @api.depends('distribution_line_ids')
    def _compute_name(self):
        res = 0
        for record in self:

            for line in record.distribution_line_ids:
                res += line.amount_to_pay
            record.payment_amount=res


    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.get_partner_invoices()

    @api.onchange('min_amount')
    def onchange_min(self):
        if self.partner_id:
            self.get_partner_invoices()

    def get_partner_invoices(self):
        invoices = []
        self.update({
            'distribution_line_ids': [(5, _, _)],
        })
        res = {'invoice': 'out_invoice', 'bills': 'in_invoice', 'credit_note': 'in_refund', 'debit_note': 'out_refund'}
        domain = [('move_type', 'in', ['out_invoice']), ('state', '=', 'posted'), ('invoice_user_id', 'in', self.partner_id.ids),  ('payment_state', 'in', ('not_paid','in_payment','partial'))]
        invoice_ids = self.env['account.move'].search(domain)
        domain_2 = [('move_type', 'in', ['out_invoice']), ('state', '=', 'posted'),
                  ('partner_id', 'in', invoice_ids.partner_id.ids),  ('payment_state', 'in', ('not_paid','in_payment','partial'))]

        vv = self.env['account.move'].read_group(domain_2, fields=['partner_id', 'amount_residual','currency_id:array_agg'],
                                                 groupby=['partner_id'], lazy='false')
        for v in vv:
            # pay_term_line_ids = v.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))

            domain = [ ('move_id.state', '=', 'posted'),
                       ('move_id.move_type', 'not in', ['out_invoice','in_invoice','in_refund']),
                      ('partner_id', '=', v['partner_id'][0]),('account_internal_type','=','receivable'),'|',
                       ('amount_residual', '!=', 0.0),
                      ('amount_residual_currency', '!=', 0.0)]
            domain.extend([('credit', '>', 0), ('debit', '=', 0)])


            # account_lines=self.env['account.move.line'].search(['|',('move_id','in',credit_notes.ids),('payment_id','in',payments.ids),('account_internal_type', '=', 'receivable'),('amount_residual','!=',0)])
            account_lines = self.env['account.move.line'].search(domain)
            real_payment =[]
            amount_residual=0
            for p in account_lines:
                x=p.amount_residual

                if x!=0:
                    real_payment.append(p)
                    amount_residual+=x
            if v['amount_residual']>=self.min_amount:
                invoices.append({
                    'partner_id': v['partner_id'][0],
                    'residual': v['amount_residual'],
                    'partner_amount_residual':-1*amount_residual,
                    'amount_to_pay':  False,
                    'currency_id':  v['currency_id'][0] or False
                })

        self.distribution_line_ids = [(0, 0, inv) for inv in invoices]

    def print(self):
        invoices = []

        res = {'invoice': 'out_invoice', 'bills': 'in_invoice', 'credit_note': 'in_refund', 'debit_note': 'out_refund'}

        total_residual =0
        count =0
        total=0

        for inv in self.distribution_line_ids:
            total_residual +=inv.residual

            total+=inv.amount_to_pay
            count +=1
            invoices.append({
                'partner_id': inv.partner_id.name,
                'date_invoice': inv.date_invoice,
                'residual': inv.residual,
                'partner_amount_residual':inv.partner_amount_residual,
                'amount_to_pay': inv.amount_to_pay or False,
                'currency_id': inv.currency_id and inv.currency_id.id or False,


            })
            if total>0:
                total_residual=0
                count =0
                invoices = []

                for inv in self.distribution_line_ids:
                    if inv.amount_to_pay>0:
                        total_residual +=inv.residual
                        count +=1
                        invoices.append({
                            'partner_id': inv.partner_id.name,
                            'date_invoice': inv.date_invoice,
                            'residual': inv.residual,
                            'partner_amount_residual':inv.partner_amount_residual,
                            'amount_to_pay': inv.amount_to_pay or False,
                            'currency_id': inv.currency_id and inv.currency_id.id or False,


                        })




        data = {
            'model_id': self.id,
            'company_name' :self.env.company.name,
            'sealman' : self.partner_id.name,
            'date' :self.payment_date,
            'total_amount' : self.payment_amount,
            'total_residual' : total_residual,
            'invoices': invoices,
            'count': count,


        }

        return self.env.ref('payment_distribution_by_client.action_report_payment_distribution').report_action(self, data=data)

    def _check_valid_payment(self):


        if self.distribution_line_ids.filtered(lambda x: x.currency_id != self.journal_id.company_id.currency_id):
           raise UserError(_("Journal and invoices must have same currency !"))

    def make_payment_distribution(self):
        self.ensure_one()
        self._check_valid_payment()

        for line in self.distribution_line_ids :
            move_lines = self.env['account.move.line']
            if line.amount_to_pay > 0 :
                payment_vals = {}


                vals = {'invoice': {'payment_type': 'inbound', 'partner_type': 'customer'},
                        'bills': {'payment_type': 'outbound', 'partner_type': 'supplier'},
                        'credit_note':{'payment_type': 'inbound', 'partner_type': 'supplier'},
                        'debit_note': {'payment_type': 'outbound', 'partner_type': 'customer'}}
                payment_vals.update(vals['invoice'])
                payment_vals.update({
                    'partner_id': line.partner_id and line.partner_id.id,
                    'journal_id': self.journal_id and self.journal_id.id or False,
                    'date': self.payment_date or self.Date.context_today(self),
                    'ref': self.reference or '',
                    'amount': line.amount_to_pay,
                    'payment_method_id': self.env.ref('account.account_payment_method_manual_in') and self.env.ref('account.account_payment_method_manual_in').id

                })
                payment = self.env['account.payment'].create(payment_vals)
                if payment:
                    self.distribution_line_ids.write({'payment_id': payment.id})
                    payment.action_post()
                lines_to_reconcile = self.distribution_line_ids.filtered(lambda x: x.payment_id)
                if not lines_to_reconcile or payment.state != 'posted':
                    raise UserError(_("Either payment not created or confirmed !"))



            domain_pay = [ ('move_id.state', '=', 'posted'),
                           ('move_id.move_type', 'not in', ['out_invoice', 'in_invoice','in_refund']),
                      ('partner_id', '=', line.partner_id.id),'|',
                      ('amount_residual', '!=', 0.0),
                      ('amount_residual_currency', '!=', 0.0),('account_internal_type', '=', 'receivable')]
            domain_pay.extend([('credit', '>', 0), ('debit', '=', 0)])
            account_lines = self.env['account.move.line'].search(domain_pay)

            domain = [('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                      ('partner_id', 'in', line.partner_id.ids), ('payment_state', 'in', ('not_paid','in_payment','partial'))]

            domain_3 = [('move_type', 'in', [ 'out_refund']), ('state', '=', 'posted'),
                        ('partner_id', 'in',line.partner_id.ids), ('payment_state', 'in', ('not_paid','in_payment','partial'))]

            credit_notes=self.env['account.move'].search(domain_3)

            invoices = self.env['account.move'].search(domain).sorted(key=lambda r: r.id)





            for p in account_lines:
                # p = self.env['account.move.line'].search([('payment_id', '=', payment_id.id), ('account_internal_type', '=', 'receivable')])


                for invoice_id in invoices:
                    if p.amount_residual == 0 or p.reconciled:
                        continue

                    invoice_id.js_assign_outstanding_line(p.id)
                    amount=0
                    # if invoice_id.amount_residual_signed ==0:
                    #     continue
                    # if abs(invoice_id.amount_residual_signed)>=abs(p.amount_residual):
                    #      amount=abs(p.amount_residual)
                    # else:
                    #     amount = invoice_id.amount_residual_signed
                    #
                    # invoice_move = invoice_id.line_ids.filtered(lambda r: not r.reconciled and r.account_id.internal_type in ('receivable'))
                    # # payment_move = payment_id.move_line_ids.filtered(lambda r: not r.reconciled and r.account_id.internal_type in ('receivable'))
                    # payment_move = p
                    # move_lines |= (invoice_move + payment_move)
                    #
                    # if line.currency_id and invoice_move and payment_move:
                    #
                    #     amount_reconcile_currency = line.currency_id.round(line.amount_to_pay )
                    #     self.env['account.partial.reconcile'].create({
                    #         'debit_move_id': invoice_move.id,
                    #         'credit_move_id': payment_move.id,
                    #         'amount': amount,
                    #         'debit_amount_currency': abs(invoice_move.amount_residual_currency),
                    #         'credit_amount_currency': abs(payment_move.amount_residual_currency),
                    #
                    #     })

                    # move_lines.reconcile()

        self.state = 'posted'
        self.is_posted=True

class PaymentDistributionByClientLine(models.Model):
    _name = 'payment.distribution.line.by.client'
    _description = 'Payment Distribution Line'


    distribution_id = fields.Many2one('payment.distribution.by.client', 'Distribution Wizard')
    amount_to_pay = fields.Monetary(string='Amount', required=True, default=0.0)
    date_invoice = fields.Date(string='Invoice Date', readonly=True)
    invoice_total = fields.Monetary(string='Invoice Total', readonly=True)
    residual = fields.Monetary(string='Amount Due', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    payment_id = fields.Many2one('account.payment', string="Payment", readonly=True)
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True ,default=lambda  self:self.env.company.currency_id)
    partner_amount_residual= fields.Monetary(string='partner Amount Residual', readonly=True)

    @api.onchange('partner_id')
    def onchange_partner(self):

        for rec in self:


            domain_2 = [('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                        ('partner_id', 'in', rec.partner_id.ids), ('payment_state', '=', 'not_paid')]

            vv = self.env['account.move'].read_group(domain_2,
                                                     fields=['partner_id', 'amount_residual', 'currency_id:array_agg'],
                                                     groupby=['partner_id'], lazy='false')

            domian_payment = [('partner_id', 'in', rec.partner_id.ids)]
            payments = self.env['account.payment'].search(domian_payment)
            domain_all = [('move_id.state', '=', 'posted'),
                      ('move_id.move_type', 'not in', ['out_invoice', 'in_invoice', 'in_refund']),
                      ('partner_id', '=', rec.partner_id.ids), ('account_internal_type', '=', 'receivable'), '|',
                      ('amount_residual', '!=', 0.0),
                      ('amount_residual_currency', '!=', 0.0)]

            account_lines = self.env['account.move.line'].search(
                [('payment_id', 'in', payments.ids), ('account_internal_type', '=', 'receivable'),('amount_residual', '!=', 0)])
            real_payment = []
            amount_residual = 0
            for p in account_lines:
                x = p.amount_residual

                if x != 0:
                    real_payment.append(p)
                    amount_residual += x

            if vv:
                rec.residual= vv[0]['amount_residual']
                rec.partner_amount_residual= -1 * amount_residual
                rec.amount_to_pay= False
                rec.currency_id= vv[0]['currency_id'][0] or False
            else:
                rec.residual = 0
                rec.partner_amount_residual = -1 * amount_residual
                rec.amount_to_pay = False
                rec.currency_id = self.env.company_id.currency_id or False


    @api.onchange('amount_to_pay')
    def onchange_amount(self):
       self.distribution_id._compute_name()


