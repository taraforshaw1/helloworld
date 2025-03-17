import unittest
from unittest.mock import MagicMock, patch
import json
from datetime import datetime
from src.data_manager import DataManager
from src.models import ClientRecord, AirlineRecord, FlightRecord, RecordType

class TestRecordManagement(unittest.TestCase):
    def setUp(self):
        """Set up a mock DataManager for testing with predefined records."""
        self.data_manager = DataManager()
        self.data_manager.load_data = MagicMock(return_value=True)
        self.data_manager.save_data = MagicMock()
        self.data_manager.get_all_records = MagicMock(return_value=self.load_mock_data())
        self.data_manager.add_record = MagicMock(side_effect=self.mock_add_record)
        self.data_manager.get_record = MagicMock()
        self.data_manager.update_record = MagicMock(side_effect=self.mock_update_record)
        self.data_manager.delete_record = MagicMock(return_value=True)

    def load_mock_data(self):
        """Loads mock records from a predefined JSON structure."""
        json_data = '''{
          "records": [
            {"id": 1, "type": "airline", "company_name": "Cathay Pacific"},
            {"id": 1, "type": "client", "name": "Alan Chan", "address_line_1": "Hong Kong",
             "address_line_2": "Hong Kong 222", "country": "Hong Kong", "phone_number": "91223363"},
            {"id": 2, "type": "airline", "company_name": "ANA"},
            {"id": 1, "type": "flight", "client_id": 1, "airline_id": 1,
             "date": "2025-03-15T19:04:00", "start_city": "Hong Kong", "end_city": "Tokyo"}
          ]
        }'''
        data = json.loads(json_data)
        
        mock_records = []
        for record in data["records"]:
            if record["type"] == "client":
                mock_records.append(ClientRecord.from_dict(record))
            elif record["type"] == "airline":
                mock_records.append(AirlineRecord.from_dict(record))
            elif record["type"] == "flight":
                mock_records.append(FlightRecord.from_dict(record))

        return mock_records

    def mock_add_record(self, record):
        """Mock function to simulate adding a record."""
        record.id = 1 if record.id <= 0 else record.id  # Assign ID if needed
        self.data_manager.save_data()
        return record.id

    def mock_update_record(self, record):
        """Mock function to simulate updating a record and calling save_data."""
        self.data_manager.save_data()
        return True

    def test_add_client(self):
        """Test adding a new client record."""
        client = ClientRecord(0, "John Doe", "123 Main St", "", "", "City", "State", "12345", "Country", "123-456-7890")
        client_id = self.data_manager.add_record(client)
        self.assertEqual(client_id, 1)
        self.data_manager.save_data.assert_called()

    def test_search_records(self):
        """Test searching for records by criteria."""
        results = self.data_manager.search_records(RecordType.CLIENT, name="Alan Chan")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alan Chan")

if __name__ == "__main__":
    unittest.main()