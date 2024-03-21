from nonebot import on_keyword, on_fullmatch
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot
from nonebot.matcher import Matcher
from nonebot.rule import Rule
from nonebot.typing import T_State

from .dule_sesion import get_session, create_session
from .rule import is_duel_event, not_blacklisted_user, is_duel_user

dule_req = on_keyword({'决斗'}, rule=Rule(is_duel_event, not_blacklisted_user))
agree_req = on_fullmatch('同意', rule=Rule(not_blacklisted_user, is_duel_user))
shot_req = on_fullmatch('开枪', rule=Rule(not_blacklisted_user, is_duel_user))


@dule_req.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    duel_user_1: int = state.get('duel_user_1')
    duel_user_2: int = state.get('duel_user_2')

    can_duel = await create_session(bot, event.group_id, duel_user_1, duel_user_2)
    if can_duel:
        await dule_req.send(
            message=MessageSegment.text(f'博士{event.sender.nickname}发起了一场决斗，请') + MessageSegment.at(
                duel_user_2) + MessageSegment.text('确认是否参与决斗，如果参与请回复同意，否则将自动取消'))


@agree_req.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    session = await get_session(bot, event.group_id)
    if session and event.user_id == session.duel_user_2:
        await session.set_user2_agreed_duel()


@shot_req.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    session = await get_session(bot, event.group_id)
    if session:
        await session.shot(event.user_id)
