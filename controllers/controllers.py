# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request, Response

import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class AgendaEsi(http.Controller):

    def event_to_dictionnary(self, event):
        return {
            "title": event.title,
            "start": event.start_datetime,
            "end": event.end_datetime
        }

    @http.route('/api/events', auth='public')
    def index(self, **kw):
        current_date = str(datetime.now())
        result = http.request.env['agenda_esi.event'].search([('start_datetime', '>=', current_date)])
        events = []
        for e in result:
            events.append(self.event_to_dictionnary(e))
        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'events': events}}
        return Response(json.dumps(body), headers=headers)
