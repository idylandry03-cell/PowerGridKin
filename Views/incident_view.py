import flet as ft

from Models import IncidentDTO
from Views.components import Components


class IncidentView:
    def __init__(self, service, page):
        self.service = service
        self.page = page

        self.reference = ft.TextField(
            label="Référence",
            width=180,
        )

        self.titre = ft.TextField(
            label="Titre",
            width=300,
        )

        self.description = ft.TextField(
            label="Description",
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=400,
        )

        self.severity = ft.Dropdown(
            label="Gravité",
            width=180,
            value="medium",
            options=[
                ft.dropdown.Option("low"),
                ft.dropdown.Option("medium"),
                ft.dropdown.Option("high"),
                ft.dropdown.Option("critical"),
            ],
        )

        self.status = ft.Dropdown(
            label="Statut",
            width=180,
            value="open",
            options=[
                ft.dropdown.Option("open"),
                ft.dropdown.Option("in_progress"),
                ft.dropdown.Option("resolved"),
                ft.dropdown.Option("closed"),
            ],
        )

        self.incidents_container = ft.Column()

    def build(self):

        self.refresh_incidents()

        form = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        Components.section_title(
                            "Ajouter un incident"
                        ),

                        ft.Row(
                            controls=[
                                self.reference,
                                self.severity,
                                self.status,
                            ],
                            wrap=True,
                        ),

                        self.titre,
                        self.description,

                        Components.primary_button(
                            "Créer l'incident",
                            self.create_incident,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

        return ft.Column(
            controls=[
                Components.page_header(
                    "Gestion des incidents",
                    "Création, suivi et supervision"
                ),

                form,

                Components.section_title(
                    "Liste des incidents"
                ),

                self.incidents_container,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def create_incident(self, e):

        incident = IncidentDTO(
            id_incident=0,
            reference=self.reference.value,
            titre=self.titre.value,
            description=self.description.value,
            commune="",
            poste="",
            severity=self.severity.value,
            status=self.status.value,
        )

        result = self.service.create_incident(
            incident
        )

        if result:

            self.reference.value = ""
            self.titre.value = ""
            self.description.value = ""

            self.refresh_incidents()

            self.page.snack_bar = ft.SnackBar(
                ft.Text("Incident enregistré")
            )
            self.page.snack_bar.open = True

        else:

            self.page.snack_bar = ft.SnackBar(
                ft.Text("Erreur lors de l'enregistrement")
            )
            self.page.snack_bar.open = True

        self.page.update()

    def refresh_incidents(self):

        incidents = self.service.retrieve_incidents()

        self.incidents_container.controls.clear()

        for incident in incidents:

            card = Components.data_card(
                title=f"{incident.reference} - {incident.titre}",
                lines=[
                    f"Description : {incident.description}",
                    f"Commune : {incident.commune}",
                    f"Poste : {incident.poste}",
                    f"Statut : {incident.status}",
                ],
                badges=[
                    incident.severity,
                    incident.status,
                ],
            )

            self.incidents_container.controls.append(card)

        if len(incidents) == 0:

            self.incidents_container.controls.append(
                Components.empty_message(
                    "Aucun incident enregistré."
                )
            )

        if self.page:
            self.page.update()