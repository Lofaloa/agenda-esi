# -*- coding: utf-8 -*-

from enum import Enum
from odoo import models, fields

class EsiPartner(models.Model):

    _inherit = 'res.partner'

    is_esi_partner = fields.Boolean(default=False)