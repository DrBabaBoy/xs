from typing import Callable

import flet as ft
from pydantic import ValidationError

from facial_recognition.model.face_data import FaceData

OnCaptureClick = Callable[[FaceData], None]

class NameTextField(ft.UserControl):
    text_field_ref = ft.Ref[ft.TextField]()
    surname_field_ref = ft.Ref[ft.TextField]()
    user_id_field_ref = ft.Ref[ft.TextField]()
    career_field_ref = ft.Ref[ft.Dropdown]()
    access_type_field_ref = ft.Ref[ft.Dropdown]()
    worker_number_field_ref = ft.Ref[ft.TextField]()

    on_capture_click: OnCaptureClick

    def __init__(self, on_capture_click: OnCaptureClick) -> None:
        super().__init__()
        self.on_capture_click = on_capture_click

    def on_click(self, event: ft.ControlEvent) -> None:
        name = self.text_field_ref.current.value
        surname = self.surname_field_ref.current.value
        user_id = self.user_id_field_ref.current.value if not self.user_id_field_ref.current.disabled else None
        career_user = self.career_field_ref.current.value if not self.career_field_ref.current.disabled else None
        worker_number = self.worker_number_field_ref.current.value if not self.worker_number_field_ref.current.disabled else None
        tipo = self.access_type_field_ref.current.value

        try:
            face_data = FaceData(name=name, surname=surname, user_id=user_id, career=career_user, worker_number=worker_number, acss=tipo)
            self.clear_text_field()
            self.on_capture_click(face_data)
            
            self.user_id_field_ref.current.disabled = True
            self.career_field_ref.current.disabled = True
            self.worker_number_field_ref.current.disabled = True
            self.user_id_field_ref.current.update()
            self.career_field_ref.current.update()
            self.worker_number_field_ref.current.update()
        except ValidationError as e:
            for error in e.errors():
                if error['loc'][0] == 'name':
                    self.text_field_ref.current.helper_text = "El nombre es requerido"
                elif error['loc'][0] == 'surname':
                    self.surname_field_ref.current.helper_text = "El apellido es requerido"
                elif error['loc'][0] == 'user_id':
                    self.user_id_field_ref.current.helper_text = "La matrícula es requerida"
                elif error['loc'][0] == 'career':
                    self.career_field_ref.current.helper_text = "La carrera es requerida"
                elif error['loc'][0] == 'worker_number':
                    self.worker_number_field_ref.current.helper_text = "El número de trabajador es requerido"
                elif error['loc'][0] == 'acss':
                    self.access_type_field_ref.current.helper_text = "El tipo de acceso es requerido"
            self.text_field_ref.current.update()
            self.surname_field_ref.current.update()
            self.user_id_field_ref.current.update()
            self.career_field_ref.current.update()
            self.worker_number_field_ref.current.update()
            self.access_type_field_ref.current.update()

    def clear_text_field(self) -> None:
        self.text_field_ref.current.value = ""
        self.text_field_ref.current.helper_text = ""
        self.text_field_ref.current.update()
        self.surname_field_ref.current.value = ""
        self.surname_field_ref.current.helper_text = ""
        self.surname_field_ref.current.update()
        self.user_id_field_ref.current.value = ""
        self.user_id_field_ref.current.helper_text = ""
        self.user_id_field_ref.current.update()
        self.career_field_ref.current.value = ""
        self.career_field_ref.current.helper_text = ""
        self.career_field_ref.current.update()
        self.worker_number_field_ref.current.value = ""
        self.worker_number_field_ref.current.helper_text = ""
        self.worker_number_field_ref.current.update()
        self.access_type_field_ref.current.value = ""
        self.access_type_field_ref.current.helper_text = ""
        self.access_type_field_ref.current.update()

        self.text_field_ref.current.focus()

    def on_access_type_change(self, event: ft.ControlEvent) -> None:
        access_type = self.access_type_field_ref.current.value
        if access_type == "Alumno":
            self.career_field_ref.current.disabled = False
            self.user_id_field_ref.current.disabled = False
            self.worker_number_field_ref.current.disabled = True
        elif access_type == "Trabajador":
            self.career_field_ref.current.disabled = True
            self.user_id_field_ref.current.disabled = True
            self.worker_number_field_ref.current.disabled = False
        else:
            self.career_field_ref.current.disabled = True
            self.user_id_field_ref.current.disabled = True
            self.worker_number_field_ref.current.disabled = True

        self.career_field_ref.current.update()
        self.user_id_field_ref.current.update()
        self.worker_number_field_ref.current.update()

    def build(self) -> ft.Column:
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.TextField(
                            label="Nombre",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            ref=self.text_field_ref,
                        ),
                        ft.TextField(
                            label="Apellido",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            ref=self.surname_field_ref,
                        ),
                        ft.Dropdown(
                            label="Tipo Acceso",
                            expand=False,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            ref=self.access_type_field_ref,
                            hint_text="Elige una opción",
                            options=[
                                ft.dropdown.Option("Alumno"),
                                ft.dropdown.Option("Trabajador"),
                                ft.dropdown.Option("Invitado"),
                            ],
                            on_change=self.on_access_type_change,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.TextField(
                            label="Matrícula",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            ref=self.user_id_field_ref,
                            disabled=True,
                            max_length=8,
                        ),
                        ft.TextField(
                            label="Número de Trabajador",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            ref=self.worker_number_field_ref,
                            disabled=True,
                            max_length=8,
                        ),
                        ft.Dropdown(
                            label="Carrera",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            disabled=True,
                            ref=self.career_field_ref,
                            hint_text="Elige una opción",
                            options=[
                                ft.dropdown.Option("Informática"),
                                ft.dropdown.Option("Animación Digital"),
                                ft.dropdown.Option("Química"),
                                ft.dropdown.Option("Industrial"),
                                ft.dropdown.Option("Electrónica"),
                                ft.dropdown.Option("Mecánica"),
                                ft.dropdown.Option("Semiconductores"),
                                ft.dropdown.Option("Bioquímica"),
                                ft.dropdown.Option("Sistemas Computacionales"),
                                ft.dropdown.Option("Petrolera"),
                                ft.dropdown.Option("Gestión Empresarial"),
                                ft.dropdown.Option("Ferroviaria"),
                            ],
                        ),
                        ft.OutlinedButton(
                            text="Capturar",
                            on_click=self.on_click
                        ),
                    ]
                ),
            ]
        )
