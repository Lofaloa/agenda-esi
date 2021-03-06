# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

import logging

class ReportAttendees(models.AbstractModel):

    _name = 'report.agenda_esi.events_recap_report_view'
    
    @api.model
    def get_report_values(self, docids, data=None):
        date_start = data['form']['event_start_date']
        date_end = data['form']['event_end_date']
        agenda = data['form']['agenda']

        docs = []
        events = self.env['agenda_esi.event'].search([
            ('start_datetime', '>=', date_start),
            ('end_datetime', '<=', date_end),
            ('agenda', '=', agenda),
        ])
        for event in events:
            docs.append({
                'title': event.title,
                'classroom': event.classroom,
                'capacity': event.capacity,
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'len_docs': len(docs),
        }
