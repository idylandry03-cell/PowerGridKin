from typing import Dict, List, Any

from Models import IncidentDTO


class PowerGridService:
    def __init__(self, repository):
        self.repository = repository

    def retrieve_incidents(self) -> List[IncidentDTO]:
        return self.repository.get_all_incidents()

    def retrieve_alertes(self):
        return self.repository.get_all_alertes()

    def retrieve_interventions(self):
        return self.repository.get_all_interventions()

    def retrieve_techniciens(self):
        return self.repository.get_all_techniciens()

    def retrieve_equipements(self):
        return self.repository.get_all_equipements()

    def retrieve_reference_data(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.repository.get_reference_data()

    def retrieve_database_overview(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.repository.get_database_overview()

    def create_incident(self, incident: IncidentDTO) -> bool:
        if not incident.reference.strip():
            return False

        if not incident.titre.strip():
            return False

        if incident.severity not in ["low", "medium", "high", "critical"]:
            return False

        return self.repository.save_incident(incident)

    def create_incident_with_relations(
        self,
        reference: str,
        titre: str,
        description: str,
        id_commune: int,
        id_poste: int,
        id_circuit: int,
        id_equipement: int,
        id_cause: int,
        severity: str,
    ) -> bool:
        if not reference.strip():
            return False

        if not titre.strip():
            return False

        if severity not in ["low", "medium", "high", "critical"]:
            return False

        return self.repository.save_incident_with_relations(
            reference=reference,
            titre=titre,
            description=description,
            id_commune=id_commune,
            id_poste=id_poste,
            id_circuit=id_circuit,
            id_equipement=id_equipement,
            id_cause=id_cause,
            severity=severity,
        )

    def changer_statut_incident(self, id_incident: int, status: str) -> bool:
        if status not in ["open", "in_progress", "resolved", "closed"]:
            return False

        return self.repository.update_incident_status(id_incident, status)

    def supprimer_incident(self, id_incident: int) -> bool:
        if id_incident <= 0:
            return False

        return self.repository.delete_incident(id_incident)

    def assigner_intervention(
        self,
        id_incident: int,
        id_technicien: int,
        action: str,
    ) -> bool:
        if id_incident <= 0:
            return False

        if id_technicien <= 0:
            return False

        if not action.strip():
            return False

        return self.repository.assign_intervention(
            id_incident=id_incident,
            id_technicien=id_technicien,
            action=action,
        )

    def cloturer_intervention(self, id_intervention: int) -> bool:
        if id_intervention <= 0:
            return False

        return self.repository.update_intervention_status(
            id_intervention=id_intervention,
            statut="done",
        )

    def changer_statut_intervention(
        self,
        id_intervention: int,
        statut: str,
    ) -> bool:
        if id_intervention <= 0:
            return False

        if statut not in ["scheduled", "ongoing", "done", "failed"]:
            return False

        return self.repository.update_intervention_status(
            id_intervention=id_intervention,
            statut=statut,
        )