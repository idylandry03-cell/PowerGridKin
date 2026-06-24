import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    def __init__(
        self,
        host: str = "127.0.0.1",
        user: str = "root",
        password: str = "1234567890",
        database: str = "power_grid_kin",
        port: int = 3306,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )

            if connection.is_connected():
                print("Connexion MySQL réussie")
                return connection

        except Error as error:
            print(f"Erreur de connexion à la base de données : {error}")

        return None