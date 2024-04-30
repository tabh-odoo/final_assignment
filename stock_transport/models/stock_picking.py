# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit='stock.picking'
    
    volume_out=fields.Float(compute='_compute_volume_out', string="Volume",store=True)
    
    
    def _compute_volume_out(self):
        for record in self:
            total_volume=0
            for product in record.move_ids:
                total_volume+=(product.quantity * product.product_id.volume)
            record.volume_out=total_volume
        return True
            
    # volume = fields.Float(compute="_compute_total_volume", string="Volume")

    # @api.depends('product_id.volume', 'move_ids.quantity')
    # def _compute_total_volume(self):
    #     for rec in self:
    #         for prod in rec:
    #             list1 = prod.move_ids.mapped('quantity')
    #             list2 = prod.move_ids.product_id.mapped('volume')
    #             volume_sum = sum(x * y for x, y in zip(list1, list2))
    #         rec.volume = volume_sum