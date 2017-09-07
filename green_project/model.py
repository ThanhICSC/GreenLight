from odoo import models, fields, api,_
import datetime

# technical advancment class
class tec_adv(models.Model):
    _name = 'technical.advancement'

    name = fields.Char("TA Name")
    ta_id=fields.Char("TA id", readonly=True, default = lambda self: _(''))


    des=fields.Text("Description")
    rem=fields.Text("Remark")

    @api.model
    def create(self, vals):
        if vals.get('ta_id', _('New')) == _('New'):
            vals['ta_id'] = self.env['ir.sequence'].next_by_code('ad.order')
            result = super(tec_adv, self).create(vals)
            return result



# technical uncertinities class
class tec_con(models.Model):
    _name = 'technical.uncertinites'



    t_id=fields.Char("Technical Uncertainity ID", readonly=True, default = lambda self: _(''))

    name=fields.Char("Technical Name")
    parent=fields.Many2one('technical.uncertinites',"Parent TU")
    des1=fields.Text("Description")
    rem1=fields.Text("Remark")


    @api.model
    def create(self, vals):
        if vals.get('t_id',_('New')) ==_('New'):
            vals['t_id'] = self.env['ir.sequence'].next_by_code('con.order')
            result1 = super(tec_con, self).create(vals)
            return result1


# experiment class
class experiment(models.Model):
    _name = 'experiment.details'

    name = fields.Char("Experiment Name")
    expy_id = fields.Char("EXPERIMENT ID", readonly=True, default=lambda self: _(''))
    des2=fields.Text("Description")
    rem2=fields.Text("Remark")

    # create sq:number for experiment
    @api.model
    def create(self, vals):
        if vals.get('expy_id',_('New')) ==_('New'):
            vals['expy_id'] = self.env['ir.sequence'].next_by_code('ex.order')
            result2 = super(experiment, self).create(vals)
            return result2




# inheriting project module
class project_extra(models.Model):

    _inherit ='project.project'
    sdate=fields.Datetime("Starting date")
    edate=fields.Date("Ending date")
    rd=fields.Boolean("this is R&D")
    cr=fields.Char("Calculated Risk(%)",compute='_compute_risk')
    html=fields.Html("Hypothesis")
    bu_ex=fields.Char(" ")
    bu_ac=fields.Char(" ")
    bu_un=fields.Char(" ")

    tu_ids = fields.One2many('project.tu','project_tu',string="tu")
    ex=fields.One2many('project.ex','ex_id',string="ex")
    ta=fields.One2many('project.ad','ad_id',string="ta")

    exorder_count = fields.Integer(compute='_compute_exorder_count')
    tuorder_count=fields.Integer(compute='_compute_tuorder_count')
    ac_count=fields.Integer(compute='_compute_activity_count')

    #experiment count
    def _compute_exorder_count(self):
        print "entered into _compute_exorder"
        print self
        sale_data = self.env['project.ex'].search([('ex_id','=',self.id)])
        data_new=len(sale_data)
        print data_new
        self.exorder_count = data_new

    #uncertnity count
    def _compute_tuorder_count(self):
        print "entered into compute"
        print self
        tu_data=self.env['project.tu'].search([('project_tu','=',self.id)])
        data1=len(tu_data)
        print data1
        self.tuorder_count=data1


    def activity_exp(self):
        view_ref = self.env['ir.model.data'].get_object_reference('green_project',
                                                                  'result_tree')
        view_id = view_ref[1] if view_ref else False

        return {
            'type': 'ir.actions.act_window',
            'name': _('activities'),
            'res_model': 'experiment.result',
            'view_type': 'form',
            'view_mode': 'tree,form',
            # 'view_id': view_id,
            'target': 'current',
            'context': {'default_net':self.ex.id,'search_default_net':self.ex.id}

        }
    #activity count
    def _compute_activity_count(self):
        view_ref = self.env['ir.model.data'].get_object_reference('green_project',
                                                                  'uncertinity_tree56')
        print "entered into compute1"
        print self
        tu_data = self.env['experiment.result'].search([('net', '=', self.ex.id)])

        # print tu_data

        data1 = len(tu_data)
        print data1
        # self.resu1 = data1
        #
        # print "Entered result_c_count1 %s" % self
        # resu_data = self.env['project.project'].search([('ex', '=', self.id)])
        # print resu_data
        # data_new = len(resu_data)
        # print data_new
        self.ac_count = data1


    def _compute_risk(self):

        print self
        tu = self.env['project.ad'].search([('ad_id','=',self.id)])#get ids of tu related to  corresponding project
        print tu
        x=0
        y=0
        for data in tu:
            x +=int(data.risk) #fetch the value of risk from table which is associated with data(id)
            y +=int(len(data))#count of corresponding tu
            Avg=x/y
            self.cr=Avg
   

