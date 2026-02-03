from odoo import models, api, _

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def ai_action_add_to_cart(self, product_ids):
        """ 
        Método principal que invoca la IA. 
        Maneja la orquestación y el commit final.
        """
        if not product_ids:
            return _("No se indicaron productos.")

        # 1. Obtener el carrito (Sale Order)
        sale_order = self._ai_get_or_create_sale_order()
        
        # 2. Procesar la adición de productos
        added_products = self._ai_add_products_to_order(sale_order, product_ids)
        
        if not added_products:
            return _("No se pudieron añadir los productos al carrito.")

        # 3. Forzar persistencia
        self.env.cr.commit()
        
        return _("¡Hecho! He añadido %s a tu carrito. Por favor, refresca la página para verlo.") % (', '.join(added_products))

    def _ai_get_or_create_sale_order(self):
        """ Busca un carrito borrador existente o crea uno nuevo """
        website = self.env['website'].get_current_website()
        partner = self.env.user.partner_id
        
        # Buscamos el carrito actual
        sale_order = self.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('website_id', '=', website.id),
            ('state', '=', 'draft')
        ], limit=1, order='date_order desc')

        # Si no existe, lo creamos
        if not sale_order:
            sale_order = self.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'website_id': website.id,
            })
        return sale_order

    def _ai_add_products_to_order(self, sale_order, product_ids):
        """ Itera sobre los IDs y los añade al objeto sale_order """
        # Aseguramos que product_ids sea una lista
        ids = [product_ids] if isinstance(product_ids, (int, str)) else product_ids
        summary = []

        for p_id in ids:
            try:
                product = self.env['product.product'].sudo().browse(int(p_id))
                if product.exists():
                    # El método nativo _cart_update asegura compatibilidad con eCommerce
                    sale_order.sudo()._cart_update(product_id=product.id, add_qty=1)
                    summary.append(product.name)
            except Exception:
                continue
        return summary