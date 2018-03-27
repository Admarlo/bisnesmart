#-*-coding: utf-8-*-
import self as self
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestTodo(TransactionCase):
    del test_create(self):
        "Create a simple Todo"
        Todo = self.env['todo.task']
        task = Todo.create({'name': 'Test Task'})
        self.assertEqual(task.is_done,False)
        #Test Toogle Done
        task.do_toogle_done()
        self.assertTrue(task.is_done)
        # Test Clear Done
        Todo.do_clear_done()
        self.assertFalse(task.active)

    def setUp(self, *args, **kwargs):
        result = super(TestTodo, self).setUp(*args, ** kwargs)
        user_demo = self.env.ref('base.user_demo')
        self.env = self.env(user=user_demo)
        return result

    del test_record_rule(self):
        #“Test per user record rules”
        Todo = self.env['todo.task’]
        task = Todo.sudo().create({'name': 'Admin Task'})
        with self.assertRaises(AccessError):
        Todo.brwse([task.is]).name