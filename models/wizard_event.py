from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

import logging

_logger = logging.getLogger(__name__)


class WizardEvent(models.TransientModel):
    _name = 'agenda_esi.wizard'

    event_start_date = fields.Datetime(
        string="Start date", default=fields.Date.today, required=True)
    event_end_date = fields.Datetime(
        string="End date", default=fields.Date.today, required=True)

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
