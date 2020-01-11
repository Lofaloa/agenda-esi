# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Event(models.Model):
    """
    An event is a gathering of poeple taking place at a given time and location

    Note about constraints: I (Logan) am not sure if we need to define both
    sql and python constraints. It is worth noting that odoo.api.constraints
    won't be triggered for fields that are not present in the view.
    For more information : 
    https://www.odoo.com/documentation/11.0/reference/orm.html#odoo.api.constrains

    Note about the location: we werea asked a location for an event. We chose
    the easy way for now. An event location is represented by a classroom
    number. We could implement a new model instead.

    Attributes:
        _name (str): This model technical name (agenda_esi.event)
        _sql_constraints (list of triples): This model sql constraints
        PERIODICITY_OPTIONS (list of pairs): Options are dayly, weekly, montly
        CLASS_ROOM_LIMIT (integer): The classroom limit number (not included)
        title (odoo.fields.Text): The event title, it should be describing
        periodicity (odoo.fields.Selection): The event recurrence
        start_datetime (odoo.fields.Date): The starting date and time
        end_datetime (odoo.fields.Date): The finishing date and time
        classroom (odoo.fields.Integer: The classroom number of this event
        capacity (odoo.fields.Integer): The number of available seats
    """

    @api.model
    def _get_default_end_time(self):
        default_end_datetime = datetime.now() + timedelta(hours=2)
        return fields.Datetime.to_string(default_end_datetime)

    _name = 'agenda_esi.event'

    PERIODICITY_OPTIONS = [
        ('d', 'Dayly'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
        ('u', 'None')
    ]

    CLASS_ROOM_LIMIT = 1000

    title = fields.Char()
    periodicity = fields.Selection(selection=PERIODICITY_OPTIONS, default='u')
    start_datetime = fields.Datetime(default=fields.Datetime.now())
    end_datetime = fields.Datetime(default=_get_default_end_time)
    classroom = fields.Integer()
    capacity = fields.Integer(default=1, required=False)

    # TODO: the attendees of an event should be members of an event agenda.
    # attendees = fields.Many2One

    @api.constrains('title')
    def _check_title_is_not_blank(self):
        """ Makes sure that the title of an event isn't blank.
        """
        for record in self:
            if not record.title:
                    msg = """Invalid event title! The event title should not be\
                    blank."""
                    raise ValidationError(msg)

    @api.constrains('start_datetime', 'end_datetime')
    def _check_start_is_before_end(self):
        """ Makes sure that the start time of an event is before its end time.
        """
        for record in self:
            if record.end_datetime < record.start_datetime:
                    msg = """Invalid event start and end times! The event
                    should start before it ends."""
                    raise ValidationError(msg)

    @api.constrains('classroom')
    def _check_capacity(self):
        """ Makes sures that an event classroom is valid. A valid classroom is
        an positive integer with a value under CLASS_ROOM_LIMIT.
        """
        for record in self:
            if record.classroom >= self.CLASS_ROOM_LIMIT:
                msg = """Invalid event classroom! It should be less than 1000.
                """
                raise ValidationError(msg)

    @api.constrains('capacity')
    def _check_capacity(self):
        """ Makes sures that an event capacity is greater than or equal to 1.
        """
        for record in self:
            if record.capacity < 1:
                msg = """Invalid event capacity! It should be greater than or\
                equal to 1."""
                raise ValidationError(msg)