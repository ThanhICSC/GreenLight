# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import request


class OdooShoppeBackendTheme(http.Controller):

    @http.route('/partners/map', type='http', auth='public', website=True)
    def web_social_feed(self, **kwargs):
        partner_datas = {}
        Partners = request.env['res.partner'].sudo().search([
            ('partner_latitude', '!=', 0.0), ('partner_longitude', '!=', 0.0)])

        for partner in Partners:
            partner_datas.update({
                partner.id: [partner.name.encode('utf8'),
                             "%.6f" % round(partner.partner_latitude, 6),
                             "%.6f" % round(partner.partner_longitude, 6)]
            })

        return request.render(
            "odoo_shoppe_backend_theme.material_osbt_partner_location_map", {
            'partners': json.dumps(partner_datas)})
