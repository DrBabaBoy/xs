import flet as ft
import facial_recognition.util.file as file_util
import facial_recognition.util.document as document_util
import facial_recognition.model.face_data as face_data_model
import facial_recognition.database as database
from facial_recognition.ui.user_controls.face_data_item import FaceDataItem
from facial_recognition.model.face_data import FaceData


class CheckPersonsScreen(ft.UserControl):
    text_ref = ft.Ref[ft.Text]()
    list_view_ref = ft.Ref[ft.ListView]()

    face_data_list: list[FaceData] = []

    def update_face_data_list(self):
        self.text_ref.current.value = f"Lista de personas encontradas: {len(self.face_data_list)}"
        face_data_items = [
            FaceDataItem(face_data=face_data)
            for face_data in self.face_data_list
        ]
        self.list_view_ref.current.controls = face_data_items
        self.update()

    def build(self) -> ft.Container:
        self.load_face_data()
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        ref=self.text_ref,
                        value=f"Lista de personas encontradas: {len(self.face_data_list)}",
                        theme_style=ft.TextThemeStyle.HEADLINE_LARGE
                    ),
                    ft.ListView(
                        ref=self.list_view_ref,
                        expand=True
                    )
                ]
            ),
            padding=ft.padding.only(top=20)
        )

    def load_face_data(self) -> None:
        with database.Database(database.Tables.FACE_DATA) as db:
            self.face_data_list = document_util.to_face_data_list(db.all())
