# -*- coding: utf-8 -*-

from odoo import models, fields

class Event(models.Model):
    """
    An event is a gathering of poeple taking place at a given time and location

    Attributes:
        _name (str): This model technical name.
        PERIODICITY_OPTIONS (list of pairs): Options are dayly, weekly, montly.
        periodicity (odoo.fields.Selection): The event recurrence.
        start_datetime (odoo.fields.Date): The starting date and time.
        end_datetime (odoo.fields.Date): The finishing date and time.
        location (?): The location where this event takes place.
        capacity (odoo.fields.Integer): The number of available seats.
    """

    _name = 'agenda_esi.event'

    PERIODICITY_OPTIONS = [('d', 'Dayly'), ('w', 'Weekly'), ('m', 'Monthly')]

    periodicity = fields.Selection(selection=PERIODICITY_OPTIONS)
    start_datetime = fields.Datetime()
    end_datetime = fields.Datetime()
    # location = fields.Selection()
    capacity = fields.Integer()