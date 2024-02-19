import flet as ft


def main(page: ft.Page):
    page.title = "My first Flet GUI"
    page.add(ft.Text("Welcome!"))
    pass


ft.app(target=main)
