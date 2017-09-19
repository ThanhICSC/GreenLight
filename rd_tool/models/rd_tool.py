# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _


class ProjectProject(models.Model):

    _inherit = 'project.project'

    start_date = fields.Datetime()
    end_date = fields.Datetime()
    is_rd = fields.Boolean("R & D Project")
    calculated_risk = fields.Integer(
        "Calculated Risk(%)", compute='_compute_risk')
    hypothesis = fields.Html("Hypothesis")

    project_uncertainity_ids = fields.One2many('project.technical.uncertainity',
                                               'project_id', string="Technical Uncertainity")
    project_experiment_ids = fields.One2many(
        'project.experiment', 'project_id')
    project_advancement_ids = fields.One2many(
        'project.technical.advancement', 'project_id')
    experiment_result_ids = fields.One2many(
        'project.experiment.result', 'project_id')

    exp_count = fields.Integer(compute='_compute_exp_count')
    uncertainities_count = fields.Integer(
        compute='_compute_uncertainites_count')
    activity_count = fields.Integer(compute='_compute_activity_count')

    def _compute_risk(self):
        for record in self:
            project_advancements = self.env['project.technical.advancement'].search(
                [('project_id', '=', record.id)])
            x = 0
            y = 0
            for advancement in project_advancements:
                x += int(advancement.risk)
                y += int(len(advancement))
                avg = x / y
                record.cr = avg

    def _compute_exp_count(self):
        for record in self:
            project_exp = self.env['project.experiment'].search_count(
                [('project_id', '=', record.id)])
            record.exp_count = project_exp

    def _compute_uncertainites_count(self):
        for record in self:
            project_uncertainities = self.env['project.technical.uncertainity'].search(
                [('project_id', '=', record.id)])
            record.uncertainities_count = project_uncertainities

    def _compute_activity_count(self):
        for record in self:
            project_experiments = self.env['project.experiment'].search(
                [('project_id', '=', record.id)])
            count = 0
            for experiment in project_experiments:
                experiment_result_count = self.env['project.experiment.result'].search_count(
                    [('experiment_id', '=', experiment.id)])
                count += experiment_result_count
                record.activity_count = count

    @api.multi
    def view_experiments(self):
        view_id = self.env.ref('rd_tool.experiment_result_tree')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Experiment Results'),
            'res_model': 'project.experiment.result',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {'default_experiment_id': self.id, 'search_default_experiment_id': self.id}
        }


class ProjectUncertainities(models.Model):

    _name = 'project.technical.uncertainity'

    project_id = fields.Many2one('project.project', string='Project')
    name = fields.Char()
    status = fields.Selection(
        [('wait', 'WAITING'), ('progress', 'In PROGRESS'), ('success', 'SUCCESS'), ('fail', 'FAILED')])
    remark = fields.Char("Remarks")
    state = fields.Selection([('solved', 'Solved'), ('unsolved', 'Unsolved')])


class ProjectExperiment(models.Model):

    _name = 'project.experiment'

    name = fields.Char()
    project_id = fields.Many2one('project.project', string='Project')
    status = fields.Selection([('wait', 'WAITING'), ('progress', 'IN PROGRESS'), (
        'success', 'SUCCESS'), ('fail', 'FAILED')])
    remark = fields.Char()
    project_advancement_ids = fields.Many2many('project.technical.advancement',
                                               compute='_get_default_advance', string="Advancements")
    current_risk = fields.Float("Current risk(%)")
    scheduled_start = fields.Date()
    from_date = fields.Date()
    to_date = fields.Date()
    stopped = fields.Boolean()
    state = fields.Selection(
        [('new', 'NEW'), ('open', 'OPEN'), ('close', 'CLOSE')], default='new')

    experiment_line_ids = fields.One2many(
        'project.experiment.line', 'experiment_id')
    experiment_result_ids = fields.One2many(
        'project.experiment.result', 'experiment_id', string="data")

    results_count = fields.Integer(
        compute='_compute_results_count', string="Count")
    uncertainities_count = fields.Integer(
        compute='_compute_uncertainities_count')

    expz = fields.Integer()
    evd = fields.Integer()
    investigation_interval = fields.Integer()

    @api.depends('project_id')
    def _get_default_advance(self):
        for record in self:
            if record.project_id:
                record.project_advancement_ids = self.project_id.project_advancement_ids.ids

    @api.depends('experiment_result_ids')
    def _compute_results_count(self):
        for record in self:
            record.results_count = len(record.experiment_result_ids)

    def _compute_uncertainities_count(self):
        for record in self:
            count = self.env['project.technical.uncertainity'].search(
                [('project_id', '=', record.project_id.id)])
            self.uncertainities_count = count

    @api.multi
    def view_project_uncertainities(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('uncertainities'),
            'res_model': 'project.technical.uncertainity',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {'default_project_id': self.project_id.id, 'search_default_project_id': self.project_id.id}
        }

    @api.multi
    def start(self):
        if self.state == 'new':
            self.write({'state': 'open'})
        else:
            self.write({'stopped': 'False', 'from_date': date.today()})

    @api.multi
    def stop(self):
        self.write({'stopped': True, 'to_date': date.today()})

    @api.multi
    def close(self):
        self.write({'state': 'close'})


class ProjectExperimentLine(models.Model):

    _name = 'project.experiment.line'

    experiment_id = fields.Many2one(
        'project.experiment', string='Project Experiment')
    eligible = fields.Char()
    recorded_date = fields.Date()
    interval = fields.Integer("Interval")
    start_date = fields.Date()
    end_date = fields.Date()
    CR = fields.Integer()
    resolved = fields.Integer()
    expanded = fields.Integer()
    remaining = fields.Integer()


class ProjectExperimentResult(models.Model):

    _name = 'project.experiment.result'

    project_id = fields.Many2one('project.project', "project id")
    data_recorded = fields.Char()
    work_hours = fields.Integer("Work hours reported")
    person = fields.Char()
    experiment_id = fields.Many2one('project.experiment', "Project Experiment")

    work_results = fields.Html()
    problems_observed = fields.Html()
    experiment_unresolved_ids = fields.One2many(
        'experiment.unresolved', 'experiment_result_id', string='Experiment Unresolved')


class ProjectTechnicalAdvancement(models.Model):

    _name = 'project.technical.advancement'

    name = fields.Char()
    number = fields.Char()
    remark = fields.Char()
    project_id = fields.Many2one('project.project', string='Project')
    status = fields.Selection([('wait', 'WAITING'), ('progress', 'In PROGRESS'), (
        'success', 'SUCCESS'), ('fail', 'FAILED')], string="Status")
    risk = fields.Integer()
    sr = fields.Char("SR&RD", compute='_compute_rd')
    ch = fields.Boolean(string="")

    @api.depends('risk')
    def _compute_rd(self):
        for record in self:
            record.sr = 'Not eligible' if record.risk <= 0 else 'Eligible'


class ExperimentUnresolved(models.Model):

    _name = 'experiment.unresolved'

    experiment_result_id = fields.Many2one('project.experiment.result')
    actions = fields.Char("Actions")
    project_uncertainities_id = fields.Many2one(
        'project.technical.uncertainity', "TUs")
    technical_uncertainities_id = fields.Many2one(
        'technical.uncertainities', "parent TU")
    risk = fields.Integer("Risk%")
    version = fields.Char("Version")
    stats = fields.Selection([('solve', 'Solved'), ('unsolve', 'Unsolved')])
