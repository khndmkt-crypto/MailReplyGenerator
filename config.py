#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作成者: こひなだ まこと
"""
MailReplyGenerator の設定管理モジュール。

- config.json を読み込んで辞書として返す
- なければデフォルト値で config.json を作成する

JSON のスキーマは README / 要件定義書に記載している内容に揃える。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


CONFIG_FILENAME = "config.json"


@dataclass
class LmStudioConfig:
    url: str = "http://localhost:1234/v1"
    model: str = "openai/gpt-oss-20b"
    api_key: str = "lm-studio"
    timeout: int = 60


@dataclass
class UiConfig:
    window_width: int = 800
    window_height: int = 600
    font_size: int = 12


@dataclass
class GenerationConfig:
    temperature: float = 0.7
    max_tokens: int = 1000


@dataclass
class LanguageDetectionConfig:
    default_language: str = "auto"
    fallback_language: str = "ja"


@dataclass
class AppConfig:
    lm_studio: LmStudioConfig
    ui: UiConfig
    generation: GenerationConfig
    language_detection: LanguageDetectionConfig

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        lm = data.get("lm_studio", {}) or {}
        ui = data.get("ui", {}) or {}
        gen = data.get("generation", {}) or {}
        lang = data.get("language_detection", {}) or {}

        return cls(
            lm_studio=LmStudioConfig(
                url=str(lm.get("url", LmStudioConfig.url)),
                model=str(lm.get("model", LmStudioConfig.model)),
                api_key=str(lm.get("api_key", LmStudioConfig.api_key)),
                timeout=int(lm.get("timeout", LmStudioConfig.timeout)),
            ),
            ui=UiConfig(
                window_width=int(ui.get("window_width", UiConfig.window_width)),
                window_height=int(ui.get("window_height", UiConfig.window_height)),
                font_size=int(ui.get("font_size", UiConfig.font_size)),
            ),
            generation=GenerationConfig(
                temperature=float(gen.get("temperature", GenerationConfig.temperature)),
                max_tokens=int(gen.get("max_tokens", GenerationConfig.max_tokens)),
            ),
            language_detection=LanguageDetectionConfig(
                default_language=str(
                    lang.get("default_language", LanguageDetectionConfig.default_language)
                ),
                fallback_language=str(
                    lang.get("fallback_language", LanguageDetectionConfig.fallback_language)
                ),
            ),
        )


def _default_config_dict() -> Dict[str, Any]:
    """デフォルト設定の辞書を返す。config.json 新規作成時にも利用する。"""
    return {
        "lm_studio": {
            "url": LmStudioConfig.url,
            "model": LmStudioConfig.model,
            "api_key": LmStudioConfig.api_key,
            "timeout": LmStudioConfig.timeout,
        },
        "ui": {
            "window_width": UiConfig.window_width,
            "window_height": UiConfig.window_height,
            "font_size": UiConfig.font_size,
        },
        "generation": {
            "temperature": GenerationConfig.temperature,
            "max_tokens": GenerationConfig.max_tokens,
        },
        "language_detection": {
            "default_language": LanguageDetectionConfig.default_language,
            "fallback_language": LanguageDetectionConfig.fallback_language,
        },
    }


def ensure_default_config_file(base_dir: Path) -> Path:
    """base_dir 配下に config.json がなければデフォルト値で作成する。"""
    cfg_path = base_dir / CONFIG_FILENAME
    if cfg_path.exists():
        return cfg_path

    data = _default_config_dict()
    cfg_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return cfg_path


def load_config(base_dir: Path | None = None) -> AppConfig:
    """設定ファイルを読み込んで AppConfig を返す。"""
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent

    cfg_path = ensure_default_config_file(base_dir)
    text = cfg_path.read_text(encoding="utf-8")
    data = json.loads(text)
    return AppConfig.from_dict(data)


__all__ = [
    "AppConfig",
    "LmStudioConfig",
    "UiConfig",
    "GenerationConfig",
    "LanguageDetectionConfig",
    "load_config",
]
