from typing import List

import flet as ft
from entities import Submission, SubmissionTable

MIMEO = "#47009e"


def st(string: str | float | int = ""):
    return ft.Text(string, color=ft.colors.BLACK87)


class Pages:
    @staticmethod
    def _get_table_data(page: ft.Page) -> SubmissionTable:
        data = page.client_storage.get("table")
        table = SubmissionTable(data)
        table.deserialize_submissions()
        return table

    @staticmethod
    def _set_table_data(page: ft.Page, sub_table: SubmissionTable):
        page.client_storage.set("table", sub_table)

    @staticmethod
    def _gen_table(sub_table: SubmissionTable, _del_submission, _edit_submission):
        rows = []
        if sub_table.is_empty():
            rows = [ft.DataRow(cells=[ft.DataCell(st("There is no Submission yet!")),
                                      ft.DataCell(st("Press the Button in the right corner to add a Submission")),
                                      ft.DataCell(st("no filetype")),
                                      ft.DataCell(st(420)),
                                      ft.DataCell(ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.GREY)),
                                      ft.DataCell(ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.GREY))])]
        else:
            for submission in sub_table.get_submissions():
                rows.append(ft.DataRow(cells=[ft.DataCell(st(submission.name)),
                                              ft.DataCell(st(submission.status)),
                                              ft.DataCell(st(submission.file_type)),
                                              ft.DataCell(st(submission.file_count)),
                                              ft.DataCell(ft.IconButton(ft.icons.EDIT, icon_color=MIMEO, on_click=lambda _: _edit_submission(submission))),
                                              ft.DataCell(ft.IconButton(ft.icons.DELETE, icon_color=MIMEO, on_click=lambda _: _del_submission(submission)))]))
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

    @staticmethod
    def _get_default_bar(page):
        db = ft.AppBar(leading=ft.Image("assets/images/mc-logo.png"),
                       title=ft.Text("MimeoCode - Anonymixer"),
                       actions=[ft.Container(
                           content=ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close()),
                           padding=10)],
                       bgcolor=MIMEO)
        return db

    @classmethod
    def get_home_page(cls, page: ft.Page):
        def _del_submission(submission):
            sub_table.remove_submission(submission)
            cls._set_table_data(page, sub_table)
            page_container[2] = cls._gen_table(sub_table, _del_submission, _edit_submission)
            page.update()

        def _edit_submission(submission):
            page.go(f"/submission/{submission.uid}")

        if page.client_storage.contains_key("table"):
            sub_table = cls._get_table_data(page)
        else:
            sub_table = SubmissionTable()
        view = ft.View(
            "/",
            page_container := [
                cls._get_default_bar(page),
                ft.Row([ft.IconButton(ft.icons.ADD,
                                      on_click=lambda _: page.go("/submission"),
                                      icon_size=40,
                                      tooltip="Add new submission to anonymize",
                                      icon_color=MIMEO), ],
                       alignment=ft.MainAxisAlignment.END, ),
                cls._gen_table(sub_table, _del_submission, _edit_submission)
            ],
            bgcolor=ft.colors.WHITE
        )
        return view

    @classmethod
    def get_submission_page(cls, page: ft.Page, submission_uid: str = None):

        def _title_change(e):
            title_field.value = e.control.value
            page.update()

        def _save_submission(e):
            sub_table = cls._get_table_data(page)
            if submission_uid is None:
                new_sub = Submission(sub_name.value, file_type.value)
            else:
                _, new_sub = sub_table.get_submission(submission_uid)
                new_sub.name = sub_name.value
            sub_table.update_submissions(new_sub)
            cls._set_table_data(page, sub_table)

        def _return_to_mainpage(e):
            _save_submission(e)
            page.go("/")

        no_sub = True
        routing = "/submission"
        if submission_uid is not None:
            routing = f"/submission/{submission_uid}"
            no_sub = False
            sub_tab = cls._get_table_data(page)
            _, submission = sub_tab.get_submission(submission_uid)

        view = ft.View(
            routing,
            [
                cls._get_default_bar(page),
                ft.Row([ft.IconButton(ft.icons.ARROW_BACK,
                                      on_click=_return_to_mainpage,
                                      icon_size=40,
                                      tooltip="Save and Return to Mainpage",
                                      icon_color=MIMEO),
                        title_field := ft.Text(color=ft.colors.BLACK87, size=25, text_align=ft.TextAlign.CENTER)],
                       alignment=ft.MainAxisAlignment.START, ),
                ft.Container(padding=20,
                             content=ft.Row([sub_name := ft.TextField(label="Submission Name",
                                                                      on_change=_title_change,
                                                                      color=ft.colors.BLACK87,
                                                                      value="" if no_sub else submission.name
                                                                      ),
                                             file_type := ft.TextField(label="File Type",
                                                                       tooltip="Example: py, ipynb, cpp, js",
                                                                       color=ft.colors.BLACK87,
                                                                       value="" if no_sub else submission.file_type,
                                                                       disabled=not no_sub,
                                                                       ),
                                             ]

                                            )),
                #ft.Row([ft.Container(padding=20, content=ft.TextButton("Save", on_click=_save_submission))],
                #      alignment=ft.MainAxisAlignment.END)
            ],
            bgcolor=ft.colors.WHITE
        )
        return view
