{
    'name': 'Multiuser To-Do',
    'description': 'Extend the To-Do app to multiuser',
    'summary': 'Maneja las tareas para multiusuario',
    'autor': 'Adrià Martin',
    'version': '1.0',
    'depends': ['todo_app', 'mail'],
    'data': [
        'views/todo_view.xml',
        'security/todo_access_rules.xml'
    ],
    'demo': ['todo.task.csv', 'todo_data.xml'],
}