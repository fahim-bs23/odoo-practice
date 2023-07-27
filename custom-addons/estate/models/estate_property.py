# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


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
