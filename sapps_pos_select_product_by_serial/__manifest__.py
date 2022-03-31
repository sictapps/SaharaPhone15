{
    # "price": "550",
    "name": "POS Scan Product by Serial",
    "version": "1.0",
    "category": "Point of Sale",
    "author": "Sapps",
    "summary":
        """ This extnsion allow POS user to scan product serial and
         automatically create order with product and serial""",
     'description': """test""",
    # "sequence": 0,
    'depends': [
        "point_of_sale", 'sale_management', 'barcodes', 'sale'
    ],
    'data': [
        'views/view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sapps_pos_select_product_by_serial/static/src/js/**/*',
        ],
    },
    "currency": "EUR",
    "installable": True,
}
