import os
import hashlib
from tinydb import TinyDB, Query
import flet as ft
from facial_recognition.ui.screens.facial_recognition_screen import FacialRecognitionScreen
from facial_recognition.ui.screens.generate_data_screen import GenerateDataScreen
from facial_recognition.ui.screens.train_model_screen import TrainModelScreen
from facial_recognition.ui.user_controls.app_bar import custom_app_bar
from facial_recognition.util.constants import APP_TITLE

# Constants
SECURITY_CODE = "5943"

data_folder = os.path.join(os.getcwd(), "data")
os.makedirs(data_folder, exist_ok=True)
db_path = os.path.join(data_folder, "usuarios.json")
db = TinyDB(db_path)


class PageManager:
    def __init__(self, page):
        self.page = page

    def show_register_page(self):
        self.page.clean()
        self.page.title = 'Registro'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_resizable = True

        img = ft.Image(
            src=f"https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        campo_usuario = ft.TextField(label='Usuario', text_align=ft.TextAlign.LEFT, width=200)
        campo_password = ft.TextField(label='Contraseña', text_align=ft.TextAlign.LEFT, width=200, password=True)
        campo_confirmar_password = ft.TextField(label='Confirmar Contraseña', text_align=ft.TextAlign.LEFT, width=200, password=True)
        campo_codigo_seguridad = ft.TextField(label='Código de Seguridad', text_align=ft.TextAlign.LEFT, width=200, password=True)
        boton_registro = ft.ElevatedButton(text='Registrar', width=200)

        def on_register_click(event):
            usuario = campo_usuario.value
            password = campo_password.value
            confirmar_password = campo_confirmar_password.value
            codigo_seguridad = campo_codigo_seguridad.value
            self.register_user(usuario, password, confirmar_password, codigo_seguridad)

        boton_registro.on_click = on_register_click

        self.page.add(
            ft.Row(controls=[ft.Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ft.Column([campo_usuario, campo_password, campo_confirmar_password, campo_codigo_seguridad, boton_registro])],
                alignment=ft.MainAxisAlignment.CENTER)
        )

    def show_login_page(self):
        self.page.clean()
        self.page.title = 'Login'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_resizable = True

        img = ft.Image(
            src=f"https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
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
            self.validate_login(usuario, password)

        boton_login.on_click = on_login_click

        self.page.add(
            ft.Row(controls=[ft.Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ft.Column([campo_usuario, campo_password, boton_login])],
                alignment=ft.MainAxisAlignment.CENTER)
        )

    def show_menu_page(self):
        self.page.clean()
        self.page.title = 'Menú'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_resizable = True

        img = ft.Image(
            src=f"https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        boton_registro = ft.ElevatedButton(text='Registrarse', width=200)
        boton_login = ft.ElevatedButton(text='Iniciar Sesión', width=200)

        def on_register_click(event):
            self.show_register_page()

        def on_login_click(event):
            self.show_login_page()

        boton_registro.on_click = on_register_click
        boton_login.on_click = on_login_click

        self.page.add(
            ft.Row(controls=[ft.Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ft.Column([boton_registro])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[ft.Column([boton_login])], alignment=ft.MainAxisAlignment.CENTER)
        )

    def register_user(self, usuario, password, confirmar_password, codigo_seguridad):
        if not usuario or not password or not confirmar_password or not codigo_seguridad:
            self.show_error_dialog("Por favor, complete todos los campos.")
            return

        if codigo_seguridad != SECURITY_CODE:
            self.show_error_dialog("Código de seguridad incorrecto.")
            return

        try:
            if password != confirmar_password:
                self.show_error_dialog("Las contraseñas no coinciden.")
                return

            password_hash = hashlib.sha256(password.encode()).hexdigest()
            Usuario = Query()
            if not db.search(Usuario.usuario == usuario):
                db.insert({'usuario': usuario, 'password': password_hash})
                print("Usuario registrado exitosamente!")
                self.show_app_page()  # Cambio a la nueva página
            else:
                self.show_error_dialog("El usuario ya existe")
        except Exception as e:
            print("Error:", e)

    def validate_login(self, usuario, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            Usuario = Query()
            resultado = db.get((Usuario.usuario == usuario) & (Usuario.password == password_hash))
            if resultado:
                print("¡Bienvenido,", usuario, "!")
                self.show_app_page()  # Cambio a la nueva página
            else:
                self.show_error_dialog("Nombre de usuario o contraseña incorrectos")
        except Exception as e:
            print("Error:", e)

    def show_app_page(self):
        # Muestra la nueva página de la aplicación
        self.page.clean()
        self.page.add(FaceRecognitionApp())
        self.page.update()

    def show_error_dialog(self, message):
        dialogo_error = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("Ok", on_click=self.close_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialogo_error
        dialogo_error.open = True
        self.page.update()

    def close_dialog(self, event):
        self.page.dialog.open = False
        self.page.update()


class FaceRecognitionApp(ft.UserControl):
    def build(self) -> ft.Control:
        return ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Generate data",
                    icon=ft.icons.INSERT_CHART,
                    content=GenerateDataScreen(),
                ),
                ft.Tab(
                    text="Train model",
                    icon=ft.icons.ATTACH_FILE,
                    content=TrainModelScreen(),
                ),
                ft.Tab(
                    text="Recognize faces",
                    icon=ft.icons.FIND_IN_PAGE,
                    content=FacialRecognitionScreen(),
                )
            ],
            expand=True,
        )


def app(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.add(FaceRecognitionApp())

    page.appbar = custom_app_bar()
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_50)
    page.update()
    page.window_center()


def main(page: ft.Page) -> None:
    page_manager = PageManager(page)
    page_manager.show_menu_page()
    page.window_center()


ft.app(main)

