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
from Views.components import Components


class PowerGridApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.lang = "FR"

        self.page.title = "POWER-GRID-KIN"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0

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

        view = LoginView(
            page=self.page,
            on_login_success=self.show_dashboard,
        )

        self.page.add(Components.app_container(view.build()))
        self.page.update()

    def show_dashboard(self, e=None):
        self.page.clean()

        view = DashboardView(
            power_service=self.power_service,
            statistique_service=self.statistique_service,
        )

        self.page.add(
            Components.app_container(
                ft.Column(
                    controls=[
                        self.build_navigation(),
                        view.build(),
                    ]
                )
            )
        )
        self.page.update()

    def show_incidents(self, e=None):
        self.page.clean()

        view = IncidentView(self.power_service, self.page)

        self.page.add(
            Components.app_container(
                ft.Column(
                    controls=[
                        self.build_navigation(),
                        view.build(),
                    ]
                )
            )
        )
        self.page.update()

    def show_alertes(self, e=None):
        self.page.clean()

        view = AlertView(self.power_service)

        self.page.add(
            Components.app_container(
                ft.Column(
                    controls=[
                        self.build_navigation(),
                        view.build(),
                    ]
                )
            )
        )
        self.page.update()

    def show_interventions(self, e=None):
        self.page.clean()

        view = InterventionView(self.power_service, self.page)

        self.page.add(
            Components.app_container(
                ft.Column(
                    controls=[
                        self.build_navigation(),
                        view.build(),
                    ]
                )
            )
        )
        self.page.update()

    def show_database(self, e=None):
        self.page.clean()

        view = DatabaseView(self.power_service)

        self.page.add(
            Components.app_container(
                ft.Column(
                    controls=[
                        self.build_navigation(),
                        view.build(),
                    ]
                )
            )
        )
        self.page.update()

    def build_navigation(self):
        return ft.Row(
            controls=[
                Components.navigation_button("Dashboard", self.show_dashboard),
                Components.navigation_button("Incidents", self.show_incidents),
                Components.navigation_button("Alertes", self.show_alertes),
                Components.navigation_button("Interventions", self.show_interventions),
                Components.navigation_button("Base de données", self.show_database),
                Components.navigation_button("Déconnexion", lambda e: self.show_login()),
            ],
            wrap=True,
        )


def main(page: ft.Page):
    app = PowerGridApp(page)
    app.show_login()


if __name__ == "__main__":
    ft.run(main)