/** @odoo-module **/
import { Message } from "@mail/core/common/message";
import { patch } from "@web/core/utils/patch";
import { A2UIGraph } from "../components/a2ui_graph/a2ui_graph"; // Importación de tu clase

patch(Message.prototype, {
    // Registramos A2UIGraph como subcomponente de Message
    setup() {
        super.setup();
        // Esto permite que el XML reconozca la etiqueta <A2UIGraph />
        this.components = { ...this.components, A2UIGraph };
    },

    get isA2UI() {
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