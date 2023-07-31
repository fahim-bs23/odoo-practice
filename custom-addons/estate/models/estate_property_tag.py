# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "id"

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer('Property Tag Color')
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Tag must be unique.'),
    ]