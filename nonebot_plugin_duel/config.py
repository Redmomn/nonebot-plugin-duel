from typing import List

try:
    # pydantic v2
    from nonebot import get_plugin_config
except ImportError:
    # pydantic v1
    from nonebot import get_driver
from pydantic import BaseModel

try:
    # pydantic v2
    from pydantic import field_validator
except ImportError:
    # pydantic v1
    from pydantic import validator as field_validator


class _ScopedConfig(BaseModel):
    nickname: str = '阿米娅'
    """
    机器人发言时的自称
    """
    blacklisted_users: List[int] = []
    """
    黑名单用户
    """


class Config(BaseModel):
    duel: _ScopedConfig = _ScopedConfig()


try:
    # pydantic v2
    config = get_plugin_config(Config).duel
except:
    # pydantic v1
    config = Config.parse_obj(get_driver().config).duel
