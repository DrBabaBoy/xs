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


class CheckPersonsScreen(ft.UserControl):

    def build(self) -> ft.Control:
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("ID Control"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("21080815")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("21080816")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("21080817")),
                    ],
                ),
            ],
        )

def app(page: ft.Page) -> None:
    check_persons_screen = CheckPersonsScreen()
    page.add(ft.Tabs(
        tabs=[
            ft.Tab(
                text="Check Persons",
                content=check_persons_screen.build(),
            ),
        ],
        selected_index=0,
        expand=True,
    ))