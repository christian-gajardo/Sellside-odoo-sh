# Odoo 19 – E-commerce Tech + IA

Este repositorio documenta el desarrollo e implementación de una tienda e-commerce basada en **Odoo 19**, enfocada en la venta de PCs y periféricos, integrando sitio web, inventario, ventas y un agente de IA capaz de asistir al cliente directamente desde el Live Chat.

El objetivo principal del proyecto es demostrar cómo Odoo puede centralizar procesos comerciales y, al mismo tiempo, extender sus capacidades mediante configuración y desarrollo en Python, manteniendo una solución clara, escalable y fácil de entender.

---

## Alcance del Proyecto

El proyecto cubre tanto **configuración funcional en Odoo** como **desarrollo técnico**, incluyendo:

* Creación y personalización del sitio web.
* Configuración de Inventario, Ventas y Live Chat.
* Activación y uso de la IA nativa de Odoo.
* Creación de agentes de IA personalizados.
* Desarrollo de funcionalidades en Python para interactuar con el carrito de compras.
* Integración de la IA con lógica real de negocio (stock, órdenes de venta y carrito).

---

## Arquitectura General

El funcionamiento del sistema se basa en la integración de varios módulos de Odoo:

* **Website**: Interfaz principal del e-commerce.
* **Live Chat**: Canal de comunicación entre el usuario y el agente de IA.
* **IA (AI)**: Agentes inteligentes que interpretan las solicitudes del cliente.
* **Inventario**: Gestión de productos, stock y disponibilidad.
* **Ventas**: Manejo de carritos y órdenes de venta.

El flujo principal es el siguiente:

1. El usuario navega por el sitio web y conversa con el agente de IA.
2. El agente responde consultas sobre productos y stock.
3. Cuando el usuario solicita agregar productos al carrito, la IA ejecuta una acción del servidor.
4. Odoo valida stock, crea o reutiliza el carrito y actualiza la orden de venta.
5. El resultado se refleja inmediatamente en la experiencia del usuario.

---

## Configuración en Odoo

### Habilitación de Módulos

Se activaron los siguientes módulos:

* Sitio Web
* Ventas
* Inventario
* Live Chat
* IA (AI)

Estos módulos permiten cubrir todo el flujo comercial sin dependencias externas.

### Agente de IA

Se creó un agente de IA personalizado, configurando:

* Nombre e imagen visibles para el usuario.
* Modelo LLM (GPT o Gemini).
* Instrucciones claras sobre su rol como asistente de ventas.
* Temas de IA, que definen qué herramientas puede usar.

### Live Chat

El Live Chat se configuró para utilizar directamente el agente de IA, permitiendo:

* Atención automática dentro del sitio web.
* Uso de reglas para activar el agente según el contexto.
* Integración directa con el website.

---

## Gestión de Inventario

Para efectos de demostración, los productos fueron cargados mediante archivos Excel (.xls), generados con ayuda de IA. El proceso incluye:

* Creación manual de categorías.
* Importación masiva de productos.
* Validación de campos obligatorios (nombre, precio, costo, stock, referencia interna).

Una vez cargados, los productos quedan disponibles tanto para el sitio web como para el agente de IA.

---

## Desarrollo en Python

### Módulo Personalizado

Se creó un módulo Odoo utilizando `odoo-bin scaffold`, lo que genera automáticamente la estructura base del módulo. Para este proyecto, el desarrollo efectivo se concentró principalmente en **un modelo Python** y en la configuración del `__manifest__.py`; el resto de los archivos corresponden a la base estándar generada por Odoo.

La estructura general del módulo es la siguiente:

```
ai_tech_agent/
├── controllers/        # Base generada por scaffold (no utilizada en esta funcionalidad)
├── models/
│   ├── mail_thread.py  # Lógica principal de integración IA + carrito
│   └── models.py      # Archivo base del módulo
├── security/           # Permisos básicos del módulo
├── views/              # Vistas base (no utilizadas directamente)
├── __manifest__.py     # Dependencias y configuración del módulo
└── __init__.py
```

### Lógica de Integración con el Carrito

La funcionalidad central se implementa heredando el modelo `mail.thread`, que es la base utilizada por Odoo para manejar mensajes y conversaciones. Esto permite que la IA ejecute acciones directamente desde el Live Chat sin romper el flujo estándar del sistema.

* **ai_action_add_to_cart**: método principal invocado por la IA. Recibe una lista de productos, obtiene o crea el carrito activo del usuario y delega la adición de productos.
* **_ai_get_or_create_sale_order**: busca una orden de venta en estado *draft* asociada al usuario y al sitio web actual. Si no existe, crea una nueva automáticamente.
* **_ai_add_products_to_order**: añade los productos al carrito utilizando `_cart_update`, el método nativo del e-commerce de Odoo, asegurando compatibilidad con precios, impuestos y stock.

Finalmente, se realiza un `commit` explícito para que los cambios se reflejen inmediatamente en la experiencia del usuario dentro del sitio web.

---

## Acciones del Servidor y Temas de IA

La acción del servidor se configuró para:

* Ser utilizada en el sitio web.
* Ser invocable desde la IA.
* Definir un esquema de entrada claro (`product_ids`).

Posteriormente, esta acción se agregó a un **Tema de IA**, permitiendo controlar exactamente qué herramientas puede usar el agente, manteniendo seguridad y control.

---

## Resultado Final

El resultado es un agente de IA totalmente integrado al e-commerce, capaz de:

* Responder consultas de productos.
* Verificar stock en tiempo real.
* Agregar productos al carrito desde el chat.
* Actualizar órdenes de venta automáticamente.

Todo esto ocurre sin salir del sitio web, entregando una experiencia fluida y moderna para el usuario.


