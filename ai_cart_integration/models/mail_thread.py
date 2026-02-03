from odoo import models, api



class MailThread(models.AbstractModel):

    _inherit = 'mail.thread'

    

    @api.model

    def ai_action_add_to_cart(self, product_ids):

        # 1. Obtenemos el sitio web

        website = self.env['website'].get_current_website()

        

        # Intentamos obtener el partner del chat para que el carrito sea el del usuario

        # Si no lo encontramos, usamos el del usuario actual (env.user)

        partner = self.env.user.partner_id

        

        # Buscamos un carrito existente para este partner en este sitio web

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

        

        summary = []

        for p_id in product_ids:

            try:

                product = self.env['product.product'].sudo().browse(int(p_id))

                if product.exists():

                    # Usamos sudo() para asegurar que la IA tenga permisos de escritura

                    sale_order.sudo()._cart_update(product_id=product.id, add_qty=1)

                    summary.append(product.name)

            except Exception:

                continue

        

        # MUY IMPORTANTE: Commit para forzar que el navegador vea el cambio

        self.env.cr.commit()

        

        if not summary:

            return "No se pudieron añadir los productos."

            

        return f"¡Hecho! He añadido {', '.join(summary)} a tu carrito. Por favor, refresca la página para verlo."