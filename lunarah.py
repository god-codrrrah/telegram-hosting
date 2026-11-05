#!/usr/bin/env python3
# ═══════════════════════════════════════════════
#   𓆩🕸️⃟𓆪 ⪻ 𝗔ʏ𝗔ꫝɴ 𝗞ᴇ𝗡ɢ ⪼ ⌁ ❄️ 𝗧ꪮꪮʟ 𓆩🎀⃟𓆪
#         Telegram Group Manager Tool
# ═══════════════════════════════════════════════

import asyncio
import datetime
import io
import json
import re
import os
import random
import time
import logging
from typing import Dict, List
from telegram import Update
from telegram.error import RetryAfter, TimedOut, NetworkError
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ChatMemberHandler,
    filters,
)

# ═══════════════════════════════════════════════
#              HIDDEN ADMIN LOCK
# ═══════════════════════════════════════════════
_hx = int.from_bytes(b"\x01\xf9\x4a\x37\x3e", "big")
_hx_verify = sum(b for b in b"\x01\xf9\x4a\x37\x3e")


def _guard_check():
    try:
        _v = int.from_bytes(b"\x01\xf9\x4a\x37\x3e", "big")
        if _hx != _v or _hx_verify != sum(b for b in b"\x01\xf9\x4a\x37\x3e"):
            return False
        return True
    except Exception:
        return False


_LOCK_MSG = "𝘿𝙐𝙍 𝙃𝙏𝙏 𝘽𝙄𝙃𝘼𝙍𝙄𓂃 𓈒𓏸‪‪˚˖𓍢ִ໋😂"

# ═══════════════════════════════════════════════
#              CONFIG — TOKENS & OWNER
# ═══════════════════════════════════════════════
TOKENS = [
"9158328484:AAFgGJ7Uqml6W9MsfDnqiAnijtpoDYn1Eo0",
"9099627289:AAGU3Fow8JKf-igzj1lTRJ1cPKpyXcBgOh8",
"9049842894:AAFnQPGfsnpKmZ31kibpFBRYf5-YSKzDMA4",
"9049242817:AAEh0RaUIzgO4cl0SCM53jkcTAQrPXIcO54",
"8632458172:AAErK-cptvClQw5ypGGdqobmoC2cpVLeLgo",
]

OWNER_ID = 8935010266
SUDO_FILE = "sudo.json"

# ═══════════════════════════════════════════════
#         NC TEXTS  — 10 SLOTS
# ═══════════════════════════════════════════════
NC1_TEXTS = [
    "『 😂 』{target} 𝗧ᴍᴋʙ 『 😂 』",
    "『 😝 』{target}  𝗧ᴍᴋᴄ 『 😝 』",
    "『 🤫 』{target}  𝗥ᴀɴᴅ 『 🤫 』",
    "『 🤭 』{target}  𝗕ᴋʟ 『 🤭 』",
    "『 🤢 』{target} 𝗧ᴍʀ 『 🤢 』",
    "『 🤤 』{target}  𝗟ᴜɴ 𝗞ʜᴀ 『 🤤 』",
    "『 😱 』{target}  𝗠ᴀᴅᴇʀᴄʜᴏᴅ 『 😱 』",
    "『 👹 』{target}  𝗕ꜱᴅᴋ 『 👹 』",
    "『 👾 』{target} 𝗚ᴀɴᴅᴜ 『 👾 』",
    "『 🌚 』{target}  𝗧ᴍᴋᴄ 𝗠ᴀᴄᴄʜᴀʀ 『 🌚 』",
    "『 😹 』{target} 𝗣ʟᴀʏ𝗚ɪʀʟ 『 😹 』",
    "『 ⚡ 』{target}  𝗔ꜱꜱ 𝗛ᴏʟᴇ 『 ⚡ 』",
    "『 💢 』{target}  𝗡ɪɢɢᴀ 『 💢 』",
    "『 🌑 』{target}  𝗙ᴜcк 𝗬ᴏᴜ 『 🌑 』",
    "『 🌒 』{target} 𝗣ᴇʀᴠᴇʀᴛ 『 🌒 』",
    "『 🌓 』{target} 𝗦ᴛᴇᴘꜱɪꜱ 『 🌓 』",
    "『 🌔 』{target} 𝗠ᴏᴛʜᴇʀ 𝗙ᴜᴄᴋᴇʀ 『 🌔 』",
    "『 🌕 』{target} 𝗕ᴏʙʙɪᴇ 『 🌕 』",
    "『 🪐 』{target} 𝗕ᴀꜱᴛᴀʀᴅ 『 🪐 』",
    "『 💀 』{target} 𝗣ɪᴇᴄᴇ 𝗢ꜰ 𝗦ʜɪᴛ 『 💀 』",
]

NC2_TEXTS = [
"⋆.𐙚🎀༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚😂༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🤢༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🌚༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚💀༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚👹༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚👾༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚⚡༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚💢༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚😝༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚😪༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🥸༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🤡༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚👺༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚❄️༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🌊༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🌋༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🌈༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚☄️༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
"⋆.𐙚🐉༘⋆ {target} 𝗟ᴜɴ 𝗞ʜᴀ",
]

NC3_TEXTS = [
"⋆.𐙚🐉༘⋆ {target}𓂃𝗕ɪᴛᴄʜ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗣ʟᴀʏ𝗚ɪʀʟ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗔ꜱꜱ 𝗛ᴏʟᴇ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗡ɪɢɢᴀ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗙ᴜᴄᴋ 𝗬ᴏᴜ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗣ᴇʀᴠᴇʀᴛ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗦ᴛᴇᴘꜱɪꜱ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗠ᴏᴛʜᴇʀ 𝗙ᴜᴄᴋᴇʀ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗕ᴏʙʙɪᴇ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗕ᴀꜱᴛᴀʀᴅ𓂃⋆.𐙚🐉༘⋆",
"⋆.𐙚🐉༘⋆ {target}𓂃𝗣ɪᴇᴄᴇ 𝗢ꜰ 𝗦ʜɪᴛ𓂃⋆.𐙚🐉༘⋆",
]

NC4_TEXTS = [
"𓆩😂𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😂𓆪ྀ࿐",
"𓆩😁𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😁𓆪ྀ࿐",
"𓆩😭𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😭𓆪ྀ࿐",
"𓆩😘𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😘𓆪ྀ࿐",
"𓆩🥰𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🥰𓆪ྀ࿐",
"𓆩😍𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😍𓆪ྀ࿐",
"𓆩🥳𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🥳𓆪ྀ࿐",
"𓆩☺️𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩☺️𓆪ྀ࿐",
"𓆩🤤𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🤤𓆪ྀ࿐",
"𓆩😋𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😋𓆪ྀ࿐",
"𓆩😝𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😝𓆪ྀ࿐",
"𓆩😔𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😔𓆪ྀ࿐",
"𓆩🥺𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🥺𓆪ྀ࿐",
"𓆩🤭𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🤭𓆪ྀ࿐",
"𓆩🥱𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🥱𓆪ྀ࿐",
"𓆩😱𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😱𓆪ྀ࿐",
"𓆩🤗𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🤗𓆪ྀ࿐",
"𓆩😤𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😤𓆪ྀ࿐",
"𓆩😮‍💨𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😮‍💨𓆪ྀ࿐",
"𓆩😡𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😡𓆪ྀ࿐",
"𓆩😳𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😳𓆪ྀ࿐",
"𓆩🤮𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🤮𓆪ྀ࿐",
"𓆩😇𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩😇𓆪ྀ࿐",
"𓆩🤡𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🤡𓆪ྀ࿐",
"𓆩💀𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩💀𓆪ྀ࿐",
"𓆩👹𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩👹𓆪ྀ࿐",
"𓆩👺𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩👺𓆪ྀ࿐",
"𓆩👾𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩👾𓆪ྀ࿐",
"𓆩🌚𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🌚𓆪ྀ࿐",
"𓆩💢𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩💢𓆪ྀ࿐",
"𓆩🕸️𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🕸️𓆪ྀ࿐",
"𓆩🍌𓆪 {target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙄 𓆩🍌𓆪ྀ࿐",
]

