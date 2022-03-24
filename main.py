from runpy import run_path

from notion.client import NotionClient

if __name__ == "__main__":
    # token.py
    # config = {"token": ""}
    token = run_path("token.py")["config"]["token"]
