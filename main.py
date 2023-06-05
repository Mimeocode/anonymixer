import flet as ft

from pages import Pages

MIMEO = "#47009e"

def main(page: ft.Page):
    page.title = "MimeoCode - Anonymixer"
    page.window_frameless = True
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.END


    def route_change(route):
        troute = ft.TemplateRoute(page.route)
        page.views.clear()
        page.views.append(
            Pages.get_home_page(page)
        )
        if page.route == "/submission":
            page.views.append(
                Pages.get_submission_page(page)
            )
        if troute.match("/submission/:submission_uid"):
            page.views.append(
                Pages.get_submission_page(page, troute.submission_uid)
            )

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
