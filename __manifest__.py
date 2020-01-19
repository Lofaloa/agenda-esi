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
        'security/security_groups.xml',
        'security/security_student_rules.xml',
        'security/security_teacher_rules.xml',
        'security/security_administrative_rules.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/agenda/form.xml',
        'views/agenda/list.xml',
        'views/event/form.xml',
        'views/event/list.xml',
        'views/event/calendar.xml',
        'views/event/graph.xml',
        'views/esi_partner/form.xml',
        'views/esi_partner/list.xml',
        'reports/attendees_report.xml',
        'views/wizards/print_report_event.xml',
        'reports/events_report.xml',
        'views/esi_partner/form.xml',
        'views/esi_partner/list.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo_teachers.xml',
        'demo/demo_students.xml',
        'demo/demo_administratives.xml',
        'demo/demo_agendas.xml',
        'demo/demo_events.xml',
    ],
}
