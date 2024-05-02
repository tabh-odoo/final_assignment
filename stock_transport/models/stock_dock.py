# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockDock(models.Model):
    _name="stock.dock"
    
    name=fields.Char()