from dataclasses import dataclass


@dataclass
class TechnicienDTO:
    id_technicien: int
    nom: str
    prenom: str
    telephone: str
    email: str
    competence: str