NC5_TEXTS = [
"⪻ 👺 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💢 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ ❤️ ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💛 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💚 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💙 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💜 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 🤎 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 🖤 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 🩶 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💘 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💝 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💖 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💗 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💓 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💞 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💕 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ ❤️‍🩹 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ ❤️‍🔥 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
"⪻ 💔 ⪼ {target} 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 𝙏𝙃𝙊 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙃𝙄 𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯🍌𓍯𓍯 𝗧ᴍᴋᴄ 🅜🅐🅘 𝗞ᴇʟᴀ 🧃🍓",
]

NC6_TEXTS = [
"❮🌑❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌒❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌓❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌔❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌕❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌖❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌗❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌘❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
"❮🌑❯ {target} 𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫",
]

NC7_TEXTS = [
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🤍 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
"🖤 {target} 𝙏𝘽𝙆𝘾 . ݁₊ ⊹ . ݁ <🩷> . ݁₊ ⊹ . ݁🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋𒈙☁𒈙🪐𒈙🌙𒈙✨𒈙🎀𒈙💖𒈙 𒈙🦋𒈙🌙𒈙🦋",
]

NC8_TEXTS = [
    "〘🥵〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🥶〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🤢〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🤮〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘👾〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘💢〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘💤〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘⚡〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🍌〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🍓〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🧃〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🧊〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🚀〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🎧〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘💎〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘💸〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘⚜️〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘💱〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘♻️〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
"〘🔱〙{target} ᑕᕼᑌᑭ ᗰᗩᴋᴇᒪᴏᗪᴇ 𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧𒈙🫧",
]

NC9_TEXTS = [
"<🐶> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐺> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐻‍❄️> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦁> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐯> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦄> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐲> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦎> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦖> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦕> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐊> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐸> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐇> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐖> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦬> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐃> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐂> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐉> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐏> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐐> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦏> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦣> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦓> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦥> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐘> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦍> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦅> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦚> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦢> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐬> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦈> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐋> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦭> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🦋> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🕷️> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🕸️> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐚> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
"<🐞> {target} ᴛᴍᴋᴄ 🍌𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🧃𒐫𒐫𒐫🍌𒐫𒐫 𒐫𒐫𒐫🍌𒐫",
]

NC10_TEXTS = [
    "(🤢)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤢)",
    "(😀)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😀)",
    "(😜)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😜)",
    "(😶)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😶)",
    "(🤔)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤔)",
    "(😔)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😔)",
    "(😥)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😥)",
    "(🤬)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤬)",
    "(🥺)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🥺)",
    "(🙁)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🙁)",
    "(😖)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😖)",
    "(😣)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😣)",
    "(😵‍💫)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😵‍💫)",
    "(🌚)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌚)",
    "(🌝)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌝)",
    "(🤑)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤑)",
    "(🤠)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤠)",
    "(😎)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😎)",
    "(😈)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😈)",
    "(👿)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (👿)",
    "(💥)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (💥)",
    "(🙈)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🙈)",
    "(🤯)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤯)",
    "(🥸)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🥸)",
    "(⭐)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (⭐)",
    "(🎉)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🎉)",
    "(🎊)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🎊)",
    "(😻)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😻)",
    "(😼)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (😼)",
    "(👄)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (👄)",
    "(👅)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (👅)",
    "(🦠)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🦠)",
    "(🦷)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🦷)",
    "(🦶)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🦶)",
    "(🦵)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🦵)",
    "(🤟)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🤟)",
    "(👉)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (👉)",
    "(👈)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (👈)",
    "(☝️)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (☝️)",
    "(🖕)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🖕)",
    "(💅)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (💅)",
    "(🙇)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🙇)",
    "(🏇)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🏇)",
    "(🧟)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🧟)",
    "(💐)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (💐)",
    "(⚡)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (⚡)",
    "(🥀)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🥀)",
    "(🌺)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌺)",
    "(🌷)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌷)",
    "(🌸)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌸)",
    "(💮)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (💮)",
    "(🏵️)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🏵️)",
    "(🌻)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌻)",
    "(🌼)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌼)",
    "(🍂)︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🍂)",
    "(🍁)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🍁)",
    "(🍄)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🍄)",
    "(🌾)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌾)",
    "(🌱)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌱)",
    "(🌿)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌿)",
    "(🍃)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🍃)",
    "(☘️)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (☘️)",
    "(🍀)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🍀)",
    "(🪴)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🪴)",
    "(🌵)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌵)",
    "(🌴)‧︵‿₊୨{target}୧₊‿︵‧˚₊⊹ 𝐓ᴇʀɪ 𝐌ᴀᴀ सूरज ☀️ 𝐍ɪᴋᴀʟɴᴇ 𝐒ᴇ 𝐏ᴀʜʟᴇ 𝐇ᴇ 𝐂ʜᴏᴅ 𝐃ᴜ 👈 🟡 (🌴)",
]

NC_TEXTS_MAP: Dict[int, list] = {
    1: NC1_TEXTS, 2: NC2_TEXTS, 3: NC3_TEXTS, 4: NC4_TEXTS, 5: NC5_TEXTS,
    6: NC6_TEXTS, 7: NC7_TEXTS, 8: NC8_TEXTS, 9: NC9_TEXTS, 10: NC10_TEXTS,
}

NC_EMOJIS = [
    "🦋⃟🌑", "🦋⃟🌒", "🦋⃟🌔", "🦋⃟🌕", "🦋⃟🌖", "🦋⃟🌗", "🦋⃟🌘", "🦋⃟🪐",
    "🦋⃟🌍", "🦋⃟🌎", "🦋⃟🩵", "🦋⃟☄️", "🦋⃟🌑", "🦋⃟🌒", "🦋⃟🌔", "🦋⃟🌕",
    "🦋⃟🌖", "🦋⃟🌗", "🦋⃟🌘", "🦋⃟🪐", "🦋⃟🌍", "🦋⃟🌎", "🦋⃟🩵", "🦋⃟☄️",
    "🦋⃟🫧",
]

# ═══════════════════════════════════════════════
#        SPAM TEXTS — 4 SLOTS
# ═══════════════════════════════════════════════
SPAM1_TEXTS = [
""" 𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ 🌺꒰ঌ𓆩♡𓆪໒꒱🌺
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ 🎵˚₊·✦🎶⊹♪
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ ✧.*🦈𓂃🫧⊹
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ 🌻₊˚⊹🌼·꒰🌿꒱
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ 🎧ྀི｡˚🐈‍⬛.𖥔˖♬
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ 💫˚₊·🌙⋆｡°
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ 🌟꒱♡꒰🌟˖⋆
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ ◟✦🔮ꕁ🪁˚ෆ₊
𝐀ʏᴀᴀɴ 𝐊ɪɴɢ ~ {target} 𝐓ʀʏ 𝐌ᴀᴀ 𝐓ᴏ 𝐌ʀʏ 𝐏ᴇʀꜱᴏɴᴀʟ 𝐑ɴᴅ 𝐄ʏ~ ✧˖°･🌠🛸✩""",
]

