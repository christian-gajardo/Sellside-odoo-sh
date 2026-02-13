{
    'name': 'Chatbot',
    'version': '0.1',
    'summary': 'Permite al agente de IA usar Chatbot',
    'author': 'Sellside-ChG',
    'depends': [
        'base',
        'mail',
        'stock',
        'product',
        'website',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/chatbot_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'chatbot/static/src/components/**/*',
            'chatbot/static/src/js/**/*',
            'chatbot/static/src/css/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}