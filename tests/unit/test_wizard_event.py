from datetime import datetime
from .util import create_wizard_event
from .util import assert_start_after_end_error
from .util import assert_date_equal

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestWizardEvent(TransactionCase):

    def test_valid_creation(self):
        start_date = datetime(2019, 1, 1, 12, 0, 0)
        end_date = datetime(2019, 1, 1, 13, 0, 0)
        wizard = create_wizard_event(self, start_date, end_date)
        assert_date_equal(self, wizard, start_date, end_date)

    def test_start_after_end(self):
        start_date = datetime(2019, 1, 1, 12, 0, 0)
        end_date = datetime(2019, 1, 1, 11, 0, 0)
        assert_start_after_end_error(self, start_date, end_date)
