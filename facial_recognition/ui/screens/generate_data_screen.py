import flet as ft
from facial_recognition.database import Database, Tables
from facial_recognition.model.face_data import FaceData
from facial_recognition.ui.user_controls.face_capturer import FaceCapturer
from facial_recognition.ui.user_controls.face_data_item import FaceDataItem
from facial_recognition.ui.user_controls.name_text_field import NameTextField
from facial_recognition.util.document import to_face_data_list
from facial_recognition.util.file import (
    delete_face_directory,
    delete_model_file,
)

class GenerateDataScreen(ft.UserControl):
    text_ref = ft.Ref[ft.Text]()
    list_view_ref = ft.Ref[ft.ListView]()

    face_data_list: list[FaceData] = []
    face_capture_dialog: ft.AlertDialog

    def __init__(self) -> None:
        super().__init__()
        self.load_face_data()

    def load_face_data(self) -> None:
        with Database(Tables.FACE_DATA) as db:
            self.face_data_list = to_face_data_list(db.all())

    def on_capture_click(self, face_data: FaceData, is_recapture: bool = False) -> None:
        def close_dialog(_event: ft.ControlEvent) -> None:
            face_capturer.stop_capture()
            self.face_capture_dialog.open = False
            self.page.update()

        face_capturer = FaceCapturer(
            face_data=face_data,
            on_capture_complete=lambda: self.on_capture_complete(face_data, is_recapture),
        )
        self.face_capture_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Capturando rostro..."),
            content=face_capturer,
            actions=[
                ft.TextButton(text="Detener", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.face_capture_dialog
        self.face_capture_dialog.open = True
        self.page.update()

    def on_capture_complete(self, face_data: FaceData, is_recapture: bool = False) -> None:
        if not is_recapture:
            with Database(Tables.FACE_DATA) as db:
                doc_id = db.insert(face_data.model_dump())
                face_data.doc_id = doc_id
                self.face_data_list.append(
                    face_data
                )
            self.update_face_dada_list()

        self.face_capture_dialog.open = False
        self.page.update()

    def on_delete_click(self, face_data: FaceData) -> None:
        with Database(Tables.FACE_DATA) as db:
            db.remove(doc_ids=[face_data.doc_id])

        self.face_data_list.remove(face_data)
        if len(self.face_data_list) == 0:
            delete_model_file()
        delete_face_directory(face_data.data_path)

        self.update_face_dada_list()

    def on_edit_click(self, face_data: FaceData) -> None:
        def save_changes(_event: ft.ControlEvent) -> None:
            face_data.name = name_field.value
            face_data.surname = surname_field.value

            if face_data.acss == "Alumno":
                face_data.user_id = user_id_field.value
            elif face_data.acss == "Trabajador":
                face_data.worker_number = worker_number_field.value

            with Database(Tables.FACE_DATA) as db:
                db.update(face_data.model_dump(), doc_ids=[face_data.doc_id])

            self.update_face_dada_list()
            self.edit_dialog.open = False
            self.page.update()

        def close_dialog(_event: ft.ControlEvent) -> None:
            self.edit_dialog.open = False
            self.page.update()

        name_field = ft.TextField(label="Nombre", value=face_data.name)
        surname_field = ft.TextField(label="Apellido", value=face_data.surname)
        acss_field = ft.Dropdown(
            label="Tipo de acceso",
            value=face_data.acss,
            options=[
                ft.dropdown.Option("Alumno"),
                ft.dropdown.Option("Trabajador"),
                ft.dropdown.Option("Invitado"),
            ],
            disabled=True  # Deshabilitamos la edición del tipo de acceso
        )

        if face_data.acss == "Alumno":
            user_id_field = ft.TextField(label="Matrícula", value=face_data.user_id, max_length=8)
            content = [name_field, surname_field, acss_field, user_id_field]
        elif face_data.acss == "Trabajador":
            worker_number_field = ft.TextField(label="Número de Trabajador", value=face_data.worker_number, max_length=8)
            content = [name_field, surname_field, acss_field, worker_number_field]
        else:  # Invitado
            content = [name_field, surname_field, acss_field]

        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar datos de la persona"),
            content=ft.Column(content),
            actions=[
                ft.TextButton(text="Guardar", on_click=save_changes),
                ft.TextButton(text="Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.edit_dialog
        self.edit_dialog.open = True
        self.page.update()

    def update_face_dada_list(self):
        self.text_ref.current.value = f"Número de rostros cargados: {len(self.face_data_list)}"
        self.list_view_ref.current.controls = [
            FaceDataItem(
                face_data=face_data,
                on_delete_click=self.on_delete_click,
                on_recapture_click=lambda f: self.on_capture_click(f, True),
                on_edit_click=self.on_edit_click  # Añadir esto
            ) for face_data in self.face_data_list
        ]
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    NameTextField(on_capture_click=self.on_capture_click),
                    ft.Text(
                        ref=self.text_ref,
                        value=f"Número de rostros cargados: {len(self.face_data_list)}",
                        theme_style=ft.TextThemeStyle.HEADLINE_LARGE
                    ),
                    ft.ListView(
                        ref=self.list_view_ref,
                        expand=True,
                        controls=[
                            FaceDataItem(
                                face_data=face_data,
                                on_delete_click=self.on_delete_click,
                                on_recapture_click=lambda f: self.on_capture_click(f, True),
                                on_edit_click=self.on_edit_click  # Añadir esto
                            ) for face_data in self.face_data_list
                        ],
                    )
                ]
            ),
            padding=ft.padding.only(top=20)
        )
