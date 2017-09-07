from odoo import api, fields, models


class ThemeResUser(models.Model):
    _inherit = 'res.users'

    theme = fields.Selection([
        ('orange', 'Orange'),
        ('gray_black', 'Gray Black'),
        ('white', 'White Gray'),

        ('dark_blue', 'Dark Blue'),
        ('blue', 'Blue'),
        ('grey', 'Grey'),

        ('dark_red', 'Dark Red'),
        ('pink', 'Pink'),
        ('yellow_green', 'Yellow'),

        ],
        'User Theme', default="gray_black")

    @api.multi
    def write(self, data):
        res = super(ThemeResUser, self).write(data)
        if data.get('theme'):
            self.env['ir.qweb'].clear_caches()
        return res
