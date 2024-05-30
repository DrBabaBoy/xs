import os
import hashlib
from tinydb import TinyDB, Query
import flet as ft
from facial_recognition.ui.screens.facial_recognition_screen import FacialRecognitionScreen
from facial_recognition.ui.screens.generate_data_screen import GenerateDataScreen
from facial_recognition.ui.screens.train_model_screen import TrainModelScreen
from facial_recognition.ui.screens.check_persons_screen import CheckPersonsScreen
from facial_recognition.ui.user_controls.app_bar import custom_app_bar
from facial_recognition.util.constants import APP_TITLE

SECURITY_CODE = "1234"

data_folder = os.path.join(os.getcwd(), "data")
os.makedirs(data_folder, exist_ok=True)
db_path = os.path.join(data_folder, "usuarios.json")
db = TinyDB(db_path)


class FaceRecognitionApp(ft.UserControl):
    def build(self) -> ft.Control:
        return ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Generate data",
                    icon=ft.icons.INSERT_CHART,
                    content=GenerateDataScreen()
                ),
                ft.Tab(
                    text="Train model",
                    icon=ft.icons.ATTACH_FILE,
                    content=TrainModelScreen(),
                ),
                ft.Tab(
                    text="Recognize faces",
                    icon=ft.icons.FIND_IN_PAGE,
                    content=FacialRecognitionScreen()
                ),
                ft.Tab(
                    text="Users Check",
                    icon=ft.icons.PERSON,
                    content=CheckPersonsScreen(),
                )
            ],
            expand=True,
        )


def show_error_dialog(page, message):
    dialogo_error = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(message),
        actions=[ft.TextButton("Ok", on_click=lambda event: close_dialog(page))],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dialogo_error
    dialogo_error.open = True
    page.update()


def close_dialog(page):
    page.dialog.open = False
    page.update()


def register_user(page, usuario, password, confirmar_password, codigo_seguridad):
    if not usuario or not password or not confirmar_password or not codigo_seguridad:
        show_error_dialog(page, "Por favor, complete todos los campos.")
        return

    if codigo_seguridad != SECURITY_CODE:
        show_error_dialog(page, "Código de seguridad incorrecto.")
        return

    if password != confirmar_password:
        show_error_dialog(page, "Las contraseñas no coinciden.")
        return

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    Usuario = Query()
    if not db.search(Usuario.usuario == usuario):
        db.insert({'usuario': usuario, 'password': password_hash})
        print("Usuario registrado exitosamente!")
        show_success_dialog(page, "Usuario registrado exitosamente!")
    else:
        show_error_dialog(page, "El usuario ya existe")


def validate_login(page, usuario, password):
    if not usuario or not password:
        show_error_dialog(page, "Por favor, complete todos los campos.")
        return

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    Usuario = Query()
    resultado = db.get((Usuario.usuario == usuario) & (Usuario.password == password_hash))
    if resultado:
        print("¡Bienvenido,", usuario, "!")
        show_success_dialog(page, f"¡Bienvenido, {usuario}!")
    else:
        show_error_dialog(page, "Nombre de usuario o contraseña incorrectos")


def show_success_dialog(page, message):
    dialogo_exito = ft.AlertDialog(
        title=ft.Text("Éxito"),
        content=ft.Text(message),
        actions=[ft.TextButton("Ok")],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dialogo_exito.open = True


def login_screen(page: ft.Page) -> ft.Control:
    img = ft.Image(
        src="https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
    )

    campo_usuario = ft.TextField(label='Usuario', text_align=ft.TextAlign.LEFT, width=200)
    campo_password = ft.TextField(label='Contraseña', text_align=ft.TextAlign.LEFT, width=200, password=True)
    boton_login = ft.ElevatedButton(text='Iniciar Sesión', width=200)

    def on_login_click(event):
        usuario = campo_usuario.value
        password = campo_password.value
        try:
            validate_login(page, usuario, password)
        except Exception as e:
            show_error_dialog(page, str(e))

    boton_login.on_click = on_login_click

    return ft.Column(
        [
            ft.Row(controls=[ft.Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ft.Column([campo_usuario, campo_password, boton_login])],
                   alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )


def register_screen(page: ft.Page) -> ft.Control:
    img = ft.Image(
        src="https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
    )

    campo_usuario = ft.TextField(label='Usuario', text_align=ft.TextAlign.LEFT, width=200)
    campo_password = ft.TextField(label='Contraseña', text_align=ft.TextAlign.LEFT, width=200, password=True)
    campo_confirmar_password = ft.TextField(label='Confirmar Contraseña', text_align=ft.TextAlign.LEFT, width=200,
                                            password=True)
    campo_codigo_seguridad = ft.TextField(label='Código de Seguridad', text_align=ft.TextAlign.LEFT, width=200,
                                          password=True)
    boton_registro = ft.ElevatedButton(text='Registrar', width=200)

    def on_register_click(event):
        usuario = campo_usuario.value
        password = campo_password.value
        confirmar_password = campo_confirmar_password.value
        codigo_seguridad = campo_codigo_seguridad.value
        try:
            register_user(page, usuario, password, confirmar_password, codigo_seguridad)
        except Exception as e:
            show_error_dialog(page, str(e))

    boton_registro.on_click = on_register_click

    return ft.Column(
        [
            ft.Row(controls=[ft.Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ft.Column(
                [campo_usuario, campo_password, campo_confirmar_password, campo_codigo_seguridad, boton_registro])],
                   alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )


def app(page: ft.Page) -> None:
    page.title = APP_TITLE

    login_tab = ft.Tab(
        text="Login",
        icon=ft.icons.PERSON,
        content=login_screen(page),
    )
    register_tab = ft.Tab(
        text="Register",
        icon=ft.icons.PERSON_ADD,
        content=register_screen(page),
    )
    main_app_tab = ft.Tab(
        text="Main App",
        icon=ft.icons.APPS,
        content=FaceRecognitionApp(),
    )

    page.add(ft.Tabs(
        selected_index=0,
        tabs=[login_tab, register_tab, main_app_tab],
        expand=True,
    ))

    page.appbar = custom_app_bar()
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE)
    page.update()
    page.window_center()


def start_app() -> None:
    ft.app(target=app)
