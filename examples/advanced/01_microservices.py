"""
Microservices Communication Example

Demonstrates using NeuroBUS for service-to-service communication.
"""

import asyncio
from dataclasses import dataclass

from neurobus import Event, NeuroBus


@dataclass
class Service:
    """Base service class."""

    name: str
    bus: NeuroBus

    async def initialize(self):
        """Initialize the service."""
        print(f"🚀 {self.name} started")


class OrderService(Service):
    """Order processing service."""

    def __init__(self, bus: NeuroBus):
        super().__init__("OrderService", bus)

    async def initialize(self):
        await super().initialize()

        @self.bus.subscribe("order.created")
        async def process_order(event: Event):
            order_id = event.data["order_id"]
            print(f"📦 [OrderService] Processing order {order_id}")

            # Validate order
            await asyncio.sleep(0.1)

            # Publish event for other services
            await self.bus.publish(
                Event(
                    topic="order.validated",
                    data={"order_id": order_id, "amount": event.data["amount"]},
                )
            )


class PaymentService(Service):
    """Payment processing service."""

    def __init__(self, bus: NeuroBus):
        super().__init__("PaymentService", bus)

    async def initialize(self):
        await super().initialize()

        @self.bus.subscribe("order.validated")
        async def process_payment(event: Event):
            order_id = event.data["order_id"]
            amount = event.data["amount"]
            print(f"💳 [PaymentService] Processing payment ${amount} for order {order_id}")

            # Process payment
            await asyncio.sleep(0.1)

            # Publish payment result
            await self.bus.publish(
                Event(
                    topic="payment.completed",
                    data={"order_id": order_id, "transaction_id": "txn_123"},
                )
            )


class ShippingService(Service):
    """Shipping service."""

    def __init__(self, bus: NeuroBus):
        super().__init__("ShippingService", bus)

    async def initialize(self):
        await super().initialize()

        @self.bus.subscribe("payment.completed")
        async def ship_order(event: Event):
            order_id = event.data["order_id"]
            print(f"📮 [ShippingService] Shipping order {order_id}")

            # Process shipping
            await asyncio.sleep(0.1)

            # Publish shipping notification
            await self.bus.publish(
                Event(
                    topic="shipping.dispatched",
                    data={"order_id": order_id, "tracking": "TRACK123"},
                )
            )


class NotificationService(Service):
    """Notification service."""

    def __init__(self, bus: NeuroBus):
        super().__init__("NotificationService", bus)

    async def initialize(self):
        await super().initialize()

        # Subscribe to all important events
        @self.bus.subscribe("*.completed")
        async def notify_completion(event: Event):
            print(f"📧 [NotificationService] Sending notification: {event.topic}")

        @self.bus.subscribe("shipping.dispatched")
        async def notify_shipping(event: Event):
            tracking = event.data["tracking"]
            print(f"📧 [NotificationService] Order shipped! Tracking: {tracking}")


async def main():
    """Run microservices example."""
    print("🎯 Microservices Communication Example\n")

    # Create shared event bus
    bus = NeuroBus()

    # Create services
    order_service = OrderService(bus)
    payment_service = PaymentService(bus)
    shipping_service = ShippingService(bus)
    notification_service = NotificationService(bus)

    async with bus:
        # Initialize all services
        await order_service.initialize()
        await payment_service.initialize()
        await shipping_service.initialize()
        await notification_service.initialize()

        print("\n📤 Creating new order...\n")

        # Simulate order creation
        await bus.publish(
            Event(
                topic="order.created",
                data={
                    "order_id": "ORD-001",
                    "customer": "alice@example.com",
                    "items": ["laptop", "mouse"],
                    "amount": 1299.99,
                },
            )
        )

        # Wait for event chain to complete
        await asyncio.sleep(1)

        print("\n✅ Order processed through entire pipeline!")
        print("   Order → Payment → Shipping → Notification")

        # Show statistics
        stats = bus.get_stats()
        print(f"\n📊 Bus Statistics:")
        print(f"   Active subscriptions: {stats['registry']['total_subscriptions']}")


if __name__ == "__main__":
    asyncio.run(main())
