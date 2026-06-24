import flet as ft
from Views.components import Components, AppColors


class InterventionView:
    def __init__(self, service, page):
        self.service = service
        self.page = page
        self.container = ft.Column()

    def build(self):
        self.refresh_interventions()

        return ft.Column(
            controls=[
                Components.page_header(
                    "Interventions",
                    "Gestion des interventions techniques",
                ),
                self.container,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh_interventions(self):

        interventions = self.service.retrieve_interventions()
        self.container.controls.clear()

        if not interventions:
            self.container.controls.append(
                Components.empty_message("Aucune intervention disponible")
            )
            return

        for i in interventions:

            card = ft.Card(
                content=ft.Container(
                    padding=15,
                    bgcolor=AppColors.CARD,
                    border_radius=12,

                    # ✔ CORRECTION FLET BORDER
                    border=ft.Border(
                        top=ft.BorderSide(1, AppColors.BORDER),
                        left=ft.BorderSide(1, AppColors.BORDER),
                        right=ft.BorderSide(1, AppColors.BORDER),
                        bottom=ft.BorderSide(1, AppColors.BORDER),
                    ),

                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"Intervention #{getattr(i, 'id_intervention', '')}",
                                weight=ft.FontWeight.BOLD,
                                size=16,
                            ),

                            ft.Text(
                                f"Incident lié : {getattr(i, 'id_incident', 'N/A')}"
                            ),

                            ft.Text(
                                f"Technicien : {getattr(i, 'id_technicien', 'Non assigné')}"
                            ),

                            ft.Text(f"Action : {getattr(i, 'action', '')}"),

                            ft.Text(f"Statut : {getattr(i, 'statut', '')}"),

                            ft.Text(
                                f"Date début : {getattr(i, 'date_debut', '')}"
                            ),
                        ],
                        spacing=6,
                    ),
                )
            )

            self.container.controls.append(card)