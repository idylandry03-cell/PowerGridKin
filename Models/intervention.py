from dataclasses import dataclass

@dataclass
class InterventionDTO:
    id_intervention: int
    incident_ref: str
    technicien_nom: str
    action: str
    date_debut: str
    date_fin: str
    statut: str