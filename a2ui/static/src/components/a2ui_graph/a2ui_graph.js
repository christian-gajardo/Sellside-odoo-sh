/** @odoo-module **/
import { Component, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class A2UIGraph extends Component {
    static template = "a2ui.A2UIGraph";

    setup() {
        this.canvasRef = useRef("canvas");
        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext('2d');
        // Usamos la librería Chart global de Odoo
        new window.Chart(ctx, {
            type: this.props.data.type || 'bar',
            data: {
                labels: this.props.data.labels,
                datasets: this.props.data.datasets
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: this.props.data.title }
                }
            }
        });
    }
}

// Registramos el componente en el sistema A2UI
registry.category("a2ui_components").add("A2UIGraph", A2UIGraph);