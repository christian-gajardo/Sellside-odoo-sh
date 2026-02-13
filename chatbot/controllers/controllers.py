# from odoo import http


# class Chatbot(http.Controller):
#     @http.route('/chatbot/chatbot', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chatbot/chatbot/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('chatbot.listing', {
#             'root': '/chatbot/chatbot',
#             'objects': http.request.env['chatbot.chatbot'].search([]),
#         })

#     @http.route('/chatbot/chatbot/objects/<model("chatbot.chatbot"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chatbot.object', {
#             'object': obj
#         })

