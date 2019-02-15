from odoo import _, api, fields, models, modules, tools


class Channel(models.Model):
    _description = 'Skype Channel'
    _name = 'skype.channel'

    login = fields.Char(string="Login", index=True, required=True)
    password = fields.Char(string="Password", required=True)
    token = fields.Char(string="Token", required=True)

