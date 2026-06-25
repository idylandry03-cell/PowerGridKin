import flet as ft

from Repositories.database_connection import DatabaseConnection
from Repositories.mysql_repository import MySQLPowerGridRepository
from Services import PowerGridService, StatistiqueService
from Views import (
    LoginView,
    DashboardView,
    IncidentView,
    AlertView,
    InterventionView,
    DatabaseView,
)
from Views.components import Components, AppColors


class PowerGridApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "POWER-GRID-KIN"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.bgcolor = AppColors.BG

        db = DatabaseConnection(
            host="127.0.0.1",
            user="root",
            password="1234567890",
            database="power_grid_kin",
            port=3306,
        )

        connection = db.get_connection()

        self.repository = None
        self.power_service = None
        self.statistique_service = None

        if connection:
            self.repository = MySQLPowerGridRepository(connection)
            self.power_service = PowerGridService(self.repository)
            self.statistique_service = StatistiqueService(self.repository)

    def show_login(self):
        self.page.clean()
        login_view = LoginView(
            page=self.page,
            on_login_success=self.show_dashboard,
        )
        self.page.add(Components.app_container(login_view.build()))
        self.page.update()

    def render_page(self, content):
        self.page.clean()

        layout = ft.Row(
            controls=[
                self.sidebar(),
                ft.Container(
                    content=ft.Column(
                        controls=[content],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                    padding=ft.Padding(30, 25, 30, 25),
                    bgcolor=AppColors.BG,
                ),
            ],
            expand=True,
            spacing=0,
        )

        self.page.add(layout)
        self.page.update()

    def sidebar(self):
        return ft.Container(
            width=260,
            bgcolor=AppColors.SIDEBAR,
            padding=ft.Padding(18, 20, 18, 20),
            content=ft.Column(
                controls=[
                    ft.Text("⚡ POWER-GRID-KIN", size=20, weight=ft.FontWeight.BOLD, color=AppColors.TEXT),
                    ft.Divider(),

                    Components.navigation_button("Dashboard", self.show_dashboard),
                    Components.navigation_button("Incidents", self.show_incidents),
                    Components.navigation_button("Alertes", self.show_alertes),
                    Components.navigation_button("Interventions", self.show_interventions),
                    Components.navigation_button("Base de données", self.show_database),

                    ft.Container(expand=True),

                    ft.Text("Système de supervision hardware", size=12, color=AppColors.MUTED),
                    Components.danger_button("Déconnexion", lambda e: self.show_login()),
                ],
                spacing=12,
                expand=True,
            ),
        )

    def show_dashboard(self, e=None):
        view = DashboardView(self.power_service, self.statistique_service)
        self.render_page(view.build())

    def show_incidents(self, e=None):
        view = IncidentView(self.power_service, self.page)
        self.render_page(view.build())

    def show_alertes(self, e=None):
        view = AlertView(self.power_service)
        self.render_page(view.build())

    def show_interventions(self, e=None):
        view = InterventionView(self.power_service, self.page)
        self.render_page(view.build())

    def show_database(self, e=None):
        view = DatabaseView(self.power_service)
        self.render_page(view.build())


def main(page: ft.Page):
    app = PowerGridApp(page)
    app.show_login()


if __name__ == "__main__":
    ft.run(main)