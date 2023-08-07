from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.villa import MessageSegment, SendMessageEvent, Message

matcher = on_command("help")


@matcher.handle()
async def Help_Main(event: SendMessageEvent, args: Message = CommandArg()):
    msg = MessageSegment.link(
        url = '',
        show_text = '', requires_bot_access_token = False
    )
    await matcher.send('QWPbot是基于nonebot2框架和villabot适配器开发的的bot\n\
                       具体指令参考下帖')
    await matcher.finish(msg)
