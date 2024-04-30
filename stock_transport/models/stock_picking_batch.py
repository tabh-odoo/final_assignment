# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class StockPickingBatch(models.Model):
    _inherit='stock.picking.batch'
    
    dock_id=fields.Many2one('stock.dock', string="Dock")
    vehicle_id=fields.Many2one('fleet.vehicle', string="Vehicle")
    vehicle_category_id=fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category")
    
    total_volume=fields.Float(compute='_compute_batch_volume', string="Volume")
    volume_percent=fields.Float(compute='_compute_batch_volume_percent', string="Volume Percent")
    
    total_weight=fields.Float(compute='_compute_batch_weight', string="Weight", store=True)
    weight_percent=fields.Float(compute='_compute_batch_weight_percent', string="Weight Percent")
    
    transfers_count=fields.Integer(compute='_compute_transfers_count', string="Tranfers", store=True)
    
    @api.depends('picking_ids')
    def _compute_batch_volume(self):
        for record in self:
            record.total_volume = sum(record.picking_ids.mapped('volume_out'))
    
    @api.depends('total_volume')
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