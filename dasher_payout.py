"""
Design an API that calculates total payout for a driver based on their delivery events.
Each delivery has events (accepted, cancelled, delivered) with timestamps, and
payment is calculated using fixed rates plus bonuses based on concurrent deliveries.
For example, if a driver has 2 ongoing deliveries when accepting a new one, they earn a higher rate for that delivery.
input:
    Events: [
        {id: 'D1', status: 'accepted', time: '10:00'},
        {id: 'D1', status: 'delivered', time: '10:30'}
    ]
    base_rate: $10

Output:
    $10 (1 delivery completed with no concurrent deliveries)
"""


def process_events(events):
    # 1. sort chronologically.
    events_sorted = sorted(events, key=lambda e: e["time"])

    active_count = 0
    # Map to store: {'D1': 0, 'D2': 1 ...}
    delivery_concurrent_counts = {}

    # 2. walk through time
    for event in events_sorted:
        delivery_id = event["id"]
        status = event["status"]

        if status == "accepted":
            # Lock in the current active count BEFORE incrementing
            delivery_concurrent_counts[delivery_id] = active_count
            active_count += 1

        elif status in ["delivered", "cancelled"]:
            active_count -= 1

    return delivery_concurrent_counts


def calculate_payout(events, delivery_concurrent_counts, base_rate, bonus_factor=0.25):
    total_payout = 0.0
    for event in events:
        # we only care about the terminal 'delivered' event for payments
        if event["status"] == "delivered":
            delivery_id = event["id"]

            # retrieve the locked_in count from out state machine
            concurrent_count = delivery_concurrent_counts[delivery_id]
            # apply the formula: base * (1 + (bonus_factor * concurrent))
            payout = base_rate * (1 + bonus_factor * concurrent_count)
            total_payout += payout
    return total_payout


# bringing it all together
from typing import Any, Dict, List


class PayoutAPI:
    def __init__(self, base_rate: float, bonus_factor: float):
        self.base_rate = base_rate
        self.bonus_factor = bonus_factor

    def get_total_payout(self, driver_events: List[Dict[str, Any]]) -> float:
        if not driver_events:
            return 0.0

        # optional validation
        self._validate_events(driver_events)

        # 1. track state
        concurrent_counts = process_events(driver_events)

        # 2. calculate finance
        final_payout = calculate_payout(
            driver_events, concurrent_counts, self.base_rate, self.bonus_factor
        )
        return final_payout

    def _validate_events(self, events: List[Dict[str, Any]]) -> None:
        accepted = {e["id"] for e in events if e["status"] == "accepted"}
        completed = {
            e["id"] for e in events if e["status"] in ("delivered", "completed")
        }
        if accepted != completed:
            raise ValueError("Mismatched accepted and completed events")


"""
time: O(N log N) where N is number of events
Space: O(N)
"""

"""
variation: time_payout irrespective of cancelled or delivered
"""


def process_events_for_time_payout(events):
    # sort chronologically as always
    events_sorted = sorted(events, key=lambda e: parse_time(e["time"]))

    active_count = 0
    # store BOTH the multipler and the start time
    delivery_state = {}

    # also need a place to store completed durations
    completed_deliveries = []

    for event in events_sorted:
        delivery_id = event['id']
        status = event['status']
        event_time = parse_time(event['time'])

        if status == 'accepted':
            # record state at acceptance
            delivery_state[delivery_id] = {
                'start_time' : event_time,
                'concurrent_count' : active_count,
            }
            active_count += 1

        elif status in ['delivered', 'cancelled']:
            # it's a terminal state. Calculate duration!
            start_time = delivery_state[delivery_id]['start_time']
            duration_minutes = (event_time - start_time).total_seconds()/60

            completed_deliveries.append({
                'id': delivery_id,
                'duration_minutes': duration_minutes,
                'concurrent_count': delivery_state[delivery_id]['concurrent_count']
            })
            active_count -= 1
    return completed_deliveries


def calculate_time_based_paayout(completed_deliveries, per_minute_rate, bonuse_factor):
    total = 0.0
    for delivery in completed_deliveries:
        base_pay = delivery["duration_minutes"] * per_minute_rate
        multiplier = 1 + (bonuse_factor * delivery["concurrent_count"])
        total += base_pay * multiplier
    return total
