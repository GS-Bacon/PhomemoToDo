from notion_client import Client
import os
import json
import pprint
from dataclasses import dataclass
from datetime import datetime as dt

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
            "sorts": [{"property": "期日", "direction": "ascending"}],
            "sorts": [{"property": "依頼者", "direction": "ascending"}],
        }
    )
    return response


def get_task(tag:str) -> list[NotionData]:
    ans: list[NotionData] = []
    result = response = client.databases.query(
        **{
            "database_id": URL,
            "filter": {"property": "タグ", "select": {"equals": tag}},
            "sorts": [{"property": "期日", "direction": "ascending"}],
            "sorts": [{"property": "依頼者", "direction": "ascending"}],
        }
    )
    for r in result["results"]:
        NData = NotionData()
        #
        NData.Text = r["properties"]["名前"]["title"][0]["plain_text"]
        # print(NData.Text)
        if r["properties"]["期日"]["date"] != None:
            #print("date"+str(r["properties"]["期日"]["date"]["start"]))
            d=dt.strptime(str(r["properties"]["期日"]["date"]["start"]),'%Y-%m-%d')
            NData.Deadline =d.strftime('%#m/%#d')
        if r["properties"]["依頼者"]["select"] != None:
            NData.Client = r["properties"]["依頼者"]["select"]["name"]
        ans.append(NData)
    return ans


if __name__ == "__main__":
    # pass
    result = read_notion_database(URL)
    pprint.pprint(result["results"])
    # pprint.pprint(result['results'][0]['properties']['名前']['title'][0]['plain_text'])
