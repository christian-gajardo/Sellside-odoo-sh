/** @odoo-module **/
import { Message } from "@mail/components/message/message";
import { patch } from "@web/core/utils/patch";

patch(Message.prototype, {
    // Definimos un getter para detectar si el mensaje es A2UI
    get isA2UI() {
        return this.message.body && this.message.body.includes('type": "a2ui_render"');
    },

    // Limpiamos el JSON del cuerpo para obtener los datos puros
    get a2uiData() {
        try {
            const rawBody = this.message.body.replace(/<[^>]*>/g, ''); // Quitamos tags HTML de Odoo
            return JSON.parse(rawBody);
        } catch (e) {
            return null;
        }
    }
});