# https://fanyi.baidu.com/#en/zh/
# (英——中)
# https://fanyi.baidu.com/#zh/en/
# (中——英)
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.villa import MessageSegment, SendMessageEvent, Message

matcher = on_command("百度翻译")

@matcher.handle()
async def baiduTran_Main(event: SendMessageEvent, args: Message = CommandArg()):
    '''翻译主函数'''
    arg = args.extract_plain_text().strip()
    if 'help' in arg or '帮助' in arg:
        await help()
    else:
        await EtoCorCtoE(arg)

async def EtoCorCtoE(arg):
    '''En to Zh or Zh to En'''
    Tran_To = arg[2:]
    Tran_Mean = arg[0:2]
    if Tran_Mean == "英汉":
        msg = MessageSegment.link(
            url="https://fanyi.baidu.com/#en/zh/" + Tran_To,
            show_text=Tran_To + "的翻译结果" , requires_bot_access_token=False
        )
    elif Tran_Mean == "汉英":
        msg = MessageSegment.link(
            url="https://fanyi.baidu.com/#zh/en/" + Tran_To,
            show_text=Tran_To + "的翻译结果", requires_bot_access_token=False
        )
    else:
        msg = MessageSegment.text("目前只支持 英汉 and 汉英，请重新艾特bot进行输入！")
    await matcher.finish(msg)

async def help():
    '''帮助'''
    msg = MessageSegment.text("如：/百度翻译 英汉Elysia\n\
        /百度翻译 汉英爱莉希雅")
    await matcher.finish(msg)
