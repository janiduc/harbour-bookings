# Known bugs (answer key)

Planted on purpose so the seed issues describe real, reproducible problems. Do not fix them before
the triage demo. Modules match the desk project's module list: bookings, payments, notifications,
other.

| # | Module | Where | Bug | Seed issue |
|---|---|---|---|---|
| 1 | bookings | `overlaps` | Uses `<=`, so a stay starting on another's check-out day is refused | "Cannot book a room on the day the previous guest leaves" (and the vague "Overbooked again!!!") |
| 2 | payments | `price` | Deposit is 20% of one night, not of the whole stay | "Deposit far too low on long stays" |
| 3 | notifications | `confirmation_email` | Prints the check-in date twice | "Confirmation email shows the wrong check-out date" |
| 4 | payments | `price` | WEEKLY discount needs more than 7 nights instead of 7 or more | "WEEKLY code does not work for a seven-night stay" |
| 5 | bookings | `rooms` | Room type filter is case-sensitive | "Room filter returns nothing" |

Not bugs, included to exercise other paths: "Send an SMS reminder the day before arrival" (feature
request, notifications) and "Can guests change their booking dates online?" (question, bookings).
