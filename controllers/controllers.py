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

    @http.route('/api/events/<string:login>', auth='public')
    def index(self, **kw):
        # TODO: search the event in which the current user is an attendee and
        # having starting in the future
        current_date = str(datetime.now())
        values = dict(kw)
        user = http.request.env['res.users'].search(
            [('login', '=', values['login']), ])

        result = http.request.env['agenda_esi.event'].search(
            ['&', ('start_datetime', '>=', current_date),
                (user.partner_id, 'in', 'attendees.ids'), ])
        events = []
        for e in result:
            events.append(self.event_to_dictionnary(e))
        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'events': events}}
        return Response(json.dumps(body), headers=headers)
