import flet as ft
import os

def main(page: ft.Page):
    page.title = "Calculadora de IMC"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Funções
    def calculate_imc(e):
        try:
            weight = float(weight_input.value)
            height = float(height_input.value)
            if height > 0:
                imc = weight / (height * height)
                category = (
                    "Abaixo do peso" if imc < 18.5 else
                    "Peso normal" if imc < 24.9 else
                    "Sobrepeso" if imc < 29.9 else
                    "Obesidade"
                )
                result_text.value = f"IMC: {imc:.2f}\nCategoria: {category}"
            else:
                result_text.value = "Por favor, insira valores válidos."
        except ValueError:
            result_text.value = "Por favor, insira valores válidos"
        page.update()

    # Limpar campos
    def clear_fields(e):
        weight_input.value = ""
        height_input.value = ""
        result_text.value = ""
        page.update()

    # Alterar tema (Ligth e Dark)
    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        theme_icon.icon = (
            ft.Icons.LIGHT_MODE
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.DARK_MODE
        )
        update_text_colors()
        update_safearea_color()
        page.update()

    # Ajustar cores de acordo com o tema
    def update_text_colors():
        """"Ajusta cors de texto e bordas dos inputs dependendo do tema."""
        if page.theme_mode == ft.ThemeMode.DARK:
            app_bar_title.color = ft.Colors.WHITE
            title_text.color = ft.Colors.WHITE
            weight_input.label_style = ft.TextStyle(color=ft.Colors.WHITE)
            weight_input.text_style = ft.TextStyle(color=ft.Colors.WHITE)
            weight_input.border_color = ft.Colors.WHITE
            height_input.label_style = ft.TextStyle(color=ft.Colors.WHITE)
            height_input.text_style = ft.TextStyle(color=ft.Colors.WHITE)
            height_input.border_color = ft.Colors.WHITE
            result_text.color = ft.Colors.WHITE
        else:
            app_bar_title.color = ft.Colors.BLACK
            title_text.color = ft.Colors.BLACK
            weight_input.label_style = None
            weight_input.text_style = None
            weight_input.border_color = None
            height_input.label_style = None
            height_input.text_style = None
            height_input.border_color = None
            result_text.color = None

    def update_safearea_color():
        """Garante que os ícones da status bar fique, visíveis no modo Light."""
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.window_title_bar_color = ft.Colors.WHITE
            page.window_title_bar_text_color = ft.Colors.BLACK
        else:
            page.window_title_bar_color = ft.Colors.BLACK
            page.window_title_bar_text_color = ft.Colors.WHITE

    # Ícone do tema
    theme_icon = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Alternar tema",
        on_click=toggle_theme,
    )
    
    # Componets da UI
    
    app_bar_title = ft.Text("Calculadora de IMC", size=22, weight=ft.FontWeight.W_500)
    title_text = ft.Text("Informe seus dados", size=20, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

    weight_input = ft.TextField(
        label="Peso(kg)",
        prefix_icon=ft.Icons.FITNESS_CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        border=ft.InputBorder.UNDERLINE,
        filled=False,
    )

    height_input = ft.TextField(
        label="Altura (m)",
        prefix_icon=ft.Icons.HEIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        border=ft.InputBorder.UNDERLINE,
        filled=False,
    )

    result_text = ft.Text("", size=18, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

    # Caminho da imagem (precisa estar no assets e no pyproject.toml)
    image_path = "Senai.png"
    image_control = (
        ft.Image(src=image_path, height=50, fit=ft.ImageFit.CONTAIN)
        if os.path.exists(image_path)
        else ft.Text("imagem Senai.png Não encontrada")
    )

    # Layout principal
    page.add(
        ft.AppBar(title=app_bar_title, center_title=True, bgcolor=ft.Colors.TRANSPARENT, actions=[theme_icon]),
        ft.Container(
            content=ft.Column(
                controls=[
                    title_text,
                    ft.Container(height=10),
                    weight_input,
                    ft.Container(height=10),
                    height_input,
                    ft.Container(height=10),
                    result_text,
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Calcular IMC",
                                bgcolor="#673AB7",
                                color=ft.Colors.WHITE,
                                width=140,
                                height=50,
                                on_click=calculate_imc,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
                            ),
                            ft.ElevatedButton(
                                "Limpar",
                                bgcolor="#FF5252",
                                color=ft.Colors.WHITE,
                                width=140,
                                height=50,
                                on_click=clear_fields,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=10),
                    image_control,
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=10,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=10),
            bgcolor=lambda: ft.Colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE,
        )
    )

ft.app(target=main)