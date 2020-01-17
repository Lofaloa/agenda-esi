# -*- coding: utf-8 -*-

from datetime import datetime
from .util import create_agenda
from .util import create_partner
from .util import assert_agenda_equal
from .util import assert_agenda_error

from odoo.tests.common import TransactionCase

class TestAgenda(TransactionCase):

    def test_valid_agenda_creation(self):
        organizer =  create_partner(self, "Logan Farci")
        record = create_agenda(self, "My Agenda", organizer.id)
        assert_agenda_equal(self, record, "My Agenda", organizer)

    def test_title_not_blank_constraint(self):
        organizer =  create_partner(self, "Logan Farci")
        assert_agenda_error(self, "", organizer)

    def test_show_calendar_action(self):
        organizer =  create_partner(self, "Logan Farci")
        agenda = create_agenda(self, "My Agenda", organizer.id)
        action = agenda.show_calendar_action()
        self.assertEqual(action["type"], 'ir.actions.act_window')
        self.assertEqual(action["name"], 'Agenda Events')
        self.assertEqual(action["view_mode"], 'calendar')
        self.assertEqual(action["res_model"], 'agenda_esi.event')
        self.assertEqual(action["context"]["default_agenda_id"], agenda.id)
        self.assertEqual(action["domain"], [('id', 'in', agenda.events.ids)])