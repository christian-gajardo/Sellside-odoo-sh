/** @odoo-module **/
import { Message } from "@mail/core/common/message";
import { patch } from "@web/core/utils/patch";
import { A2UIGraph } from "../components/a2ui_graph/a2ui_graph"; // <--- IMPORTANTE: Verifica esta ruta

patch(Message.prototype, {
    setup() {
        // En OWL, los subcomponentes se declaran en el objeto this.components
        this.components = {
            ...this.components,
            A2UIGraph
        };
        return super.setup(...arguments);
    },

    get isA2UI() {
        // Accedemos a props.message porque estamos en el componente Message
        const body = this.props.message.body || "";
        return body.includes('type": "a2ui_render"');
    },

    get a2uiData() {
        try {
            const div = document.createElement('div');
            div.innerHTML = this.props.message.body;
            const rawText = div.textContent || div.innerText || "";
            return JSON.parse(rawText);
        } catch (e) {
            return null;
        }
    }
});