import os
import pickle
from collections import namedtuple
from runpy import run_path
from typing import Set

from pyarxiv import query

from notion.client import NotionClient

Paper = namedtuple("Paper", ["title", "time", "url"])
TEST_URL = "https://www.notion.so/Test-2280881536fa4feea6ee071eab9a5031"


def get_papers(keyword: str) -> Set[Paper]:
    """Get papers uploaded on arxiv."""
    entries = query(title=keyword)
    papers = {
        Paper(title=entry["title"], time=entry["published"], url=entry["id"])
        for entry in entries
    }
    return papers


def update_notion_page(papers: Set[Paper]) -> None:
    """Update notion page."""
    # check already recorded data
    recorded = "already_recorded.pickle"

    # load data
    logged_papers = papers
    if os.path.exists(recorded):
        with open(recorded, "rb") as fr:
            prev = set(pickle.load(fr))

            logged_papers = papers | prev
            papers = papers - prev

    # save data
    with open(recorded, "wb") as fw:
        pickle.dump(logged_papers, fw)

    # get token and url
    config = run_path("token_v2.py")["config"]
    client = NotionClient(token_v2=config["token"])
    database = client.get_collection_view(config["database_url"])

    # update notion page
    for idx, paper in enumerate(list(papers)):
        print(f"({idx + 1}/{len(papers)}) <<{paper.title}>> is uploaded...")

        row = database.collection.add_row()
        row.set_property("Title", paper.title)
        row.set_property("Updated Time", paper.time)
        row.set_property("Link", paper.url)


if __name__ == "__main__":
    keyword = "Reinforcement Learning"
    papers = get_papers(keyword)

    # update
    update_notion_page(papers)
