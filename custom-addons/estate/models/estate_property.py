# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


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