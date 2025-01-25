from odoo import fields, models,api
from odoo.exceptions import ValidationError
from odoo.fields import One2many


class ToDoTask(models.Model):
    _name="todo.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Task'

    ref = fields.Char(default ='New' ,readonly=True )
    name=fields.Char('Task Name' )
    due_date=fields.Date(tracking=True)
    is_late = fields.Boolean()
    description=fields.Char()
    estimated_time=fields.Integer()
    assign_to_id=fields.Many2one('res.partner',default= lambda self:self.env.uid)
    state=fields.Selection(
        [
            ('new','New'),
            ('in_progress','In Progress'),
            ('completed','Completed'),
            ('closed','Closed'),
        ],default='new',tracking=True
    )

    line_ids = fields.One2many('task.line','task_id')

    active=fields.Boolean(default=True)

    def action_new(self):
        for rec in self:
            rec.state='new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    @api.constrains('line_ids','line_ids.time')
    def _check_total_time_less_than_estimated_time(self):
        for rec in self:
            total_time = 0
            for line in rec.line_ids:
                total_time += line.time
            if total_time > rec.estimated_time:
                raise ValidationError("Total time exceeds estimated time")

    def check_due_date(self):
        task_ids = self.search([])
        for rec in task_ids:
            if rec.state in ['new','in_progress'] and rec.due_date and rec.due_date < fields.date.today():
                rec.is_late = True

    @api.model
    def create(self, vals):
        print(self)
        res = super(ToDoTask,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('task_seq')
        return res

    def action_open_assign_task_wizard(self):
        task_ids =self.env.context.get('active_ids')
        #note we assign this list ex([1,2,3]) to the task_ids in the assign.task model
        print(task_ids)
        for task in self.env["todo.task"].browse(task_ids):
            if task.state in ('completed', 'closed'):
                raise ValidationError("You can not assign completed or closed tasks to another user")

        action = self.env['ir.actions.actions']._for_xml_id('todo_app.assign_task_wizard_action')
        action['context'] = {'default_task_ids': task_ids}
        return action

class TaskLine(models.Model):
    _name = 'task.line'

    task_id=fields.Many2one('todo.task')
    date=fields.Date()
    description=fields.Char()
    time=fields.Integer()

