# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id"

    name = fields.Char('Estate Name', required=True)
    description = fields.Text()
    postcode = fields.Char('Postal Code', required=True)
    date_availability = fields.Date(required=False)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', required=True)
    bedrooms = fields.Integer('Bedrooms', required=True)
    living_area = fields.Integer('Living Area', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage', default=True)
    garden = fields.Boolean('Garden', default=True)
    garden_area = fields.Integer('Garden area', required=True)
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden orientation")
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offer')
    price_difference = fields.Float(compute="_compute_price_difference")
    status = fields.Selection(
        string='Status',
        selection=[('pending', 'Pending'), ('cancel', 'Cancel'), ('sold', 'Sold')],
        default="pending")
    user_id = fields.Many2one('res.users', string='Property User')

    # @api.model
    def write(self, vals):
        estate_property = self
        property_offer_status = False
        if 'status' in vals:
            status = vals['status']
            if status == 'sold':
                if any(offer.status == "accepted" for offer in estate_property.property_offer_ids):
                    property_offer_status = True
                if not property_offer_status:
                    raise exceptions.ValidationError("No accepted offer found.")
        return super(EstateProperty, self).write(vals)

    @api.depends("expected_price", "selling_price")
    def _compute_price_difference(self):
        for record in self:
            record.price_difference = abs(record.expected_price - record.selling_price)

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
    

    def action_sold(self):
        if self.status == "pending":
            self.status = "sold"
        else:
            return False

    def action_cancel(self):
        if self.status == "pending":
            self.status = "cancel"
        else:
            return False

    @api.constrains("expected_price", "selling_price")
    def _check_positive_value(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("Expected price cannot be negative.")
            if record.selling_price < 0:
                raise ValidationError("Selling price cannot be negative.")
    
    def action_view_property_offer(self):
       return {
            'name': _('Property Offer'),           
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('id', 'in', self.property_offer_ids.ids)],
            'target': 'self',
        }

    def unlink(self):
        for record in self:
            if record.status == 'sold':
                raise exceptions.UserError("You cannot delete this record because it's sold.")
        return super(EstateProperty, self).unlink()

