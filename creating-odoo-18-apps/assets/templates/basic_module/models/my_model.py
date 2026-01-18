# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence', default=10)
    date = fields.Date(string='Date', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    user_id = fields.Many2one('res.users', string='Responsible',
                              default=lambda self: self.env.user)

    def action_confirm(self):
        """Confirm the record."""
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Only draft records can be confirmed.")
            record.state = 'confirmed'

    def action_done(self):
        """Mark as done."""
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        """Cancel the record."""
        for record in self:
            record.state = 'cancelled'

    def action_draft(self):
        """Reset to draft."""
        for record in self:
            record.state = 'draft'
