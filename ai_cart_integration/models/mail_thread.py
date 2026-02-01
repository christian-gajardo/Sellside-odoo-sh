from odoo import models, api, _

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def action_add_to_cart_ai(self, product_ids):
        """
        Esta función será llamada por el Agente de IA.
        """
        if not product_ids:
            return "No se especificaron productos."

        sale_order = self.env['website'].get_current_website().sale_get_order(force_create=True)
        
        for p_id in product_ids:
            sale_order._cart_update(
                product_id=int(p_id),
                add_qty=1
            )
        
        return f"¡Listo! He añadido {len(product_ids)} productos a tu carrito de compras."