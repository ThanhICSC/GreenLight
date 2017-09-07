# -*- coding: utf-8 -*-
# Copyright (C) Kanak Infosystems LLP.

{
    'name': "OdooShoppe Backend Theme",
    'version': '1.0',
    'summary': 'Odooshoppe Backend Theme',
    'description': """
OdooShoppe - Backend Theme
================================
    """,
    'author': "Kanak Infosystems LLP.",
    'website': "http://www.kanakinfosystems.com",
    'images': ['static/description/main_screenshot.png'],
    'category': 'Theme/Backend',
    'depends': ['mail', 'calendar', 'base', 'base_geolocalize', 'website'],
    'data': [
        'views/material_osbt_templates.xml',
        'views/material_osbt_views.xml',
        'data/material_osbt_data.xml'
    ],
    'qweb': [
        'static/src/xml/material_osbt_templates.xml',
    ],
    'application': True,
    'price': 149,
    'currency': 'EUR',
    'live_test_url': 'http://v10.odooshoppe.com/web?db=backend_theme',
}
