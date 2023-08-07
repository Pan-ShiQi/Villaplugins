# https://api.bilibili.com/x/web-interface/wbi/search/square?limit=10&platform=web&w_rid=4f897877ed4da5f4f022f9b6c90c441b&wts=1691159783
import requests
import random
import re
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.villa import MessageSegment, SendMessageEvent, Message

matcher = on_command("b站")


@matcher.handle()

async def Bilibili_Main(event: SendMessageEvent, args: Message = CommandArg()):
    '''bilibili主函数'''
    arg = args.extract_plain_text().strip()
    api_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Cookie': "buvid3=1FE7DD8C-6EAE-7DFD-E425-8E0B0DFBA9BA14424infoc; b_nut=1689641721; i-wanna-go-back=-1; b_ut=7; _uuid=9C5EA10B6-83EF-2A22-102F4-B54F8B7BE95516088infoc; buvid_fp=39e5c946c69ed1b8bf1392a0ca037f5c; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; buvid4=A656411F-D8FD-E70C-D0DD-A912885960C118865-023071808-EOsu%2BNwSLYykq7xjJeCJdg%3D%3D; home_feed_column=4; browser_resolution=1320-25; CURRENT_FNVAL=4048; fingerprint=39e5c946c69ed1b8bf1392a0ca037f5c; buvid_fp_plain=undefined; rpdid=|(J~R~uRk|J|0J'uYm||mkluJ; sid=6fnrki8c; b_lsid=5C6E9A67_189C519FE5E; PVID=1; innersign=0; bsource=search_bing"
    }
    if 'help' in arg or '帮助' in arg:
        await help()
    elif '搜索' in arg:
        await Bilibili_Search(arg,api_header)
    elif '热榜' in arg:
        await Bilibili_Hot(arg,api_header)
    else:
        return

async def Bilibili_Search(arg,api_header):
    '''b站搜索'''
    keyword = arg[3:]
    # api
    URL = 'https://api.bilibili.com/x/web-interface/wbi/search/type?__refresh__=true&_extra=\
        &context=&page=1&page_size=42&from_source=&platform=pc&highlight=1&single_column=0\
            &keyword={}&source_tag=3&search_type=video'
    try:
        JsonPage = requests.get(url = URL.format(keyword),headers = api_header)
        data = JsonPage.json()
    except ConnectionError:
        await matcher.finish('请求数据异常，请检查输入格式，若无误请联系bot作者本人，@潘_p')
    else:
        result = data['data']['result']
        Ran = random.randint(0,5)
        title = str(result[Ran]['title'])
        msg = MessageSegment.preview_link(
            icon_url = "https://ts2.cn.mm.bing.net/th?id=ODLS.e42d2c4d-ad65-4c7a-b0fd-817a1c3bed01&w=\
                32&h=32&qlt=90&pcl=fffffa&o=6&pid=1.2",
            image_url = 'https:' + result[Ran]['pic'],
            is_internal_link=False,
            # 正则表达式{},<>
            title = re.sub(u"\\{.*?\\}|\\<.*?\\>", "", title),
            content = result[Ran]['description'],
            url = result[Ran]['arcurl'],
            source_name = 'bilibili',
        )
        await matcher.send(msg)

async def Bilibili_Hot(arg,api_header):
    URL = 'https://api.bilibili.com/x/web-interface/wbi/search/square?limit=10&platform=web&w_rid=4f897877ed4da5f4f022f9b6c90c441b&wts=1691159783'
    try:
        JsonPage = requests.get(url = URL,headers = api_header)
        data = JsonPage.json()
    except ConnectionError:
        await matcher.finish('请求数据异常，请检查输入格式，若无误请联系bot作者本人，@潘_p')
    else:
        result = data['data']['trending']['list']
        msg = ''
        for Hot in result:
            msg += Hot['keyword'] + '\n'
        await matcher.send(msg.rstrip('\n'))
async def help():
    '''帮助'''
    await matcher.send('如：/b站 搜索 爱莉希雅')
