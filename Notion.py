from notion_client import Client
import os
import json
import pprint
from dataclasses import dataclass

URL = "14992f0abee4807aafe0cb4bb725c087"
token = open("token.txt").read()
client = Client(auth=token)


@dataclass
class NotionData:
    Text: str = ""
    Client: str = ""
    Deadline: str = ""


def read_notion_database(database_id):
    response = client.databases.query(
        **{
            "database_id": database_id,
            "filter": {"property": "タグ", "select": {"equals": "今日やる"}},
        }
    )
    return response


def get_task() -> list[NotionData]:
    ans: list[NotionData] = []
    result = read_notion_database(URL)
    for r in result["results"]:
        NData = NotionData()
        #
        NData.Text = r["properties"]["名前"]["title"][0]["plain_text"]
        # print(NData.Text)
        if r["properties"]["期日"]["date"] != None:
            NData.Deadline = r["properties"]["期日"]["date"]
        if r["properties"]["依頼者"]["select"] != None:
            NData.Client = r["properties"]["依頼者"]["select"]["name"]
        ans.append(NData)
    return ans


if __name__ == "__main__":
    pass
    # result=read_notion_database(URL)
    # pprint.pprint(result['results'][0]['properties']['名前']['title'][0]['plain_text'])
