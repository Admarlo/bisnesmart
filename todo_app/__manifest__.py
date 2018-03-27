{
    'name': 'To-Do application',
    'description': 'Manage your personal To-Do tasks.',
    'summary': 'Maneja las tareas de cada usuario',
    'autor': 'Adrià Martin',
    'version': '1.0',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'security/todo_access_rules.xml',
        'views/todo_view.xml',
        'views/todo_menu.xml',
    ],
}