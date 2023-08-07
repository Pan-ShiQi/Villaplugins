from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.villa import MessageSegment, SendMessageEvent, Message
import requests
import random


# @机器人 /米游社 gid 版区 内容
GIDS = {
    # gid : ['同人','cos']
    '3':['40'],
    '1':['4'],
    '2':['29','49'],
    '4':['38'],
    '6':['56','62'],
    '8':['59'],
    '5':['39','47']
}

matcher = on_command("米游社")


@matcher.handle()

async def Miyoushe_Main(event: SendMessageEvent, args: Message = CommandArg()):
    '''米游社主函数'''
    # roomID = event.room_id
    keyword = args.extract_plain_text().strip()
    gid = keyword[0:1]
    URL_POST = 'https://www.miyoushe.com/ys/article/{}'
    Random = random.randint(0,20)
    if GIDS.get(gid) != None:
        if '同人图' in keyword:
            URL = 'https://bbs-api.miyoushe.com/post/wapi/getForumPostList?forum_id=' + GIDS[gid][0] \
                + '&gids=' + gid + '&is_good=false&is_hot=true&page_size=20'
            await Miyoushe_CosAndHomo(keyword,Random,URL,URL_POST)
        elif 'cos' in keyword:
            try:
                URL = 'https://bbs-api.miyoushe.com/post/wapi/getForumPostList?forum_id=' + GIDS[gid][1] \
                    + '&gids=' + gid + '&is_good=false&is_hot=true&page_size=20'
            except IndexError:
                await matcher.finish('不存在cos区，或GIDS[gid][i]越界')
            else:
                await Miyoushe_CosAndHomo(keyword,Random,URL,URL_POST)
        elif 'help' in keyword or '帮助' in keyword:
            help()
        else:
            await Miyoushe_Post(gid,Random,keyword,URL_POST)
    else:
         await Error()
        
async def Miyoushe_CosAndHomo(keyword,Random,URL,URL_POST):
    '''cosAndHomo'''
    try:
        response = requests.get(URL)
        data = response.json()
    except ConnectionError:
        await matcher.finish('请求数据异常，请检查输入格式，若无误请联系bot作者本人，@潘_p')
    else:
        if '随机图' in keyword:
            postID = data['data']['list'][Random]['post']['post_id']
            reply_msg = MessageSegment.post(
                post_id = URL_POST.format(postID)
            )
            await matcher.finish(reply_msg)
        else:
            postID = []
            List = data['data']['list']
            for i in List:
                postTitle = i['post']['subject']
                if keyword[7:] in postTitle:
                    postID.append(i['post']['post_id'])
            Len = len(postID)
            Random = random.randint(0,Len)
            reply_msg = MessageSegment.post(
                post_id = URL_POST.format(postID[Random-1])
            )
            await matcher.finish(reply_msg)

async def Miyoushe_Post(gid,Random,keyword,URL_POST):
    '''帖子搜索'''
    URL_POST_FORMA = 'https://bbs-api.miyoushe.com/post/wapi/searchPosts?GIDS=' + gid \
            + '&keyword=' + keyword[2:] + '&preview=true&size=20'
    try:
        response = requests.get(URL_POST_FORMA)
        data = response.json()
        postID = data['data']['posts'][Random]['post']['post_id']
    except:
        await matcher.finish('请求数据异常，请检查输入格式，若无误请联系bot作者本人，@潘_p')
    reply_msg = MessageSegment.post(
        post_id = URL_POST.format(postID)
    )
    await matcher.finish(reply_msg)

async def Error():
    '''错误处理'''
    await matcher.send('gid:\n1 崩坏3\n2 原神\n3 崩坏学院2\n4 未定事件簿\n5 大别野\n6 崩坏：星穹铁道\n8 绝区零')
    await matcher.send('格式：/米游社 gid 同人图/cos 内容\n如：@机器人 /米游社 1 同人图 爱莉希雅')
    await matcher.finish('还有其他问题或不懂的联系bot作者本人，@潘_p')

async def help():
    '''帮助'''
    await matcher.send('如：/米游社 1 同人图 爱莉希雅\n\
        /米游社 gid 同人图/cos 内容\n')
    await matcher.finish('gid参考为游戏频道，具体如下：\n\
        1 崩坏3\n2 原神\n3 崩坏学院2\n4 未定事件簿\n5 大别野\n6 崩坏：星穹铁道\n8 绝区零')
