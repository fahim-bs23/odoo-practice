# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "offer_price"

    offer_price = fields.Float(string='Offer price', required=True)
    status = fields.Selection(
        string='Offer Status',
        selection=[('pending', 'Pending'), ('refused', 'Refused'), ('accepted', 'Accepted')])
    property_id = fields.Many2one('estate.property', string='Estate Property')

    def action_accepted(self):
        self.status = "accepted"
        self.property_id.status = "sold"
        self.property_id.selling_price = self.offer_price
    
    def action_refused(self):
        self.status = "refused"

    @api.constrains("offer_price")
    def _check_positive_value(self):
        for record in self:
            if record.offer_price < 0:
                raise ValidationError("Offer price cannot be negative.")
