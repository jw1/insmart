from django.test import TestCase
from polls.models import Product, Vendor, InventoryAuditLog

# Create your tests here.
class InsmartDataTierTestCase(TestCase):

    def setUp(self):
        Vendor.objects.create(name="Test Vendor")
        Product.objects.create(name="Test Product")
        Product.objects.create(name="Unassociated Product")

        # oh, and associate them to each other
        vendor_to_link = Vendor.objects.filter(name="Test Vendor").first()
        product_to_link = Product.objects.filter(name="Test Product").first()
        vendor_to_link.product_set.add(product_to_link)

    def test_product_count(self):
        count = Product.objects.count()
        self.assertEqual(count, 2)

    def test_vendor_count(self):
        count = Vendor.objects.count()
        self.assertEqual(count, 1)

    def test_find_product(self):
        selected = Product.objects.filter(name="Test Product").first()
        self.assertIsNotNone(selected)

    def test_find_product_miss(self):
        selected = Vendor.objects.filter(name="mystery object").first()
        self.assertIsNone(selected)

    def test_find_vendor(self):
        selected = Vendor.objects.filter(name="Test Vendor").first()
        self.assertIsNotNone(selected)

    def test_find_vendor_miss(self):
        selected = Vendor.objects.filter(name="mystery object").first()
        self.assertIsNone(selected)

    def test_find_linked_vendor(self):
        selected = Vendor.objects.filter(name="Test Vendor").first()
        associated_product = selected.product_set.first()
        self.assertIsNotNone(associated_product)

    def test_update_product(self):
        selected = Product.objects.filter(name="Test Product").first()
        selected.description = "vague description"
        Product.save(selected)

        updated = Product.objects.filter(name="Test Product").first()
        self.assertEqual(updated.description, "vague description")

    def test_update_vendor(self):
        selected = Vendor.objects.filter(name="Test Vendor").first()
        selected.website_address = "sysanalproj16.wixsite.com/insmart"
        Vendor.save(selected)

        updated = Vendor.objects.filter(name="Test Vendor").first()
        self.assertEqual(updated.website_address, "sysanalproj16.wixsite.com/insmart")

    def test_delete_product(self):
        to_delete = Product.objects.filter(name="Test Product").first()
        self.assertIsNotNone(to_delete)
        Product.delete(to_delete)

        not_found = Product.objects.filter(name="Test Product").first()
        self.assertIsNone(not_found)

    def test_delete_vendor(self):
        to_delete = Vendor.objects.filter(name="Test Vendor").first()
        self.assertIsNotNone(to_delete)
        Vendor.delete(to_delete)

        not_found = Vendor.objects.filter(name="Test Vendor").first()
        self.assertIsNone(not_found)

    def test_adjust_inventory(self):
        product = Product.objects.filter(name="Test Product").first()
        InventoryAuditLog.objects.create(user_id=1, product_id=product.id, before=product.current, after=product.current, adjustment=product.current)

    def test_add_inventory(self):
        change = 1
        product = Product.objects.filter(name="Test Product").first()

        # simulate the inventory change (write the log, adjust the inventory)
        InventoryAuditLog.objects.create(user_id=1,
                                         product_id=product.id,
                                         before=product.current,
                                         after=product.current + change,
                                         adjustment=change)
        product.current += change
        Product.save(product)

        after_inventory_change = Product.objects.filter(name="Test Product").first()
        self.assertEqual(change, after_inventory_change.current)

