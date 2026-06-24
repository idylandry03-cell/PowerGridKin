import flet as ft
from Views.components import Components, AppColors


class AlertView:
    def __init__(self, service):
        self.service = service
        self.alertes_container = ft.Column()

    def build(self):
        self.refresh_alertes()

        return ft.Column(
            controls=[
                Components.page_header(
                    "Alertes",
                    "Liste des alertes du système",
                ),
                self.alertes_container,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh_alertes(self):

        alertes = self.service.retrieve_alertes()
        self.alertes_container.controls.clear()

        for a in alertes:

            card = ft.Card(
                content=ft.Container(
                    padding=15,
                    bgcolor=AppColors.CARD,
                    border_radius=12,
                    border=ft.Border(
                        top=ft.BorderSide(1, AppColors.BORDER),
                        left=ft.BorderSide(1, AppColors.BORDER),
                        right=ft.BorderSide(1, AppColors.BORDER),
                        bottom=ft.BorderSide(1, AppColors.BORDER),
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                a.type_alerte,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(a.message),
                            ft.Text(str(a.date_alerte)),
                        ]
                    ),
                )
            )

            self.alertes_container.controls.append(card)