# -*- coding: utf-8 -*-
from odoo import http

# class AgendaEsi(http.Controller):
#     @http.route('/agenda_esi/agenda_esi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/agenda_esi/agenda_esi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('agenda_esi.listing', {
#             'root': '/agenda_esi/agenda_esi',
#             'objects': http.request.env['agenda_esi.agenda_esi'].search([]),
#         })

#     @http.route('/agenda_esi/agenda_esi/objects/<model("agenda_esi.agenda_esi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('agenda_esi.object', {
#             'object': obj
#         })