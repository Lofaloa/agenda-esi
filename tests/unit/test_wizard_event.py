from datetime import datetime
from .util import create_wizard_event
from .util import assert_date_error

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestWizardEvent(TransactionCase):
    def test_invalid_creation_date(self):
        start_date = datetime(datetime(2019, 1, 1, 12, 0, 0))
        end_date = datetime(2019, 1, 1, 13, 0, 0)
        create_wizard_event(start_date, end_date)
        assert_date_error(self)
