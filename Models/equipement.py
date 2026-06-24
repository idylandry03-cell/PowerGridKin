from dataclasses import dataclass

@dataclass
class EquipementDTO:
    id_equipement: int
    type_equipement: str
    reference: str
    statut: str
    details: str