# project uncertinities
class project_tu(models.Model):
    _name ='project.tu'

    project_tu=fields.Many2one('project.project',string='PROJECT ID')
    name=fields.Many2one('technical.uncertinites',string='Tu Name')
    desc=fields.Char(string="Description")
    remark=fields.Char("Remarks")
    status=fields.Selection([('solve','Solved'),('unsolve','Unsolved')])





#  experiment tab&form in project
class project_ex(models.Model):
    _name ='project.ex'

    ex_id=fields.Many2one('project.project',string='Project ID')
    exp_id=fields.Many2one('experiment.details',string="Experiment Name:")
    desc1=fields.Selection([('wait', 'WAITING'),('progress', 'IN PROGRESS'), ('success', 'SUCCESS'), ('fail', 'FAILED')],string="Description")
    remark1=fields.Char('Remarks')
    status1=fields.Selection([('open','OPENED'),('close','CLOSED')],string="Status")
    experiment_title = fields.Char("")
    target = fields.Many2many('project.ad',compute='_get_default_advance')
    current_risk = fields.Float("Current risk(%):")
    scheduled_start = fields.Date("Scheduled start:")
    Investigation = fields.Char("Investigation intervel:")
    From = fields.Date("From:")
    To = fields.Date("To:")
    exp_ids = fields.One2many('experiment.line', 'tech_id', string='id')
    status = fields.Selection([('new', 'NEW'), ('open', 'OPEN'), ('close', 'CLOSE')], default='new')
    exp_res = fields.One2many('experiment.result', 'net', string="data")
    c_count = fields.Integer(compute='result_count', string="Count")
    b = fields.Integer("int")
    resu = fields.Integer(compute='_compute_tuorder_count2')

    expz=fields.Integer()
    evd=fields.Integer()


    # display default values in experiment form in project
    @api.depends('ex_id')
    def _get_default_advance(self):
        # print "self == %s" % self
        # print self.ad_id
        tar_ids = self.env['project.ad'].search([('ad_id', '=', self.ex_id.id)])
        # print("target obj is %s" % tar_ids)
        self.target = tar_ids

    # count of activity in experiment form
    def result_count(self):
        print "Entered result_c_count %s" % self
        resu_data = self.env['experiment.result'].search([('net', '=', self.id)])
        print resu_data
        data_new = len(resu_data)
        print data_new
        self.c_count = data_new

    # button function for uncertinity in xperiment form
    def uncertinity_exp(self):

        view_ref = self.env['ir.model.data'].get_object_reference('green_project',
                                                                  'uncertinity_tree56')
        view_id = view_ref[1] if view_ref else False


        return {
            'type': 'ir.actions.act_window',
            'name': _('uncertainities'),
            'res_model': 'project.tu',
            'view_type': 'form',
            'view_mode': 'tree,form',
            # 'view_id': view_id,
            'target': 'current',
            'context': {'default_project_tu': self.ex_id.id,'search_default_project_tu':self.ex_id.id}
        }


    # count for uncertnity in experiment form
    def _compute_tuorder_count2(self):

        view_ref = self.env['ir.model.data'].get_object_reference('green_project',
                                                                  'uncertinity_tree56')
        print "entered into compute"
        print self
        tu_data = self.env['project.tu'].search([('project_tu','=', self.ex_id.id)])

        # print tu_data

        data1 = len(tu_data)
        print data1
        self.resu = data1

        print "Entered result_c_count %s" % self
        resu_data = self.env['experiment.result'].search([('net', '=', self.id)])
        print resu_data
        data_new = len(resu_data)
        print data_new
        self.c_count = data_new







    @api.multi
    def start(self):

        for sta in self:
            sta.write({'status': 'open'})
        return True

    @api.multi
    def stop(self):

        for sto in self:
            sto.write({'status': 'new'})
        return True

    @api.multi
    def close(self):

        for clo in self:
            clo.write({'status': 'close'})
        return True

# investigation tab for experiment form in project
class experiment_line(models.Model):
           _name = 'experiment.line'

           tech_id = fields.Many2one('project.ex', string='tech_id')
           eligible = fields.Char("Eligible")
           recorded = fields.Date("Recorded")
           interval = fields.Integer("Interval")
           started = fields.Date("Started")
           ended = fields.Date("Ended")
           CR = fields.Float("CR")
           resolved = fields.Integer("Resolved")
           expanded = fields.Integer("Expanded")
           remaining = fields.Integer("Remaining")


# project advancements tab in project form
class project_ad(models.Model):
    _name = 'project.ad'

    name = fields.Many2one('technical.advancement',"TA name")
    ad_id=fields.Many2one('project.project',string='Project Id')
    desc2 = fields.Selection([('wait', 'WAITING'), ('progress', 'In PROGRESS'), ('success', 'SUCCESS'), ('fail', 'FAILED')],string="Status")
    risk=fields.Char(string="Risk")
    sr=fields.Selection([('eligible','ELIGIBLE'),('not eligible','NOT ELIGIBLE')],string='SR&RD')
    ch=fields.Boolean(string="R&D")







