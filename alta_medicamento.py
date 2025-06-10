import flet as ft
import modelo  

# Variables globales
txt_clave = txt_descripcion = txt_presentacion = None
drp_clasificacion = drp_nivel = drp_nombre_farmaco = None
mensaje_alerta = None  # Mensaje reutilizable

def obtener_datos():
    lista_clasificaciones = []
    lista_niveles_atencion = []
    lista_nombres_farmaco = []

    res = modelo.supabase.table("medicamento").select("clasificacion").execute()
    clasificaciones = list({m["clasificacion"] for m in res.data if m.get("clasificacion")})
    lista_clasificaciones = [ft.dropdown.Option(c) for c in clasificaciones]

    res = modelo.supabase.table("medicamento").select("nivel_atencion").execute()
    niveles = list({m["nivel_atencion"] for m in res.data if m.get("nivel_atencion")})
    lista_niveles_atencion = [ft.dropdown.Option(n) for n in niveles]

    res = modelo.supabase.table("farmaco").select("nombre").execute()
    nombres = [f["nombre"] for f in res.data if f.get("nombre")]
    lista_nombres_farmaco = [ft.dropdown.Option(n) for n in nombres]

    return lista_clasificaciones, lista_niveles_atencion, lista_nombres_farmaco

def guardar_y_salir(page, e):
    clave = txt_clave.value.strip()
    descripcion = txt_descripcion.value.strip()
    presentacion = txt_presentacion.value.strip()
    clasificacion = drp_clasificacion.value
    nivel_atencion = drp_nivel.value
    nombre_farmaco = drp_nombre_farmaco.value

    mensaje_alerta.value = ""
    mensaje_alerta.color = "red"

    if not (clave and descripcion and presentacion and clasificacion and nivel_atencion):
        mensaje_alerta.value = "Todos los campos son obligatorios."
        page.update()
        return

    nuevo_medicamento = {
        "clave": clave,
        "descripcion": descripcion,
        "presentacion": presentacion,
        "clasificacion": clasificacion,
        "nivel_atencion": nivel_atencion,
        "nombre_farmaco": nombre_farmaco
    }

    try:
        insert_res = modelo.supabase.table("medicamento").insert(nuevo_medicamento).execute()
        if insert_res.data:
            mensaje_alerta.value = "Medicamento guardado con éxito"
            mensaje_alerta.color = "green"

            txt_clave.value = "S/C "
            txt_descripcion.value = ""
            txt_presentacion.value = ""
            drp_clasificacion.value = None
            drp_nivel.value = None
            drp_nombre_farmaco.value = None
        else:
            mensaje_alerta.value = "Error al guardar medicamento"
            mensaje_alerta.color = "red"
    except Exception as ex:
        mensaje_alerta.value = f"⚠️ Error: {str(ex)}"
        mensaje_alerta.color = "red"

    page.update()

def cancelar(e):
    # Puedes agregar alguna acción aquí o dejarlo vacío
    print("Operación cancelada")

def main(page: ft.Page, volver_a_menu=None):
    global txt_clave, txt_descripcion, txt_presentacion
    global drp_clasificacion, drp_nivel, drp_nombre_farmaco, mensaje_alerta

    page.title = 'FARMI-UJAT'
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"  
    page.scroll = True  

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MEDICAL_SERVICES),
        title=ft.Text('Nuevo Medicamento'),
        center_title=True,
        bgcolor="pink",
        color="white"
    )

    lista_clasificaciones, lista_niveles_atencion, lista_nombres_farmaco = obtener_datos()

    txt_clave = ft.TextField(label="Clave", width=370, border="underline", filled=True, value="S/C ")
    txt_descripcion = ft.TextField(label="Descripción", width=370, multiline=True, min_lines=1, max_lines=3)
    txt_presentacion = ft.TextField(label="Presentación", width=370, multiline=True, min_lines=1, max_lines=3)

    drp_clasificacion = ft.Dropdown(options=lista_clasificaciones, width=179, label="Clasificación")
    drp_nivel = ft.Dropdown(options=lista_niveles_atencion, width=177, label="Nivel de Atención") 
    drp_nombre_farmaco = ft.Dropdown(options=lista_nombres_farmaco, width=370, label="Fármaco (opcional)") 

    mensaje_alerta = ft.Text(value="", color="red", size=14)

    btn_guardar_salir = ft.ElevatedButton(
        "Guardar", bgcolor="blue", color="white", width=160, icon=ft.Icons.SAVE,
        on_click=lambda e: guardar_y_salir(page, e)
    )
    btn_cancelar = ft.ElevatedButton(
        "Cancelar", bgcolor="red", color="white", width=160, icon=ft.Icons.CLOSE,
        on_click=cancelar
    )

    # Botón para regresar al menú principal
    btn_regresar = ft.ElevatedButton(
        "Regresar al menú", bgcolor="gray", color="white", width=160, icon=ft.Icons.HOME,
        on_click=lambda e: (page.clean(), volver_a_menu(page)) if volver_a_menu else None
    )

    page.add(
        txt_clave,
        txt_descripcion,
        txt_presentacion,
        ft.Row([drp_clasificacion, drp_nivel], alignment="center"),
        drp_nombre_farmaco,
        mensaje_alerta,
        ft.Row([btn_guardar_salir, btn_cancelar, btn_regresar], alignment="center"),
    )

    page.update()
