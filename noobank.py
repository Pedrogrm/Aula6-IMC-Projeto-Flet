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
        # Atualiza o nome do usuario ou mantem "Cliente" se vazio
        self.user_name = e.control.value if e.control.value else "Cliente"
    
    def toggle_values(self, e):
        """
        Alterna entre mostrar e ocultar valor financeiros
        """
        # Inverte o estado de visibilidade
        self.show_values = not self.show_values

        # Atualiza o texto do saldo prinipal
        self.saldo_text.value = "R$ 9.295,90" if self.show_values else "R$ ****,**"

        # Atualiza o icone do botao (olho aberto fechato/ fechado)
        self.toggle_saldo_btn.icon = ft.Icons.VISIBILITY_OF if self.show_values else ft.Icons.VISIBILITY

        # Atualiza todos os valores das movimenações
        for item in self.movement_texts:
            item["value"].value = f"R$ {item['data']['value']}" if self.show_values else "R$ ****,**"

        # Atualiza a interface
        self.page.update()

    def build_login_view(self):
        """
        Constroi a tela de login/boas-vindas
        """
        # Campo de entrada para o nome do usuario
        input_name = ft.TextField(
            border=ft.InputBorder.UNDERLINE, # Borda apenas embaixo
            hint_text="Digite seu nome aqui...",
            on_change=self.handle_name_change, # Chama função quando texto muda
            hint_style=ft.TextStyle(color="#9e9e9e"), # Cor do placeholder
            text_style=ft.TextStyle(color="white"), # Cor do texto digitado
            cursor_color="white", # Cor do cursor
        )

        def handle_login(e):
            """
            Função interna para lidar com o clique do botão entrar
            """
            # Limpa a tela atual e mosrar a tela  principal
            self.page.controls.clear()
            self.page.add(self.build_home_view())
            self.page.update()

        # Retorna container com layout da tela de login
        return ft.Container(
            bgcolor="#8a05be", # MEsma cor de fundo roxa
            alignment=ft.alignment.top_center, # Alinhamento no topo e centro
            expand=True, # Expande para ocupar espaço disponivel
            padding=ft.padding.only(left=16, right=16, top=16), # ESpaçamento interno
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START, # Alinha elementos no inicio
                controls=[
                    # Titulo de boas-vindas
                    ft.Text("Bem-vindo(a) ao NooBank!",  size=25, weight=ft.FontWeight.NORMAL, color="white"),
                    # Campo de entrada do nome
                    input_name,
                    # Botão para entrar no app
                    ft.ElevatedButton(
                        "ENTRAR",
                        bgcolor="#a126d7", # Cor de fundo roxa mais clara
                        color="white", # Cor do texto
                        on_click=handle_login, # Função chamada no clique
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8), # Bordas arredondadas
                        ),
                        width=200,
                        height=50,
                    )
                ]
            )
        )
    
    def build_home_view(self):
        """
        Constroi a tela  principal do aplicativo (após login)
        """
        # Texto que mostra o saldo(iniciamente oculto)
        self.saldo_text - ft.Text("R$ ****,**", color="#2ecc71", size=22)

        # Botão para mostrar/ocular valores
        self.toggle_saldo_btn = ft.IconButton(
            ft.Icons.VISIBILITY, # Icone de olho
            icon_color="white",
            on_click=self.toggle_values
        )

        # Layout principal em coluna
        return ft.Column(
            spacing=0,
            controls=[
                self.build_header(), # Cabeçalho com nome e botões
                ft.Container(
                    expand=True, # Expande para ocupar espaço restante
                    content=ft.Column(
                        spacing=0,
                        scroll=True, #Permite rolagem do conteudo
                        controls=[
                            self.build_balnce(), # Seção do saldo
                            self.build_shortcuts_caroulsel(), # Carrossel de atalhos
                            self.build_movements_list(),
                        ]
                    )
                )
            ]
        )
    
    def build_header(self):
        """
        Constrói o cabeçalho da tela principal
        """
        return ft.Container(
            bgcolor="#8a05be", # Cor de fundo roxa
            padding=ft.padding.only(left=16, right=16, top=16, bottom=16),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Distribui espaço entre elementos
                controls=[
                    # Nome do usuário à esquerda
                    ft.Text(self.user_name, size=18, weight=ft.FontWeight.BOLD, color="white"), 
                    # Botão a direita 
                    ft.Row(
                        controls=[
                            self.toggle.saldo_bn, # Botão de mostrar/ocultar saldo
                            ft.IconButton(icon=ft.Icons.PERSON, icon_color="white") # Botão de perfil
                        ]
                    )
                ]
            )
        )
    
    def build_balance(self):
        """
        Constroi a seção que mostra o saldo da conta
        """
        return ft.Container(
            bgcolor="#1e1e1e", # Fundo escuro
            border_radius=16, #NBordas arredondadas
            margin=ft.margin.only(left=14, right=14, top=10), # Margens externas
            padding=ft.padding.only(left=18, right=18, top=22, bottom=22), # Espaçamentos interno
            content=fr.Column(
                controls=[
                    # Label "Saldo"
                    ft.Text("Saldo", color="#9e9e9e", size=20),
                    # Linha com símbolo R$ e valor
                    ft.Row(
                        controls=[
                            ft.Text("R$",  color="#9e9e9e"), # Símbolo da moeda
                            self.saldo_text # Valor do saldo (pode estar oculto)
                        ]
                    )
                ]
            )
        )
    
    def build_shortcuts_carousel(self):
        """
        Constrói o carrossel horizontal de atalhos/funcionalidades
        """
        # Lista de atalhos disponíveis no app
        shortcuts = [
            {"icon": ft.Icons.QR_CODE, "label": "Área Pix", "color":"#ffffff"},
            {"icon": ft.Icons.PAYMENT, "label": "Pagar", "color":"#fffff"},
            {"icon": ft.Icons.STORE, "label": "Comprar", "color":"#ffffff"},
            {"icon": ft.Icons.SWAP_HORIZ, "label": "Transferir", "color":"#fffff"},
            {"icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "label": "Depositar", "color":"#ffffff"},
            {"icon": ft.Icons.CREDIT_CARD, "label": "Cartão", "color":"#ffffff"},
            {"icon": ft.Icons.LOCAL_ATM, "label": "Emprestimo", "color":"#ffffff"},
            {"icon": ft.Icons.MONEY_OFF, "label": "Cobrar", "color":"#ffffff"},
        ]

        shortcuts_items = []
        # Cria um item visual para cada atalho
        for shortcut in shortcuts:
            shortcut_items.append(
                ft.Container(
                    width=80, # Largura fixa para cada item
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                        controls=[
                            # Circulo com icone
                            ft.Container(
                                width=60,
                                height=60,
                                border_radius=30, # Faz o container circular
                                bgcolor="#2e2e2e", # Fundo escuro
                                alignment=ft.alignment.center,
                                content=ft.Icon(
                                    shortcut["icon"],
                                    color=shortcut["color"],
                                    size=24,
                                )
                            ),
                            # Texto do label abaixo do ícone
                            ft.Text(
                                shortcut["label"],
                                color="#ffffff",
                                size=12,
                                text_align=ft.TextAlign.CENTER,
                            )
                        ]
                    )
                )
            )
        
        # Container scrollável horizontal com os atalhos 
        return ft.Container(
            margin=ft.margin.only(top=16, bottom=16),
            height=100, # Alura_fixa
            content=ft.Row(
                scroll=True, # Permite rolagem horizontal
                spacing=0,
                controls=shortcuts_items,
            )
        )
    
    def build_movements_list(self):
        """
        Constroi a lista de movimentaçoes financeiras recentes
        """
        # Lisa para armazenar referencias dos texos de valores(para toggle)
        self.movements_texts = []

        movement_items = []
        # Cria um item visual para cada movimentação
        for iem in self.movements:
            movement_items.append(self.build_movements_item(item))

        return ft.Container(
            margin=ft.margin.only(left=14, right=14, bottom=16),
            content=ft.Column(
                controls=[
                    # Titulo da seção
                    ft.Container(
                        margin=f.margin.only(bottom=12),
                        content=ft.Text(
                            "Atividade recente",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="whie"
                        )
                    ),
                    # Lisa de movimenações (usando *unpacking para adicionar todos os itens)
                    *movement_items
                ]
            )
        )
    
    def build_movement_item(self, data):
        """
        Constrói um item individual da lista de movimentações
        """
        # Dtermina se é receita (entrada) ou despesa (saída)
        is_revenue = data["type"] == 1

        # Cria texto do valor com cor baseada no tipo
        # Verde para receitas, vermelho para despesas
        value_text = ft.Text(
            "R$ ****,**" # Inicialmene oculo
            color="#2ecc71" if is_revenue else
        )