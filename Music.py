import requests
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.villa import MessageSegment, SendMessageEvent, Message

matcher = on_command("音乐")


@matcher.handle()
async def Music_Main(event: SendMessageEvent, args: Message = CommandArg()):
    '''音乐主函数'''
    arg = args.extract_plain_text().strip()
    if 'help' in arg or '帮助' in arg:
        await help()
    else:
        await Cloud_music(arg)
async def Cloud_music(arg):
    '''search'''
    # http://cloud-music.pl-fe.cn/search?keywords={}&limit=3
    if arg[0:2] == '搜索':
        S_URL_FOR = 'https://music.163.com/#/song?id={}'
        JsonPage = requests.get('http://cloud-music.pl-fe.cn/search?keywords='+ arg[3:] +'&limit=3')
        data = JsonPage.json()
        songs = data['result']['songs']
        for Message in range(3):
            msg = MessageSegment.preview_link(
            icon_url = "https://ts3.cn.mm.bing.net/th?id=ODLS.08f56e86-962a-4f3d-a18d-ce003b52590a&w=32&h=32&qlt=90&pcl=fffffa&o=6&pid=1.2",
            image_url = "https://s1.music.126.net/style/favicon.ico?v20180823",
            is_internal_link = False,
            title = songs[Message]['name'],
            content = '音乐人：' + songs[Message]['artists'][0]['name'],
            url = S_URL_FOR.format(songs[Message]['id']),
            source_name = "网易云音乐",
            )
            await matcher.send(msg)

async def help():
    '''帮助'''
    msg = MessageSegment.text('如：/音乐 搜索 Da Capo')
    await matcher.finish(msg)
