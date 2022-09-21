# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IrModelFieldsLog(models.Model):
    _name = 'ir.model.fields.log'
    _description = 'Log model fields'

    model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade')
    fields_ids = fields.Many2many('ir.model.fields', 'ir_model_fields_log_fields', 'model_field_log_id', 'field_id',
                                  string='Fields to log')
    active = fields.Boolean('Active', default=True)

    @api.onchange('model_id')
    def onchange_model_id(self):
        self.fields_ids = False

    @api.model
    def _update_tracked_fields(self, model_name, fields):
        domain = [('model', '=', model_name)]
        model = self.env['ir.model'].search(domain)
        fields_to_consider = self.search([('model_id', '=', model.id)]).mapped('fields_ids').mapped('name')
        fields = fields.union(set(fields_to_consider))
        return fields

    # we have to deal with cache in the case of update or delete
    @api.model
    def create(self, vals):
        self.env['mail.thread']._get_tracked_fields.clear_cache(self)
        return super(IrModelFieldsLog, self).create(vals)

    def write(self, vals):
        self.env['mail.thread']._get_tracked_fields.clear_cache(self)
        return super(IrModelFieldsLog, self).write(vals)

    def unlink(self):
        self.env['mail.thread']._get_tracked_fields.clear_cache(self)
        return super(IrModelFieldsLog, self).unlink()

    @api.constrains('model_id', 'fields_ids')
    def _check_model_fields_coherence(self):
        if self.model_id and self.fields_ids:
            model_ids = self.fields_ids.mapped('model_id')
            if any(model.id != self.model_id.id for model in model_ids):
                raise UserError(_("One or many fields selected does not belong to selected model!"))
