import flet as ft
from datetime import datetime

class NooBank:
    """
    Classe principal do aplicativo NooBank
    """
    def __init__(self):
        # Inicializa o aplicativo Flet apontando para o metodo main
        self.app = ft.app(target=self.main)

    def main(self, page: ft.Page):
        """
        Metodo principal que configura a página inicial do aplicativo
        """
        # Configurações básicas da janela/Página
        page.title = "NooBank"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.window_width = 400
        page.window_height = 800
        page.bgcolor = "#8a05be"

        # Armazena referencia da página para uso em outros métodos
        self.page = page
        # Nome padrão do usuario
        self.user_name = "Cliente"
        # Controla se os valores financeiros estão visiveis ou ocultos
        self.show_values = False

        # Lista de movimentações bancárias ficticias
        # type: 1 entrada (receita), 0 = saídas (despesa)
        self.movements = [
            {"id": 1, "label": "Depósito Bancánrio", "value": "4.395,90", "date": "03/02/2025", "type": 1},
            {"id": 2, "label": "Conta de luz", "value": "300,90", "date": "09/02/2025", "type": 0},
            {"id": 3, "label": "Salário", "value": "7350,00", "date": "05/03/2025", "type": 1},
            {"id": 4, "label": "Salario", "value": "2300,90", "date": "05/04/2025", "type": 0},
        ]

        # Adiciona a tela de login como primeira tela
        self.page.add(self.build_login_view())

    def handle_name_change(self, e):
        """
        Alterna entre mostrar e ocultar valores financeiros
        """
        # Atualiza o nome do usuario ou mantem "Cliente se vazio"


