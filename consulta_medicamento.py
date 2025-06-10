import flet as ft
import modelo  

def mostrar_lista(page: ft.Page, volver_a_menu=None):
    page.title = 'FARMI-UJAT'
    page.theme_mode = "dark"
    page.scroll = "auto"

    # Función para regresar al menú principal
    def regresar_menu(e):
        if volver_a_menu:
            page.clean()
            volver_a_menu(page)

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Volver",
            on_click=regresar_menu
        ),
        title=ft.Text('Medicamentos registrados'),
        center_title=True,
        bgcolor="pink",
        color="white"
    )

    response = modelo.supabase.table("medicamento").select("descripcion", "nivel_atencion", "clasificacion").limit(1000).execute()
    todos_medicamentos = response.data if response.data else []

    txt_busqueda = ft.TextField(
        label="Buscar por descripción...",
        width=400,
        on_change=lambda e: actualizar_tabla(e.control.value)
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Descripción")),
            ft.DataColumn(label=ft.Text("Nivel de Atención")),
            ft.DataColumn(label=ft.Text("Clasificación")),
        ],
        rows=[]
    )

    def actualizar_tabla(filtro=""):
        filtro = filtro.lower()
        filtrados = [m for m in todos_medicamentos if filtro in m["descripcion"].lower()]

        tabla.rows = []
        for m in filtrados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text(m.get("descripcion", "")), width=700)),
                    ft.DataCell(ft.Container(ft.Text(m.get("nivel_atencion", "")), width=180)),
                    ft.DataCell(ft.Container(ft.Text(m.get("clasificacion", "")), width=200)),
                ]
            )
            tabla.rows.append(fila)

        page.update()

    actualizar_tabla()

    page.add(
        txt_busqueda,
        tabla
    )
