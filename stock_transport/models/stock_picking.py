# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit='stock.picking'
    
    volume_out=fields.Float(compute='_compute_volume_out', string="Volume")
    
    @api.depends('move_ids.quantity')
    def _compute_volume_out(self):
        for record in self:
            total_volume=0
            for product in record.move_ids:
                total_volume+=(product.quantity * product.product_id.volume)
            record.volume_out=total_volume
        return True