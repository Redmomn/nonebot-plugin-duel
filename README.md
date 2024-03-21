<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-vits-tts

✨ 来一场西部牛仔决斗吧 ✨

<p align="center">
  <a href="https://github.com/Redmomn/nonebot-plugin-duel/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Redmomn/nonebot-plugin-duel.svg" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <a href="https://pypi.org/project/nonebot-plugin-duel">
    <img src="https://badgen.net/pypi/v/nonebot-plugin-duel" alt="pypi">
  </a>
</p>

</div>
## 📖 介绍
NoneBot2决斗插件  

已兼容pydantic v1&v2

## 💿 安装

<details open>
<summary>nb-cli</summary>

    nb plugin install nonebot-plugin-duel

</details>

<details open>
<summary>pip</summary>

    pip install nonebot_plugin_duel

</details>

## ⚙️ 配置

默认配置示例

```text
# 机器人的自称
DUEL__NICKNAME=阿米娅
# 插件的黑名单用户，是一个int类型的列表
DUEL__BLACKLISTED_USERS=[]
```

## 🎉 使用

- 发送关键词`决斗`并@一个人即可和他发起决斗，例如`决斗@阿米娅`
- 在同一个群里，未结束先前的决斗不会开启新的决斗

```text
- 说 `兔兔，我要与[@一个人]决斗` 
- 对方需在30秒内回复`同意`，否则决斗会取消。
- 接下来，阿米娅会在60秒内的一个随机时间喊出`开始`，在这之后最先发送`开枪`的博士胜出，在喊开始之前发送的博士会被视为犯规。
```

## 💡 感谢

此插件基于[AmiyaBot](https://www.amiyabot.com/)的[决斗插件](https://github.com/hsyhhssyy/amiyabot-game-hsyhhssyy-duel/)
移植而来
