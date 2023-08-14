import pytz
import datetime
import base64
from io import BytesIO
import xlsxwriter
from odoo import models
from odoo.modules.module import get_module_resource


class EstatePropertyXlS(models.AbstractModel):
    _name = "report.estate.report_estate_property_xls"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, property):
        worksheet = workbook.add_worksheet('Estate Report')

        worksheet.write('A1', 'Property name')
        worksheet.write('B1', 'Property description')
        worksheet.write('C1', 'Property expected_price')
        worksheet.write('D1', 'Property status')

        worksheet.write(1, 0, property.name)
        worksheet.write(1, 1, property.description)
        worksheet.write(1, 2, property.expected_price)
        worksheet.write(1, 3, property.status)

        if property.property_offer_ids:
            worksheet.write('E1', 'Offer price')
            worksheet.write('F1', 'Status')
        row = 2
        for offer in property.property_offer_ids:
            worksheet.write(row, 4, offer.offer_price)
            worksheet.write(row, 5, offer.status)
            row += 1
