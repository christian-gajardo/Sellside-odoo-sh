from odoo import models, api, _

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def ai_action_add_to_cart(self, product_ids):
        """
        Método principal invocado por la IA para añadir productos al carrito.
        Gestiona la obtención del pedido, la adición de líneas y la confirmación de la transacción.

        :param product_ids: ID o lista de IDs de los productos a añadir.
        :return: Mensaje de éxito o error traducido.
        """
        if not product_ids:
            return _("No se indicaron productos.")

        sale_order = self._ai_get_or_create_sale_order()
        added_products = self._ai_add_products_to_order(sale_order, product_ids)

        if not added_products:
            return _("No se pudieron añadir los productos al carrito.")

        self._ai_update_crm_lead(sale_order, added_products)

        self.env.cr.commit()
        return _("¡Hecho! He añadido %s a tu carrito. Por favor, refresca la página para verlo.") % (', '.join(added_products))

    def _ai_get_or_create_sale_order(self):
        """
        Busca un pedido de venta en estado borrador (carrito) para el usuario y sitio web actuales.
        Si no existe ninguno, crea uno nuevo.

        :return: Registro de sale.order.
        """
        website = self.env['website'].get_current_website()
        partner = self.env.user.partner_id
        sale_order = self.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('website_id', '=', website.id),
            ('state', '=', 'draft')
        ], limit=1, order='date_order desc')

        if not sale_order:
            sale_order = self.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'website_id': website.id,
            })
        return sale_order

    def _ai_add_products_to_order(self, sale_order, product_ids):
        """
        Añade los productos especificados al pedido de venta.
        Utiliza el método nativo _cart_update para asegurar compatibilidad con el flujo de eCommerce.

        :param sale_order: Pedido de venta donde añadir los productos.
        :param product_ids: ID o lista de IDs de productos.
        :return: Lista con los nombres de los productos añadidos correctamente.
        """
        ids = [product_ids] if isinstance(product_ids, (int, str)) else product_ids
        summary = []

        for p_id in ids:
            try:
                product = self.env['product.product'].sudo().browse(int(p_id))
                if product.exists():
                    sale_order.sudo()._cart_update(product_id=product.id, add_qty=1)
                    summary.append(product.name)
            except Exception:
                continue
        return summary
    
    def _ai_update_crm_lead(self, sale_order, product_names):
        """
        Sincroniza la actividad del carrito con el CRM.
        Si existe una oportunidad abierta para el cliente, actualiza su descripción.
        De lo contrario, crea una nueva iniciativa con prioridad basada en el monto del pedido.

        :param sale_order: Registro del pedido de venta (carrito).
        :param product_names: Lista de nombres de los productos añadidos.
        """
        crm_lead_obj = self.env['crm.lead'].sudo()

        existing_lead = crm_lead_obj.search([
            ('partner_id', '=', sale_order.partner_id.id),
            ('type', '=', 'opportunity'),
            ('probability', '<', 100)
        ], limit=1)

        description = _("Productos en carrito: %s") % (', '.join(product_names))

        if existing_lead:
            existing_lead.description = (existing_lead.description or '') + "\n" + description
        else:
            crm_lead_obj.create({
                'name': _("Interés en Hardware: %s") % sale_order.partner_id.name,
                'partner_id': sale_order.partner_id.id,
                'user_id': self.env.user.id,
                'team_id': self.env['crm.team'].search([], limit=1).id,
                'description': description,
                'planned_revenue': sale_order.amount_total,
                'priority': '2' if sale_order.amount_total > 1000 else '1',
            })