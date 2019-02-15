# -*- coding: utf-8 -*-

import base64
import datetime
import dateutil
import hashlib
import hmac
import lxml
import logging
import pytz
import re
import socket
import time


from odoo import _, api, exceptions, fields, models, tools
from odoo.tools import pycompat, ustr
from odoo.tools.misc import clean_context
from odoo.tools.safe_eval import safe_eval


_logger = logging.getLogger(__name__)


class SkypeThread(models.AbstractModel):

    _name = 'skype.thread'
    _description = 'Skype Thread'
    _Attachment = namedtuple('Attachment', ('fname', 'content', 'info'))
    message_channel_ids = fields.Many2many(
        comodel_name='skype.channel')
    message_ids = fields.One2many(
        'skype.message')
    message_unread = fields.Boolean(
        'Unread Messages', compute='_get_message_unread',
        help="If checked new messages require your attention.")
    message_unread_counter = fields.Integer(
        'Unread Messages Counter', compute='_get_message_unread',
        help="Number of unread messages")
    message_attachment_count = fields.Integer('Attachment Count', compute='_compute_message_attachment_count')
    message_main_attachment_id = fields.Many2one(string="Main Attachment", comodel_name='ir.attachment', index=True)
