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

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class BranchGroup(models.Model):
    _name = 'res.branch.group'
    _description = "Branch Group"
    _check_company_auto = True

    name = fields.Char(
        "Branch Group", 
        required=True, 
        translate=True
    )
    company_id = fields.Many2one(
        'res.company', 
        required=True, 
        default=lambda self: self.env.company
    )
    excluded_branch_ids = fields.Many2many(
        'res.branch', 
        string="Excluded Branches", 
        domain="[('company_id', '=', company_id)]",
        check_company=True
    )
    sequence = fields.Integer(
        default=10
    )

    _sql_constraints = [
        (
            'uniq_name', 
            'unique(company_id, name)', 
            'A branch group name must be unique per company.'
        ),
    ]


class BranchBranch(models.Model):
    _name = 'res.branch'
    _description = "Branch"

    branch_code = fields.Char('Branch Code/Ref.')
    name = fields.Char('Name', required=True)
    is_shopify_branch = fields.Boolean('Is Shopify Branch')
    address = fields.Text('Branch Address')
    telephone_no = fields.Char('Telephone No.')
    gst_no = fields.Char('GSTIN')
    state_id = fields.Many2one('res.country.state', 'State')
    company_id = fields.Many2one('res.company', 'Company', required=True)
    term_conditions = fields.Text('Terms and Conditions (Quotation/Order)')
    term_conditions1 = fields.Text('Terms and Conditions (Invoice)')
    term_conditions_proforma = fields.Text('Terms and Conditions (Proforma)')
    term_conditions_purchase = fields.Text('Terms and Conditions (Purchase)')
