# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
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

    @api.model
    def create(self, vals):
        if 'property_id' in vals and 'offer_price' in vals:
            existing_offers = self.search([('property_id', '=', vals['property_id'])])
            if existing_offers and any(offer.offer_price > vals['offer_price'] for offer in existing_offers):
                raise exceptions.ValidationError("New offer amount must be higher than existing offers.")
            
            property_id = vals['property_id']
            property_record = self.env['estate.property'].browse(property_id)
            if property_record and property_record.status == 'sold':
                raise exceptions.ValidationError("This property has been already sold.")
            
        return super(EstatePropertyOffer, self).create(vals)