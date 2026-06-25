import flet as ft


class AppColors:
    BG = "#1B1C22"
    SIDEBAR = "#20212A"
    TOPBAR = "#2A2B35"
    CARD = "#262733"
    CARD_LIGHT = "#2E3040"
    PRIMARY = "#7F8CFF"
    BLUE = "#2196F3"
    TEXT = "#F2F2F5"
    MUTED = "#B8B8C7"
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    DANGER = "#F44336"
    BORDER = "#3A3B48"


class AppText:
    FR = {
        "dashboard": "Dashboard",
        "incidents": "Incidents",
        "alerts": "Alertes",
        "interventions": "Interventions",
        "database": "Base de données",
        "logout": "Déconnexion",
    }

    @staticmethod
    def get(lang, key):
        return AppText.FR.get(key, key)


def app_border():
    return ft.Border(
        top=ft.BorderSide(1, AppColors.BORDER),
        left=ft.BorderSide(1, AppColors.BORDER),
        right=ft.BorderSide(1, AppColors.BORDER),
        bottom=ft.BorderSide(1, AppColors.BORDER),
    )


class Components:

    @staticmethod
    def title(text):
        return ft.Text(text, size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT)

    @staticmethod
    def subtitle(text):
        return ft.Text(text, size=14, color=AppColors.MUTED)

    @staticmethod
    def section_title(text):
        return ft.Text(text, size=20, weight=ft.FontWeight.BOLD, color=AppColors.TEXT)

    @staticmethod
    def page_header(title, subtitle=""):
        return ft.Column(
            controls=[
                Components.title(title),
                Components.subtitle(subtitle),
            ],
            spacing=5,
        )

    @staticmethod
    def navigation_button(text, on_click=None):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=AppColors.CARD_LIGHT,
            color=AppColors.TEXT,
            width=210,
            height=45,
        )

    @staticmethod
    def primary_button(text, on_click=None):
        return ft.ElevatedButton(text, on_click=on_click, bgcolor=AppColors.PRIMARY, color="white")

    @staticmethod
    def success_button(text, on_click=None):
        return ft.ElevatedButton(text, on_click=on_click, bgcolor=AppColors.SUCCESS, color="white")

    @staticmethod
    def danger_button(text, on_click=None):
        return ft.ElevatedButton(text, on_click=on_click, bgcolor=AppColors.DANGER, color="white")

    @staticmethod
    def info_card(title, value, color=AppColors.PRIMARY, icon=""):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(icon, size=26),
                        ft.Text(title, size=14, color=AppColors.MUTED),
                        ft.Text(str(value), size=28, weight=ft.FontWeight.BOLD, color=color),
                    ],
                    spacing=8,
                ),
                width=260,
                height=145,
                padding=18,
                bgcolor=AppColors.CARD,
                border_radius=14,
                border=app_border(),
            )
        )

    @staticmethod
    def data_card(title, lines, badges=None):
        controls = [
            ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=AppColors.TEXT)
        ]

        for line in lines:
            controls.append(ft.Text(str(line), size=13, color=AppColors.MUTED))

        if badges:
            controls.append(
                ft.Row(
                    controls=[Components.status_badge(b) for b in badges],
                    wrap=True,
                    spacing=8,
                )
            )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(controls=controls, spacing=7),
                padding=16,
                bgcolor=AppColors.CARD,
                border_radius=14,
                border=app_border(),
            )
        )

    @staticmethod
    def status_badge(text):
        value = str(text or "").lower()
        color = AppColors.BLUE

        if value in ["critical", "failed"]:
            color = AppColors.DANGER
        elif value in ["high", "warning", "medium", "ongoing", "in_progress", "scheduled"]:
            color = AppColors.WARNING
        elif value in ["done", "resolved", "closed", "ok"]:
            color = AppColors.SUCCESS

        return ft.Container(
            content=ft.Text(str(text), size=12, color="white", weight=ft.FontWeight.BOLD),
            bgcolor=color,
            padding=ft.Padding(10, 5, 10, 5),
            border_radius=20,
        )

    @staticmethod
    def app_container(content):
        return ft.Container(
            content=content,
            expand=True,
            bgcolor=AppColors.BG,
        )

    @staticmethod
    def empty_message(text):
        return ft.Text(text, size=14, color=AppColors.MUTED)