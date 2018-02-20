import unittest
from invoice_generator import models
from tests.ModelsAssets import ModelsAssets


class TestModels(unittest.TestCase, ModelsAssets):
    def test_Vendor_additional_text_suffix(self):
        vendor = self.vendor  # type: models.Vendor
        self.assertEqual(3 * '"\\a" ', vendor.additional_text_suffix)

    def test_Order_shipping_from(self):
        order = self.order()  # type: models.Order

        self.assertEqual(order.shipping_from, self.DEFAULT_SHIPPING_MIN)
        self.assertEqual(order.shipping_to, self.DEFAULT_SHIPPING_MAX)
