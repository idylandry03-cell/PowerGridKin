from typing import Dict

from Services.protocols import IPowerGridRepository


class StatistiqueService:
    def __init__(self, repository: IPowerGridRepository):
        self.repository = repository

    def calculer_indicateurs(self) -> Dict[str, int]:
        incidents = self.repository.get_all_incidents()
        alertes = self.repository.get_all_alertes()
        interventions = self.repository.get_all_interventions()
        techniciens = self.repository.get_all_techniciens()

        incidents_ouverts = 0
        incidents_resolus = 0
        alertes_critiques = 0
        interventions_terminees = 0

        for incident in incidents:
            if incident.status in ["open", "in_progress"]:
                incidents_ouverts += 1

            if incident.status in ["resolved", "closed"]:
                incidents_resolus += 1

        for alerte in alertes:
            if alerte.niveau == "critical" and alerte.resolved is False:
                alertes_critiques += 1

        for intervention in interventions:
            if intervention.statut == "done":
                interventions_terminees += 1

        return {
            "incidents_total": len(incidents),
            "incidents_ouverts": incidents_ouverts,
            "incidents_resolus": incidents_resolus,
            "alertes_critiques": alertes_critiques,
            "interventions_total": len(interventions),
            "interventions_terminees": interventions_terminees,
            "techniciens_total": len(techniciens),
        }