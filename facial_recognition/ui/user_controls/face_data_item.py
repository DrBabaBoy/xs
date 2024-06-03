from typing import Callable
import flet as ft
from humanize import naturaltime
from facial_recognition.model.face_data import FaceData

type OnDeleteClick = Callable[[FaceData], None]
type OnRecaptureClick = Callable[[FaceData], None]
type OnEditClick = Callable[[FaceData], None]

class FaceDataItem(ft.UserControl):
    on_delete_click: OnDeleteClick
    on_recapture_click: OnRecaptureClick
    on_edit_click: OnEditClick

    face_data: FaceData

    def __init__(self, face_data: FaceData, on_delete_click: OnDeleteClick,
                 on_recapture_click: OnRecaptureClick, on_edit_click: OnEditClick) -> None:  # Añadir on_edit_click aquí
        super().__init__()
        self.face_data = face_data
        self.on_delete_click = on_delete_click
        self.on_recapture_click = on_recapture_click
        self.on_edit_click = on_edit_click

    def build(self) -> ft.Card:
        return ft.Card(
            ft.ListTile(
                title=ft.Text(f"{self.face_data.name} {self.face_data.surname}"),
                subtitle=ft.Text(f"Tipo de acceso: {self.face_data.acss}, creado: {naturaltime(self.face_data.created_at)}"),
                trailing=ft.PopupMenuButton(
                    icon=ft.icons.MORE_VERT,
                    items=[
                        ft.PopupMenuItem(
                            icon=ft.icons.CLOSE,
                            text="Eliminar rostro",
                            on_click=lambda _: self.on_delete_click(self.face_data),
                        ),
                        ft.PopupMenuItem(
                            icon=ft.icons.REFRESH,
                            text="Recapturar rostro",
                            on_click=lambda _: self.on_recapture_click(self.face_data),
                        ),
                        ft.PopupMenuItem(
                            icon=ft.icons.EDIT,
                            text="Editar datos",
                            on_click=lambda _: self.on_edit_click(self.face_data),
                        )
                    ]
                )
            )
        )
