import flet as ft

from Views.components import Components, AppColors


class LoginView:
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success

        self.username_input = ft.TextField(
            label="Nom d'utilisateur",
            width=300,
        )

        self.password_input = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            width=300,
        )

    def build(self) -> ft.Control:
        return ft.Container(
            content=ft.Column(
                controls=[
                    Components.title("POWER-GRID-KIN"),
                    Components.subtitle("Connexion au système de supervision"),
                    self.username_input,
                    self.password_input,
                    ft.ElevatedButton(
                        "Se connecter",
                        bgcolor=AppColors.PRIMARY,
                        color="white",
                        on_click=self.login,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            alignment=ft.Alignment(0, 0),
            expand=True,
        )

    def login(self, e) -> None:
        username = self.username_input.value.strip().upper()
        password = self.password_input.value.strip()

        techniciens = [
            "AKONKWA BAGANIZI",
            "CHYROMOD MUGOLI",
            "DOMO TYTY",
            "FANSAK A FANSAK",
            "IDY KANGELA",
            "IKOKO LOKIKI",
            "ILUNGA NGINDU",
            "KANYERE NYAVINGI",
            "KAYEMBE KAPIAMBA",
            "KITSA KAWAYA",
            "LUKOKI MINU",
            "MAMADOU SONA",
            "MASANKA KALALA",
            "MASIALA MUANDA",
            "MAWANIKA NGWANZA",
            "MBALI KANYINDA",
            "MINANGA NDAMBOLU",
            "MPOZE MOUAFO",
            "MUMBAMBI OMBAM",
            "MUNKOY KATUMBA",
            "MWELWA KALUMBA",
            "TABU LUMBALUMBA",
            "TSHONGO VIKYO",
            "WABATINGA MWAYUMA",
            "ZULU SONA",
        ]

        if username in techniciens and password == "1234567890":
            self.on_login_success()
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Nom d'utilisateur ou mot de passe incorrect.")
            )
            self.page.snack_bar.open = True
            self.page.update()