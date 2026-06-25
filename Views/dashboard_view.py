import flet as ft
from Views.components import Components, AppColors


class DashboardView:
    def __init__(self, power_service, statistique_service):
        self.power_service = power_service
        self.statistique_service = statistique_service

    def build(self):

        stats = self.power_service.repository.get_dashboard_stats()

        return ft.Column(
            controls=[
                Components.page_header(
                    "Dashboard",
                    "Vue globale du système Power Grid Kin",
                ),

                ft.Row(
                    controls=[
                        Components.info_card("Incidents", stats["incidents_total"], AppColors.DANGER),
                        Components.info_card("Ouverts", stats["incidents_ouverts"], AppColors.WARNING),
                        Components.info_card("Résolus", stats["incidents_resolus"], AppColors.SUCCESS),
                        Components.info_card("Alertes", stats["alertes_critiques"], AppColors.DANGER),
                    ],
                    wrap=True,
                ),

                ft.Row(
                    controls=[
                        Components.info_card("Interventions", stats["interventions_total"]),
                        Components.info_card("Techniciens", stats["techniciens_total"]),
                        Components.info_card("Équipements", stats["equipements_total"]),
                        Components.info_card("Capteurs", stats["capteurs_total"]),
                    ],
                    wrap=True,
                ),
            ]
        )