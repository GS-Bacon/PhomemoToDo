import asyncio
from typing import Optional

from bleak import BleakScanner, BLEDevice, BleakClient

from dataclasses import dataclass
from enum import Enum
from PIL import ImageFont, Image, ImageDraw

DEVICE_NAME = "M02 Pro"
CONNECTION_RETRY_MAX_COUNT = 3
CHARACTERISTIC_UUID_WRITE = "0000ff02-0000-1000-8000-00805f9b34fb"
MACADD="AC:C5:F4:F6:FF:98"
ESC = b"\x1b"
GS = b"\x1d"
# 1 line = 576 dots = 72 bytes x 8 bit
DOT_PER_LINE = 576
BYTE_PER_LINE = DOT_PER_LINE // 8


@dataclass
class BitmapData:
    bitmap: bytes
    width: int
    height: int

class PrintMode(Enum):
    DEFAULT=0
    LINE=1
    FEED=2

@dataclass
class PrintStyle:
    size: int=24
    text: str=""
    mode:PrintMode=PrintMode.DEFAULT


async def main(texts: list[PrintStyle]):
    # scan and connect
    device = await connect()
    if device:
        print("connected.")
    else:
        print("device not found.")
        return
    async with BleakClient(device) as client:
        await init_printer(client=client)
        for i, t in enumerate(texts):
            if(t.mode==PrintMode.DEFAULT):
                await print_text(client=client, text=t.text, fontsize=t.size)
            elif(t.mode==PrintMode.LINE):
                await print_line(client=client)
            elif(t.mode==PrintMode.FEED):
                await feed(client=client)
        # 印字データ書き込みのあとにすぐDisconnectしてしまうとうまく動かないので少し待つ
        await feed(client=client, line=4)
        await asyncio.sleep(2)

async def PrintLabel():
    device = await connect()
    if device:
        print("connected.")
    else:
        print("device not found.")
        return
    async with BleakClient(device) as client:
        await init_printer(client=client)
        while (True):
            t=input("input text or exit\n")
            if(t=="/exit"):
                await feed(client=client,line=4)
                break
            elif(t==""):
                pass
            elif(t=="/feed"):
                await feed(client=client,line=4)
            else:await print_text(client=client,text=t,fontsize=40)
        await asyncio.sleep(2)

# 初期化
async def init_printer(client: BleakClient):
    print(f"init printer")
    await send_command(client=client, data=ESC + b"@" + b"\x1f\x11\x02\x04")

# コマンド送信
async def send_command(client: BleakClient, data: bytes):
    await client.write_gatt_char(
        char_specifier=CHARACTERISTIC_UUID_WRITE, data=data, response=True
    )


# 紙送り
async def feed(client: BleakClient, line: int = 1):
    print(f"feed paper: {line} lines")
    await send_command(client=client, data=ESC + b"d" + line.to_bytes(1, "little"))


# 接続
async def connect() -> Optional[BLEDevice]:
    retry_count = 0
    device = None
    while not device and retry_count < CONNECTION_RETRY_MAX_COUNT:
        device = await BleakScanner.find_device_by_address(MACADD)
        retry_count += 1
    return device


async def print_line(client: BleakClient):
    # GS v 0 コマンド
    # パラメータの詳細はESC/POSのコマンドリファレンスを参照
    # ビットマップのx,yサイズはリトルエンディアンで送信する必要があるので注意
    command = (
        GS
        + b"v0"
        + int(0).to_bytes(1, byteorder="little")
        + int(BYTE_PER_LINE).to_bytes(2, byteorder="little")
        + int(1).to_bytes(2, byteorder="little")
    )
    await send_command(client=client, data=command)

    # 上記コマンドで指定したバイト数分のビットマップデータを送信する
    line_data = bytearray([0xFF] * BYTE_PER_LINE)
    await send_command(client=client, data=line_data)


async def print_text(client: BleakClient, text: str, fontsize: int = 24):
    # 指定した文字が描かれたビットマップを生成して取得
    bitmap_data = text_to_bitmap(text=text, fontsize=fontsize)

    # GS v 0 コマンド
    command = (
        GS
        + b"v0"
        + int(0).to_bytes(1, byteorder="little")
        + int(BYTE_PER_LINE).to_bytes(2, byteorder="little")
        + int(bitmap_data.height).to_bytes(2, byteorder="little")
    )
    await send_command(client=client, data=command)

    # 上記コマンドで指定したバイト数分のビットマップデータを送信する
    await send_command(client=client, data=bitmap_data.bitmap)


async def print_line(client: BleakClient):
    # GS v 0 コマンド
    # パラメータの詳細はESC/POSのコマンドリファレンスを参照
    # ビットマップのx,yサイズはリトルエンディアンで送信する必要があるので注意
    command = (
        GS
        + b"v0"
        + int(0).to_bytes(1, byteorder="little")
        + int(BYTE_PER_LINE).to_bytes(2, byteorder="little")
        + int(1).to_bytes(2, byteorder="little")
    )
    await send_command(client=client, data=command)

    # 上記コマンドで指定したバイト数分のビットマップデータを送信する
    line_data = bytearray([0xFF] * BYTE_PER_LINE)
    await send_command(client=client, data=line_data)


def text_to_bitmap(text: str, fontsize: int) -> BitmapData:
    # 必要なビットマップサイズ
    font = ImageFont.truetype("ipaexm.ttf", fontsize)
    image_width = DOT_PER_LINE
    image_height = int(fontsize)

    # ビットマップを作成
    img = Image.new("1", (image_width, image_height), 0)
    draw = ImageDraw.Draw(img)

    # 文字を描画する
    draw.text((0, 0), text, font=font, fill=1)

    # ビットマップのバイト列を返却する
    return BitmapData(img.tobytes(), image_width, image_height)


if __name__ == "__main__":
    asyncio.run(PrintLabel())
    pass
    # asyncio.run(main(["AAAAAA","あいうえおかきくけこさしすせそたちつてと","BBBBBBBBBBBBBBBBBBBBBB"]))
