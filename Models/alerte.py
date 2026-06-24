from dataclasses import dataclass

@dataclass
class AlerteDTO:
    id_alerte: int
    incident_ref: str
    type_alerte: str
    niveau: str
    message: str
    date_alerte: str
    resolved: bool