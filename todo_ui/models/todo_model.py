# -*- coding:utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.base.res.res_request import referenciable_models


class Tag(models.Model):
    _name = 'todo.task.tag'
    _description = 'To-do Tag'

    #_parent_name = 'parent_id'
    name = fields.Char('Name', 40, translate=True)

    # Tag class relationship to Tasks (Many2many inverse relationship):
    task_ids = fields.Many2many(
        'todo.task',  # related model
        string='Tasks')

    _parent_store = True
    _parent_name='parent_id' #the default
    parent_id = fields.Many2one(
        'todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many(
        'todo.task.tag', 'parent_id', 'Child Tags')



class Stage(models.Model):
    _name = 'todo.task.stage'
    _description = 'To-do Stage'
    _order = 'sequence, name'
    _rec_name = 'name' #The default
    _table_name = 'todo_task_stage' #The default

    # Stage class relationship with Tasks:
    task = fields.One2many(
        'todo.task', #related model
        'stage_id',  #field for "this" on related model
        'Tasks in this stage')

    # String fields:
    name = fields.Char('Name', 40)
    desc = fields.Text('Description')
    state = fields.Selection(
        [('draft','New'), ('open','Started'),
        ('done','Closed')],'State')
    docs = fields.Html('Documentation')

    #Numeric fields:
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete', (3,2))

    #Date fields:
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Changed')

    #Other fields:
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')

class TodoTask(models. Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many(
        comodel_name='todo.task.tag',
        relation='todo_task_tag_rel',
        column1='task_id',
        column2='tag_id',
        string='Tags')
    refers_to = fields.Reference(
        referenciable_models, 'Refers to')
    stage_fold = fields.Boolean(
        'Stage Folded?',
        compute = '_compute_stage_fold',
        # store=False, #the default
        search='_search_stage_fold',
        inverse='_write_stage_fold')

    def_search_stage_fold(self, operator, value):
        return[('stage_id.fold', operator, value)]

    def_write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage State')

    _sql_constraints=[
        ('todo_task_name_uniq',
         'UNIQUE(name,active)',
         'Task title must be unique!')]

    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        for task in self:
            task.stage_fold = task.stage_id.fold

    @api.constrains('name')
    def _check_name_size(self):
        for todo in self:
            if len(todo.name)<5:
                raise ValidationError('Must have 5 chars!')

    def compute_use_todo_count(self):
        for task in self:
            task.user_todo_count = task.search_count([('user_id', '=', task.user_id.id)])

    user_todo_count = fields.Integer(
        'User To-Do Count',
        compute = 'compute_user_todo_count')

    effort_estimate = fields.Integer('Effort Estimate')