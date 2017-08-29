from odoo import models, fields, api

class experiment_result(models.Model):

    _name='experiment.result'

    data_recorded = fields.Char("Data recorded:")
    work_hours=fields.Integer("Work hours reported:")
    person=fields.Char("Person:")
    exper=fields.One2many('experiment.unresolved','unre',string='exper')

    net=fields.Many2one('project.ex','net')
    wr = fields.Html("work results")
    po = fields.Html("Problems Observed")




class experiment_unresolved(models.Model):

    _name='experiment.unresolved'
    unre=fields.Many2one('experiment.result',string='unre')
    actins=fields.Char("Actions")
    tu=fields.Many2one('project.tu',"TUs")
    parent=fields.Many2one('technical.uncertinites',"parent TU")
    risk=fields.Integer("Risk %")
    version=fields.Char("Version")
    stats = fields.Selection([('solve', 'Solved'), ('unsolve', 'Unsolved')])