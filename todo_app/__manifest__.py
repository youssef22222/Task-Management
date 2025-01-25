{
    'name': 'To-Do App',
    'author': 'Youssef Elsayed',
    'category': 'Custom',
    'version': '17.0.0.1',
    'depends':['base','mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'wizard/assign_task_wizard_view.xml',
        'reports/task_report.xml'
    ],
    'application': True,
}