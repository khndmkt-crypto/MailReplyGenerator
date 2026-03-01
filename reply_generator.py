#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作成者: こひなだ まこと
"""
MailReplyGenerator の返信生成モジュール。

LM Studio の OpenAI 互換 API を使って、受信メールと返信概要から返信文を生成する。
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from config import AppConfig

logger = logging.getLogger(__name__)


class ReplyGenerator:
    """LM Studio を用いてメール返信文を生成する。"""

    def __init__(self, config: "AppConfig") -> None:
        self.config = config

    def generate(self, email_text: str, summary: str, lang: str) -> str:
        """
        受信メールと返信概要から返信文を生成する。

        Args:
            email_text: 受信メール本文
            summary: 返信の概要（ユーザー入力）
            lang: 言語コード（"ja" / "en" など）

        Returns:
            生成された返信文
        """
        lm = self.config.lm_studio
        gen = self.config.generation

        if lang == "ja":
            lang_instruction = "返信は日本語で、自然なビジネスメールの文体で書いてください。"
        else:
            lang_instruction = """返信は英語で書いてください。
「返信の概要」はユーザーが日本語で入力している場合があります。概要の内容を逐語英訳するのではなく、概要の意図（何を伝えたいか）を汲み取り、受信メールへの適切な英語の返信として自然に書いてください。英語圏のビジネスメールの慣習に沿った文体にしてください。"""

        prompt = f"""以下は受信したメールです。このメールに対する返信を、ユーザーが指定した「返信の概要」の意図に従って作成してください。
返信文のみを出力し、件名・ヘッダー・説明文は一切書かないでください。

{lang_instruction}

【受信メール】
{email_text}

【返信の概要】
{summary}

【返信文】
"""

        url = f"{lm.url.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {lm.api_key}",
        }
        payload = {
            "model": lm.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": gen.temperature,
            "max_tokens": gen.max_tokens,
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=lm.timeout,
        )
        response.raise_for_status()
        data = response.json()

        reply = ""
        for choice in data.get("choices", []):
            msg = choice.get("message", {})
            if isinstance(msg.get("content"), str):
                reply = msg["content"].strip()
                break

        if not reply:
            raise ValueError("LM Studio から返信文が取得できませんでした。")

        return reply
