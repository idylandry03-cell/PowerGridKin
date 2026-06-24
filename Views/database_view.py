import flet as ft
from Views.components import Components


class DatabaseView:
    def __init__(self, service):
        self.service = service

    def build(self):

        data = self.service.retrieve_database_overview()

        return ft.Column(
            controls=[
                Components.page_header(
                    "Base de données",
                    "Vue complète du système POWER-GRID-KIN",
                ),

                self.section_communes(data.get("communes", [])),
                self.section_postes(data.get("postes", [])),
                self.section_circuits(data.get("circuits", [])),
                self.section_equipements(data.get("equipements", [])),
                self.section_capteurs(data.get("capteurs", [])),
                self.section_techniciens(data.get("techniciens", [])),
            ],
            spacing=25,
            scroll=ft.ScrollMode.AUTO,
        )

    def section_communes(self, communes):

        cards = []

        for c in communes:
            cards.append(
                Components.data_card(
                    title=c.get("nom", ""),
                    lines=[
                        f"Population : {c.get('population', '')}",
                        f"Description : {c.get('description', '')}",
                    ],
                )
            )

        return ft.Column(
            controls=[
                Components.section_title("Communes"),
                ft.ResponsiveRow(cards),
            ]
        )

    def section_postes(self, postes):

        cards = []

        for p in postes:
            cards.append(
                Components.data_card(
                    title=p.get("nom", ""),
                    lines=[
                        f"Commune : {p.get('commune', '')}",
                        f"Centrale : {p.get('centrale', '')}",
                        f"Tension : {p.get('tension_kv', '')} kV",
                        f"Adresse : {p.get('adresse', '')}",
                    ],
                )
            )

        return ft.Column(
            controls=[
                Components.section_title("Postes électriques"),
                ft.ResponsiveRow(cards),
            ]
        )

    def section_circuits(self, circuits):

        cards = []

        for c in circuits:
            cards.append(
                Components.data_card(
                    title=c.get("code", ""),
                    lines=[
                        f"Intitulé : {c.get('intitule', '')}",
                        f"Poste : {c.get('poste', '')}",
                        f"Tension : {c.get('tension_kv', '')} kV",
                        f"Zone : {c.get('zone_description', '')}",
                    ],
                )
            )

        return ft.Column(
            controls=[
                Components.section_title("Circuits"),
                ft.ResponsiveRow(cards),
            ]
        )

    def section_equipements(self, equipements):

        cards = []

        for e in equipements:
            cards.append(
                Components.data_card(
                    title=e.get("reference", ""),
                    lines=[
                        f"Type : {e.get('type_equipement', '')}",
                        f"Circuit : {e.get('circuit', '')}",
                        f"Poste : {e.get('poste', '')}",
                        f"Détails : {e.get('details', '')}",
                    ],
                    badges=[e.get("statut", "ok")],
                )
            )

        return ft.Column(
            controls=[
                Components.section_title("Équipements"),
                ft.ResponsiveRow(cards),
            ]
        )

    def section_capteurs(self, capteurs):

        cards = []

        for s in capteurs:
            cards.append(
                Components.data_card(
                    title=s.get("code_sensor", ""),
                    lines=[
                        f"Type : {s.get('type_sensor', '')}",
                        f"Équipement : {s.get('equipement', '')}",
                        f"Circuit : {s.get('circuit', '')}",
                        f"Valeur : {s.get('last_value', '')}",
                        f"Mise à jour : {s.get('last_update', '')}",
                    ],
                )
            )

        return ft.Column(
            controls=[
                Components.section_title("Capteurs"),
                ft.ResponsiveRow(cards),
            ]
        )

    def section_techniciens(self, techs):

        cards = []

        for t in techs:
            cards.append(
                Components.data_card(
                    title=f"{t.get('nom', '')} {t.get('prenom', '')}",
                    lines=[
                        f"Téléphone : {t.get('telephone', '')}",
                        f"Email : {t.get('email', '')}",
                        f"Compétence : {t.get('competence', '')}",
                        f"Commune : {t.get('commune', '')}",
                    ],
                )
            )

        return ft.Column(
            controls=[
                Components.section_title("Techniciens"),
                ft.ResponsiveRow(cards),
            ]
        )