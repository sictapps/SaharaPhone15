
{
    'name': 'POS Custom Receipt',
    'category': 'Sales/Point of Sale',
    'summary': 'This module is used to customized receipt of point of sale when a user adds a product in the cart and validates payment and print receipt, then the user can see the client name on POS Receipt. | Custom Receipt | POS Reciept | Payment | POS Custom Receipt',
    'description': "Customized our point of sale receipt",
    'version': '15.0.1.0',
    'author': "Mohammad Haitham Salman",
    'website': "https://www.s-apps.io/",
    'depends': ['base', 'point_of_sale'],
    'assets': {
        'web.assets_qweb': [
            "custom_pos_receipt/static/src/xml/pos.xml",
        ],
    },
    'installable': True,
}
