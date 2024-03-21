import asyncio
import re

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.log import logger
from nonebot.typing import T_State

from .config import config
from .dule_sesion import get_session_users

lock = asyncio.Lock()
duel_sesiions: dict[Bot:list[int]] = {}


async def not_blacklisted_user(event: GroupMessageEvent) -> bool:
    return event.user_id not in config.blacklisted_users


async def is_duel_user(event: GroupMessageEvent, state: T_State) -> bool:
    """
    判断是否是决斗用户
    :param event:
    :param state:
    :return:
    """
    all_users = await get_session_users()
    users = all_users.get(event.group_id, [])
    return event.user_id in users


async def is_duel_event(event: GroupMessageEvent, state: T_State) -> bool:
    """
    判断是否是决斗事件
    :param event:
    :param state:
    :return:
    """
    duel_user_1 = event.user_id
    duel_user_2 = await get_at(event)
    if duel_user_2 == 0 or duel_user_1 == duel_user_2:
        return False
    state['duel_user_1'] = duel_user_1
    state['duel_user_2'] = duel_user_2
    return True


async def get_at(event: GroupMessageEvent) -> int:
    pattern = r'\[CQ:at,qq=(\d+)]'
    matches = re.findall(pattern, event.raw_message)
    if len(matches) == 1:
        return int(matches[0])
    return 0
