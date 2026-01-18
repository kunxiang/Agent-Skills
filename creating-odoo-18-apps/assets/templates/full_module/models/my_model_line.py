# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MyModelLine(models.Model):
    _name = 'my.model.line'
    _description = 'My Model Line'
    _order = 'sequence, id'

    parent_id = fields.Many2one(
        'my.model',
        string='Parent',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Description', required=True)
    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    quantity = fields.Float(
        string='Quantity',
        default=1.0,
        required=True,
    )
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
    )
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )
    company_id = fields.Many2one(
        related='parent_id.company_id',
        store=True,
    )
    currency_id = fields.Many2one(
        related='parent_id.currency_id',
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.list_price
