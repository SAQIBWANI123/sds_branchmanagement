from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_shopify_order = fields.Boolean(
        string='Is Shopify Order',
        default=False,
        readonly=False,
    )
    shopify_branch_id = fields.Many2one(
        'res.branch',
        string='Shopify Branch',
        domain=[('is_shopify_branch', '=', True)],
    )
    shopify_order_ref = fields.Char(string='Shopify Order Reference')
    # shopify_store_ref is defined on sale.order in shati_shopify_register_payment

    @api.model
    def _get_default_shopify_branch(self, company_id=None):
        """Return the first Shopify branch for the given company."""
        company_id = company_id or self.env.company.id
        return self.env['res.branch'].search([
            ('is_shopify_branch', '=', True),
            ('company_id', '=', company_id),
        ], limit=1, order='id')

    @api.model_create_multi
    def create(self, vals_list):
        # If the Shopify connector passes shopify ref/branch (or sets context flags),
        # automatically mark the order as Shopify.
        ctx_flag = self.env.context.get('is_shopify_order') or self.env.context.get('default_is_shopify_order')
        for vals in vals_list:
            branch_id = vals.get('branch_id')
            shopify_branch_id = vals.get('shopify_branch_id')

            if 'is_shopify_order' not in vals:
                is_shopify_by_ref = bool(vals.get('shopify_order_ref'))
                is_shopify_by_store_ref = bool(vals.get('shopify_store_ref'))
                is_shopify_by_shopify_branch = bool(shopify_branch_id)
                is_shopify_by_branch = False
                if branch_id:
                    is_shopify_by_branch = bool(self.env['res.branch'].browse(branch_id).is_shopify_branch)

                if ctx_flag or is_shopify_by_ref or is_shopify_by_store_ref or is_shopify_by_shopify_branch or is_shopify_by_branch:
                    vals['is_shopify_order'] = True

            if vals.get('is_shopify_order'):
                if shopify_branch_id:
                    vals['branch_id'] = shopify_branch_id
                elif branch_id and self.env['res.branch'].browse(branch_id).is_shopify_branch:
                    vals['shopify_branch_id'] = branch_id
                else:
                    company_id = vals.get('company_id') or self.env.company.id
                    default_shopify_branch = self._get_default_shopify_branch(company_id)
                    if not default_shopify_branch:
                        raise ValidationError(_(
                            "No Shopify branch is configured. "
                            "Please enable 'Is Shopify Branch' on at least one branch."
                        ))
                    vals['shopify_branch_id'] = default_shopify_branch.id
                    vals['branch_id'] = default_shopify_branch.id

            if vals.get('branch_id') and not vals.get('warehouse_id'):
                branched_warehouse = self.env['stock.warehouse'].search([
                    ('branch_id', '=', vals['branch_id'])
                ], limit=1)
                if branched_warehouse:
                    vals['warehouse_id'] = branched_warehouse.id
        return super().create(vals_list)

    def write(self, vals):
        if self.env.context.get('skip_shopify_branch_sync'):
            return super().write(vals)

        res = super().write(vals)

        for order in self:
            if not order.is_shopify_order:
                continue
            if order.shopify_branch_id and order.branch_id != order.shopify_branch_id:
                branched_warehouse = self.env['stock.warehouse'].search([
                    ('branch_id', '=', order.shopify_branch_id.id)
                ], limit=1)
                order.with_context(skip_shopify_branch_sync=True).write({
                    'branch_id': order.shopify_branch_id.id,
                    'warehouse_id': branched_warehouse.id if branched_warehouse else False,
                })
            elif not order.shopify_branch_id:
                if order.branch_id and order.branch_id.is_shopify_branch:
                    order.with_context(skip_shopify_branch_sync=True).write({
                        'shopify_branch_id': order.branch_id.id,
                    })
                else:
                    default_shopify_branch = order._get_default_shopify_branch(
                        order.company_id.id
                    )
                    if default_shopify_branch:
                        branched_warehouse = self.env['stock.warehouse'].search([
                            ('branch_id', '=', default_shopify_branch.id)
                        ], limit=1)
                        order.with_context(skip_shopify_branch_sync=True).write({
                            'shopify_branch_id': default_shopify_branch.id,
                            'branch_id': default_shopify_branch.id,
                            'warehouse_id': branched_warehouse.id if branched_warehouse else False,
                        })

        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Keep the res.branch relation in the module which owns res.branch.
    shopify_branch_id = fields.Many2one(
        'res.branch', string='Shopify Branch', copy=False,
    )

    def _get_linked_shopify_sale_order(self):
        self.ensure_one()
        orders = self.line_ids.sale_line_ids.order_id.filtered('is_shopify_order')
        if orders:
            return orders[0]
        if self.invoice_origin:
            origin_names = [name.strip() for name in self.invoice_origin.split(',') if name.strip()]
            if origin_names:
                return self.env['sale.order'].search([
                    ('name', 'in', origin_names),
                    ('is_shopify_order', '=', True),
                ], limit=1)
        return self.env['sale.order']


class SaleOrderShopifyBranchRules(models.Model):
    """
    Separate class for constraints/onchange to keep the main sync logic readable.
    """

    _inherit = 'sale.order'

    @api.onchange('branch_id')
    def _onchange_branch_id_shopify_only(self):
        for order in self:
            if not order.is_shopify_order:
                return
            if order.branch_id and not order.branch_id.is_shopify_branch:
                raise UserError(_(
                    "For Shopify orders, 'Branch' must be a Shopify branch. "
                    "Please select a branch where 'Is Shopify Branch' is enabled."
                ))
            if order.branch_id:
                order.shopify_branch_id = order.branch_id
            else:
                order.shopify_branch_id = False

    @api.constrains('is_shopify_order', 'branch_id', 'shopify_branch_id')
    def _check_shopify_branch(self):
        for order in self:
            if not order.is_shopify_order:
                continue
            if order.branch_id and not order.branch_id.is_shopify_branch:
                raise ValidationError(_(
                    "Shopify orders must use a Shopify branch in 'Branch'."
                ))
            if order.shopify_branch_id and not order.shopify_branch_id.is_shopify_branch:
                raise ValidationError(_(
                    "Shopify orders must use a Shopify branch in 'Shopify Branch'."
                ))
            if order.branch_id and order.shopify_branch_id and order.branch_id.id != order.shopify_branch_id.id:
                raise ValidationError(_(
                    "For Shopify orders, 'Branch' and 'Shopify Branch' must be the same."
                ))

    @api.onchange('shopify_branch_id')
    def _onchange_shopify_branch_id_sync(self):
        for order in self:
            if not order.is_shopify_order:
                return
            if order.shopify_branch_id and not order.shopify_branch_id.is_shopify_branch:
                raise UserError(_(
                    "For Shopify orders, 'Shopify Branch' must be a Shopify branch."
                ))
            if order.shopify_branch_id:
                order.branch_id = order.shopify_branch_id
                branched_warehouse = self.env['stock.warehouse'].search([
                    ('branch_id', '=', order.shopify_branch_id.id)
                ], limit=1)
                order.warehouse_id = branched_warehouse.id if branched_warehouse else False
            else:
                order.branch_id = False
