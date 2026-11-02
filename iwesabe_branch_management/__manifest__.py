# * coding: utf8 *
##############################################################################
#
#    Global Creative Concepts Tech Co Ltd.
#    Copyright (C) 2018TODAY iWesabe (<http://www.iwesabe.com>).
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'iwesabe Branch Management',
    'version': '19.0.1.0.0',
    'category': '',
    'description': """
        Branch
    """,
    'author': 'SmartDeskSolutions',
    'website': 'https://www.smartdesksolutions.com',
    'description':
        """
            This module allows to manage multiple branch or manage multiple unit or manage multiple 
            operation in Sales, Purchases, Accounting, Payment, Voucher, Accounting Reports
            inside single company.
        """,
    'depends': ['base', 'sale_management', 'account', 'shati_shopify_register_payment'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_branch.xml',
        'views/res_users.xml',
        'views/sale_order_shopify_view.xml',
        'views/account_move_shopify_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'images': ['static/description/banner.png'],
    'price': 49.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'installable': True,
    'application': True
}
