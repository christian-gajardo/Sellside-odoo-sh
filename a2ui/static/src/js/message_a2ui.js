/** @odoo-module **/
import { Message } from "@mail/core/common/message"; // Esta es la ruta correcta en Odoo 19
import { patch } from "@web/core/utils/patch";

patch(Message.prototype, {
    // En Odoo 19, accedemos a través de props
    get isA2UI() {
        const body = this.props.message.body || "";
        return body.includes('type": "a2ui_render"');
    },

    get a2uiData() {
        try {
            // Eliminamos etiquetas HTML (Odoo envuelve el texto en <p>)
            const rawBody = this.props.message.body.replace(/<[^>]*>/g, '');
            return JSON.parse(rawBody);
        } catch (e) {
            console.error("A2UI: Error parseando el JSON del mensaje", e);
            return null;
        }
    }
});