from typing import Callable

import flet as ft
from pydantic import ValidationError

from facial_recognition.model.face_data import FaceData

type OnCaptureClick = Callable[[FaceData], None]


class NameTextField(ft.UserControl):
    text_field_ref = ft.Ref[ft.TextField]()
    surname_field_ref = ft.Ref[ft.TextField]()
    user_id_field_ref = ft.Ref[ft.TextField]()
    career_field_ref = ft.Ref[ft.TextField]()
    access_type_field_ref = ft.Ref[ft.TextField]()

    on_capture_click: OnCaptureClick

    def __init__(self, on_capture_click: OnCaptureClick) -> None:
        super().__init__()
        self.on_capture_click = on_capture_click

    def on_click(self, event: ft.ControlEvent) -> None:
        name = self.text_field_ref.current.value
        surname = self.surname_field_ref.current.value
        user_id = self.user_id_field_ref.current.value if not self.user_id_field_ref.current.disabled else None
        career_user = self.career_field_ref.current.value if not self.career_field_ref.current.disabled else None
        type = self.access_type_field_ref.current.value

        try:
            face_data = FaceData(name=name, surname=surname, user_id=user_id, career=career_user, acss=type)
            self.clear_text_field()
            self.on_capture_click(face_data)
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
                elif error['loc'][0] == 'acss':
                    self.access_type_field_ref.current.helper_text = "El tipo de acceso es requerido"
            self.text_field_ref.current.update()
            self.surname_field_ref.current.update()
            self.user_id_field_ref.current.update()
            self.career_field_ref.current.update()
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
        self.access_type_field_ref.current.value = ""
        self.access_type_field_ref.current.helper_text = ""
        self.access_type_field_ref.current.update()

    def on_access_type_change(self, event: ft.ControlEvent) -> None:
        if self.access_type_field_ref.current.value == "Alumno":
            self.career_field_ref.current.disabled = False
            self.user_id_field_ref.current.disabled = False
        else:
            self.career_field_ref.current.disabled = True
            self.user_id_field_ref.current.disabled = True

        self.career_field_ref.current.update()
        self.user_id_field_ref.current.update()

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
                            hint_text="Elige una opcion",
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
                            label="Matricula",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            ref=self.user_id_field_ref,
                            disabled=True,
                        ),
                        ft.Dropdown(
                            label="Carrera",
                            expand=True,
                            border=ft.InputBorder.OUTLINE,
                            filled=True,
                            disabled=True,
                            ref=self.career_field_ref,
                            hint_text="Elige una opcion",
                            options=[
                                ft.dropdown.Option("Informatica"),
                                ft.dropdown.Option("Animacion Digital"),
                                ft.dropdown.Option("Quimica"),
                                ft.dropdown.Option("Industrial"),
                                ft.dropdown.Option("Electronica"),
                                ft.dropdown.Option("Mecanica"),
                                ft.dropdown.Option("Semiconductores"),
                                ft.dropdown.Option("Bioquimica"),
                                ft.dropdown.Option("Sistemas Computacionales"),
                                ft.dropdown.Option("Petrolera"),
                                ft.dropdown.Option("Gestion Empresarial"),
                                ft.dropdown.Option("Ferroviaria"),
                            ],
                        ),
                        ft.OutlinedButton(
                            text="Capture",
                            on_click=self.on_click
                        ),
                    ]
                ),
            ]
        )
