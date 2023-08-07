from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

echo = on_command("复读机", to_me())


@echo.handle()
async def Etc_Main(message: Message = CommandArg()):
    '''其他'''
    if 'help' in message or '帮助' in message:\
        help()
    elif '复读机' in message:
        Reprint(message)
    else:
        await echo.finish('诶嘿～')

async def Reprint(message):
    '''复读'''
    if message == '':
        await echo.send("复读机啊你")
    else:
        await echo.send(message=message)

async def help():
    '''帮助'''
    await echo.finish('具体参考作者帖子')
