# -*- coding: utf-8 -*-

from datetime import datetime

from odoo.tests.common import TransactionCase

class TestAgenda(TransactionCase):

    TESTED_MODEL_NAME = 'agenda_esi.agenda'

    def test_valid_agenda_creation(self):
        self.assertTrue(False)