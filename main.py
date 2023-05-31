import flet as ft
from entities import Submission, SubmissionTable

MIMEO = "#6700ba"


def st(string: str | float | int = ""):
    return ft.Text(string, color=ft.colors.BLACK87)


def main(page: ft.Page):
    page.title = "MimeoCode - Anonymixer"
    page.window_frameless = True
    page.bgcolor = ft.colors.WHITE

    page.appbar = ft.AppBar(leading=ft.Image("assets/images/mc-logo.png"),
                            title=ft.Text("MimeoCode - Anonymixer"),
                            actions=[ft.Container(content=ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close()),
                                                  padding=10
                                                  )],
                            bgcolor=MIMEO,
                            )
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.END

    sub_table = SubmissionTable()
    if page.client_storage.contains_key("submission_table"):
        sub_table = page.client_storage.get("submission_table")

    def _close_popup(e):
        popup_modal.open = False
        page.update()

    popup_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Select Files"),
        content=ft.Column(
            [
                ft.Text("Select the submissions to anonymize. zip files are supported."),
            ],
            alignment=ft.MainAxisAlignment.START, ),
        actions=[
            ft.TextButton("Yes", on_click=_close_popup),
            ft.TextButton("No", on_click=_close_popup),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def _add_submission(e):
        page.dialog = popup_modal
        popup_modal.open = True
        page.update()

    def _gen_table():
        rows = []
        if sub_table.is_empty():
            rows = [ft.DataRow(cells=[ft.DataCell(st("There is no Submission yet!")),
                                      ft.DataCell(st("Press the Button in the right corner to add a Submission")),
                                      ft.DataCell(st("no filetype")),
                                      ft.DataCell(st(420)),
                                      ft.DataCell(ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.GREY)),
                                      ft.DataCell(ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.GREY))])]
        else:
            for submission in sub_table.get_submission():
                rows.append(ft.DataRow(cells=[ft.DataCell(st(submission.name)),
                                              ft.DataCell(st(submission.status)),
                                              ft.DataCell(st(submission.file_type)),
                                              ft.DataCell(st(submission.file_count)),
                                              ft.DataCell(ft.IconButton(ft.icons.EDIT, icon_color=MIMEO)),
                                              ft.DataCell(ft.IconButton(ft.icons.DELETE, icon_color=MIMEO))]))
                # TODO: add button functionality

        table = ft.Row([
            ft.Divider(height=50),
            ft.DataTable(columns=[ft.DataColumn(st("Submission")),
                                  ft.DataColumn(st("Status")),
                                  ft.DataColumn(st("File Type")),
                                  ft.DataColumn(st("Number of Files")),
                                  ft.DataColumn(st("Edit")), ft.DataColumn(st("Delete"))],
                         rows=rows,
                         width="60%")],
            alignment=ft.MainAxisAlignment.CENTER)
        return table

    # Toolbar for adding new submissions
    page.add(
        ft.Row([ft.IconButton(ft.icons.ADD,
                              on_click=_add_submission,
                              icon_size=40,
                              tooltip="Add new submission to anonymize",
                              icon_color=MIMEO), ],
               alignment=ft.MainAxisAlignment.END,
               )
    )

    # submission table
    page.add(
        _gen_table()
    )


ft.app(target=main)