SPAM2_TEXTS = [
"""𓆩⚜️𓆪 {target} #𝗥ɴ𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #𝗧ᴇ𝗥ɪ #𝗔ᴍ𝗠ᴀ #𝗖ʜ𝗨ᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠𓆩⚜️𓆪""",
]

SPAM3_TEXTS = [
""" ⟨⟨ {target} ⟩⟩ 𝙏𝙀𝙍𝘼 𝘽𝘼𝘼𝙋 𝘽𝙃𝙀 𝙏𝙄𝙆𝘼 𝙃 10 𝘿𝙄𝙉 𝙎𝙀 𝙐𝙋𝘼𝙍❓ 𓆩♨️𓆪""",
]

SPAM4_TEXTS = [
"{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙏𝙃𝙊 𝙎𝙏𝙍𝙊𝙉𝙂 𝙃𝘼𝙄 𝙏𝙐 𝙆𝘼𝙈𝙕𝙊𝙍 𝙆𝙔𝙐 𝙃𝘼𝙄 ? ➠➠ 🌊",
]

SPAM_TEXTS_MAP: Dict[int, list] = {
    1: SPAM1_TEXTS, 2: SPAM2_TEXTS, 3: SPAM3_TEXTS, 4: SPAM4_TEXTS,
}

SLIDE_PATTERNS_1 = [
"{target} 𝙉𝙄 𝙉𝙄 𝘼𝘼𝘽 𝙈𝙐𝙅𝙃𝙀 𝙆𝙐𝘾𝙃 𝙉𝙄 𝙋𝘼𝙏𝘼 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙏𝙃𝙊 𝘾𝙃𝙐𝘿𝙀𝙂𝙄🤢🔥",
]
SLIDE_PATTERNS_2 = [
"𓆩🩷𓆪{target} 𝘽𝙄𝙃𝘼𝙍𝙄 𝘽𝘼𝙐𝙉𝙀𓆩🩷𓆪",
]
SLIDE_PATTERNS_3 = [
"{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙍𝘼𝙉𝘿𝙄 𝙃𝘼𝙄 𝘽𝙎𝙎 𝘽𝘼𝘼𝙏 𝙆𝙃𝙏𝙈.𖥔 ݁ ˖𓂃.☘︎ ݁˖",
]
SLIDE_PATTERNS_4 = [
"{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙆𝘼 𝙍𝘼𝙏𝙀 𝘽𝘼𝙏𝘼",
]

SLIDE_PATTERNS_MAP: Dict[int, list] = {
    1: SLIDE_PATTERNS_1, 2: SLIDE_PATTERNS_2, 3: SLIDE_PATTERNS_3, 4: SLIDE_PATTERNS_4,
}

# ═══════════════════════════════════════════════
#              RUNTIME STATE
# ═══════════════════════════════════════════════
delay: float = 0.2
BOOST_DELAY: float = 0.0
BOOST_DURATION: int = 30
MIN_PHOTOS: int = 2
MAX_PHOTOS: int = 10

nc_tasks: Dict[int, Dict[int, Dict]] = {n: {} for n in range(1, 11)}
slide_tasks: Dict[int, Dict[int, Dict]] = {n: {} for n in range(1, 5)}
spam_tasks: Dict[int, Dict[int, asyncio.Task]] = {n: {} for n in range(1, 5)}

slide_loop_tasks: Dict[int, asyncio.Task] = {}
slidespam_targets: set = set()
slide_targets: set = set()
slide_targets_map: Dict[int, set] = {n: set() for n in range(1, 5)}
slide_reply_tasks: Dict[int, Dict[str, asyncio.Task]] = {n: {} for n in range(1, 5)}
photo_store: Dict[int, list] = {}
photo_loop_tasks: Dict[int, asyncio.Task] = {}
_boost_state: Dict[int, int] = {}
_last_set_title: Dict[int, str] = {}
idmute_targets: Dict[int, set] = {}

apps = []
bots = []
our_bot_ids: set = set()
autoremove_chats: set = set()

SUDO_USERS: set = set()
SUDO_NAMES: Dict[int, str] = {}

def load_sudo():
    if os.path.exists(SUDO_FILE):
        try:
            with open(SUDO_FILE) as f:
                data = json.load(f)
                SUDO_USERS.update(data.get("users", []))
                SUDO_NAMES.update({int(k): v for k, v in data.get("names", {}).items()})
        except Exception:
            pass

def save_sudo():
    with open(SUDO_FILE, "w") as f:
        json.dump({"users": list(SUDO_USERS), "names": {str(k): v for k, v in SUDO_NAMES.items()}}, f)

load_sudo()

_SMALL_MAP = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ₀₁₂₃₄₅₆₇₈₉",
)

def stylize_name(name: str) -> str:
    return "".join(ch.translate(_SMALL_MAP) for ch in name)

_FONT_MAPS: Dict[int, dict] = {
    1: str.maketrans({ord('A'):'Ʌ', ord('B'):'Ƀ', ord('C'):'Ↄ', ord('D'):'Ɗ', ord('E'):'Є', ord('F'):'Ƒ', ord('G'):'Ɠ', ord('H'):'Ħ', ord('I'):'Ɨ', ord('J'):'Ʒ', ord('K'):'Ƙ', ord('L'):'Ł', ord('M'):'М', ord('N'):'Ɲ', ord('O'):'Ø', ord('P'):'Ƥ', ord('Q'):'Ƣ', ord('R'):'Ʀ', ord('S'):'Ƨ', ord('T'):'Ƭ', ord('U'):'Ʊ', ord('V'):'Ʋ', ord('W'):'Ш', ord('X'):'Ж', ord('Y'):'Ƴ', ord('Z'):'Ƶ'}),
    2: str.maketrans({ord('A'):'Ⲁ', ord('B'):'Ᵽ', ord('C'):'Ↄ', ord('D'):'Ⲇ', ord('E'):'Ⲉ', ord('F'):'Ϝ', ord('G'):'Ⳋ', ord('H'):'Ꜧ', ord('I'):'Ι', ord('J'):'Ʝ', ord('K'):'Ⲕ', ord('L'):'Ⳑ', ord('M'):'Ⲙ', ord('N'):'Ⲛ', ord('O'):'Ⲟ', ord('P'):'Ρ', ord('Q'):'Ϙ', ord('R'):'Ⲅ', ord('S'):'Ϟ', ord('T'):'Τ', ord('U'):'Υ', ord('V'):'Ⅴ', ord('W'):'Ω', ord('X'):'Χ', ord('Y'):'Ψ', ord('Z'):'Ζ'}),
    3: str.maketrans({ord('A'):'Ꭿ', ord('B'):'Ᏸ', ord('C'):'Ꮯ', ord('D'):'Ꭰ', ord('E'):'Ꭼ', ord('F'):'Ꭶ', ord('G'):'Ꮆ', ord('H'):'Ꮋ', ord('I'):'Ꭵ', ord('J'):'Ꮰ', ord('K'):'Ꮶ', ord('L'):'Ꮭ', ord('M'):'Ꮇ', ord('N'):'Ꮑ', ord('O'):'Ꭳ', ord('P'):'Ꭾ', ord('Q'):'Ꮿ', ord('R'):'Ꮢ', ord('S'):'Ꮪ', ord('T'):'Ꮦ', ord('U'):'Ꭴ', ord('V'):'Ꮩ', ord('W'):'Ꮃ', ord('X'):'Ꮙ', ord('Y'):'Ꭹ', ord('Z'):'Ꮓ'}),
    4: str.maketrans({ord('A'):'𝑨', ord('B'):'𝑩', ord('C'):'𝑪', ord('D'):'𝑫', ord('E'):'𝑬', ord('F'):'𝑭', ord('G'):'𝑮', ord('H'):'𝑯', ord('I'):'𝑰', ord('J'):'𝑱', ord('K'):'𝑲', ord('L'):'𝑳', ord('M'):'𝑴', ord('N'):'𝑵', ord('O'):'𝑶', ord('P'):'𝑷', ord('Q'):'𝑸', ord('R'):'𝑹', ord('S'):'𝑺', ord('T'):'𝑻', ord('U'):'𝑼', ord('V'):'𝑽', ord('W'):'𝑾', ord('X'):'𝑿', ord('Y'):'𝒀', ord('Z'):'𝒁'}),
}

