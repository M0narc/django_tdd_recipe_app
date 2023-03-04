"""
Test custom Django management commands.
"""
# first we mock the behaviour of the DB
from unittest.mock import patch
# one posible error we might get
from psycopg2 import OperationalError as Psycopg2Error
# helper function to actually call a command that we're testing by name
from django.core.management import call_command
from django.db.utils import OperationalError
# base test class, we are testing "when DB is not available"
from django.test import SimpleTestCase


# the patch decorator is being used on top of the class
# because we're going to be using it on all tests
# the path let us use the check provided by the BaseCommand
# because we're using the patch there we're gonna need
# to add a new parameter to our test cases in order to catch it
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patch_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
