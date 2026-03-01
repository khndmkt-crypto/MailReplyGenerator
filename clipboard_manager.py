#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作成者: こひなだ まこと
"""クリップボード操作ユーティリティ。"""

from __future__ import annotations

import logging
from typing import Optional

import pyperclip

logger = logging.getLogger(__name__)


def get_text_from_clipboard() -> str:
    """クリップボードからテキストを取得する。

    取得できない場合は ValueError を送出する。
    """
    try:
        text = pyperclip.paste()
    except Exception as exc:  # pragma: no cover - 環境依存
        logger.exception("クリップボード取得中にエラーが発生しました")
        raise ValueError("クリップボードからテキストを取得できませんでした") from exc

    if not isinstance(text, str) or not text.strip():
        raise ValueError("クリップボードに有効なテキストがありません")

    return text


def set_text_to_clipboard(text: str) -> None:
    """テキストをクリップボードに設定する。"""
    try:
        pyperclip.copy(text)
    except Exception as exc:  # pragma: no cover - 環境依存
        logger.exception("クリップボードへのコピー中にエラーが発生しました")
        raise ValueError("クリップボードにコピーできませんでした") from exc


__all__ = ["get_text_from_clipboard", "set_text_to_clipboard"]
