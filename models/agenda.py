# -*- coding: utf-8 -*-

from .esi_partner import EsiPartner

from odoo import models, fields, api

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

    @api.multi
    def show_calendar_action(self):
        """ Return an action as a dictionnary. The action shows a calendar view
        that contains all this agenda events.

        This action should be called by the button (Calendar) in the agenda
        list view cell.

        Note (Logan): I didn't find any documentation concerning Odoo 11. The
        dictionnary entries are based on the Odoo 8 documentation.

        Checkint out the table schema helps too (describe table).

        https://www.odoo.com/documentation/8.0/reference/actions.html
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agenda Events',
            'view_mode': 'calendar',
            'res_model': 'agenda_esi.event',
            'domain': [('id', 'in', self.events.ids)]
        }