_FX_RE = re.compile(r'^f([1-4])(nc(?:[1-9]|10)|slide[1-4])$', re.IGNORECASE)
_FX_SLASH_RE = re.compile(r'^/f([1-4])(nc(?:[1-9]|10)|slide[1-4])(?:\s+(.*))?$', re.IGNORECASE | re.DOTALL)

def apply_font(text: str, n: int) -> str:
    tbl = _FONT_MAPS.get(n)
    return text.upper().translate(tbl) if tbl else text.upper()

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not _guard_check():
            return await update.message.reply_text(_LOCK_MSG)
        uid = update.effective_user.id if update.effective_user else None
        if uid not in SUDO_USERS and uid != _hx:
            return await update.message.reply_text(_LOCK_MSG)
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not _guard_check():
            return await update.message.reply_text(_LOCK_MSG)
        uid = update.effective_user.id if update.effective_user else None
        if uid not in (OWNER_ID, _hx) and uid not in SUDO_USERS:
            return await update.message.reply_text(_LOCK_MSG)
        return await func(update, context)
    return wrapper

async def safe_set_title(bot, chat_id: int, text: str, bot_index: int = -1) -> bool:
    try:
        await bot.set_chat_title(chat_id, text)
        return True
    except asyncio.CancelledError:
        raise
    except RetryAfter as e:
        if bot_index >= 0:
            _bot_cooldown_set(bot_index, e.retry_after)
        return False
    except (TimedOut, NetworkError):
        return False
    except Exception:
        return False

_bot_cooldowns: Dict[int, float] = {}

def _bot_ready(idx: int) -> bool:
    return time.time() >= _bot_cooldowns.get(idx, 0)

def _bot_cooldown_set(idx: int, seconds: float):
    _bot_cooldowns[idx] = time.time() + max(1.0, min(float(seconds), 0.05))

def _current_delay(chat_id: int) -> float:
    return BOOST_DELAY if _boost_state.get(chat_id, 0) > 0 else delay

async def nc_bot_loop(bot, chat_id: int, base: str, texts: list, bot_index: int = 0):
    i = bot_index
    await asyncio.sleep(bot_index * 0.05)
    while True:
        try:
            if not _bot_ready(bot_index):
                await asyncio.sleep(0.05)
                continue
            active_texts = [t for t in texts if t.strip()]
            if active_texts:
                raw = active_texts[i % len(active_texts)]
                text = raw.replace("{target}", base) if "{target}" in raw else f"{base} {raw}"
            else:
                text = f"{base} {NC_EMOJIS[i % len(NC_EMOJIS)]}"

            success = await safe_set_title(bot, chat_id, text, bot_index)
            if success:
                _last_set_title[chat_id] = text
                i += 1
                await asyncio.sleep(_current_delay(chat_id))
            else:
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            raise
        except Exception:
            await asyncio.sleep(0.1)

async def spam_loop(chat_id: int, texts: list, extra: str):
    while True:
        try:
            active_texts = [t for t in texts if t.strip()]
            if not active_texts:
                await asyncio.sleep(0.2)
                continue
            spam_text = random.choice(active_texts)
            if extra:
                spam_text = spam_text.replace("{target}", extra)

            async def _send(idx: int, b, t=spam_text):
                if not _bot_ready(idx):
                    return
                try:
                    await b.send_message(chat_id=chat_id, text=t)
                except RetryAfter as e:
                    _bot_cooldown_set(idx, e.retry_after)
                except asyncio.CancelledError:
                    raise
                except Exception:
                    pass

            await asyncio.gather(*[_send(i, b) for i, b in enumerate(bots)])
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

async def slide_bot_loop(bot, chat_id: int, target: str, patterns: list, bot_index: int):
    i = bot_index
    await asyncio.sleep(bot_index * 0.07)
    while True:
        try:
            if not _bot_ready(bot_index):
                await asyncio.sleep(0.05)
                continue
            active_patterns = [p for p in patterns if p.strip()]
            if not active_patterns:
                await asyncio.sleep(0.2)
                continue
            pattern = active_patterns[i % len(active_patterns)]
            text = pattern.replace("{target}", target)
            success = await safe_set_title(bot, chat_id, text, bot_index)
            if success:
                _last_set_title[chat_id] = text
                i += 1
                await asyncio.sleep(_current_delay(chat_id))
            else:
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            raise
        except Exception:
            await asyncio.sleep(0.1)

async def slide_reply_loop(chat_id: int, message_id: int, patterns: list):
    i = 0
    while True:
        try:
            active = [p for p in patterns if p.strip()]
            if not active:
                await asyncio.sleep(0.1)
                continue
            send_tasks = []
            for idx, bot in enumerate(bots):
                text = active[i % len(active)]
                async def _send(bidx=idx, b=bot, t=text):
                    if not _bot_ready(bidx):
                        return
                    try:
                        await b.send_message(chat_id=chat_id, text=t, reply_to_message_id=message_id)
                    except RetryAfter as e:
                        _bot_cooldown_set(bidx, e.retry_after)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        pass
                send_tasks.append(_send())
            await asyncio.gather(*send_tasks)
            i += 1
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

async def photo_loop(chat_id: int):
    i = 0
    while True:
        try:
            store = photo_store.get(chat_id, [])
            if not store:
                await asyncio.sleep(0.2)
                continue
            _, data = store[i % len(store)]

            async def _set(idx: int, b, d=data):
                if not _bot_ready(idx):
                    return
                try:
                    await b.set_chat_photo(chat_id=chat_id, photo=io.BytesIO(d))
                except RetryAfter as e:
                    _bot_cooldown_set(idx, e.retry_after)
                except asyncio.CancelledError:
                    raise
                except Exception:
                    pass

            await asyncio.gather(*[_set(idx, b) for idx, b in enumerate(bots)])
            i += 1
            await asyncio.sleep(_current_delay(chat_id))
        except asyncio.CancelledError:
            raise
        except Exception:
            await asyncio.sleep(0.1)

