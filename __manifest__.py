# -*- coding: utf-8 -*-
{
    'name': "L'agenda ESI",

    'summary': """
        Gère les événements présents dans l'agenda d'un étudiant de l'ESI.
    """,

    'description': """
        Gère les événements présents dans l'agenda d'un étudiant de l'ESI.
        On retrouve dans ces événements les cours suivis, les
        interrogations, les remises de projets, les réunions et toutes
        autres activités organisées par les étudiants.
    """,

    'author': "Anthony Farci et Logan Farci",
    'website': "https://git.esi-bru.be/ERPG5-E11-2019/47923_49737",
    'category': 'Events',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
