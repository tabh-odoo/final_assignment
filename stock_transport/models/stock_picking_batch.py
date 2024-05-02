# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StockPickingBatch(models.Model):
    _inherit='stock.picking.batch'
    
    dock_id=fields.Many2one('stock.dock', string="Dock")
    vehicle_id=fields.Many2one('fleet.vehicle', string="Vehicle")
    vehicle_category_id=fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category")
    
    total_volume=fields.Float(compute='_compute_batch_volume', string="Volume")
    volume_for_graph=fields.Float()
    volume_percent=fields.Float(compute='_compute_batch_volume_percent', string="Volume Percent")
    
    total_weight=fields.Float(compute='_compute_batch_weight', string="Weight")
    weight_for_graph=fields.Float()
    weight_percent=fields.Float(compute='_compute_batch_weight_percent', string="Weight Percent")
    
    transfers_count=fields.Integer(compute='_compute_transfers_count', string="Tranfers",store=True)
    no_of_lines=fields.Integer(compute='_compute_no_of_lines', string="Lines",store=True)
    
    @api.depends('picking_ids.volume_out')
    def _compute_batch_volume(self):
        for record in self:
            record.total_volume = sum(record.picking_ids.mapped('volume_out'))
            record.volume_for_graph=record.total_volume
    
    @api.depends('picking_ids.volume_out','total_volume','vehicle_category_id.max_volume')
    def _compute_batch_volume_percent(self):
        for record in self:
            if record.vehicle_category_id.max_volume:
                record.volume_percent=(record.total_volume/record.vehicle_category_id.max_volume)*100
            else:
                record.volume_percent=0
    
    @api.depends('picking_ids')        
    def _compute_batch_weight(self):
        for record in self:
            w=0
            for p_ids in record.picking_ids:
                w+=p_ids.shipping_weight
            record.total_weight=w
            print(record.total_weight)
            record.weight_for_graph=w
    
    @api.depends('total_weight')
    def _compute_batch_weight_percent(self):
        for record in self:
            if record.vehicle_category_id.max_weight:
                record.weight_percent=(record.total_weight/record.vehicle_category_id.max_weight)*100
            else:
                record.weight_percent=0
    
    @api.depends('picking_ids')        
    def _compute_transfers_count(self):
        for record in self:
            if record.picking_ids:
                record.transfers_count=len(record.picking_ids)
    
    @api.depends('move_line_ids')
    def _compute_no_of_lines(self):
        for record in self:
            record.no_of_lines = len(record.move_line_ids)
            
    # @api.constrains('weight_for_graph')
    # def _check_weight(self):
    #     for record in self:
    #         print("\n\n  ",record.total_weight)
    #         if record.total_weight > record.vehicle_category_id.max_weight:
    #             raise ValidationError("Total weight cannot exceed the max weight")
            
    