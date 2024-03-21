from nonebot.plugin import PluginMetadata

from .config import Config
from .matcher import dule_req, agree_req, shot_req

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-duel",
    description="决斗插件",
    usage="",
    type="application",
    homepage="https://github.com/Redmomn/nonebot-plugin-duel",
    supported_adapters={"~onebot.v11"},
    config=Config,
    extra={"author": "Redmomn"}
)

__all__ = ['dule_req', 'agree_req', 'shot_req']
