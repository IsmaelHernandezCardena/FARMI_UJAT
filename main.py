import flet as ft
from interacciones import mainint
from consulta_medicamento import mostrar_lista
from alta_medicamento import main as alta_medicamento_main  # Importamos la interfaz de alta

def main(page: ft.Page):
    page.title = 'FARMI-UJAT'

    def mostrar_interacciones(e: ft.ControlEvent):
        page.clean()
        mainint(page, volver_a_menu=main)

    def mostrar_alta_medicamento(e: ft.ControlEvent):
        page.clean()
        alta_medicamento_main(page, volver_a_menu=main)

    def mostrar_lista_medicamentos(e: ft.ControlEvent):
        page.clean()
        mostrar_lista(page, volver_a_menu=main)

    # Botón: Interacciones Medicamentosas
    btn_interacciones = ft.FilledButton(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon("medication", size=40, color="black"),
                    ft.Text("Interacciones Medicamentosas")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=10
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, "orange")
        ),
        bgcolor="orange100",
        color="black",
        width=200,
        on_click=mostrar_interacciones
    )

    # Botón: Alta de Medicamento
    btn_alta = ft.FilledButton(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon("add", size=40, color="black"),
                    ft.Text("Alta de Medicamento")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=10
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, "green")
        ),
        bgcolor="green100",
        color="black",
        width=200,
        on_click=mostrar_alta_medicamento
    )

    # Botón: Lista de Medicamentos con ícono
    btn_lista = ft.FilledButton(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon("list", size=40, color="black"),
                    ft.Text("Lista de Medicamentos")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=10
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, "blue")
        ),
        bgcolor="blue100",
        color="black",
        width=200,
        on_click=mostrar_lista_medicamentos
    )

    fila_botones = ft.Row(
        controls=[btn_interacciones, btn_alta, btn_lista],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.appbar = ft.AppBar(
        title=ft.Text("FARMI-UJAT", size=40),
        center_title=True,
        bgcolor="pink",  
        color="white"
    )

    page.add(fila_botones)

# Ejecutar la app en navegador
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
