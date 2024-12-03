import Notion
import asyncio
import Pomemo
import datetime
import time


def main():
    client_name=""
    dt = datetime.datetime.today()
    textList: list[Pomemo.PrintStyle] = []
    textList.append(Pomemo.PrintStyle(size=24, text=str(dt.date())))
    tasks=Notion.get_task()

    client_name=tasks[0].Client
    if client_name!="":
        textList.append(Pomemo.PrintStyle(size=24, text=str(client_name)))

    for t in tasks:
        if client_name!=t.Client:
            textList.append(Pomemo.PrintStyle(mode=Pomemo.PrintMode.LINE))
            textList.append(Pomemo.PrintStyle(size=24, text=str(t.Client)))
            client_name=t.Client
        textList.append(Pomemo.PrintStyle(size=32, text=str("□ " + t.Text)))
    asyncio.run(Pomemo.main(textList))


if __name__ == "__main__":
    main()
