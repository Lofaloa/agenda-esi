# -*- coding: utf-8 -*-

from odoo import models

class Event(models.Model):
    """
    An event is a gathering of poeple taking place at a given time and location
    """
    
    _name = 'agenda_esi.event'