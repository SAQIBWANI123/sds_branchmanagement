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
    'name': 'iWesabe Branch Management',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Manage branches, user assignments and warehouses; trace Shopify orders and invoices in Odoo 19.',
    'author': 'SmartDeskSolutions',
    'website': 'https://www.smartdesksolutions.com',
    'description':
        """
            Manage company branches, assign main and allowed branches to users,
            group branches for reporting, and link warehouses to branches. Add
            branch information to accounting records and connect Shopify orders
            and invoices to branches and store references. Requires
            shati_shopify_register_payment in addition to Sales, Accounting,
            and Inventory.
        """,
    'depends': ['base', 'sale_management', 'account', 'stock', 'shati_shopify_register_payment'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_branch.xml',
        'views/res_users.xml',
        'views/stock_warehouse_views.xml',
        'views/account_move_views.xml',
        'views/sale_order_shopify_view.xml',
        'views/account_move_shopify_view.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'price': 49.00,
    'currency': 'EUR',
    'installable': True,
    'application': True
}
