import Notion
import asyncio
import Pomemo
import datetime
import time


def main():
    client_name=""
    dt = datetime.datetime.today()
    textList: list[Pomemo.PrintStyle] = []
    textList.append(Pomemo.PrintStyle(size=24, text=str(dt.date())+"のToDo -"+str(datetime.datetime.now().hour)))
    tasks=Notion.get_task("今日やる")

    client_name=tasks[0].Client
    if client_name!="":
        textList.append(Pomemo.PrintStyle(size=24, text=str(client_name)))

    for t in tasks:
        if client_name!=t.Client:
            textList.append(Pomemo.PrintStyle(mode=Pomemo.PrintMode.LINE))
            textList.append(Pomemo.PrintStyle(size=24, text=str(t.Client)))
            client_name=t.Client
        if t.Deadline!="":
            textList.append(Pomemo.PrintStyle(size=26, text=str("□ " + t.Text+" ("+t.Deadline+")")))
        else :textList.append(Pomemo.PrintStyle(size=26, text=str("□ " + t.Text)))
    textList.append(Pomemo.PrintStyle(mode=Pomemo.PrintMode.FEED))
    textList.append(Pomemo.PrintStyle(text="確認タスク"))
    textList.append(Pomemo.PrintStyle(mode=Pomemo.PrintMode.LINE))
    wait_tasks=Notion.get_task("待ち")
    for tw in wait_tasks:
        textList.append(Pomemo.PrintStyle(size=26, text=str("□ " + tw.Text)))
    asyncio.run(Pomemo.PrintText(textList))


if __name__ == "__main__":
    main()
