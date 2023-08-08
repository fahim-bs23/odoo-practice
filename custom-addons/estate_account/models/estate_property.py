from odoo import models

class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()

        for record in self:
            move = self.env["account.move"].sudo().create(
                {
                    "partner_id": record.user_id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": record.name,
                                "quantity": 1.0,
                                "price_unit": record.selling_price * 6.0 / 100.0,
                            },
                        ),
                    ],
                }
            )
        return res
            