import unittest
from pyautoserve import HashRegistry


class HashRegistryTests(unittest.TestCase):

    def test_register_new_key(self):
        registry = HashRegistry()

        result = registry.register("key", "value")
        self.assertTrue(result)
        self.assertIn("key", registry)

    def test_register_existing_key_without_force(self):
        registry = HashRegistry()
        registry.register("key", "value")

        result = registry.register("key", "value2")
        self.assertFalse(result)
        self.assertIn("key", registry)
        self.assertEqual(registry["key"], hash("value"))

    def test_register_existing_key_with_force(self):
        registry = HashRegistry()
        registry.register("key", "value")

        result = registry.register("key", "value2", force=True)
        self.assertTrue(result)
        self.assertIn("key", registry)
        self.assertEqual(registry["key"], hash("value2"))

    def test_update_existing_key(self):
        registry = HashRegistry()
        registry.register("key", "value")

        registry.update("key", "value2")
        self.assertIn("key", registry)
        self.assertEqual(registry["key"], hash("value2"))

    def test_compare_existing_key_with_matching_value(self):
        registry = HashRegistry()
        registry.register("key", "value")

        result = registry.compare("key", "value")
        self.assertTrue(result)

    def test_compare_existing_key_with_non_matching_value(self):
        registry = HashRegistry()
        registry.register("key", "value")

        result = registry.compare("key", "value2")
        self.assertFalse(result)

    def test_compare_non_existing_key(self):
        registry = HashRegistry()

        result = registry.compare("key", "value")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
