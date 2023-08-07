import requests
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.villa import MessageSegment, SendMessageEvent, Message

matcher = on_command("知乎日报")


@matcher.handle()
async def Daynew_Main(event: SendMessageEvent, args: Message = CommandArg()):
    '''知乎日报主函数'''
    arg = args.extract_plain_text().strip()
    if 'help' in arg or '帮助' in arg:
        await help()
    else:
        await Daynew(arg)

async def Daynew(arg):
    '''每日'''
    if arg == "每日":
        S_URL_FOR = "https://daily.zhihu.com/story/{}"
        JsonPage = requests.get('https://news-at.zhihu.com/api/4/news/latest')
        data = JsonPage.json()
        stories = data['stories']
        for story in stories:
            msg = MessageSegment.preview_link(
                icon_url = "https://static.zhihu.com/heifetz/assets/zhihuDaily.7af86465.png",
                image_url = story['images'][0],
                is_internal_link=False,
                title = story['title'],
                content = "知乎日报，点击查看详情",
                url = S_URL_FOR.format(story['id']),
                source_name = "知乎日报",
        )
            await matcher.send(msg)

async def help():
    '''帮助'''
    msg = MessageSegment.text("如：/知乎日报 每日")
    await matcher.finish(msg)
