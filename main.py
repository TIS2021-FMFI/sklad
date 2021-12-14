from Warehouse import Warehouse
from DataImporter import DataImporter
if __name__ == "__main__":
    w = Warehouse("121", "C:\\uniba\\TiS\\sklad\\config_mock_data.json")
    w.load_configuration()
    di = DataImporter()
    di.getShelvingUnits(w)
    print(w)
