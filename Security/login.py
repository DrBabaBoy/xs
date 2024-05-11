import flet as ft
from flet import TextField, ElevatedButton, Column, Row, AlertDialog, TextButton, Text
from tinydb import TinyDB, Query
import hashlib
import os

data_folder = os.path.join(os.getcwd(), "data")
os.makedirs(data_folder, exist_ok=True)
db_path = os.path.join(data_folder, "usuarios.json")
db = TinyDB(db_path)


class PaginaRegistro:
    def __init__(self, pagina):
        self.pagina = pagina
        self.dialogo_error = AlertDialog(
            title=Text("Error"),
            content=Text("Por favor, complete todos los campos."),
            actions=[TextButton("Ok", on_click=self.cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.dialogo_usuario_existente = AlertDialog(
            title=Text("Error"),
            content=Text("El usuario ya existe"),
            actions=[TextButton("Ok", on_click=self.cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.dialogo_codigo_incorrecto = AlertDialog(
            title=Text("Error"),
            content=Text("Código de seguridad incorrecto."),
            actions=[TextButton("Ok", on_click=self.cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def cerrar_dialogo(self, event):
        self.dialogo_error.open = False
        self.dialogo_usuario_existente.open = False
        self.dialogo_codigo_incorrecto.open = False
        self.pagina.update()

    def registrar_usuario(self, usuario, password, confirmar_password, codigo_seguridad):
        if not usuario or not password or not confirmar_password or not codigo_seguridad:
            self.pagina.dialog = self.dialogo_error
            self.dialogo_error.open = True
            self.pagina.update()
            return

        if codigo_seguridad != "5943":
            self.pagina.dialog = self.dialogo_codigo_incorrecto
            self.dialogo_codigo_incorrecto.open = True
            self.pagina.update()
            return

        try:
            if password != confirmar_password:
                self.pagina.dialog = self.dialogo_error
                self.dialogo_error.open = True
                self.pagina.update()
                return

            password_hash = hashlib.sha256(password.encode()).hexdigest()
            Usuario = Query()
            if not db.search(Usuario.usuario == usuario):
                db.insert({'usuario': usuario, 'password': password_hash})
                print("Usuario registrado exitosamente!")
                self.pagina.clean()
                # Aquí podrías redirigir a la página de login después del registro
            else:
                self.pagina.dialog = self.dialogo_usuario_existente
                self.dialogo_usuario_existente.open = True
                self.pagina.update()
        except Exception as e:
            print("Error:", e)

    def mostrar_pagina(self):
        self.pagina.clean()
        self.pagina.title = 'Registro'
        self.pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.pagina.theme_mode = ft.ThemeMode.DARK
        self.pagina.window_resizable = True

        img = ft.Image(
            src=f"https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        campo_usuario = TextField(label='Usuario', text_align=ft.TextAlign.LEFT, width=200)
        campo_password = TextField(label='password', text_align=ft.TextAlign.LEFT, width=200, password=True)
        campo_confirmar_password = TextField(label='Confirmar password', text_align=ft.TextAlign.LEFT, width=200, password=True)
        campo_codigo_seguridad = TextField(label='Código de Seguridad', text_align=ft.TextAlign.LEFT, width=200, password=True)
        boton_registro = ElevatedButton(text='Registrar', width=200)

        def on_registro_click(event):
            usuario = campo_usuario.value
            password = campo_password.value
            confirmar_password = campo_confirmar_password.value
            codigo_seguridad = campo_codigo_seguridad.value
            self.registrar_usuario(usuario, password, confirmar_password, codigo_seguridad)

        boton_registro.on_click = on_registro_click

        self.pagina.add(
            Row(controls=[Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            Row(controls=[Column([campo_usuario, campo_password, campo_confirmar_password, campo_codigo_seguridad, boton_registro])],
                alignment=ft.MainAxisAlignment.CENTER)
        )


class PaginaLogin:
    def __init__(self, pagina):
        self.pagina = pagina
        self.dialogo_error = AlertDialog(
            title=Text("Error"),
            content=Text("Nombre de usuario o password incorrectos"),
            actions=[TextButton("Ok", on_click=self.cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def cerrar_dialogo(self, event):
        self.dialogo_error.open = False
        self.pagina.update()

    def validar_login(self, usuario, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            Usuario = Query()
            resultado = db.get((Usuario.usuario == usuario) & (Usuario.password == password_hash))
            if resultado:
                print("¡Bienvenido,", usuario, "!")
                self.pagina.clean()
                # Aquí podrías redirigir a la página de dashboard después del inicio de sesión
            else:
                self.pagina.dialog = self.dialogo_error
                self.dialogo_error.open = True
                self.pagina.update()
        except Exception as e:
            print("Error:", e)

    def mostrar_pagina(self):
        self.pagina.clean()
        self.pagina.title = 'Login'
        self.pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.pagina.theme_mode = ft.ThemeMode.DARK
        self.pagina.window_resizable = True

        img = ft.Image(
            src=f"https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        campo_usuario = TextField(label='Usuario', text_align=ft.TextAlign.LEFT, width=200)
        campo_password = TextField(label='password', text_align=ft.TextAlign.LEFT, width=200, password=True)
        boton_login = ElevatedButton(text='Iniciar Sesión', width=200)

        def on_login_click(event):
            usuario = campo_usuario.value
            password = campo_password.value
            self.validar_login(usuario, password)

        boton_login.on_click = on_login_click

        self.pagina.add(
            Row(controls=[Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            Row(controls=[Column([campo_usuario, campo_password, boton_login])],
                alignment=ft.MainAxisAlignment.CENTER)
        )


class PaginaMenu:
    def __init__(self, pagina):
        self.pagina = pagina

    def mostrar_menu(self):
        self.pagina.clean()
        self.pagina.title = 'Menú'
        self.pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.pagina.theme_mode = ft.ThemeMode.DARK
        self.pagina.window_resizable = True


        img = ft.Image(
            src=f"https://raw.githubusercontent.com/DrBabaBoy/FaceScan/main/img/Animation.gif",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        boton_registro = ElevatedButton(text='Registrarse', width=200)
        boton_login = ElevatedButton(text='Iniciar Sesión', width=200)

        def on_registro_click(event):
            pagina_registro = PaginaRegistro(self.pagina)
            pagina_registro.mostrar_pagina()

        def on_login_click(event):
            pagina_login = PaginaLogin(self.pagina)
            pagina_login.mostrar_pagina()

        boton_registro.on_click = on_registro_click
        boton_login.on_click = on_login_click

        self.pagina.add(
            Row(controls=[Column([img])], alignment=ft.MainAxisAlignment.CENTER),
            Row(controls=[Column([boton_registro])], alignment=ft.MainAxisAlignment.CENTER),
            Row(controls=[Column([boton_login])], alignment=ft.MainAxisAlignment.CENTER)
        )


def main(pagina: ft.Page) -> None:
    pagina_menu = PaginaMenu(pagina)
    pagina_menu.mostrar_menu()


ft.app(target=main)