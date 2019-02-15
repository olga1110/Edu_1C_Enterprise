# -*- coding: utf-8 -*-
from odoo import http

import skpy
import requests
import logging
import threading
import base64
import psycopg2


from odoo import api, http, registry, SUPERUSER_ID
from odoo.http import request
from odoo.tools import consteq, pycompat

_logger = logging.getLogger(__name__)



class SkypeListener(http.Controller, skpy.SkypeEventLoop):
    @http.route('/skype_listener', type='http', auth='user')
    def onEvent(self, event, req):
        if isinstance(event, skpy.SkypeNewMessageEvent):
            message = 'New message from user {} at {}: \'{} \''.format(event.msg.userId,
                                                                       event.msg.time.strftime(
                                                                           '%H:%M dd. %d.%m.%Y'),
                                                                       event.msg.content))
            env = api.Environment(SUPERUSER_ID, {})
            env['skype.thread'].message_process(None, message)

    @classmethod
    def _check_token(cls, token):
        base_link = request.httprequest.path
        params = dict(request.params)
        params.pop('token', '')
        valid_token = request.env['skype.thread']._notify_encode_link(base_link, params)
        return consteq(valid_token, str(token))

    @classmethod
    def _check_token_and_record_or_redirect(cls, model, res_id, token):
        comparison = cls._check_token(token)
        if not comparison:
            _logger.warning(_('Invalid token in route %s') % request.httprequest.url)
            return comparison, None, cls._redirect_to_messaging()
        try:
            record = request.env[model].browse(res_id).exists()
        except Exception:
            record = None
            redirect = cls._redirect_to_messaging()
        else:
            redirect = cls._redirect_to_record(model, res_id)
        return comparison, record, redirect




