import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.data_manager import DataManager
from src.models import ClientRecord, AirlineRecord, FlightRecord, RecordType

class TestRecordManagement(unittest.TestCase):
    def setUp(self):
        """Set up a mock DataManager for testing."""
        self.data_manager = DataManager()
        self.data_manager.load_data = MagicMock(return_value=True)
        self.data_manager.save_data = MagicMock()
        self.data_manager.get_all_records = MagicMock(return_value=[])
        self.data_manager.add_record = MagicMock(side_effect=self.mock_add_record)
        self.data_manager.get_record = MagicMock()
        self.data_manager.update_record = MagicMock(return_value=True)
        self.data_manager.delete_record = MagicMock(return_value=True)

    def mock_add_record(self, record):
        """Mock function to simulate adding a record and calling save_data()."""
        record.id = 1 if record.id <= 0 else record.id  # Assign ID if needed
        self.data_manager.save_data()  # Ensure save_data is called
        return record.id

    def test_load_data_empty_file(self):
        """Test handling of an empty data file."""
        with patch("builtins.open", unittest.mock.mock_open(read_data="")):
            result = self.data_manager.load_data()
            self.assertTrue(result)
            self.assertEqual(self.data_manager.records, [])

    def test_add_client(self):
        """Test adding a new client record."""
        client = ClientRecord(0, "John Doe", "123 Main St", "", "", "City", "State", "12345", "Country", "123-456-7890")
        client_id = self.data_manager.add_record(client)
        self.assertEqual(client_id, 1)
        self.data_manager.save_data.assert_called_once()

    def test_add_airline(self):
        """Test adding a new airline record."""
        airline = AirlineRecord(0, "Air Test")
        airline_id = self.data_manager.add_record(airline)
        self.assertEqual(airline_id, 1)
        self.data_manager.save_data.assert_called_once()

    def test_add_flight(self):
        """Test adding a new flight record."""
        flight = FlightRecord(0, 1, 2, datetime.now(), "StartCity", "EndCity")
        flight_id = self.data_manager.add_record(flight)
        self.assertEqual(flight_id, 1)
        self.data_manager.save_data.assert_called_once()

    def test_delete_client_with_linked_flight(self):
        """Test preventing deletion of a client linked to a flight."""
        self.data_manager.get_all_records.return_value = [FlightRecord(1, 1, 2, datetime.now(), "A", "B")]
        self.data_manager.delete_record.return_value = False
        result = self.data_manager.delete_record(1, RecordType.CLIENT)
        self.assertFalse(result)

    def test_update_client(self):
        """Test updating a client record."""
        updated_client = ClientRecord(1, "Jane Doe", "456 Elm St", "", "", "NewCity", "NewState", "54321", "NewCountry", "098-765-4321")
        result = self.data_manager.update_record(updated_client)
        self.assertTrue(result)
        self.data_manager.save_data.assert_called_once()

    def test_search_records(self):
        """Test searching for records by criteria."""
        self.data_manager.get_all_records.return_value = [
            ClientRecord(1, "John Doe", "123 Main St", "", "", "City", "State", "12345", "Country", "123-456-7890"),
            ClientRecord(2, "Jane Doe", "456 Elm St", "", "", "NewCity", "NewState", "54321", "NewCountry", "098-765-4321")
        ]
        results = self.data_manager.search_records(RecordType.CLIENT, name="Jane Doe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Jane Doe")
    
    def test_client_to_dict(self):
        """Test serialization of ClientRecord."""
        client = ClientRecord(1, "John Doe", "123 Main St", country="Country", phone_number="1234567890")
        client_dict = client.to_dict()
        self.assertEqual(client_dict["name"], "John Doe")
        self.assertEqual(client_dict["country"], "Country")

    def test_flight_from_dict(self):
        """Test deserialization of FlightRecord."""
        flight_data = {
            "id": 1,
            "type": "flight",
            "client_id": 2,
            "airline_id": 3,
            "date": "2025-03-15T19:04:00",
            "start_city": "London",
            "end_city": "Paris"
        }
        flight = FlightRecord.from_dict(flight_data)
        self.assertEqual(flight.id, 1)
        self.assertEqual(flight.client_id, 2)
        self.assertEqual(flight.date, datetime.fromisoformat("2025-03-15T19:04:00"))

if __name__ == "__main__":
    unittest.main()