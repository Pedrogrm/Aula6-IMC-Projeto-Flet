import flet as ft
import random
import string

def main(page: ft.Page):
    page.title = "Gerador de Senhas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 350
    page.window_height = 600
    page.padding = 20
    
    # Variável para armazenar a senha atual
    senha_atual = ""
    
    def gerar_senha(e):
        nonlocal senha_atual
        comprimento = int(slider.value)
        caracteres = ""
        if upper_switch.value:
            caracteres += string.ascii_uppercase
        if lower_switch.value:
            caracteres += string.ascii_lowercase
        if numbers_switch.value:
            caracteres += string.digits
        if symbols_switch.value:
            caracteres += string.punctuation
        
        if caracteres:
            senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
            senha_output.value = senha
            senha_atual = senha
            # Mostrar o botão de copiar explícito
            copiar_btn.visible = True
        else:
            senha_output.value = "Selecione ao menos um tipo de caractere."
            senha_atual = ""
            copiar_btn.visible = False
        page.update()
    
    def mostrar_senha_copiada(e):
        if senha_atual:
            # Exibir mensagem de feedback usando text_display
            text_display.value = f"Senha copiada: {senha_atual}"
            text_display.visible = True
            page.update()
            
            # Opcional: tentar usar os métodos de clipboard disponíveis
            try:
                page.set_clipboard(senha_atual)
            except:
                pass  # Ignora se falhar
    
    def toggle_theme(e):
        nonlocal is_dark
        is_dark = not is_dark
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        theme_button.icon = ft.Icons.DARK_MODE if is_dark else ft.Icons.LIGHT_MODE
        page.update()
    
    is_dark = False
    
    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        on_click=toggle_theme
    )

    title_switch_row = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            # Adicione um container vazio para empurrar o texto e o botão
            ft.Container(expand=True), 
            ft.Text("Gerador de Senhas", size=28, weight="bold"),
            ft.Container(
                content=theme_button,
                expand=True, 
                alignment=ft.alignment.center_right
            )
        ]
    )
    
    title_switch_container = ft.Container(
        content=title_switch_row,
        padding=ft.padding.only(top=50),
    )
    
    senha_output = ft.TextField(
        value="",
        label="Senha Gerada",
        read_only=True,
        width=280
        # bgcolor=ft.Colors.ON_SURFACE_VARIANT
    )
    
    # Campo de texto para exibir feedback quando a senha for "copiada"
    text_display = ft.Text(
        value="",
        color=ft.Colors.GREEN,
        visible=False
    )
    
    # Botão explícito para copiar
    copiar_btn = ft.ElevatedButton(
        text="COPIAR SENHA",
        on_click=mostrar_senha_copiada,
        color=ft.Colors.ON_SECONDARY,
        bgcolor=ft.Colors.SECONDARY,
        visible=False
    )
    
    slider = ft.Slider(
        min=8,
        max=20,
        value=12,
        divisions=12,
        label="CARACTERES: {value}"
    )
    
    upper_switch = ft.Switch(label="Letras maiúsculas")
    lower_switch = ft.Switch(label="Letras minúsculas", value=True)
    numbers_switch = ft.Switch(label="Incluir números")
    symbols_switch = ft.Switch(label="Incluir símbolos")
    
    preferencias_column = ft.Column(
        [
            ft.Text("PREFERÊNCIAS", size=16, weight="bold"),
            upper_switch,
            lower_switch,
            numbers_switch,
            symbols_switch,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10
    )
    
    preferencias_container = ft.Container(
        content=preferencias_column,
        padding=ft.padding.all(20),
        alignment=ft.alignment.top_left
    )
    
    gerar_button = ft.ElevatedButton(
        text="GERAR SENHA",
        on_click=gerar_senha,
        color=ft.Colors.ON_PRIMARY,
        bgcolor=ft.Colors.PRIMARY
    )
    
    page.add(
        ft.Column(
            [
                title_switch_container,
                senha_output,
                text_display,
                copiar_btn,
                slider,
                preferencias_container,
                gerar_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    )

ft.app(
    target=main,
    assets_dir="assets"
)