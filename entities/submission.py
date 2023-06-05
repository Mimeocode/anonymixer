from typing import List
import os
import shutil
import uuid

class Submission:

    def __init__(self,
                 name: str,
                 file_type: str,
                 uid: str = None,
                 file_count: int = 0,
                 status: str = "In Progess",
                 file_names: List[str] = [],
                 hashed_file_names: List[str] = []
                 ):
        self.uid = uuid.uuid4().hex if uid is None else uid

        self.name = name
        self.file_type = file_type

        self.file_count = file_count
        self.status = status
        self.file_names = file_names
        self.hashed_file_names = hashed_file_names

    def anonymize_submissions(self, path: str, seperator: str = None, snippet_index: int = None):
        os.makedirs(hashed_path := f"{path}_hashed")
        file_tree: list  # TODO: make file tree from path

        def _splitter(string: str):
            cond = (seperator is not None) and (snippet_index is not None)
            return_string = string.split("/")[-1]
            if cond:
                return return_string.split(seperator)[snippet_index]
            return return_string

        for file in file_tree:
            file_name = _splitter(file)
            hashed_file_name = str(abs(hash(file_name)))
            self.file_names.append(file_name)
            self.hashed_file_names.append(hashed_file_name)
            shutil.copy(file, f"{hashed_path}/{hashed_file_name}.{self.file_type}")

            self.__iter__()

    def unanonymize_report(self, report):
        self.status = "Finnished"

    def __iter__(self):
        self.file_count += 1