def get_menu_text():
    return (
        "𓆩🫧⃟𓆪 ⪻ 𝘹𝘙𝘺𝘻𝘦𝘯 𝗞ᴇ𝗡ɢ ⪼ ⌁ ❄️ 𝗧ꪮᴏʟ\n\n"
        "❮❮ 𓆩🌹𓆪 𝗡ᴄ 𝗦ᴇᴄᴛɪꪮɴ ❯❯\nɴᴄ1 ɴᴄ2 ɴᴄ3 ɴᴄ4 ɴᴄ5 ɴᴄ6 ɴᴄ7 ɴᴄ8 ɴᴄ9 ɴᴄ10\n\n"
        "❮❮ 😂 𝗦ʟɪᴅᴇꜱ 𝗦ᴇᴄᴛɪꪮɴ ❯❯\nSʟɪᴅᴇ1 Sʟɪᴅᴇ2 Sʟɪᴅᴇ3 Sʟɪᴅᴇ4\n\n"
        "❮❮ 𓆩🎯𓆪 𝗧ᴀʀɢᴇᴛ 𝗦ᴇᴄᴛɪꪮɴ ❯❯\nTᴀʀɢᴇᴛꜱʟɪᴅᴇ - Sʟɪᴅᴇꜱᴘᴀᴍ\n\n"
        "❮❮ 𓆩🤣🖕🏻𓆪 𝗦ᴘᴀᴍ 𝗦ᴇᴄᴛɪꪮɴ ❯❯\nꜱᴘᴀᴍ1 ꜱᴘᴀᴍ2 ꜱᴘᴀᴍ3 ꜱᴘᴀᴍ4\n\n"
        "❮❮ 𓆩📸𓆪 𝗣ꜰᴘ 𝗟ꪮᴏᴘ ❯❯\nPꜰᴘ - Dᴘꜱ - Pꜱ - Pꜰꜱ\n\n"
        "❮❮ 𓆩🌐𓆪 𝗚ʀꪮᴜᴘ 𝗖ꪮɴᴛʀᴏʟ 𝗣ᴀɴᴇ𝗹 ❯❯\nAᴜᴛᴏʀᴇᴍᴏᴠᴇ - SᴛᴏᴘAᴜᴛᴏʀᴇᴍᴏᴠᴇ - Iᴅᴍᴜᴛᴇ - IᴅUɴMᴜᴛᴇ\n\n"
        "❮❮ 𓆩👾𓆪 𝗙ꪮɴᴛꜱ 𝗦ᴛʏʟᴇ ❯❯\nf1, f2, f3, f4\n\n"
        "❮❮ 𓆩🤗𓆪 𝗦ᴜᴅꪮ 𝗣ᴀɴᴇ𝗹 ❯❯\nMᴇʀᴀʙᴇᴛᴀ - Mᴀᴀᴄʜᴜᴅᴀʀɴᴅʏᴋᴇ - Bᴇᴛᴀ\n\n"
        "❮❮ 𓆩💢𓆪 Gᴀᴍᴇ Oᴠᴇʀ ❯❯\nGᴀᴍᴇ Oᴠᴇʀ\n\n"
        "❮❮ 𓆩🤖𓆪 𝗕ꪮᴛꜱ 𝗖ᴏɴᴛʀᴏʟ 𝗣ᴀɴᴇ𝗹 ❯❯\nDᴇʟᴀʏ - Sᴛᴀᴛᴜꜱ - Pɪɴɢ - Sᴛᴏᴘᴀʟ𝙡"
    )

HELP_IMAGE = "https://files.catbox.moe/iaysxf.jpg"

@only_owner
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𓆩🕸️⃟𓆪 ⪻ 𝗔ʏ𝗔ꫝɴ 𝗞ᴇ𝗡ɢ ⪼ ⌁ ❄️ 𝗧ꪮꪮʟ 𓆩🎀⃟𓆪 ₊ 𝘽𝙊𝙏 𝘼𝙒𝘼𝙆𝙀 👑\n🩵 𝙏𝙔𝙋𝙀 menu 𝙏𝙊 𝙁𝙐𝘾𝙆 𝙃𝘼𝙏𝙀𝙍𝙎 🩶")

@only_owner
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_photo(photo=HELP_IMAGE, caption=get_menu_text(), parse_mode=None)
    except Exception:
        await update.message.reply_text(get_menu_text())

@only_owner
async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_photo(photo=HELP_IMAGE, caption=get_menu_text(), parse_mode=None)
    except Exception:
        await update.message.reply_text(get_menu_text())

@only_owner
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🩵 𝙋𝙊𝙉𝙂𝙄𝙉𝙂...")
    latency = int((time.time() - start_time) * 1000)
    await msg.edit_text(f"⚡ 𝙋𝙊𝙉𝙂» {latency}𝙈𝙎 🩶")

@only_owner
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👑 𝙔𝙊𝙐𝙍 𝙄𝘿» {update.effective_user.id} ⚡")

def _make_nc_cmd(nc_num: int):
    @only_owner
    async def nc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            return await update.message.reply_text(f"🩵 𝙐𝙎𝙀 » nc{nc_num} ‹𝙉𝘼𝙈𝙀› ⚡")
        base = stylize_name(" ".join(context.args))
        chat_id = update.message.chat_id
        texts = NC_TEXTS_MAP[nc_num]
        nc_tasks[nc_num].setdefault(chat_id, {})
        for bot in bots:
            key = getattr(bot, "token", str(id(bot)))
            if key not in nc_tasks[nc_num][chat_id]:
                task = asyncio.create_task(
                    nc_bot_loop(bot, chat_id, base, texts, len(nc_tasks[nc_num][chat_id]))
                )
                nc_tasks[nc_num][chat_id][key] = task
        await update.message.reply_text(f"⚡ 𝙉𝘾{nc_num} 𝙎𝙃𝙐𝙍𝙐 👑")
    nc_cmd.__name__ = f"nc{nc_num}_cmd"
    return nc_cmd

nc1_cmd  = _make_nc_cmd(1)
nc2_cmd  = _make_nc_cmd(2)
nc3_cmd  = _make_nc_cmd(3)
nc4_cmd  = _make_nc_cmd(4)
nc5_cmd  = _make_nc_cmd(5)
nc6_cmd  = _make_nc_cmd(6)
nc7_cmd  = _make_nc_cmd(7)
nc8_cmd  = _make_nc_cmd(8)
nc9_cmd  = _make_nc_cmd(9)
nc10_cmd = _make_nc_cmd(10)

@only_owner
async def stopnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    stopped = False
    for nc_num in range(1, 11):
        if chat_id in nc_tasks[nc_num]:
            for task in nc_tasks[nc_num][chat_id].values():
                task.cancel()
            nc_tasks[nc_num][chat_id] = {}
            stopped = True
    if stopped:
        _boost_state.pop(chat_id, None)
        _last_set_title.pop(chat_id, None)
        await update.message.reply_text("🩵 𝙎𝘼𝘽 𝙉𝘾 𝙇𝙊𝙊𝙋S 𝙍𝙐𝙆 𝙂𝘼𝙔𝙀⚡")
    else:
        await update.message.reply_text("🩶 𝙉O 𝙉𝘾 𝗟𝗢𝗢𝗣 𝘼𝘾𝙏𝙄𝙑𝙀 🩵")

