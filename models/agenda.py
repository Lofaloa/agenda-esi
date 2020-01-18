# -*- coding: utf-8 -*-

import logging
from .esi_partner import EsiPartner

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Agenda(models.Model):
    """
    An agenda is a set of event organized by an event organizer. The organizer
    can be a person or an organization active at the Haute École Bruxelles
    -Brabant, école supérieure d’informatique.

    Partner can become a member of an agenda. A member gets notified whenever
    the organizer creates a new event.

    Attributes:
        _name (str): This model technical name (agenda_esi.agenda)
        title (odoo.fields.Text): The title of this agenda
        organizer (odoo.fields.Many2One): The partner who organizes this agenda
        events (odoo.fields.Many2One): The set of organized events
        members (odoo.fields.Many2One): The set of an angenda members
    """
    _name = 'agenda_esi.agenda'

    title = fields.Char(required=True)

    # TODO: should they have the matching role? E.g. Can a student organize an
    # event in a pedagogic agenda?
    organizer = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        ondelete='set null',
        default=lambda self: self.env.user.partner_id,
        readonly=True)

    events = fields.Many2many(
        comodel_name='agenda_esi.event',
        required=False,
        ondelete='restrict')

    # TODO: the organizer should not be able to be a member
    members = fields.Many2many(
        comodel_name='res.partner',
        required=False,
        ondelete='set null')

    is_current_user_member = fields.Boolean(compute="_set_is_current_user_member")

    @api.depends('members')
    def _set_is_current_user_member(self):
        for record in self:
            current_user = self.env.user.partner_id
            records = self.members.filtered(lambda m: m.id == current_user.id)
            record.is_current_user_member = len(records) == 1

    @api.constrains('title')
    def _check_title_is_not_blank(self):
        """ Makes sure that the title of an agenda isn't blank.
        """
        for record in self:
            if not record.title:
                msg = """Invalid agenda title! The event title should not be\
                    blank."""
                raise ValidationError(msg)

    @api.multi
    def show_calendar_action(self):
        """ Return an action as a dictionnary. The action shows a calendar view
        that contains all this agenda events. This agenda id is passed in the
        action context and can be found with the key 'default_agenda_id'.

        This action should be called by the button (Calendar) in the agenda
        list view cell.

        Note (Logan): I didn't find any documentation concerning Odoo 11. The
        dictionnary entries are based on the Odoo 8 documentation.

        Checking out the table schema helps too (describe table).

        https://www.odoo.com/documentation/8.0/reference/actions.html
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agenda Events',
            'view_mode': 'calendar',
            'res_model': 'agenda_esi.event',
            'context': {'default_agenda_id': self.id},
            'domain': [('id', 'in', self.events.ids)]
        }

    def _is_current_user_member(self):
        current_user = self.env.user.partner_id
        records = self.members.filtered(lambda m: m.id == current_user.id)
        return len(records) == 1

    @api.multi
    def show_graph_action(self):
        """ Return an action as a dictionnary. The action shows a calendar view
        that contains all this agenda events. This agenda id is passed in the
        action context and can be found with the key 'default_agenda_id'.

        This action should be called by the button (Calendar) in the agenda
        list view cell.

        Note (Logan): I didn't find any documentation concerning Odoo 11. The
        dictionnary entries are based on the Odoo 8 documentation.

        Checking out the table schema helps too (describe table).

        https://www.odoo.com/documentation/8.0/reference/actions.html
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Graph events',
            'view_mode': 'graph',
            'res_model': 'agenda_esi.event',
            # 'context': {'default_agenda_id': self.id},
            # 'domain': [('id', 'in', self.events.ids)]
        }
    
    def follow(self):
        """ Adds the current user to this agenda members. If the user is a
        member then a call to this method removes him from this agenda members.

        TODO: find a way to unit test this function. I was not able to set the
        current user in a unit test context (Logan).
        """
        current_user = self.env.user.partner_id
        if not self._is_current_user_member():
            self.write({'members': [(4, current_user.id)]})
        else:
            self.write({'members': [(3, current_user.id)]})
        return True