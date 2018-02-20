import random
import datetime

from invoice_generator import models


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'


class CachedProperty(object):
    def __init__(self, fn):
        self.fn = fn
        self.name = fn.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.fn(instance)
        return res


class ModelsAssets:
    DEFAULT_DELTATIME = datetime.timedelta(days=4)

    DEFAULT_DATE = datetime.date(2018, 2, 20)
    DEFAULT_PAY_DATE = DEFAULT_DATE + DEFAULT_DELTATIME

    DEFAULT_SHIPPING_MIN = DEFAULT_PAY_DATE + DEFAULT_DELTATIME
    DEFAULT_SHIPPING_MAX = DEFAULT_SHIPPING_MIN + DEFAULT_DELTATIME

    SHIPPING_RANGE = (DEFAULT_SHIPPING_MIN, DEFAULT_SHIPPING_MAX)

    DEFAULT_TAX_RATE = 20
    DEFAULT_SHIPPING_PRICE = 10.3

    DEFAULT_TOTAL_GROSS = 12.0
    DEFAULT_TOTAL_NET = 10.0
    DEFAULT_TOTAL_TAX = 2.0

    @property
    def executive(self):
        executive = models.Executive(
            'Ruth W. Blatt', 'RuthWBlatt@example.org')

        return executive

    @CachedProperty
    def vendor(self):
        address = models.Address(
            'Henry H. Rice', '159 Hornor Avenue', '74119', 'Tulsa, OK')

        vendor = models.Vendor(
            self.executive, address,
            'VT000112',
            ('Additional Information', 'test + email', 'HenryHRice@example.org'))

        return vendor

    @CachedProperty
    def address(self):
        address = models.Address(
            'Brittany J. Tynes', '2719 Powder House Road',
            '33301', 'Fort Lauderdale, FL')

        return address

    def invoice(self, *items, **kwargs):
        defaults = (
            ('order_data', self.order),
            ('vendor', self.vendor),
            ('billing_address', self.address),
            ('items', items)
        )

        for k, fn in defaults:
            if k not in kwargs:
                kwargs[k] = callable(fn) and fn() or fn

        invoice = models.Invoice(**kwargs)

        return invoice

    @classmethod
    def order(cls, invoice_id='INV0001', order_id='ORD0002', **data):
        data.setdefault('date', cls.DEFAULT_DATE)
        data.setdefault('payment_date_limit', cls.DEFAULT_PAY_DATE)
        data.setdefault('shipping_date_range', cls.SHIPPING_RANGE)
        data.setdefault('tax_rate', cls.DEFAULT_TAX_RATE)
        data.setdefault('total_discounted', None)
        data.setdefault('total_shipping_net', cls.DEFAULT_SHIPPING_PRICE)

        net = data.setdefault('total_net', cls.DEFAULT_TOTAL_NET)
        gross = data.setdefault('total_gross', cls.DEFAULT_TOTAL_GROSS)

        data.setdefault('total_tax', gross - net)

        order = models.Order(invoice_id, order_id, **data)

        return order

    @CachedProperty
    def item(self):
        order = self.order()

        item = models.OrderItem(
            order,
            'PR-ABC', 'Product Example', 1, 10.0, 10.0)

        return item

    @staticmethod
    def random_item(order):
        ref_length = random.randrange(2, 7)
        quantity = random.randrange(1, 7)
        price = float(random.randrange(50))
        total = quantity * price

        reference = 'RF-' + ''.join([
            random.choice(ALPHABET) for i in range(ref_length)
        ])
        name = 'Product ' + reference

        item = models.OrderItem(
            order, reference, name, quantity, price, total)

        return item

    def random_items(self, count=3, order=None):
        items = []
        order = order or self.order()

        for i in range(count + 1):
            item = self.random_item(order)
            items.append(item)

        return items, order
