import Notion
import asyncio
import Pomemo
import datetime
import time


def printTodo(bard_name:list[str]):
    client_name=""
    dt = datetime.datetime.today()
    textList: list[Pomemo.PrintStyle] = []
    textList.append(Pomemo.PrintStyle(size=24, text=str(dt.date())+"のToDo -"+str(datetime.datetime.now().hour)))
    for name in bard_name:
        tasks=Notion.get_task(name)
        if not tasks==[]:
            textList.append(Pomemo.PrintStyle(size=24, text=str(name)))
            textList.append(Pomemo.PrintStyle(mode=Pomemo.PrintMode.LINE))
            for t in tasks:
                if t.Deadline=="":
                    textList.append(Pomemo.PrintStyle(size=26, text=str("□ " + t.Text)))
                else:
                    textList.append(Pomemo.PrintStyle(size=26, text=str("□ " + t.Text+" ("+t.Deadline+")")))
            textList.append(Pomemo.PrintStyle(mode=Pomemo.PrintMode.FEED))
    asyncio.run(Pomemo.PrintText(textList))


if __name__ == "__main__":
    printTodo(["今日やる","金型製作","aaa"])