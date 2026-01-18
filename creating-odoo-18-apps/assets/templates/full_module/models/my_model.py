# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, name'
    _rec_name = 'display_name'

    # -------------------------------------------------------------------------
    # FIELDS
    # -------------------------------------------------------------------------
    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        copy=False,
        default='New',
    )
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
    )
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string='Priority', default='0')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    # Relational fields
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
    )
    line_ids = fields.One2many(
        'my.model.line',
        'parent_id',
        string='Lines',
        copy=True,
    )
    tag_ids = fields.Many2many(
        'my.model.tag',
        string='Tags',
    )

    # Computed fields
    line_count = fields.Integer(
        string='Line Count',
        compute='_compute_line_count',
    )
    total_amount = fields.Monetary(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id',
    )

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS
    # -------------------------------------------------------------------------
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name, company_id)',
         'Reference must be unique per company!'),
    ]

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    @api.depends('partner_id.name', 'name')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id:
                record.display_name = f"{record.name} - {record.partner_id.name}"
            else:
                record.display_name = record.name

    @api.depends('line_ids')
    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.line_ids)

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('subtotal'))

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.user_id:
            self.user_id = self.partner_id.user_id

    # -------------------------------------------------------------------------
    # CONSTRAINT METHODS
    # -------------------------------------------------------------------------
    @api.constrains('date')
    def _check_date(self):
        for record in self:
            if record.date and record.date > fields.Date.today():
                raise ValidationError(_("Date cannot be in the future!"))

    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('my.model') or 'New'
        return super().create(vals_list)

    def unlink(self):
        for record in self:
            if record.state not in ('draft', 'cancelled'):
                raise UserError(_("You can only delete draft or cancelled records!"))
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = 'New'
        return super().copy(default)

    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------
    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Only draft records can be confirmed."))
            record.state = 'confirmed'

    def action_start(self):
        for record in self:
            record.state = 'in_progress'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_view_lines(self):
        self.ensure_one()
        return {
            'name': _('Lines'),
            'type': 'ir.actions.act_window',
            'res_model': 'my.model.line',
            'view_mode': 'tree,form',
            'domain': [('parent_id', '=', self.id)],
            'context': {'default_parent_id': self.id},
        }


class MyModelTag(models.Model):
    _name = 'my.model.tag'
    _description = 'My Model Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tag name must be unique!'),
    ]
