from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


# @tagged('post_install', '-at_install')
class TestPropertyOffers(TransactionCase):

    def setUp(self):
        super(TestPropertyOffers, self).setUp()
        self.property_model = self.env['estate.property']
        self.property_offer_model = self.env['estate.property.offer']

    def test_accepted_offers_on_sold_property(self):
        property_vals = {
            'name': 'Sample Property',
            'postcode': '1200',
            'expected_price': '12000',
            'selling_price': '0',
            'bedrooms': '2',
            'living_area': '900',
            'facades': '5',
            'garden_area': '1200',
            'status': 'pending',
        }
        property_record = self.property_model.create(property_vals)

        offer_vals = {
            'offer_price': '15000',
            'status': 'pending',
            'property_id': property_record.id,
        }
        self.property_offer_model.create(offer_vals)

        with self.assertRaises(ValidationError):
            property_record.write({'status': 'sold'})

        self.assertEqual(property_record.status, 'pending'," Property status should remain pending.")
