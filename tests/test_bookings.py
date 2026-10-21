"""Happy-path tests. They pass, and deliberately do not cover the planted bugs (see KNOWN_BUGS.md)."""
import unittest

from bookings import BOOKINGS, SENT_EMAILS, create_app


class BookingTests(unittest.TestCase):
    def setUp(self):
        BOOKINGS.clear()
        SENT_EMAILS.clear()
        self.client = create_app().test_client()

    def book(self, room, check_in, check_out, **extra):
        return self.client.post("/api/bookings", json={"room": room, "check_in": check_in,
                                                       "check_out": check_out, **extra})

    def test_book_a_room(self):
        res = self.book(101, "2026-11-10", "2026-11-12")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["total"], 19000)

    def test_clash_refused(self):
        self.book(102, "2026-11-10", "2026-11-14")
        self.assertEqual(self.book(102, "2026-11-11", "2026-11-13").status_code, 400)

    def test_weekly_discount_for_long_stay(self):
        res = self.book(101, "2026-11-01", "2026-11-11", code="WEEKLY")
        self.assertEqual(res.get_json()["total"], 9500 * 10 * 0.85)

    def test_filter_rooms_by_type(self):
        rooms = self.client.get("/api/rooms?type=suite").get_json()
        self.assertEqual([r["room"] for r in rooms], [201])


if __name__ == "__main__":
    unittest.main()
