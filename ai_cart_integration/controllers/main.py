from odoo import http
from odoo.http import request

class AiCartController(http.Controller):

    @http.route('/shop/cart/update_json_ai', type='jsonrpc', auth="public", methods=['POST'], website=True)
    def add_to_cart_ai(self, product_ids, **kw):
        """
        Recibe una lista de IDs de productos (product.product) y los añade al carrito.
        """
        if not product_ids:
            return {'status': 'error', 'message': 'No se proporcionaron IDs de producto'}

        sale_order = request.website.sale_get_order(force_create=True)
        
        try:
            for p_id in product_ids:
                sale_order._cart_update(
                    product_id=int(p_id),
                    add_qty=1
                )
            
            return {
                'status': 'success',
                'cart_quantity': sale_order.cart_quantity,
                'message': 'Productos añadidos correctamente'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}