import logging
import os
import shutil
import tempfile
import zipfile
from typing import IO
from components.project import Projects


class ZipSource:
    source_bytes: bytes
    temp_file: IO
    zip_file: zipfile.ZipFile

    def __init__(self, source: bytes):
        self.source_bytes = source

    def __enter__(self):
        self.temp_file = tempfile.TemporaryFile("wb+")
        self.temp_file.write(self.source_bytes)
        self.zip_file = zipfile.ZipFile(self.temp_file)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.zip_file.close()
        self.temp_file.close()

    def extract(self, path: str, subdir_name: str) -> None:
        """
        Extract the zip file to a folder.

        :param path: the folder to extract to
        :param subdir_name: where to extract in the path?
        :return: the folder path
        """
        self.zip_file.extractall(os.path.join(path, subdir_name))
        pass


def create_projects_archive(projects: Projects, filename: str):
    with tempfile.TemporaryDirectory() as workdir:
        for project in projects:
            name = project.get("name")
            data = project.get("data")

            if name and data:
                with ZipSource(data) as source_zip:
                    source_zip.extract(workdir, name)
            else:
                logging.error("you should run create_projects_archive() first!")

        shutil.make_archive(filename, "zip", workdir)
