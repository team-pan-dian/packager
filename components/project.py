import asyncio
import logging
from typing import TypedDict, List, Optional
import yaml
from yaml import BaseLoader

from components.http import get_file


class Project(TypedDict):
    name: str
    url: Optional[str]
    data: Optional[bytes]


Projects = List[Project]


def list_all_projects(filename: str) -> Projects:
    projects: Projects = []

    with open(filename, "r") as raw_pkg_file:
        logging.debug(f"opened {filename}")
        raw_pkg_data = raw_pkg_file.read()
        raw_pkg = yaml.load(raw_pkg_data, BaseLoader)

        for key in raw_pkg.keys():
            package: Project = raw_pkg[key]
            url = package.get("url")
            data = package.get("data")

            projects.append(Project(
                name=key,
                url=url,
                data=data
            ))

    return projects


async def fetch_projects_data(projects: Projects) -> Projects:
    async def _fetch_project_data(project: Project) -> None:
        if not project.get("data"):
            url = project.get("url")

            if url:
                project["data"] = await get_file(url)
            else:
                raise Exception("url should not be None")

    new_projects = projects.copy()
    await asyncio.wait([_fetch_project_data(proj) for proj in new_projects])
    return new_projects
