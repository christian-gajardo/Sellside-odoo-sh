from odoo import models, api, _
from odoo.http import request  # <--- IMPORTANTE: Necesario para la sesión

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def ai_action_add_to_cart(self, product_ids):
        if not product_ids:
            return _("No se indicaron productos.")

        sale_order = self._ai_get_or_create_cart()
        added_names = self._ai_process_cart_items(sale_order, product_ids)
        
        if added_names:
            # --- VINCULACIÓN VISUAL ---
            # Si hay una petición web activa, guardamos el ID en la sesión
            if request and hasattr(request, 'session'):
                request.session['sale_order_id'] = sale_order.id
            
            self.env.cr.commit()
            return _("¡Listo! He añadido %s a tu carrito.") % (", ".join(added_names))
        
        return _("No pude añadir los productos.")

    def _ai_get_or_create_cart(self):
        website = self.env['website'].get_current_website()
        partner = self.env.user.partner_id
        
        # Intentamos obtener la orden de la sesión actual primero
        order = website.sale_get_order()
        
        if not order:
            # Si no hay en sesión, buscamos en DB por partner
            order = self.env['sale.order'].sudo().search([
                ('partner_id', '=', partner.id),
                ('website_id', '=', website.id),
                ('state', '=', 'draft')
            ], limit=1, order='date_order desc')

        if not order:
            order = self.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'website_id': website.id,
                'company_id': website.company_id.id,
            })
        return order

    def _ai_process_cart_items(self, sale_order, product_ids):
        ids = [product_ids] if isinstance(product_ids, (int, str)) else product_ids
        success_names = []
        
        for p_id in ids:
            try:
                # Usamos sudo() para evitar problemas de acceso en el carrito
                product = self.env['product.product'].sudo().browse(int(p_id))
                if product.exists():
                    # El método _cart_update es el que hace la magia del eCommerce
                    sale_order.sudo()._cart_update(product_id=product.id, add_qty=1)
                    success_names.append(product.name)
            except Exception:
                continue
        return success_names