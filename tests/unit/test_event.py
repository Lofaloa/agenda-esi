# -*- coding: utf-8 -*-

from datetime import datetime
from .util import create_event
from .util import assert_event_equal
from .util import assert_event_error

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestEvent(TransactionCase):

    def test_valid_event_creation(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        record = create_event(self, 'My Event', 'd', start, end, 405, 1)
        assert_event_equal(self, record, 'My Event', 'd', start, end , 405, 1)

    def test_title_not_blank_constraint(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        assert_event_error(self, '', 'd', start, end, 405, 1)

    def test_start_is_before_end_constraint(self):
        start = datetime(2019, 1, 1, 14, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        assert_event_error(self, 'My Event', 'd', start, end, 405, 1)

    def test_classroom_constraint(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        assert_event_error(self, 'My Event', 'd', start, end, 1000, 1)

    def test_capacity_is_greater_than_one_constraint(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        assert_event_error(self, 'My Event', 'd', start, end, 1000, 0)