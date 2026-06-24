from typing import Protocol

from Models import (
    IncidentDTO,
    InterventionDTO,
    AlerteDTO,
    TechnicienDTO,
    EquipementDTO
)


class IPowerGridRepository(Protocol):

    def get_all_incidents(self) -> list[IncidentDTO]:
        ...

    def save_incident(self, incident: IncidentDTO) -> bool:
        ...

    def get_all_interventions(self) -> list[InterventionDTO]:
        ...

    def get_all_alertes(self) -> list[AlerteDTO]:
        ...

    def get_all_techniciens(self) -> list[TechnicienDTO]:
        ...

    def get_all_equipements(self) -> list[EquipementDTO]:
        ...