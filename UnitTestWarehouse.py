import unittest
import json
from Warehouse import Warehouse


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse("Gefco", "config_mock_data.json")
        self.warehouse.load_configuration()

    def test_get_name(self):
        self.assertEqual(self.warehouse.get_name(), 'Gefco')

    def test_load_configuration_shelving_units(self):
        shelving_unit = self.warehouse['01']
        self.assertEqual(shelving_unit.get_name(), "01")
        self.assertEqual(shelving_unit.get_x(), 400.28412509523724)
        self.assertEqual(shelving_unit.get_y(), 452.35358727376064)

    def test_load_configuration_shelves(self):
        shelf = self.warehouse['01']['A']
        self.assertEqual(shelf.get_name(), "A")
        self.assertEqual(shelf.get_level(), 1)

    def test_load_configuration_cells(self):
        cell = self.warehouse['01']['A']['01']
        self.assertEqual(cell.get_name(), "01")
        self.assertEqual(cell.get_position(), 5)
        self.assertEqual(cell.is_blocked(), False)

##    def test_save_configuration(self):
##        self.warehouse.save_configuration()
##        with open('config_copy.json') as config_file:
##            config = json.load(config_file)
##        self.assertEqual(self.warehouse.get_warehouse(),  config)


if __name__ == '__main__':
    unittest.main()
