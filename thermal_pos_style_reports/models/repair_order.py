# -*- coding: utf-8 -*-
try:
    import qrcode
except ImportError:
    qrcode = None
import base64
from io import BytesIO

from odoo import models, fields


class RepairOrder(models.Model):
    """Same isolated QR approach as models/account_move.py in this module,
    applied to repair.order: encodes company name + repair order name
    (instead of the invoice number). Same qrcode pip lib, same pattern as
    sahara_planet/models/qr_code.py, reused rather than reinvented.
    """
    _inherit = 'repair.order'

    pos_style_qr_code = fields.Binary(
        string='Thermal (POS Style) QR Code',
        compute='_compute_pos_style_qr_code',
    )

    def _compute_pos_style_qr_code(self):
        for repair in self:
            repair.pos_style_qr_code = False
            if not qrcode:
                continue
            if not repair.name or repair.name == '/':
                continue
            qr_text = "%s\n%s" % (repair.company_id.name or '', repair.name)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=4,
                border=2,
            )
            qr.add_data(qr_text)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            repair.pos_style_qr_code = base64.b64encode(buffer.getvalue())
