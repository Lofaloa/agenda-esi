from odoo.exceptions import ValidationError

def create_event(test, title, periodicity, start, end, classroom, capacity):
    return test.env['agenda_esi.event'].create({
        'title': title,
        'periodicity': periodicity,
        'start_datetime': start,
        'end_datetime': end,
        'classroom': classroom,
        'capacity': capacity
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

def assert_event_equal(test, record, title, periodicity, start, end, classroom, capacity):
    test.assertEqual(record.title, title)
    test.assertEqual(record.start_datetime, start.__str__())
    test.assertEqual(record.end_datetime, end.__str__())
    test.assertEqual(record.periodicity, periodicity)
    test.assertEqual(record.capacity, capacity)

def assert_agenda_equal(test, record, title, organizer):
    test.assertEqual(record.title, title)
    test.assertEqual(record.organizer, organizer)

def assert_agenda_error(test, title, organizer):
    test.assertRaises(ValidationError, create_agenda, test, title, organizer.id)