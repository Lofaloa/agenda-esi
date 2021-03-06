# -*- coding: utf-8 -*-

from datetime import datetime
from .util import create_event
from .util import create_agenda
from .util import create_partner
from .util import assert_event_equal
from .util import assert_event_error
from .util import assert_agenda_contains
from .util import assert_event_capacity_error

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestEvent(TransactionCase):

    def test_valid_event_creation(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        organizer = create_partner(self, "Logan Farci")
        agenda = create_agenda(self, "My Agenda", organizer.id)
        event = create_event(self, 'My Event', 'd', start, end, 405, 1, agenda.id)
        assert_event_equal(self, event, 'My Event', 'd', start, end, 405, 1)
        assert_agenda_contains(self, agenda, event)

    def test_event_with_too_much_attendees(self):
        only_attendee = create_partner(self, "Michael Jackson")
        intruder = create_partner(self, "Charles Manson")
        assert_event_capacity_error(self, 1, [only_attendee, intruder])

    def test_title_not_blank_constraint(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        organizer = create_partner(self, "Logan Farci")
        agenda = create_agenda(self, "My Agenda", organizer.id)
        assert_event_error(self, '', 'd', start, end, 405, 1, agenda.id)

    def test_start_is_before_end_constraint(self):
        start = datetime(2019, 1, 1, 14, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        organizer = create_partner(self, "Logan Farci")
        agenda = create_agenda(self, "My Agenda", organizer.id)
        assert_event_error(self, 'My Event', 'd', start, end, 405, 1, agenda.id)

    def test_classroom_constraint(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        organizer = create_partner(self, "Logan Farci")
        agenda = create_agenda(self, "My Agenda", organizer.id)
        assert_event_error(self, 'My Event', 'd', start, end, 1000, 1, agenda.id)

    def test_capacity_is_greater_than_one_constraint(self):
        start = datetime(2019, 1, 1, 12, 0, 0)
        end = datetime(2019, 1, 1, 13, 0, 0)
        organizer =  create_partner(self, "Logan Farci")
        agenda = create_agenda(self, "My Agenda", organizer.id)
        assert_event_error(self, 'My Event', 'd', start, end, 1000, 0, agenda.id)
