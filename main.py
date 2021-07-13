import asyncio
import logging

from components.archive import create_projects_archive
from components.project import list_all_projects, fetch_projects_data

logging.basicConfig(
    level=logging.DEBUG
)

async def main():
    projects = list_all_projects("project.yml")
    projects_data = await fetch_projects_data(projects)
    create_projects_archive(projects_data, "project")


asyncio.run(main())
