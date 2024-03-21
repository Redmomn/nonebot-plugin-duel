from nonebot.plugin import PluginMetadata

from .config import Config
from .matcher import dule_req, agree_req, shot_req

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-duel",
    description="决斗插件",
    usage="发送关键词`决斗`并@一个人即可和他发起决斗，例如`决斗@阿米娅`",
    type="application",
    homepage="https://github.com/Redmomn/nonebot-plugin-duel",
    supported_adapters={"~onebot.v11"},
    config=Config,
    extra={"author": "Redmomn"}
)

__all__ = ['dule_req', 'agree_req', 'shot_req']
