# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'
    
    max_weight=fields.Float(string="Max Weight")
    max_volume=fields.Float(string="Max Volume")
    
    display_name = fields.Char(compute='_compute_display_name')
    
    @api.depends('max_weight','max_volume')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.max_weight and record.max_volume:
                name = f"{name} ({record.max_weight} kg, {record.max_volume} m3)"
            record.display_name = name 
    
    @api.depends('max_weight','max_volume','name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.name}({rec.max_weight}kg,{rec.max_volume}m³)'
    
