# -*- coding: utf-8 -*-
{
    'name': "skype_listener",

    'summary': """
    receive skype's messages as Odoo notifications
        """,

    'description': """
        The app is listening the specific skype-channel and send it to admin-user in Odoo as message
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'complexity': 'easy',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup', 'bus'],

    'installable': True,
    'auto_install': True
}