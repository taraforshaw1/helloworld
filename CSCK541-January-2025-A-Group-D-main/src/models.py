"""
Models for the Record Management System.
This module defines the data structures for Client, Airline, and Flight records.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional


class RecordType:
    CLIENT = "client"
    AIRLINE = "airline"
    FLIGHT = "flight"


class BaseRecord:
    """Base class for all records"""
    def __init__(self, id: int, record_type: str):
        self.id = id
        self.type = record_type

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary for storage"""
        return {
            "id": self.id,
            "type": self.type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseRecord':
        """Create record from dictionary"""
        return cls(id=data["id"], record_type=data["type"])


class ClientRecord(BaseRecord):
    """Client record model"""
    def __init__(self, id: int, name: str, address_line_1: str, address_line_2: str = "",
                 address_line_3: str = "", city: str = "", state: str = "",
                 zip_code: str = "", country: str = "", phone_number: str = ""):
        super().__init__(id, RecordType.CLIENT)
        self.name = name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone_number = phone_number

    def to_dict(self) -> Dict[str, Any]:
        """Convert client record to dictionary for storage"""
        data = super().to_dict()
        data.update({
            "name": self.name,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "address_line_3": self.address_line_3,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "phone_number": self.phone_number
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClientRecord':
        """Create client record from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            address_line_1=data["address_line_1"],
            address_line_2=data.get("address_line_2", ""),
            address_line_3=data.get("address_line_3", ""),
            city=data.get("city", ""),
            state=data.get("state", ""),
            zip_code=data.get("zip_code", ""),
            country=data.get("country", ""),
            phone_number=data.get("phone_number", "")
        )


class AirlineRecord(BaseRecord):
    """Airline company record model"""
    def __init__(self, id: int, company_name: str):
        super().__init__(id, RecordType.AIRLINE)
        self.company_name = company_name

    def to_dict(self) -> Dict[str, Any]:
        """Convert airline record to dictionary for storage"""
        data = super().to_dict()
        data.update({
            "company_name": self.company_name
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AirlineRecord':
        """Create airline record from dictionary"""
        return cls(
            id=data["id"],
            company_name=data["company_name"]
        )


class FlightRecord(BaseRecord):
    """Flight record model"""
    def __init__(self, id: int, client_id: int, airline_id: int, 
                 date: datetime, start_city: str, end_city: str):
        super().__init__(id, RecordType.FLIGHT)
        self.client_id = client_id
        self.airline_id = airline_id
        self.date = date
        self.start_city = start_city
        self.end_city = end_city

    def to_dict(self) -> Dict[str, Any]:
        """Convert flight record to dictionary for storage"""
        data = super().to_dict()
        data.update({
            "client_id": self.client_id,
            "airline_id": self.airline_id,
            "date": self.date.isoformat(),
            "start_city": self.start_city,
            "end_city": self.end_city
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FlightRecord':
        """Create flight record from dictionary"""
        return cls(
            id=data["id"],
            client_id=data["client_id"],
            airline_id=data["airline_id"],
            date=datetime.fromisoformat(data["date"]),
            start_city=data["start_city"],
            end_city=data["end_city"]
        )