"""
Data Manager for the Record Management System.
This module handles loading and saving records to the filesystem.
"""
import os
import json
from typing import List, Optional
from src.models import (
    BaseRecord, ClientRecord, AirlineRecord, FlightRecord, RecordType
)


class DataManager:
    """Manage data storage and retrieval for the record management system"""

    def __init__(self, data_file: str = "src/record/record.json"):
        """Initialize the data manager with the path to the data file"""
        self.data_file = data_file
        self.records = []
        #Set the next ID for each record type
        self.next_client_id = 1
        self.next_airline_id = 1
        self.next_flight_id = 1

    def load_data(self) -> bool:
        """
        Load records from the data file.
        Returns True if successful, False otherwise.
        """
        if not os.path.exists(self.data_file):
            print(f"Data file {self.data_file} not found. Creating new file.")
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            try:
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump({"records": [], "next_id": 1}, f)
                self.records = []
                self.next_id = 1
                return True
            except Exception as e:
                print(f"Failed to create new data file: {e}")
                return False

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print(f"Data file {self.data_file} is empty. Initializing with empty data.")
                    self.records = []
                    self.next_id = 1
                    # Write empty structure to file
                    with open(self.data_file, 'w', encoding='utf-8') as fw:
                        json.dump({"records": [], "next_id": 1}, fw)
                    return True
                
                # Reset file pointer and load JSON
                f.seek(0)
                data = json.load(f)
                self.records = []

                for record_dict in data.get("records", []):
                    record_type = record_dict.get("type")

                    if record_type == RecordType.CLIENT:
                        record = ClientRecord.from_dict(record_dict)
                    elif record_type == RecordType.AIRLINE:
                        record = AirlineRecord.from_dict(record_dict)
                    elif record_type == RecordType.FLIGHT:
                        record = FlightRecord.from_dict(record_dict)
                    else:
                        print(f"Skipping unknown record type: {record_type}")
                        continue

                    self.records.append(record)

                self.next_id = data.get("next_id", 1)
                return True
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in {self.data_file}: {e}")
            return False
        except PermissionError as e:
            print(f"Permission denied accessing {self.data_file}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error loading data from {self.data_file}: {e}")
            return False

    def save_data(self) -> bool:
        """
        Save records to the data file.
        Returns True if successful, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

            record_dicts = [record.to_dict() for record in self.records]

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "records": record_dicts,
                    "next_id": self.next_id
                }, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def add_record(self, record: BaseRecord) -> int:
        """
        Add a new record to the system.
        Returns the ID of the new record.
        """
        # If a specific ID is provided and exists, raise an error
        if record.id > 0 and self.get_record(record.id, record.type):
            raise ValueError(f"ID {record.id} already exists for {record.type} records")
        
        # Assign the next available ID if id <= 0
        if record.id <= 0:
            if record.type == RecordType.CLIENT:
                candidate_id = self.next_client_id
                while self.get_record(candidate_id, RecordType.CLIENT):
                    candidate_id += 1
                record.id = candidate_id
                self.next_client_id = max(self.next_client_id, candidate_id + 1)
            elif record.type == RecordType.AIRLINE:
                candidate_id = self.next_airline_id
                while self.get_record(candidate_id, RecordType.AIRLINE):
                    candidate_id += 1
                record.id = candidate_id
                self.next_airline_id = max(self.next_airline_id, candidate_id + 1)
            elif record.type == RecordType.FLIGHT:
                candidate_id = self.next_flight_id
                while self.get_record(candidate_id, RecordType.FLIGHT):
                    candidate_id += 1
                record.id = candidate_id
                self.next_flight_id = max(self.next_flight_id, candidate_id + 1)
        
        self.records.append(record)
        return record.id

    def update_record(self, record: BaseRecord) -> bool:
        """
        Update an existing record.
        Returns True if successful, False if record not found.
        """
        for i, existing_record in enumerate(self.records):
            if existing_record.id == record.id and existing_record.type == record.type:
                self.records[i] = record
                self.save_data()
                return True
        return False

    def delete_record(self, record_id: int, record_type: str) -> bool:
        """
        Delete a record by ID and type.
        Returns True if successful, False if record not found.
        """
        for i, record in enumerate(self.records):
            if record.id == record_id and record.type == record_type:
                self.records.pop(i)
                return True
        return False

    def get_record(self, record_id: int, record_type: str) -> Optional[BaseRecord]:
        """
        Get a record by ID and type.
        Returns the record if found, None otherwise.
        """
        for record in self.records:
            if record.id == record_id and record.type == record_type:
                return record
        return None

    def search_records(self, record_type: str = None, **kwargs) -> List[BaseRecord]:
        """
        Search for records matching the given criteria.
        Returns a list of matching records.
        """
        results = []

        for record in self.records:
            if record_type and record.type != record_type:
                continue

            match = True
            for key, value in kwargs.items():
                if not hasattr(record, key) or getattr(record, key) != value:
                    match = False
                    break

            if match:
                results.append(record)

        return results

    def get_all_records(self, record_type: str = None) -> List[BaseRecord]:
        """
        Get all records of the specified type.
        If no type is specified, returns all records.
        """
        if record_type:
            return [r for r in self.records if r.type == record_type]
        return self.records