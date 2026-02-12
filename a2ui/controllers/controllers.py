# from odoo import http


# class A2ui(http.Controller):
#     @http.route('/a2ui/a2ui', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/a2ui/a2ui/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('a2ui.listing', {
#             'root': '/a2ui/a2ui',
#             'objects': http.request.env['a2ui.a2ui'].search([]),
#         })

#     @http.route('/a2ui/a2ui/objects/<model("a2ui.a2ui"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('a2ui.object', {
#             'object': obj
#         })

