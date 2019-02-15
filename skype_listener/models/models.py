# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class SkypeConfig(models.Model):

    @api.multi
    def _send_to_channel(self, channel_name, message):
        notifications = []
        if channel_name == "skype.channel":
            channel = self._get_full_channel_name(channel_name)
            notifications.append([channel, message])
        else:
            for ps in self.env['pos.session'].search([('state', '!=', 'closed'), ('config_id', 'in', self.ids)]):
                channel = ps.config_id._get_full_channel_name(channel_name)
                notifications.append([channel, message])
        return 1

    @api.multi
    def _get_full_channel_name(self, channel_name):
        self.ensure_one()
        return '["%s","%s","%s"]' % (self._cr.dbname, channel_name, self.id)

    @api.multi
    def _notify(self, message):
        if not self:
            return
        message.ensure_one()
        notifications = self._channel_message_notifications(message)
        self.env['bus.bus'].sendone(notifications)

    @api.multi
    def _channel_message_notifications(self, message):
        message_values = message.message_format()[0]
        notifications = []
        for channel in self:
            notifications.append([(self._cr.dbname, 'skype.channel', channel.id), dict(message_values)])



