from typing import Callable
import pdflatex
import subprocess
import glob
import zipfile
import os
import shutil
import uuid

class Submission:

    def __init__(self,
                 name: str = "",
                 file_type: str = "",
                 uid: str = None,
                 file_count: int = 0,
                 status: str = "In Progess",
                 hash_table: dir = {},
                 ):
        self.uid = uuid.uuid4().hex if uid is None else uid

        self.name = name
        self.file_type = file_type

        self.file_count = file_count
        self.status = status
        self.hash_table = hash_table

    def anonymize_submissions(self, path: str, snippet_index: Callable = None, seperator: str = None):
        if ".zip" in path:
            n_dir = path.split(".zip")[0]
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(n_dir)
        else:
            n_dir = path
        os.makedirs(hashed_path := f"{n_dir}_hashed")
        file_tree: list = glob.glob(f"{n_dir}/**/*.{self.file_type}", recursive=True)

        def _splitter(string: str):
            cond = (seperator is not None) and (snippet_index is not None)
            return_string = string.split("\\")[-1].split(f".{self.file_type}")[0]
            if cond:
                return snippet_index(return_string.split(seperator))
            return return_string

        for file in file_tree:
            file_name = _splitter(file)
            hashed_file_name = str(abs(hash(file_name)))
            self.hash_table[file_name] = hashed_file_name
            shutil.copy(file, f"{hashed_path}/{hashed_file_name}.{self.file_type}")
            self.__iter__()
        shutil.make_archive(hashed_path, "zip", hashed_path)
        shutil.rmtree(hashed_path)
        shutil.rmtree(n_dir)
        self.status = "Anonymized - Waiting for Results"

    def unanonymize_report(self, report_path: str):
        # TODO: make this work
        dirname, _ = os.path.split(report_path)
        with open(report_path, "r") as f:
            tex = f.read()
            for key, h in self.hash_table.items():
                tex.replace(h, key)
            subprocess.check_call(['pdflatex', report_path])
        self.status = "Finnished"


    def __iter__(self):
        self.file_count += 1