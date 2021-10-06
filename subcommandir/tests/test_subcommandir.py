from django.core.management import call_command, CommandError
from django.test import TestCase


class SimpleTest(TestCase):
    def test_simple_call_command(self):
        call_command('tests_subcommandir_load', 'month_report')

    def test_call_command_with_args(self):
        call_command('tests_subcommandir_load', 'month_report', type=2)

    def test_call_other_command(self):
        call_command('tests_subcommandir_load', 'year_report')

    def test_call_other_command_error(self):
        # with self.assertRaises(CommandError):
        call_command('tests_subcommandir_load', 'year_report', type=2)
