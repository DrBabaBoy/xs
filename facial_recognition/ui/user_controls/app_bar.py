import flet as ft


def custom_app_bar() -> ft.AppBar:
    return ft.AppBar(
        title=ft.Text("FaceScan"),
        leading=ft.Icon(ft.icons.FACE),
    )
