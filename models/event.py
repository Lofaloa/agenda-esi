# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Event(models.Model):
    """
    An event is a gathering of people taking place at a given time and location

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

    @api.model
    def _exist_current_agenda(self):
        """ Tells if the default_agenda_id context variable is defined. This
        function is used to tell if this event agenda fiel should be readonly.

        The agenda field should be readonly when the variable is defined.
        """
        return self.env.context.get('default_agenda_id', False)

    _name = 'agenda_esi.event'

    PERIODICITY_OPTIONS = [
        ('d', 'Dayly'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
        ('u', 'None')
    ]

    EVENT_TYPE = [
        # An event of type Student can only by created/ written by a student
        ('s', 'Student'),
        # An event of type Pedagogic can only by created/ written by a teacher
        ('p', 'Pedagogic'),
        # An event of type Administrative can only by created/ written by an
        # administrative partner
        ('a', 'Administrative')
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
    attendees = fields.Many2many(
        comodel_name='res.partner',
        required=False,
        ondelete='set null')

    agenda = fields.Many2one(
        comodel_name="agenda_esi.agenda",
        required=True,
        default=lambda self: self.env.context.get('default_agenda_id', False)
    )

    attendees_count = fields.Integer(
        string="Attendees count",
        compute="_get_attendees_count",
        store=True)

    is_current_user_attendee = fields.Boolean(
        compute="_set_is_current_user_attendee")
    exist_current_agenda_in_context = fields.Boolean(
        default=_exist_current_agenda)

    @api.depends('attendees')
    def _set_is_current_user_attendee(self):
        for record in self:
            current_user = self.env.user.partner_id
            records = self.attendees.filtered(
                lambda a: a.id == current_user.id)
            record.is_current_user_attendee = len(records) == 1

    @api.depends('attendees')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendees)

    @api.constrains('attendees', 'agenda')
    def _check_attendees_are_agenda_members(self):
        for record in self:
            for attendee in record.attendees:
                members = self.agenda.members.filtered(
                    lambda m: m.id == attendee.id)
                if len(members) == 0:
                    msg = '''{user} cannot attend this event, (s)he is not\
                    following this event agenda ({agenda})!
                    '''.format(user=attendee.name, agenda=self.agenda.title)
                    raise ValidationError(msg)

    @api.constrains('attendees', 'capacity')
    def _check_attendees_capacity(self):
        """The number of attendees should respect the event's capacity."""
        for record in self:
            if len(record.attendees) > record.capacity:
                msg = """There are too many attendees registered to this
                event."""
                raise ValidationError(msg)

    @api.constrains('attendees', 'agenda')
    def _check_attendees_capacity(self):
        """ Makes sure an attendee is a member o"""
        for record in self:
            if len(record.attendees) > record.capacity:
                msg = """There are too many attendees registered to this
                event."""
                raise ValidationError(msg)

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
    def _check_classroom(self):
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

    def _is_current_user_attendee(self):
        current_user = self.env.user.partner_id
        records = self.attendees.filtered(lambda a: a.id == current_user.id)
        return len(records) == 1

    def attend(self):
        """ Adds the current user to this event attendees. If the user is
        already one then a call to this method removes him from this event
        attendees.

        TODO: the current user should be a member of this event agenda.
        """
        current_user = self.env.user.partner_id
        if not self._is_current_user_attendee():
            self.write({'attendees': [(4, current_user.id)]})
        else:
            self.write({'attendees': [(3, current_user.id)]})
        return True
