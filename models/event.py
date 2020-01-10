# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Event(models.Model):
    """
    An event is a gathering of poeple taking place at a given time and location

    Note about constraints : I (Logan) am not sure if we need to define both
    sql and python constraints. It is worth noting that odoo.api.constraints
    won't be triggered for fields that are not present in the view.
    
    For more information : 
    https://www.odoo.com/documentation/11.0/reference/orm.html#odoo.api.constrains

    Attributes:
        _name (str): This model technical name.
        _sql_constraints (list of triples): This model sql constraints.
        PERIODICITY_OPTIONS (list of pairs): Options are dayly, weekly, montly.
        title (odoo.fields.Text): The event title, it should be describing.
        periodicity (odoo.fields.Selection): The event recurrence.
        start_datetime (odoo.fields.Date): The starting date and time.
        end_datetime (odoo.fields.Date): The finishing date and time.
        location (?): The location where this event takes place.
        capacity (odoo.fields.Integer): The number of available seats.
    """

    _name = 'agenda_esi.event'

    PERIODICITY_OPTIONS = [
        ('d', 'Dayly'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
        ('u', 'None')]

    title = fields.Text()
    periodicity = fields.Selection(selection=PERIODICITY_OPTIONS)
    start_datetime = fields.Datetime()
    end_datetime = fields.Datetime()
    # location = fields.Selection() - should be a foreign key to another table
    capacity = fields.Integer()

    @api.constrains('capacity')
    def _check_capacity(self):
        """ Makes sures that an event capacity is greater than or equal to 1.
        """
        for record in self:
            if record.capacity < 1:
                msg = """Invalid event capacity! It should be greater than or
                equal to 1."""
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

    @api.constrains('title')
    def _check_title_is_not_blank(self):
        """ Makes sure that the title of an event isn't blank.
        """
        for record in self:
            if not record.title:
                    msg = """Invalid event title! The event title should not be
                     blank should start before it ends."""
                    raise ValidationError(msg)