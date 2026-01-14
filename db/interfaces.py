from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Ticket:
    id: Optional[int] = None                 # PK, wird von DB gesetzt
    customer_id: int = 0                     # Pflichtfeld
    thema: str = ""                          # Pflichtfeld
    beschreibung: str = ""                   # Pflichtfeld
    status: str = "Open"                     # Default beim Erstellen
    created_at: Optional[date] = None        # Pflichtfeld beim Create
    prioritaet: Optional[int] = None
    related_ticket_id: Optional[int] = None
    firma: str = ""                          # Pflichtfeld
    updated_at: Optional[date] = None
    employee_id: Optional[int] = None        # Wird später gesetzt
    mitarbeiter_notizen: Optional[str] = None

@dataclass
class Employee:
    id: int          # PK
    vorname: str
    nachname: str
    email: str

@dataclass
class Customer:
    id: int          # PK
    vorname: str
    nachname: str
    email: str