# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    branch_id = fields.Many2one(
        'res.branch',
        string='Branch',
        copy=False,
        index=True,
    )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    branch_id = fields.Many2one(
        'res.branch',
        string='Branch',
        copy=False,
        index=True,
    )