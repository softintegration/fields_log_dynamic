# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @tools.ormcache('self.env.uid', 'self.env.su')
    def _get_tracked_fields(self):
        """ Return the set of tracked fields names for the current model. """
        fields = super(MailThread, self)._get_tracked_fields()
        # here we have to add the dynamic log fields
        # note that we have to pass the self._name as argument to give the concerned model to the configurator
        return self.env['ir.model.fields.log'].sudo()._update_tracked_fields(self._name, fields)
