import flet as ft
import modelo as md  # Debe contener: supabase = create_client(...)

def mainint(page: ft.Page, volver_a_menu=None):
    # Dropdowns y campos de texto definidos como locales para usarlos en varias funciones
    drp_medicamento1 = ft.Dropdown()
    drp_medicamento2 = ft.Dropdown()
    drp_medicamento3 = ft.Dropdown()
    drp_medicamento4 = ft.Dropdown()
    drp_medicamento5 = ft.Dropdown()

    txt_interaccion1 = ft.TextField(read_only=True, width=400)
    txt_interaccion2 = ft.TextField(read_only=True, width=400)
    txt_interaccion3 = ft.TextField(read_only=True, width=400)
    txt_interaccion4 = ft.TextField(read_only=True, width=400)
    txt_interaccion5 = ft.TextField(read_only=True, width=400)

    mensaje = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    def mostrar_interacciones(e: ft.ControlEvent):
        control_to_text = {
            drp_medicamento1: txt_interaccion1,
            drp_medicamento2: txt_interaccion2,
            drp_medicamento3: txt_interaccion3,
            drp_medicamento4: txt_interaccion4,
            drp_medicamento5: txt_interaccion5,
        }

        txt = control_to_text.get(e.control)
        # Aquí puedes añadir lógica para mostrar interacciones reales
        txt.value = "No se encontraron interacciones" if e.control.value else ""
        txt.update()

    def limpiar_campos():
        for dropdown in [drp_medicamento1, drp_medicamento2, drp_medicamento3, drp_medicamento4, drp_medicamento5]:
            dropdown.value = None
            dropdown.update()
        for txt in [txt_interaccion1, txt_interaccion2, txt_interaccion3, txt_interaccion4, txt_interaccion5]:
            txt.value = ""
            txt.update()

    def guardar_Receta(e: ft.ControlEvent):
        medicamentos = [
            (drp_medicamento1, txt_interaccion1),
            (drp_medicamento2, txt_interaccion2),
            (drp_medicamento3, txt_interaccion3),
            (drp_medicamento4, txt_interaccion4),
            (drp_medicamento5, txt_interaccion5),
        ]

        if not any(drp.value for drp, _ in medicamentos):
            mensaje.value = "Selecciona al menos un medicamento"
            mensaje.color = "red"
            mensaje.update()
            return

        try:
            for drp, txt in medicamentos:
                if drp.value:
                    md.supabase.table("receta").insert([{
                        "medicamento": drp.value,
                        "interaccion": txt.value or ""
                    }]).execute()

            mensaje.value = "Receta guardada exitosamente"
            mensaje.color = "green"
            limpiar_campos()
        except Exception as ex:
            mensaje.value = f"Error al guardar: {ex}"
            mensaje.color = "red"

        mensaje.update()

    def limpiar_formulario(e: ft.ControlEvent):
        limpiar_campos()
        mensaje.value = ""
        mensaje.update()

    # Configuración de la página
    page.title = 'FARMI-UJAT'
    page.theme_mode = "dark"
    page.appbar = ft.AppBar(
        title=ft.Text("Interacciones UJAT", weight=ft.FontWeight.BOLD),
        leading=ft.Icon(ft.Icons.MEDICAL_SERVICES),
        bgcolor="pink",
        color="white"
    )

    # Obtener medicamentos desde Supabase
    response = md.supabase.table("medicamento").select("descripcion").execute()
    opciones = [ft.dropdown.Option(m["descripcion"]) for m in response.data]

    # Configurar dropdowns con opciones y eventos
    for drp in [drp_medicamento1, drp_medicamento2, drp_medicamento3, drp_medicamento4, drp_medicamento5]:
        drp.options = opciones
        drp.editable = True
        drp.enable_filter = True
        drp.width = 200
        drp.on_change = mostrar_interacciones

    # Etiquetas
    drp_medicamento1.label = "Selecciona el medicamento 1"
    drp_medicamento2.label = "Selecciona el medicamento 2"
    drp_medicamento3.label = "Selecciona el medicamento 3"
    drp_medicamento4.label = "Selecciona el medicamento 4"
    drp_medicamento5.label = "Selecciona el medicamento 5"

    txt_interaccion1.label = "Interacciones del medicamento 1"
    txt_interaccion2.label = "Interacciones del medicamento 2"
    txt_interaccion3.label = "Interacciones del medicamento 3"
    txt_interaccion4.label = "Interacciones del medicamento 4"
    txt_interaccion5.label = "Interacciones del medicamento 5"

    # Columnas
    col_medicamentos = ft.Column([
        ft.Text("Medicamentos", weight=ft.FontWeight.BOLD),
        ft.Divider(),
        drp_medicamento1,
        drp_medicamento2,
        drp_medicamento3,
        drp_medicamento4,
        drp_medicamento5,
    ], expand=True, spacing=10)

    col_interacciones = ft.Column([
        ft.Text("Interacciones", weight=ft.FontWeight.BOLD),
        ft.Divider(),
        txt_interaccion1,
        txt_interaccion2,
        txt_interaccion3,
        txt_interaccion4,
        txt_interaccion5,
    ], expand=True, spacing=10)

    # Botones
    btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, bgcolor="green", color="white", width=150, on_click=guardar_Receta)
    btn_limpiar = ft.ElevatedButton("Limpiar", icon=ft.Icons.CLEAR, bgcolor="blue", color="white", width=150, on_click=limpiar_formulario)

    # Botón para regresar al menú principal
    btn_regresar = ft.ElevatedButton(
        "Regresar al menú", bgcolor="gray", color="white", width=150, icon=ft.Icons.HOME,
        on_click=lambda e: (page.clean(), volver_a_menu(page)) if volver_a_menu else None
    )

    # Layout principal
    page.add(
        ft.Row([col_medicamentos, col_interacciones], spacing=10),
        ft.Column([
            ft.Row([btn_guardar, btn_limpiar, btn_regresar], alignment="end", spacing=20),
            mensaje
        ])
    )

    page.update()
