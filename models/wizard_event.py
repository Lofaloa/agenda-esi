from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class WizardEvent(models.TransientModel):
    """A wizardEvent is the class representing the data used by the wizard. 
        event_start_date is the first date of printed events.
        event_end_date is the last date of printed events.
    """
    _name = 'agenda_esi.wizard'

    event_start_date = fields.Datetime(
        string="Start date", default=fields.Date.today, required=True)
    event_end_date = fields.Datetime(
        string="End date", default=fields.Date.today, required=True)

    """Function called when the button print is clicked. All the needed information is passed to the report."""
    @api.multi
    def print_event_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'event_start_date': self.event_start_date,
                'event_end_date': self.event_end_date,
                'agenda': self.env.context.get('default_agenda_id'),
            },
        }
        return self.env.ref('agenda_esi.recap_report').report_action(self, data=data)

    @api.constrains('event_start_date', 'event_end_date')
    def _check_dates(self):
        for record in self:
            if record.event_end_date < record.event_start_date:
                msg = "Start date must be before end date"
                raise ValidationError(msg)
