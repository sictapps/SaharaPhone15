from num2words import num2words
from odoo import fields,api, models, _
class TextAccountMove(models.Model):
   _inherit = "account.move"
   sapps_text_amount = fields.Char(string="Total In Words", required=False, compute="amount_to_words" )
   order_payment_method = fields.Char(string="payment type", required=False, compute="get_payment_type" )
  #  order_discount = fields.Integer(string="discount", required=False,compute="get_order_discount")
   discount_total = fields.Monetary("Discount Total",compute='total_discount')
    #  salesperson_id = fields.Many2one('hr.employee', string='Salesperson',compute="get_order_line_salesperson_id")

   @api.depends('amount_total')
   def amount_to_words(self):
       for rec in self:
            rec.sapps_text_amount = num2words(rec.amount_total).upper()
  
   def get_order_line_salespersos(self,line):
       salespersons = []
       for rec in self:
            move_id = line.move_id.id
            pos_order = self.env['pos.order'].search([('account_move','=',line.move_id.id)])
            pos_order_line = self.env['pos.order.line'].search([('order_id','=',pos_order.id),('product_id','=',line.product_id.id)])
            salespersons.append({
                                'id': pos_order_line.salesperson_id,
                                'name': pos_order_line.salesperson_id.name
                            })
       return salespersons


   @api.depends('pos_payment_ids')
   def get_payment_type(self):
       for rec in self:
           accountMoveInv = self.env['account.move'].search([('id','=',(rec.id)+1)])
           rec.order_payment_method = "-" 
           for pos_payment_id in accountMoveInv.pos_payment_ids:
                if pos_payment_id.payment_method_id:
                  rec.order_payment_method =pos_payment_id.payment_method_id.name
                else:
                  rec.order_payment_method = "-"  
  
  #  def get_order_discount(self):
  #     result = 0
  #     for rec in self.invoice_line_ids:
  #         result = result + rec.discount
  #     return result  

   @api.depends('invoice_line_ids.quantity','invoice_line_ids.price_unit','invoice_line_ids.discount')
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
                invoice.update({'discount_total':final_discount_amount})
   
   def check_tax_amount(self,line):
      result = 0
      for rec in self:
         result = line.price_total / line.quantity
      return result  

   def get_line_lots(self,line):
        lot_values = []
        move_id = line.move_id.id
        pos_order = self.env['pos.order'].search([('account_move','=',line.move_id.id)])
        pos_order_line = self.env['pos.order.line'].search([('order_id','=',pos_order.id),('product_id','=',line.product_id.id)])
        lots = pos_order_line.pack_lot_ids or False
        if lots:
          for lot in lots:
            lot_values.append({
                                'product_name': lot.product_id.name,
                                'quantity': line.qty if lot.product_id.tracking == 'lot' else 1.0,
                                'uom_name': line.product_uom_id.name,
                                'lot_name': lot.lot_name,
                            })
        if lot_values ==[]:
           move_id = line.move_id.id
           account_move = self.env['account.move'].search([('id','=',line.move_id.id)]) 
           order_lines = self.env['stock.move.line'].search([('picking_id','in',account_move.invoice_line_ids.sale_line_ids.order_id.picking_ids.ids),('product_id','=',line.product_id.id)])
           if order_lines:
              for lot in order_lines:
                lot_values.append({
                                    'product_name': lot.product_id.name,
                                    'quantity': line.qty if lot.product_id.tracking == 'lot' else 1.0,
                                    'uom_name': line.product_uom_id.name,
                                    'lot_name': lot.lot_id.name,
                                })
                            

        return lot_values



class SaharaAccountPayment(models.Model):
  _inherit = "account.payment"

  def _check_fill_line(self, amount_str):
        return amount_str or ''      

  # def _check_get_pages(self):
  #       """ Returns the data structure used by the template : a list of dicts containing what to print on pages.
  #       """
  #       stub_pages = self._check_make_stub_pages() or [False]
  #       pages = []
  #       new_Pages=[]
  #       for i, p in enumerate(stub_pages):
  #           pages.append(self._check_build_page_info(i, p))
  #       new_Pages.append(pages[0])    
  #       return new_Pages