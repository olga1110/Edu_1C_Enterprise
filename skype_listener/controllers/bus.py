# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, tools
from odoo.http import request, route
from odoo.addons.bus.controllers.main import BusController

import odoo.addons.skype_listener.config as config
import odoo.addons.skype_listener.models.skype_channel as skype_channel


class SkypeController(BusController):

    def _default_request_uid(self):
        return request.session.uid and request.session.uid or SUPERUSER_ID

    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            registry, cr, uid, context = request.registry, request.cr, request.session.uid, request.context
            new_channel = (request.db, skype_channel.Channel(config.login, config.password, config.token), request.uid)
            channels.append(new_channel)
        return super(SkypeController, self)._poll(dbname, channels, last, options)














