# -*- coding: utf-8 -*-
try:
    import qrcode
except ImportError:
    qrcode = None
import base64
from io import BytesIO

from odoo import models, fields


class AccountMove(models.Model):
    """Adds one new, isolated Binary field to account.move for the
    "Thermal (POS Style)" report only. Does not touch the unrelated
    `qr_code` field already added by sahara_planet (different field name
    on purpose, to avoid any collision with that module's own compute).

    Encodes the company name and invoice number - the same real QR
    generation approach (qrcode pip lib + base64) already used in
    sahara_planet/models/qr_code.py, reused here rather than reinventing a
    second way to build a QR image.
    """
    _inherit = 'account.move'

    pos_style_qr_code = fields.Binary(
        string='Thermal (POS Style) QR Code',
        compute='_compute_pos_style_qr_code',
    )

    def _compute_pos_style_qr_code(self):
        for move in self:
            move.pos_style_qr_code = False
            if not qrcode:
                continue
            if not move.name or move.name == '/':
                continue
            qr_text = "%s\n%s" % (move.company_id.name or '', move.name)
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
            move.pos_style_qr_code = base64.b64encode(buffer.getvalue())
