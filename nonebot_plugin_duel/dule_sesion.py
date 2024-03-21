import asyncio
import random
from typing import Optional

from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.log import logger

from .config import config

lock = asyncio.Lock()


class DuleSession:
    state: int = 0
    """
    0: 等待被邀请人同意
    1: 等待开枪
    2: 结束
    """
    is_time_out: bool = False
    user2_agreed_duel: bool = False
    """
    决斗的被邀请人是否同意决斗
    """
    duel_start_time: int = 0
    """
    决斗开始的时间
    """
    duel_time_can_shot: int = 0
    """
    在此时间后才可以开枪
    """
    agree_future = None
    ahead_future = None
    shot_future = None

    def __init__(self, bot: Bot, group_id: int, duel_user_1: int, duel_user_2: int):
        self.bot = bot
        self.group_id = group_id
        self.duel_user_1 = duel_user_1
        self.duel_user_2 = duel_user_2

        asyncio.create_task(self.wait_user2_agree())

    async def set_user2_agreed_duel(self) -> None:
        """
        设置被邀请人同意决斗
        :return:
        """
        self.user2_agreed_duel = True
        time_delta = random.randint(5, 60)
        if self.agree_future and not self.agree_future.done() and not self.is_time_out:
            self.agree_future.set_result(True)

            # 抢跑标志
            self.ahead_future = asyncio.get_event_loop().create_future()

            logger.info(f'{time_delta}秒后开始决斗')
            await self.bot.send_group_msg(group_id=self.group_id,
                                          message=(f'接下来，{config.nickname}会在60秒内喊出开始，'
                                                   '在这之后最先发送“开枪”的博士胜出，在喊开始之前发送的博士会被视为犯规，'
                                                   '输的人会被禁言哦。'))
            try:
                # 先开枪犯规了
                fouler = await asyncio.wait_for(self.ahead_future, time_delta)
                await asyncio.create_task(self.bot.send_group_msg(group_id=self.group_id,
                                                                  message=MessageSegment.text(
                                                                      '玩家') + MessageSegment.at(
                                                                      fouler) + MessageSegment.text(
                                                                      '抢跑犯规，被禁言10分钟，对方被击毙，禁言1分钟')))
                await asyncio.create_task(
                    self.bot.set_group_ban(group_id=self.group_id, user_id=fouler, duration=10 * 60))
                await asyncio.create_task(
                    self.bot.set_group_ban(group_id=self.group_id,
                                           user_id=self.duel_user_1 if self.duel_user_1 != fouler else self.duel_user_2,
                                           duration=1 * 60))
                await self.finish()
                return
            except asyncio.TimeoutError:
                # 进入正常对局
                await self.bot.send_group_msg(group_id=self.group_id, message='开始')
                await self.wait_shot()

    async def shot(self, user_id: int):
        if self.state == 2 or self.is_time_out:
            return
        if self.ahead_future and not self.ahead_future.done():
            # {user_id}抢跑
            self.ahead_future.set_result(user_id)
            self.state = 2
            return
        if self.shot_future and not self.shot_future.done():
            # {user_id}先开枪
            self.shot_future.set_result(user_id)
            self.state = 2
            return

    async def wait_shot(self):
        self.shot_future = asyncio.get_event_loop().create_future()
        try:
            winner = await asyncio.wait_for(self.shot_future, 10)
            await self.bot.send_group_msg(group_id=self.group_id,
                                          message=MessageSegment.text('玩家') + MessageSegment.at(
                                              winner) + MessageSegment.text('胜出，对方被禁言3分钟'))
            await self.bot.set_group_ban(group_id=self.group_id,
                                         user_id=self.duel_user_1 if self.duel_user_1 != winner else self.duel_user_2,
                                         duration=3 * 60)
        except asyncio.TimeoutError:
            self.is_time_out = True
            await self.bot.send_group_msg(group_id=self.group_id, message="双方10秒内都没有回应，一起被禁言5分钟")
            await self.bot.set_group_ban(group_id=self.group_id, user_id=self.duel_user_1, duration=5 * 60)
            await self.bot.set_group_ban(group_id=self.group_id, user_id=self.duel_user_2, duration=5 * 60)

        await self.finish()

    async def wait_user2_agree(self):
        """
        等待被邀请人同意
        :return:
        """
        self.agree_future = asyncio.get_event_loop().create_future()
        try:
            await asyncio.wait_for(self.agree_future, 30)
        except asyncio.TimeoutError:
            self.is_time_out = True
            await self.bot.send_group_msg(group_id=self.group_id, message="对方30秒内未响应同意")
            await self.finish()

    async def finish(self):
        await finsh_session(self)


sessions: list[DuleSession] = []


async def create_session(bot: Bot, group_id: int, duel_user_1: int, duel_user_2: int) -> bool:
    """
    创建一个session
    :param bot:
    :param group_id:
    :param duel_user_1:
    :param duel_user_2:
    :return:
    """
    async with lock:
        for session in sessions:
            if session.bot == bot and session.group_id == group_id:
                return False
    async with lock:
        sessions.append(DuleSession(bot, group_id, duel_user_1, duel_user_2))
        return True


async def get_session(bot: Bot, group_id: int) -> Optional[DuleSession]:
    """
    根据bot和group_id获取一个session，同一个bot和群只能有一个session
    :param bot:
    :param group_id:
    :return:
    """
    async with lock:
        for session in sessions:
            if session.bot == bot and session.group_id == group_id:
                return session
    return None


async def finsh_session(session: DuleSession):
    """
    删除session
    :param session:
    :return:
    """
    logger.debug(f'删除session')
    async with lock:
        try:
            sessions.remove(session)
            logger.debug('session removed')
        except ValueError:
            logger.warning('session not found')


async def get_session_users() -> dict[int, list[int]]:
    """
    获取所有session的用户
    :return:
    """
    async with lock:
        users: dict[int, list[int]] = {}
        for session in sessions:
            users[session.group_id] = [session.duel_user_1, session.duel_user_2]
        return users
