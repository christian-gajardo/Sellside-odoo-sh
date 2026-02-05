# from odoo import models, fields, api


# class ai_cart_integration(models.Model):
#     _name = 'ai_cart_integration.ai_cart_integration'
#     _description = 'ai_cart_integration.ai_cart_integration'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

