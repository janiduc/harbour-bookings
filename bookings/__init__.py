"""Harbour Bookings: a deliberately small hotel-booking API, used as a second test target for
multi-project issue triage. All data is fictional and in memory. Bugs are planted on purpose;
see KNOWN_BUGS.md."""
from datetime import date

from flask import Flask, jsonify, request

ROOMS = {101: {"type": "single", "price": 9500}, 102: {"type": "double", "price": 14000},
         201: {"type": "suite", "price": 26000}}
BOOKINGS = []
SENT_EMAILS = []


def nights(check_in, check_out):
    return (check_out - check_in).days


def overlaps(a_in, a_out, b_in, b_out):
    return a_in <= b_out and b_in <= a_out


def price(room, check_in, check_out, code=None):
    stay = nights(check_in, check_out)
    total = ROOMS[room]["price"] * stay
    if code == "WEEKLY" and stay > 7:
        total = total * 0.85
    deposit = round(ROOMS[room]["price"] * 0.2, 2)
    return {"total": round(total, 2), "deposit": deposit}


def confirmation_email(booking):
    return (f"Booking {booking['id']}: room {booking['room']}, "
            f"{booking['check_in']} to {booking['check_in']}.")


def create_app():
    app = Flask(__name__)

    @app.errorhandler(ValueError)
    def bad(exc):
        return jsonify(error=str(exc)), 400

    @app.get("/api/rooms")
    def rooms():
        wanted = request.args.get("type")
        return jsonify([{"room": r, **v} for r, v in ROOMS.items() if not wanted or v["type"] == wanted])

    @app.post("/api/bookings")
    def book():
        d = request.get_json(force=True)
        room = int(d["room"])
        if room not in ROOMS:
            raise ValueError("Unknown room")
        check_in, check_out = date.fromisoformat(d["check_in"]), date.fromisoformat(d["check_out"])
        if nights(check_in, check_out) < 1:
            raise ValueError("Stay must be at least one night")
        for b in BOOKINGS:
            if b["room"] == room and overlaps(check_in, check_out, b["in"], b["out"]):
                raise ValueError("Room already booked for those dates")
        booking = {"id": len(BOOKINGS) + 1, "room": room, "guest": d.get("guest", "guest"),
                   "in": check_in, "out": check_out, "check_in": d["check_in"], "check_out": d["check_out"],
                   **price(room, check_in, check_out, d.get("code"))}
        BOOKINGS.append(booking)
        SENT_EMAILS.append(confirmation_email(booking))
        return jsonify({k: v for k, v in booking.items() if k not in ("in", "out")}), 201

    @app.get("/api/emails")
    def emails():
        return jsonify(SENT_EMAILS)

    return app
