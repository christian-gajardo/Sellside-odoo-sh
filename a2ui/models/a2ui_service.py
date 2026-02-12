# -*- coding: utf-8 -*-
from odoo import models, fields, api

class A2UIService(models.Model):
    _name = 'a2ui.service'
    _description = 'Servicio Lógico A2UI'

    def prepare_a2ui_payload(self, source_id):
        source = self.env['a2ui.source'].browse(source_id)
        raw_text = source.get_web_content()

        # Este es el esquema que le pasaremos al LLM de Odoo
        # Para que el testeo sea real, forzamos a la IA a seguir el protocolo A2UI
        system_prompt = f"""
        Analiza el siguiente texto extraído de {source.url}:
        ---
        {raw_text[:2000]} 
        ---
        Genera un resumen ejecutivo y un gráfico comparativo.
        DEBES responder exclusivamente en formato JSON siguiendo el protocolo A2UI:
        {{
            "type": "a2ui_render",
            "component": "A2UIGraph",
            "data": {{
                "title": "Análisis de {source.name}",
                "labels": ["Item 1", "Item 2", "..."],
                "datasets": [{{ "label": "Valor", "data": [10, 20, "..."] }}]
            }},
            "summary": "Tu resumen aquí"
        }}
        """
        return system_prompt