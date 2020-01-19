from datetime import datetime
from odoo.exceptions import ValidationError


def create_event(test, context, title, periodicity, start, end, classroom, capacity):
    return test.env['agenda_esi.event'].with_context(context).create({
        'title': title,
        'periodicity': periodicity,
        'start_datetime': start,
        'end_datetime': end,
        'classroom': classroom,
        'capacity': capacity
    })


def attendees_to_commands(attendees):
    commands = []
    for attendee in attendees:
        commands.append((4, attendee.id))
    return commands


def create_event_with_attendees(test, context, capacity, attendees):
    return test.env['agenda_esi.event'].with_context(context).create({
        'title': "Attended event",
        'periodicity': 'u',
        'start_datetime': datetime(2019, 1, 1, 12, 0, 0),
        'end_datetime': datetime(2019, 1, 1, 13, 0, 0),
        'classroom': 345,
        'capacity': capacity,
        'attendees': attendees_to_commands(attendees)
    })


def create_partner(test, name):
    return test.env['res.partner'].create({'name': name})


def create_agenda(test, title, organizer):
    return test.env['agenda_esi.agenda'].create({
        'title': title,
        'organizer': organizer
    })


def assert_event_error(test, title, periodicity, start, end, classroom, capacity):
    test.assertRaises(ValidationError, create_event, test,
                      title, periodicity, start, end, classroom, capacity
                      )


def assert_event_capacity_error(test, capacity, attendees):
    test.assertRaises(ValidationError, create_event_with_attendees, test,
                      capacity, attendees
                      )


def assert_event_equal(test, record, title, periodicity, start, end, classroom, capacity):
    test.assertEqual(record.title, title)
    test.assertEqual(record.start_datetime, start.__str__())
    test.assertEqual(record.end_datetime, end.__str__())
    test.assertEqual(record.periodicity, periodicity)
    test.assertEqual(record.capacity, capacity)


def assert_agenda_contains(test, agenda, event):
    matching_events = agenda.events.search([('id', '=', event.id)])
    test.assertTrue(matching_events.ensure_one())


def assert_agenda_equal(test, record, title, organizer):
    test.assertEqual(record.title, title)
    test.assertEqual(record.organizer, organizer)


def assert_agenda_error(test, title, organizer):
    test.assertRaises(ValidationError, create_agenda,
                      test, title, organizer.id)


def create_wizard_event(event_start_date, event_end_date):
    return test.env['agenda_esi.wizard'].create({
        'event_start_date': event_start_date,
        'event_end_date': event_end_date,
    })


def assert_date_error(test):
    test.assertRaises(ValidationError)
