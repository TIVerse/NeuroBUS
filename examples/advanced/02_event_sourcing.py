"""
Event Sourcing Example

Demonstrates using NeuroBUS for event sourcing patterns with temporal replay.
"""

import asyncio
from datetime import datetime

from neurobus import Event, NeuroBus
from neurobus.config import NeuroBusConfig


class Account:
    """Bank account aggregate."""

    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0.0
        self.transactions = []

    def apply_event(self, event: Event):
        """Apply event to update state."""
        if event.topic == "account.created":
            self.balance = event.data["initial_balance"]
        elif event.topic == "account.deposited":
            self.balance += event.data["amount"]
            self.transactions.append({"type": "deposit", "amount": event.data["amount"]})
        elif event.topic == "account.withdrawn":
            self.balance -= event.data["amount"]
            self.transactions.append({"type": "withdrawal", "amount": event.data["amount"]})

    def __str__(self):
        return f"Account({self.account_id}): Balance=${self.balance:.2f}, Tx={len(self.transactions)}"


async def main():
    """Demonstrate event sourcing."""
    print("🎯 Event Sourcing Example\n")

    config = NeuroBusConfig(temporal={"enabled": True, "db_path": ":memory:"})
    bus = NeuroBus(config=config)

    async with bus:
        print("📝 Recording account events...\n")

        await bus.publish(
            Event(topic="account.created", data={"account_id": "ACC001", "initial_balance": 1000.0})
        )
        await bus.publish(Event(topic="account.deposited", data={"account_id": "ACC001", "amount": 500.0}))
        await asyncio.sleep(0.1)
        await bus.publish(Event(topic="account.withdrawn", data={"account_id": "ACC001", "amount": 200.0}))
        await asyncio.sleep(0.1)
        await bus.publish(Event(topic="account.deposited", data={"account_id": "ACC001", "amount": 100.0}))
        await asyncio.sleep(0.2)

        print("🔄 Rebuilding state from events...\n")
        account = Account("ACC001")
        
        # Get all events and replay them
        all_events = await bus.temporal.query_past(hours=1)

        for event in all_events:
            if event.data.get("account_id") == "ACC001":
                account.apply_event(event)
                print(f"   Applied: {event.topic}")

        print(f"\n✅ Final state: {account}")
        print("\n💡 This is Event Sourcing!")
        print("   - All changes stored as events")
        print("   - State rebuilt by replaying events")
        print("   - Complete audit trail")


if __name__ == "__main__":
    asyncio.run(main())
