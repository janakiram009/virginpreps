
from oscar.apps.order.utils import OrderNumberGenerator as BaseOrderNumberGenerator
# from oscar.apps.order.utils import OrderCreator as BaseOrderCreator
import uuid

class OrderNumberGenerator(BaseOrderNumberGenerator):
    def order_number(self, basket=None):
        # if basket:
        #     return str(1000000 + basket.id)  # Keep your existing pattern for now
        return f"ORD-{uuid.uuid4().hex[:8]}"  # Fallback to UUID-based

# Retain default OrderCreator to ensure order placement works
# OrderCreator = BaseOrderCreator
