from num2words import num2words
from odoo import fields,api, models, _
class TextAccountMove(models.Model):
   _inherit = "account.move"
   sapps_text_amount = fields.Char(string="Total In Words", required=False, compute="amount_to_words" )
   order_payment_method = fields.Char(string="payment type", required=False, compute="get_payment_type" )
   @api.depends('amount_total')
   def amount_to_words(self):
       for rec in self:
            rec.sapps_text_amount = num2words(rec.amount_total).upper()

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