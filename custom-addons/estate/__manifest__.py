# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['report_xlsx'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        "report/estate_property_offer_reports.xml",
        "report/estate_property_offer_templates.xml",
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/user_property_views.xml',
        'views/estate_menus.xml',
        "data/demo_data.xml",
    ],
    'test': [
        'tests/test_property_offer.py',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
