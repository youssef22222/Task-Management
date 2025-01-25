from odoo import http
from odoo.http import request
from .utils import *
import json

class ToDoTaskApi(http.Controller):

    @http.route("/v1/task/<int:task_id>", methods=["DELETE"],type="http", auth="none",csrf=False)
    def delete_task(self, task_id):
        try:
            task = request.env["todo.task"].sudo().search([("id","=",task_id)])
            if not task:
                return invalid_response("Task not found",404)
            task.sudo().unlink()
            return valid_response("Task Deleted Successfully",200)
        except Exception as error:
            return invalid_response(str(error),400)


    @http.route("/v1/task/<int:task_id>",methods=["GET"],type="http",auth="none",csrf=False)
    def get_task(self,task_id):
        try:
            task = request.env["todo.task"].sudo().search([("id","=",task_id)])
            if not task:
                return invalid_response("Task not found",status=404)
            return valid_response({
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "due_date": task.due_date,
                "assign_to_id": task.assign_to_id.name,
                "state": task.state
            },status=200)
        except Exception as error:
            return invalid_response(error,status=400)

    @http.route("/v1/tasks",methods=["GET"],type="http",auth="none",csrf=False)
    def get_tasks(self):
        try:
            tasks = request.env["todo.task"].sudo().search([])
            if not tasks:
                return invalid_response("There are no tasks found",status=404)

            return valid_response([{
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "due_date": task.due_date,
                "assign_to_id": task.assign_to_id.name,
                "state": task.state
            } for task in tasks],status=200)
        except Exception as error:
            return invalid_response(error,status=400)