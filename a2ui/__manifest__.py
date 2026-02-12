{
    'name': 'A2UI',
    'version': '0.1',
    'summary': 'Permite al agente de IA usar A2UI',
    'author': 'A2UI-Sellside-ChG',
    'depends': [
        'base',
        'mail',
        'ai',
        'ai_app',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/a2ui_source_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'a2ui/static/src/components/**/*',
            'a2ui/static/src/js/**/*',
            'a2ui/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}