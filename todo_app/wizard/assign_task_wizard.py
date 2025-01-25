from stdnum.exceptions import ValidationError

from odoo import fields,models


class AssignTask(models.TransientModel):
    _name = 'assign.task'

    task_ids = fields.Many2many('todo.task')

    user_id = fields.Many2one('res.partner',default=lambda self: self.env.uid)

    def action_confirm(self):
     for task in self.task_ids:
            task.assign_to_id = self.user_id