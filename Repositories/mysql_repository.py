from typing import List, Dict, Any

from Models import (
    IncidentDTO,
    TechnicienDTO,
    InterventionDTO,
    AlerteDTO,
    EquipementDTO,
)


class MySQLPowerGridRepository:
    def __init__(self, connection):
        self.connection = connection

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def execute(self, query: str, params: tuple = ()) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()
        return True

    def get_all_incidents(self) -> List[IncidentDTO]:
        query = """
        SELECT 
            i.id_incident,
            i.reference,
            i.titre,
            i.description,
            COALESCE(co.nom, '') AS commune,
            COALESCE(p.nom, '') AS poste,
            i.severity,
            i.status
        FROM INCIDENT i
        LEFT JOIN COMMUNE co ON i.id_commune = co.id_commune
        LEFT JOIN POSTE p ON i.id_poste = p.id_poste
        ORDER BY i.id_incident DESC
        """

        rows = self.fetch_all(query)

        return [
            IncidentDTO(
                id_incident=row["id_incident"],
                reference=row["reference"] or "",
                titre=row["titre"] or "",
                description=row["description"] or "",
                commune=row["commune"] or "",
                poste=row["poste"] or "",
                severity=row["severity"] or "",
                status=row["status"] or "",
            )
            for row in rows
        ]

    def get_all_techniciens(self) -> List[TechnicienDTO]:
        query = """
        SELECT 
            id_technicien,
            nom,
            prenom,
            telephone,
            email,
            competence
        FROM TECHNICIEN
        ORDER BY nom ASC
        """

        rows = self.fetch_all(query)

        return [
            TechnicienDTO(
                id_technicien=row["id_technicien"],
                nom=row["nom"] or "",
                prenom=row["prenom"] or "",
                telephone=row["telephone"] or "",
                email=row["email"] or "",
                competence=row["competence"] or "",
            )
            for row in rows
        ]

    def get_all_interventions(self) -> List[InterventionDTO]:
        query = """
        SELECT 
            it.id_intervention,
            COALESCE(i.reference, '') AS incident_ref,
            COALESCE(CONCAT(t.nom, ' ', t.prenom), '') AS technicien_nom,
            it.action,
            it.date_debut,
            it.date_fin,
            it.statut
        FROM INTERVENTION it
        LEFT JOIN INCIDENT i ON it.id_incident = i.id_incident
        LEFT JOIN TECHNICIEN t ON it.id_technicien = t.id_technicien
        ORDER BY it.id_intervention DESC
        """

        rows = self.fetch_all(query)

        return [
            InterventionDTO(
                id_intervention=row["id_intervention"],
                incident_ref=row["incident_ref"] or "",
                technicien_nom=row["technicien_nom"] or "",
                action=row["action"] or "",
                date_debut=str(row["date_debut"]) if row["date_debut"] else "",
                date_fin=str(row["date_fin"]) if row["date_fin"] else "",
                statut=row["statut"] or "",
            )
            for row in rows
        ]

    def get_all_alertes(self) -> List[AlerteDTO]:
        query = """
        SELECT 
            a.id_alerte,
            COALESCE(i.reference, '') AS incident_ref,
            a.type_alerte,
            a.niveau,
            a.message,
            a.date_alerte,
            a.resolved
        FROM ALERTE a
        LEFT JOIN INCIDENT i ON a.id_incident = i.id_incident
        ORDER BY a.id_alerte DESC
        """

        rows = self.fetch_all(query)

        return [
            AlerteDTO(
                id_alerte=row["id_alerte"],
                incident_ref=row["incident_ref"] or "",
                type_alerte=row["type_alerte"] or "",
                niveau=row["niveau"] or "",
                message=row["message"] or "",
                date_alerte=str(row["date_alerte"]) if row["date_alerte"] else "",
                resolved=bool(row["resolved"]),
            )
            for row in rows
        ]

    def get_all_equipements(self) -> List[EquipementDTO]:
        query = """
        SELECT 
            id_equipement,
            type_equipement,
            reference,
            statut,
            details
        FROM EQUIPEMENT
        ORDER BY id_equipement ASC
        """

        rows = self.fetch_all(query)

        return [
            EquipementDTO(
                id_equipement=row["id_equipement"],
                type_equipement=row["type_equipement"] or "",
                reference=row["reference"] or "",
                statut=row["statut"] or "",
                details=row["details"] or "",
            )
            for row in rows
        ]

    def get_dashboard_stats(self) -> Dict[str, int]:
        incidents = self.fetch_all("SELECT COUNT(*) AS total FROM INCIDENT")
        ouverts = self.fetch_all(
            "SELECT COUNT(*) AS total FROM INCIDENT WHERE status IN ('open', 'in_progress')"
        )
        resolus = self.fetch_all(
            "SELECT COUNT(*) AS total FROM INCIDENT WHERE status IN ('resolved', 'closed')"
        )
        alertes_critiques = self.fetch_all(
            "SELECT COUNT(*) AS total FROM ALERTE WHERE niveau = 'critical' AND resolved = FALSE"
        )
        interventions = self.fetch_all("SELECT COUNT(*) AS total FROM INTERVENTION")
        techniciens = self.fetch_all("SELECT COUNT(*) AS total FROM TECHNICIEN")
        equipements = self.fetch_all("SELECT COUNT(*) AS total FROM EQUIPEMENT")
        capteurs = self.fetch_all("SELECT COUNT(*) AS total FROM SENSOR")

        return {
            "incidents_total": incidents[0]["total"],
            "incidents_ouverts": ouverts[0]["total"],
            "incidents_resolus": resolus[0]["total"],
            "alertes_critiques": alertes_critiques[0]["total"],
            "interventions_total": interventions[0]["total"],
            "techniciens_total": techniciens[0]["total"],
            "equipements_total": equipements[0]["total"],
            "capteurs_total": capteurs[0]["total"],
        }

    def get_reference_data(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "communes": self.fetch_all(
                "SELECT id_commune, nom FROM COMMUNE ORDER BY nom"
            ),
            "postes": self.fetch_all(
                "SELECT id_poste, nom FROM POSTE ORDER BY nom"
            ),
            "circuits": self.fetch_all(
                "SELECT id_circuit, code, intitule FROM CIRCUIT ORDER BY code"
            ),
            "equipements": self.fetch_all(
                "SELECT id_equipement, type_equipement, reference FROM EQUIPEMENT ORDER BY type_equipement"
            ),
            "causes": self.fetch_all(
                "SELECT id_cause, libelle FROM CAUSE ORDER BY libelle"
            ),
            "techniciens": self.fetch_all(
                "SELECT id_technicien, nom, prenom FROM TECHNICIEN ORDER BY nom"
            ),
        }

    def get_database_overview(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "communes": self.fetch_all(
                "SELECT id_commune, nom, population, description FROM COMMUNE ORDER BY nom"
            ),
            "postes": self.fetch_all(
                """
                SELECT 
                    p.id_poste,
                    p.nom,
                    COALESCE(c.nom, '') AS commune,
                    COALESCE(ce.nom, '') AS centrale,
                    p.tension_kv,
                    p.adresse
                FROM POSTE p
                LEFT JOIN COMMUNE c ON p.id_commune = c.id_commune
                LEFT JOIN CENTRALE ce ON p.id_centrale = ce.id_centrale
                ORDER BY p.nom
                """
            ),
            "circuits": self.fetch_all(
                """
                SELECT 
                    ci.id_circuit,
                    ci.code,
                    ci.intitule,
                    COALESCE(p.nom, '') AS poste,
                    ci.tension_kv,
                    ci.zone_description
                FROM CIRCUIT ci
                LEFT JOIN POSTE p ON ci.id_poste = p.id_poste
                ORDER BY ci.code
                """
            ),
            "equipements": self.fetch_all(
                """
                SELECT 
                    e.id_equipement,
                    e.type_equipement,
                    e.reference,
                    COALESCE(ci.code, '') AS circuit,
                    COALESCE(p.nom, '') AS poste,
                    e.statut,
                    e.details
                FROM EQUIPEMENT e
                LEFT JOIN CIRCUIT ci ON e.id_circuit = ci.id_circuit
                LEFT JOIN POSTE p ON e.id_poste = p.id_poste
                ORDER BY e.id_equipement
                """
            ),
            "capteurs": self.fetch_all(
                """
                SELECT 
                    s.id_sensor,
                    s.code_sensor,
                    s.type_sensor,
                    COALESCE(e.reference, '') AS equipement,
                    COALESCE(ci.code, '') AS circuit,
                    s.last_value,
                    s.last_update
                FROM SENSOR s
                LEFT JOIN EQUIPEMENT e ON s.id_equipement = e.id_equipement
                LEFT JOIN CIRCUIT ci ON s.id_circuit = ci.id_circuit
                ORDER BY s.id_sensor
                """
            ),
            "techniciens": self.fetch_all(
                """
                SELECT 
                    t.id_technicien,
                    t.nom,
                    t.prenom,
                    t.telephone,
                    t.email,
                    t.competence,
                    COALESCE(c.nom, '') AS commune
                FROM TECHNICIEN t
                LEFT JOIN COMMUNE c ON t.id_commune = c.id_commune
                ORDER BY t.nom
                """
            ),
        }

    def save_incident(self, incident: IncidentDTO) -> bool:
        query = """
        INSERT INTO INCIDENT (
            reference, titre, description, severity, status, start_time
        )
        VALUES (%s, %s, %s, %s, %s, NOW())
        """

        values = (
            incident.reference,
            incident.titre,
            incident.description,
            incident.severity,
            incident.status,
        )

        return self.execute(query, values)

    def save_incident_with_relations(
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
        query = """
        INSERT INTO INCIDENT (
            reference,
            titre,
            description,
            id_commune,
            id_poste,
            id_circuit,
            id_equipement,
            id_cause,
            severity,
            status,
            start_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'open', NOW())
        """

        values = (
            reference,
            titre,
            description,
            id_commune,
            id_poste,
            id_circuit,
            id_equipement,
            id_cause,
            severity,
        )

        return self.execute(query, values)

    def update_incident_status(self, id_incident: int, status: str) -> bool:
        query = """
        UPDATE INCIDENT
        SET status = %s
        WHERE id_incident = %s
        """

        return self.execute(query, (status, id_incident))

    def delete_incident(self, id_incident: int) -> bool:
        query = """
        DELETE FROM INCIDENT
        WHERE id_incident = %s
        """

        return self.execute(query, (id_incident,))

    def assign_intervention(
        self,
        id_incident: int,
        id_technicien: int,
        action: str,
    ) -> bool:
        query = """
        INSERT INTO INTERVENTION (
            id_incident,
            id_technicien,
            date_debut,
            action,
            statut
        )
        VALUES (%s, %s, NOW(), %s, 'scheduled')
        """

        return self.execute(query, (id_incident, id_technicien, action))

    def update_intervention_status(self, id_intervention: int, statut: str) -> bool:
        query = """
        UPDATE INTERVENTION
        SET statut = %s,
            date_fin = CASE WHEN %s = 'done' THEN NOW() ELSE date_fin END
        WHERE id_intervention = %s
        """

        return self.execute(query, (statut, statut, id_intervention))