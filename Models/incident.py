from dataclasses import dataclass

@dataclass
class IncidentDTO:
    id_incident: int
    reference: str
    titre: str
    description: str
    commune: str
    poste: str
    severity: str
    status: str