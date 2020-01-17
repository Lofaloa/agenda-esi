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

def assert_event_equal(test, record, title, periodicity, start, end, classroom, capacity):
    test.assertEqual(record.title, title)
    test.assertEqual(record.start_datetime, start.__str__())
    test.assertEqual(record.end_datetime, end.__str__())
    test.assertEqual(record.periodicity, periodicity)
    test.assertEqual(record.capacity, capacity)

def assert_event_error(test, title, periodicity, start, end, classroom, capacity):
    test.assertRaises(ValidationError, create_event, test,
        title, periodicity, start, end, classroom, capacity
    )