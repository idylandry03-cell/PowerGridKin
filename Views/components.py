import flet as ft


class AppColors:
    PRIMARY = "#0B5394"
    SECONDARY = "#3D85C6"
    BACKGROUND = "#F4F7FB"
    CARD = "#FFFFFF"
    BORDER = "#D9E2EF"
    TEXT = "#1C1C1C"
    MUTED = "#6B7280"
    SUCCESS = "#2E7D32"
    WARNING = "#F1B600"
    DANGER = "#D00000"
    INFO = "#1976D2"


class AppText:
    FR = {
        "dashboard": "Tableau de bord",
        "incidents": "Incidents",
        "alerts": "Alertes",
        "interventions": "Interventions",
        "database": "Base de données",
        "logout": "Déconnexion",
        "language": "Langue",
        "french": "Français",
        "english": "Anglais",
    }

    EN = {
        "dashboard": "Dashboard",
        "incidents": "Incidents",
        "alerts": "Alerts",
        "interventions": "Interventions",
        "database": "Database",
        "logout": "Logout",
        "language": "Language",
        "french": "French",
        "english": "English",
    }

    @staticmethod
    def get(lang, key):
        data = AppText.FR if lang == "FR" else AppText.EN
        return data.get(key, key)


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
        return ft.Text(
            text,
            size=28,
            weight=ft.FontWeight.BOLD,
            color=AppColors.PRIMARY,
        )

    @staticmethod
    def subtitle(text):
        return ft.Text(
            text,
            size=14,
            color=AppColors.MUTED,
        )

    @staticmethod
    def section_title(text):
        return ft.Text(
            text,
            size=20,
            weight=ft.FontWeight.BOLD,
            color=AppColors.TEXT,
        )

    @staticmethod
    def page_header(title, subtitle=""):
        return ft.Column(
            controls=[
                Components.title(title),
                Components.subtitle(subtitle),
            ],
            spacing=4,
        )

    @staticmethod
    def navigation_button(text, on_click=None):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
        )

    @staticmethod
    def primary_button(text, on_click=None):
        return ft.ElevatedButton(
            text,
            bgcolor=AppColors.PRIMARY,
            color="white",
            on_click=on_click,
        )

    @staticmethod
    def success_button(text, on_click=None):
        return ft.ElevatedButton(
            text,
            bgcolor=AppColors.SUCCESS,
            color="white",
            on_click=on_click,
        )

    @staticmethod
    def danger_button(text, on_click=None):
        return ft.ElevatedButton(
            text,
            bgcolor=AppColors.DANGER,
            color="white",
            on_click=on_click,
        )

    @staticmethod
    def info_card(title, value, color=AppColors.PRIMARY, icon=""):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(icon, size=22),
                        ft.Text(title, size=14, color=AppColors.MUTED),
                        ft.Text(
                            str(value),
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                        ),
                    ],
                    spacing=6,
                ),
                padding=ft.Padding(18, 16, 18, 16),
                bgcolor=AppColors.CARD,
                border_radius=12,
                border=app_border(),
                width=230,
            )
        )

    @staticmethod
    def data_card(title, lines, badges=None):
        controls = [
            ft.Text(
                title,
                size=16,
                weight=ft.FontWeight.BOLD,
                color=AppColors.TEXT,
            )
        ]

        for line in lines:
            controls.append(
                ft.Text(
                    str(line),
                    size=13,
                    color=AppColors.TEXT,
                )
            )

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
                content=ft.Column(
                    controls=controls,
                    spacing=7,
                ),
                padding=ft.Padding(16, 14, 16, 14),
                bgcolor=AppColors.CARD,
                border_radius=12,
                border=app_border(),
                width=280,
            )
        )

    @staticmethod
    def status_badge(text):
        value = str(text or "").lower()

        color = AppColors.INFO

        if value in ["critical", "failed", "critique"]:
            color = AppColors.DANGER
        elif value in ["high", "warning", "medium", "ongoing", "in_progress", "scheduled"]:
            color = AppColors.WARNING
        elif value in ["done", "resolved", "closed", "ok"]:
            color = AppColors.SUCCESS

        return ft.Container(
            content=ft.Text(
                str(text),
                size=12,
                color="white",
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=color,
            padding=ft.Padding(10, 5, 10, 5),
            border_radius=20,
        )

    @staticmethod
    def app_container(content):
        return ft.Container(
            content=content,
            expand=True,
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor=AppColors.BACKGROUND,
        )

    @staticmethod
    def empty_message(text):
        return ft.Text(
            text,
            size=14,
            color=AppColors.MUTED,
        )