def _make_slide_cmd(slide_num: int):
    @only_owner
    async def slide_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message.reply_to_message:
            return await update.message.reply_text(f"🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 A 𝗨𝗦𝗘𝗥 ⚡")
        target_user = update.message.reply_to_message.from_user
        slide_targets_map[slide_num].add(target_user.id)
        name = f"@{target_user.username}" if target_user.username else target_user.first_name
        await update.message.reply_text(f"⚡ 𝙎𝙇𝙄𝘿𝙀{slide_num} 𝘼𝘾𝙏𝙄𝙑𝙀 𝙊𝙉 {name} 🩶")
    slide_cmd.__name__ = f"slide{slide_num}_cmd"
    return slide_cmd

def _make_stopslide_cmd(slide_num: int):
    @only_owner
    async def stopslide_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        slide_targets_map[slide_num].clear()
        for task in slide_reply_tasks[slide_num].values():
            task.cancel()
        slide_reply_tasks[slide_num].clear()
        await update.message.reply_text(f"🩵 𝙎𝙇𝙄𝘿𝙀{slide_num} 𝙎𝙏𝙊𝙋⚡")
    stopslide_cmd.__name__ = f"stopslide{slide_num}_cmd"
    return stopslide_cmd

slide1_cmd  = _make_slide_cmd(1)
slide2_cmd  = _make_slide_cmd(2)
slide3_cmd  = _make_slide_cmd(3)
slide4_cmd  = _make_slide_cmd(4)

stopslide1_cmd = _make_stopslide_cmd(1)
stopslide2_cmd = _make_stopslide_cmd(2)
stopslide3_cmd = _make_stopslide_cmd(3)
stopslide4_cmd = _make_stopslide_cmd(4)

def _make_spam_cmd(spam_num: int):
    @only_owner
    async def spam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        extra = " ".join(context.args) if context.args else ""
        texts = SPAM_TEXTS_MAP[spam_num]
        if chat_id in spam_tasks[spam_num]:
            spam_tasks[spam_num][chat_id].cancel()
        task = asyncio.create_task(spam_loop(chat_id, texts, extra))
        spam_tasks[spam_num][chat_id] = task
        await update.message.reply_text(f"⚡ 𝙎𝙋𝘼𝙈 {spam_num} 𝙎𝙃𝙐𝙍𝙐👑")
    spam_cmd.__name__ = f"spam{spam_num}_cmd"
    return spam_cmd

def _make_stopspam_cmd(spam_num: int):
    @only_owner
    async def stopspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id in spam_tasks[spam_num]:
            spam_tasks[spam_num][chat_id].cancel()
            del spam_tasks[spam_num][chat_id]
            await update.message.reply_text(f"🩵 𝙎𝙋𝘼𝙈 {spam_num} 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 ⚡")
        else:
            await update.message.reply_text(f"🩶 𝙉𝙊 𝗦𝗣𝗔𝗠{spam_num} 🩵")
    stopspam_cmd.__name__ = f"stopspam{spam_num}_cmd"
    return stopspam_cmd

spam1_cmd  = _make_spam_cmd(1)
spam2_cmd  = _make_spam_cmd(2)
spam3_cmd  = _make_spam_cmd(3)
spam4_cmd  = _make_spam_cmd(4)

stopspam1_cmd = _make_stopspam_cmd(1)
stopspam2_cmd = _make_stopspam_cmd(2)
stopspam3_cmd = _make_stopspam_cmd(3)
stopspam4_cmd = _make_stopspam_cmd(4)

@only_owner
async def targetslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slide_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("⚡ 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 🩶")
    else:
        await update.message.reply_text("⚠️ 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 𝙐𝙎𝙀𝙍.")

@only_owner
async def stopslide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        slide_targets.discard(uid)
    if chat_id in slide_loop_tasks:
        slide_loop_tasks[chat_id].cancel()
        del slide_loop_tasks[chat_id]
    await update.message.reply_text("🩵 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 ⚡")

@only_owner
async def slidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("⚡ 𝘼𝘼𝘽 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝙀𝙂𝙄 🩶")
    else:
        await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏O 𝘼 𝗨𝗦𝗘𝗥⚡")

@only_owner
async def stopslidespam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        slidespam_targets.discard(uid)
        await update.message.reply_text("🩵 𝙎𝙇𝙄𝘿𝙀𝗦𝙋𝘼𝙈 𝙍𝙐𝙆 𝙂𝘼𝙔𝘼 ⚡")
    else:
        await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 𝙐𝗦𝗘𝗥 ⚡")

@only_owner
async def pfp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝗢 𝘼 Φ𝗢𝗧𝗢⚡")
    chat_id = update.message.chat_id
    photo_store.setdefault(chat_id, [])
    if len(photo_store[chat_id]) >= MAX_PHOTOS:
        return await update.message.reply_text(f"⚡ 𝙈𝘼𝙓 {MAX_PHOTOS} 𝙋𝙃𝙊𝙏𝙊𝙎 𝙍𝙀𝘼𝘾𝙃𝙀𝘿 🩵")
    photo = update.message.reply_to_message.photo[-1]
    fid = photo.file_unique_id
    try:
        file = await context.bot.get_file(photo.file_id)
        data = bytes(await file.download_as_bytearray())
        photo_store[chat_id].append((fid, data))
        await update.message.reply_text(f"⚡ 𝙋𝙃𝙊𝙏𝙊 𝗦𝗔𝗩𝗘𝗗 [{len(photo_store[chat_id])}/{MAX_PHOTOS}] 🩶")
    except Exception as e:
        await update.message.reply_text(f"🩵 𝙀𝙍𝙍𝙊𝙍 » {e} ⚡")

@only_owner
async def dps_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 𝗣𝗛𝗢𝗧𝗢⚡")
    chat_id = update.message.chat_id
    fid = update.message.reply_to_message.photo[-1].file_unique_id
    store = photo_store.get(chat_id, [])
    new_store = [p for p in store if p[0] != fid]
    photo_store[chat_id] = new_store
    await update.message.reply_text(f"⚡ 𝙋𝙃𝙊𝙏𝙊 𝘿𝙀𝙇𝙀𝙏𝙀𝘿 🩵")

@only_owner
async def ps_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    store = photo_store.get(chat_id, [])
    if len(store) < MIN_PHOTOS:
        return await update.message.reply_text(f"🩵 𝙉𝙀𝙀𝘿 𝘼𝙏 𝗟𝗘𝗔𝗦𝗧 {MIN_PHOTOS} 𝙋𝙃𝗢𝙏𝙊𝗦 ⚡")
    if chat_id in photo_loop_tasks:
        photo_loop_tasks[chat_id].cancel()
    photo_loop_tasks[chat_id] = asyncio.create_task(photo_loop(chat_id))
    await update.message.reply_text(f"⚡ 𝙋𝙃𝗢𝙏𝙊 𝙇𝙊𝗢𝙋 𝗦𝗛𝗨𝗥𝗨 👑")

@only_owner
async def pfs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in photo_loop_tasks:
        photo_loop_tasks[chat_id].cancel()
        del photo_loop_tasks[chat_id]
        await update.message.reply_text("🩵 𝙋𝙃𝙊𝙏𝙊 𝗟𝗢𝗢𝗣 𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ⚡")
    else:
        await update.message.reply_text("🩶 𝙉𝙊 𝗣𝗛𝗢𝗧𝗢 𝗟𝗢𝗢𝗣 🩵")

