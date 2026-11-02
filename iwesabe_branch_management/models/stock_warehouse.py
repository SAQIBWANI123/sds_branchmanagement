from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_id = fields.Many2one(
        'res.branch',
        string='Branch',
        index=True,
    )