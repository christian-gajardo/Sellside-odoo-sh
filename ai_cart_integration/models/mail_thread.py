from odoo import models, api, _

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def ai_action_add_to_cart(self, product_ids):
        """ Puerta de enlace para la IA """
        if not product_ids:
            return _("No se indicaron productos.")

        # 1. Obtener o crear el carrito usando el sub-método
        sale_order = self._ai_get_or_create_cart()
        
        # 2. Procesar los productos usando el sub-método
        added_names = self._ai_process_cart_items(sale_order, product_ids)
        
        if added_names:
            self.env.cr.commit()
            return _("Añadido: %s") % (", ".join(added_names))
        return _("No pude añadir los productos al carrito.")

    def _ai_get_or_create_cart(self):
        """ Busca el carrito actual del usuario o crea uno nuevo """
        website = self.env['website'].get_current_website()
        partner = self.env.user.partner_id
        
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
        """ Itera y añade los productos al pedido """

        ids = [product_ids] if isinstance(product_ids, (int, str)) else product_ids
        success_names = []
        
        for p_id in ids:
            try:
                product = self.env['product.product'].sudo().browse(int(p_id))
                if product.exists():
                    sale_order._cart_update(product_id=product.id, add_qty=1)
                    success_names.append(product.name)
            except Exception:
                continue
        return success_names