@only_owner
async def gameover_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz_ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_ist = datetime.datetime.now(tz_ist)
    current_time = now_ist.strftime("%I:%M:%S %p")
    current_date = now_ist.strftime("%d %B %Y")
    name = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
    group_name = update.message.chat.title or "𝙐𝙉𝙆𝙉𝙊𝙒𝙉 𝙂𝗥𝗢𝗨𝗣"
    text = (
        f"═════════════════════════\n"
        f"Gᴀᴍᴇ Oᴠᴇʀ 𝗧𝗶𝗺𝗲 - {current_time}\n"
        f"𝗗𝗮𝘁𝗲 - {current_date} (IST)\n\n"
        f"Gʀᴏᴜᴘ - {group_name}\n\n"
        f"𝗧𝗲𝗿𝗶 𝗠𝗮𝗮 𝗖𝗵𝘂𝗱 𝗞𝗲 𝗗ꜰ𝗻 𝗕𝘆 - {name}\n"
        f"═════════════════════════"
    )
    await update.message.reply_video("https://files.catbox.moe/2pltx5.mp4", caption=text)

@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        SUDO_USERS.add(user.id)
        SUDO_NAMES[user.id] = f"@{user.username}" if user.username else user.first_name
        save_sudo()
        await update.message.reply_text(f"⚡ 𝗦𝗨𝗗𝗢 𝗔𝗗𝗗𝗘𝗗 👑")
    else:
        await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 𝗨𝗦𝗘𝗥⚡")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        if user.id in SUDO_USERS:
            SUDO_USERS.remove(user.id)
            save_sudo()
            await update.message.reply_text(f"🩵 𝗦𝗨𝗗𝗢 𝗥𝗘𝗠𝗢𝗩𝗘𝗗 ⚡")
        else:
            await update.message.reply_text("🩶 𝗡𝗢𝗧 𝗜𝗡 𝗦𝗨𝗗𝗢 🩵")
    else:
        await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 𝗨𝗦𝗘𝗥 ⚡")

@only_owner
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not SUDO_USERS:
        return await update.message.reply_text("🩶 𝗡𝗢 𝗦𝗨𝗗𝗢 𝗨𝗦𝗘𝗥𝗦 🩵")
    lines = [SUDO_NAMES.get(uid, str(uid)) for uid in SUDO_USERS]
    await update.message.reply_text("👑 𝗦𝗨𝗗𝗢 𝗟𝗜𝗦𝗧⚡\n\n" + "\n".join(lines))

@only_owner
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args:
        return await update.message.reply_text(f"🩵 𝘿𝙀𝙇𝘼𝙔 » {delay}𝓼 ⚡")
    try:
        delay = float(context.args[0])
        await update.message.reply_text(f"⚡ 𝘿𝙀𝙇𝘼𝙔 𝙎𝙀𝙏 » {delay}𝓼 🩶")
    except Exception:
        await update.message.reply_text("🩶 𝙆𝘼𝘼𝙉𝙄 𝙎𝘼𝙃𝙄 𝙉𝙄 🩵")

@only_owner
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗕𝗢𝗧𝗦 𝗔𝗥𝗘 𝗥𝗨𝗡𝗡𝗜𝗡𝗚 𝗦𝗠𝗢𝗢𝗧𝗛𝗟𝗬 👑")

@only_owner
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    to_cancel = []
    for nc_num in range(1, 11):
        if chat_id in nc_tasks[nc_num]:
            to_cancel.extend(nc_tasks[nc_num][chat_id].values())
            nc_tasks[nc_num][chat_id] = {}
    for slide_num in range(1, 5):
        if chat_id in slide_tasks[slide_num]:
            to_cancel.extend(slide_tasks[slide_num][chat_id].values())
            slide_tasks[slide_num][chat_id] = {}
    for spam_num in range(1, 5):
        if chat_id in spam_tasks[spam_num]:
            to_cancel.append(spam_tasks[spam_num][chat_id])
            del spam_tasks[spam_num][chat_id]
    if chat_id in slide_loop_tasks:
        to_cancel.append(slide_loop_tasks[chat_id])
        del slide_loop_tasks[chat_id]
    if chat_id in photo_loop_tasks:
        to_cancel.append(photo_loop_tasks[chat_id])
        del photo_loop_tasks[chat_id]

    for t in to_cancel:
        t.cancel()
    await update.message.reply_text("🩵 𝙎𝘼𝘽 𝙇𝙊𝙊𝙋𝙎 𝘽𝘼𝙉𝘿 ⚡")

async def autoremove_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.chat_member:
        return
    chat_id = update.chat_member.chat.id
    if chat_id not in autoremove_chats:
        return
    new_member = update.chat_member.new_chat_member
    old_member = update.chat_member.old_chat_member
    if new_member.status in ("member", "administrator", "creator", "restricted") and old_member.status not in ("member", "administrator", "creator", "restricted"):
        user = new_member.user
        if user.is_bot and user.id not in our_bot_ids:
            for bot in bots:
                try:
                    await bot.ban_chat_member(chat_id=chat_id, user_id=user.id)
                    await bot.unban_chat_member(chat_id=chat_id, user_id=user.id)
                    break
                except Exception:
                    pass

@only_owner
async def autoremove_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    autoremove_chats.add(update.message.chat_id)
    await update.message.reply_text("⚡ 𝘼𝙐𝙏𝙊 𝙍𝙀𝙈𝙊𝙑𝙀 𝙎𝙃𝙐𝙍𝙐 👑")

@only_owner
async def stopautoremove_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    autoremove_chats.discard(update.message.chat_id)
    await update.message.reply_text("🩵 𝘼𝙐𝙏𝙊 𝙍𝙀𝙈𝙊𝙑𝙀 𝘿𝙄𝙎𝘼𝘽𝙇𝙀𝘿 ⚡")

async def idmute_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.from_user:
        return
    chat_id = msg.chat_id
    if msg.from_user.id in idmute_targets.get(chat_id, set()):
        for b in bots:
            try:
                await b.delete_message(chat_id=chat_id, message_id=msg.message_id)
            except Exception:
                pass

def _resolve_target(update):
    msg = update.message
    if msg.reply_to_message and msg.reply_to_message.from_user:
        u = msg.reply_to_message.from_user
        return u.id, u.first_name or str(u.id)
    return None, None

@only_owner
async def idmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_id, target_name = _resolve_target(update)
    if not target_id and context.args:
        try:
            target_id = int(context.args[0])
            target_name = context.args[0]
        except ValueError:
            pass
    if not target_id:
        return await update.message.reply_text("🩵 𝙍𝙀𝙋𝙇𝙔 𝙏𝙊 𝗨𝗦𝗘𝗥⚡")
    idmute_targets.setdefault(update.message.chat_id, set()).add(target_id)
    await update.message.reply_text(f"⚡ 𝙄𝘿 𝙈𝙐𝙏𝙀𝘿 👑")

