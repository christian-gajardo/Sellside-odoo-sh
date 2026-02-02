from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    
    @api.model
    def ai_action_add_to_cart(self, product_ids):
        """
        product_ids: lista de strings o ints, ej: ["10", "15"]
        """
        # 1. Obtener el contexto del sitio web y el carrito actual
        website = self.env['website'].get_current_website()
        sale_order = website.sale_get_order(force_create=True)
        
        summary = []
        
        # 2. Iterar sobre la lista de IDs
        for p_id in product_ids:
            try:
                # Convertimos a int por seguridad si viene como string
                product = self.env['product.product'].browse(int(p_id))
                
                if product.exists():
                    # Añadimos una unidad de cada ID recibido
                    sale_order._cart_update(
                        product_id=product.id, 
                        add_qty=1
                    )
                    summary.append(product.name)
            except (ValueError, TypeError):
                continue # Si un ID no es válido, pasamos al siguiente
        
        if not summary:
            return "No se pudieron añadir los productos. Por favor, verifica los códigos."
            
        return f"¡Hecho! He añadido {', '.join(summary)} a tu carrito."