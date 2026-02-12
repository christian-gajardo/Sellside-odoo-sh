# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup

class A2UISource(models.Model):
    _name = 'a2ui.source'
    _description = 'Fuentes Web para IA'

    name = fields.Char(string='Nombre de la Fuente', required=True)
    url = fields.Char(string='URL de la Web', required=True)
    selector = fields.Char(string='Selector CSS (Opcional)', help="Para extraer solo una parte específica de la web")
    active = fields.Boolean(default=True)

    def get_web_content(self):
        """ Método para extraer texto plano de la URL """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Si hay un selector, filtramos; si no, traemos el body
            target = soup.select_one(self.selector) if self.selector else soup.body
            return target.get_text(separator=' ', strip=True) if target else "No se encontró contenido."
        except Exception as e:
            return f"Error al acceder a la web: {str(e)}"