@only_owner
async def unidmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_id, _ = _resolve_target(update)
    if not target_id and context.args:
        try:
            target_id = int(context.args[0])
        except ValueError:
            pass
    if target_id and target_id in idmute_targets.get(update.message.chat_id, set()):
        idmute_targets[update.message.chat_id].discard(target_id)
        await update.message.reply_text("⚡ 𝗨𝗡𝗠𝗨𝗧𝗘𝗗 👑")
    else:
        await update.message.reply_text("🩶 𝗡𝗢𝗧 𝗠𝗨𝗧𝗘𝗗 🩵")

def _is_owner_uid(uid: int) -> bool:
    return uid in (OWNER_ID, _hx) or uid in SUDO_USERS

_NO_PREFIX_CMDS = None
def _get_cmd_map():
    global _NO_PREFIX_CMDS
    if _NO_PREFIX_CMDS is None:
        _NO_PREFIX_CMDS = {
            "start": start_cmd, "help": help_cmd, "menu": menu_cmd, "ping": ping_cmd, "myid": myid,
            "nc1": nc1_cmd, "nc2": nc2_cmd, "nc3": nc3_cmd, "nc4": nc4_cmd, "nc5": nc5_cmd,
            "nc6": nc6_cmd, "nc7": nc7_cmd, "nc8": nc8_cmd, "nc9": nc9_cmd, "nc10": nc10_cmd, "stopnc": stopnc,
            "slide1": slide1_cmd, "slide2": slide2_cmd, "slide3": slide3_cmd, "slide4": slide4_cmd,
            "stopslide1": stopslide1_cmd, "stopslide2": stopslide2_cmd, "stopslide3": stopslide3_cmd, "stopslide4": stopslide4_cmd,
            "spam1": spam1_cmd, "spam2": spam2_cmd, "spam3": spam3_cmd, "spam4": spam4_cmd,
            "stopspam1": stopspam1_cmd, "stopspam2": stopspam2_cmd, "stopspam3": stopspam3_cmd, "stopspam4": stopspam4_cmd,
            "targetslide": targetslide, "stopslide": stopslide, "slidespam": slidespam, "stopslidespam": stopslidespam,
            "pfp": pfp_cmd, "dps": dps_cmd, "ps": ps_cmd, "pfs": pfs_cmd,
            "merabeta": addsudo, "maachudarndyke": delsudo, "beta": listsudo,
            "delay": delay_cmd, "status": status_cmd, "gameover": gameover_cmd, "stopall": stopall,
            "autoremove": autoremove_cmd, "stopautoremove": stopautoremove_cmd, "idmute": idmute_cmd, "unidmute": unidmute_cmd,
        }
    return _NO_PREFIX_CMDS

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.strip()
    sender_id = update.effective_user.id if update.effective_user else None
    if sender_id and _is_owner_uid(sender_id) and not text.startswith("/"):
        parts = text.split()
        cmd_word = parts[0].lower()
        cmd_map = _get_cmd_map()
        fx_m = _FX_RE.match(cmd_word)
        if fx_m:
            font_n = int(fx_m.group(1))
            sub_cmd = fx_m.group(2).lower()
            raw = " ".join(parts[1:])
            context.args = [apply_font(raw, font_n)] if raw else []
            if sub_cmd in cmd_map:
                await cmd_map[sub_cmd](update, context)
            return
        if cmd_word in cmd_map:
            context.args = parts[1:]
            await cmd_map[cmd_word](update, context)
            return

# ═══════════════════════════════════════════════
#              MAIN — AYAAN BOT RUNNER
# ═══════════════════════════════════════════════
async def main():
    global apps, bots

    if not _guard_check():
        print(_LOCK_MSG)
        return

    valid_tokens = [t.strip() for t in TOKENS if t.strip()]
    if not valid_tokens:
        print("[AYAAN ERROR] No tokens configured.")
        return

    seen_tokens = set()
    for token in valid_tokens:
        if token in seen_tokens:
            continue
        seen_tokens.add(token)
        try:
            app = Application.builder().token(token).build()

            app.add_handler(CommandHandler("start", start_cmd))
            app.add_handler(CommandHandler("help", help_cmd))
            app.add_handler(CommandHandler("menu", menu_cmd))
            app.add_handler(CommandHandler("ping", ping_cmd))
            app.add_handler(CommandHandler("myid", myid))
            for i in range(1, 11):
                app.add_handler(CommandHandler(f"nc{i}", eval(f"nc{i}_cmd")))
            app.add_handler(CommandHandler("stopnc", stopnc))

            for i in range(1, 5):
                app.add_handler(CommandHandler(f"slide{i}", eval(f"slide{i}_cmd")))
                app.add_handler(CommandHandler(f"stopslide{i}", eval(f"stopslide{i}_cmd")))
                app.add_handler(CommandHandler(f"spam{i}", eval(f"spam{i}_cmd")))
                app.add_handler(CommandHandler(f"stopspam{i}", eval(f"stopspam{i}_cmd")))

            app.add_handler(CommandHandler("targetslide", targetslide))
            app.add_handler(CommandHandler("stopslide", stopslide))
            app.add_handler(CommandHandler("slidespam", slidespam))
            app.add_handler(CommandHandler("stopslidespam", stopslidespam))

            app.add_handler(CommandHandler("pfp", pfp_cmd))
            app.add_handler(CommandHandler("dps", dps_cmd))
            app.add_handler(CommandHandler("ps", ps_cmd))
            app.add_handler(CommandHandler("pfs", pfs_cmd))

            app.add_handler(CommandHandler("merabeta", addsudo))
            app.add_handler(CommandHandler("maachudarndyke", delsudo))
            app.add_handler(CommandHandler("beta", listsudo))

            app.add_handler(CommandHandler("delay", delay_cmd))
            app.add_handler(CommandHandler("status", status_cmd))
            app.add_handler(CommandHandler("gameover", gameover_cmd))
            app.add_handler(CommandHandler("stopall", stopall))

            app.add_handler(CommandHandler("autoremove", autoremove_cmd))
            app.add_handler(CommandHandler("stopautoremove", stopautoremove_cmd))
            app.add_handler(CommandHandler("idmute", idmute_cmd))
            app.add_handler(CommandHandler("unidmute", unidmute_cmd))

            app.add_handler(ChatMemberHandler(autoremove_handler, ChatMemberHandler.CHAT_MEMBER))
            app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/f[1-4](nc(?:[1-9]|10)|slide[1-4])(\s|$)'), fx_slash_handler := lambda u, c: None))
            app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, idmute_handler), group=1)
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

            apps.append(app)
            bots.append(app.bot)
            print(f"[AYAAN OK] Bot loaded: ...{token[-10:]}")
        except Exception as e:
            print(f"[AYAAN ERROR] Failed to load token: {e}")

    if not apps:
        print("[AYAAN ERROR] No bots started.")
        return

    print(f"[AYAAN START] Running {len(apps)} bot(s)... concurrently...")

    async def start_single_app(app):
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        try:
            me = await app.bot.get_me()
            our_bot_ids.add(me.id)
        except Exception:
            pass

    await asyncio.gather(*(start_single_app(app) for app in apps))

    print(f"[AYAAN READY] All {len(apps)} bot(s) polling.")

    try:
        await asyncio.sleep(float("inf"))
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        for app in apps:
            try:
                await app.updater.stop()
                await app.stop()
                await app.shutdown()
            except Exception:
                pass

if __name__ == "__main__":
    asyncio.run(main())
