#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作成者: こひなだ まこと
"""メールテキストの前処理と言語判定ロジック。"""

from __future__ import annotations

import logging
import re
from typing import Literal

logger = logging.getLogger(__name__)

Language = Literal["ja", "en"]


def normalize_newlines(text: str) -> str:
    """改行コードを統一し、末尾の空行を整理する。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 連続空行を 2 行までに抑える
    text = re.sub("\n{3,}", "\n\n", text)
    return text.strip()


def detect_language(text: str) -> Language:
    """非常にシンプルなヒューリスティックで日本語/英語を判定する。"""
    # ひらがな・カタカナの出現数で判定
    jp_chars = re.findall(r"[ぁ-んァ-ン]", text)
    if len(jp_chars) > 0:
        return "ja"
    return "en"


__all__ = ["normalize_newlines", "detect_language", "Language"]
