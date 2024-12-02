import Notion
import asyncio
import Pomemo
import datetime
import time



def main():
    dt=datetime.datetime.today()
    textList:list[Pomemo.PrintStyle]=[]
    textList.append(Pomemo.PrintStyle(size=24,text=str(dt.date())))
    for t in Notion.get_task():
        if(t.Client!=""):
            text1=Pomemo.PrintStyle(size=24,text=str(t.Client))
            textList.append(text1)
        text2=Pomemo.PrintStyle(size=32,text=str("□ "+t.Text))
        textList.append(text2)
    asyncio.run(Pomemo.main(textList))

if __name__ == "__main__":
    main()