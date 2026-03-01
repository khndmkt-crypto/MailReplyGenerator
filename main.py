#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作成者: こひなだ まこと
"""MailReplyGenerator のエントリーポイント。"""

from __future__ import annotations

from pathlib import Path

from config import load_config
from gui import MailReplyGUI


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    config = load_config(base_dir)
    app = MailReplyGUI(config)
    app.run()


if __name__ == "__main__":  # pragma: no cover
    main()
