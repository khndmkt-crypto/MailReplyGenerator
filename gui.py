#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作成者: こひなだ まこと
"""MailReplyGenerator の tkinter GUI 実装。"""

from __future__ import annotations

import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path

from clipboard_manager import get_text_from_clipboard, set_text_to_clipboard
from config import AppConfig, load_config
from mail_processor import normalize_newlines, detect_language
from reply_generator import ReplyGenerator

logger = logging.getLogger(__name__)


class MailReplyGUI:
    """メール返信作成 GUI アプリケーション。"""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.root = tk.Tk()
        self.root.title("MailReplyGenerator")

        ui = self.config.ui
        self.root.geometry(f"{ui.window_width}x{ui.window_height}")

        self._build_widgets()
        self.generator = ReplyGenerator(self.config)

    # ウィジェット構築 -------------------------------------------------
    def _build_widgets(self) -> None:
        # 受信メール表示
        email_frame = tk.LabelFrame(self.root, text="受信メール", padx=5, pady=5)
        email_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.email_text = scrolledtext.ScrolledText(email_frame, wrap=tk.WORD, height=12)
        self.email_text.pack(fill=tk.BOTH, expand=True)

        # 返信概要入力
        summary_frame = tk.LabelFrame(self.root, text="返信の概要", padx=5, pady=5)
        summary_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

        self.summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, height=6)
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # ボタン群
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="クリップボードから取得", command=self.on_load_clipboard).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="返信生成", command=self.on_generate).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(btn_frame, text="クリア", command=self.on_clear).pack(side=tk.LEFT, padx=5)

        # ステータス表示
        self.status_var = tk.StringVar(value="準備完了")
        status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w")
        status_label.pack(fill=tk.X, padx=10, pady=(0, 10))

    # イベントハンドラ -------------------------------------------------
    def on_load_clipboard(self) -> None:
        try:
            text = get_text_from_clipboard()
        except ValueError as e:
            messagebox.showwarning("クリップボード取得エラー", str(e))
            return

        self.email_text.delete("1.0", tk.END)
        self.email_text.insert(tk.END, text)
        self.status_var.set("クリップボードから受信メールを読み込みました")

    def on_generate(self) -> None:
        email_text = self.email_text.get("1.0", tk.END).strip()
        summary = self.summary_text.get("1.0", tk.END).strip()

        if not email_text:
            messagebox.showwarning("入力エラー", "受信メールが空です。まずメールを貼り付けるか、クリップボードから取得してください。")
            return

        if not summary:
            messagebox.showwarning("入力エラー", "返信の概要を入力してください。")
            return

        email_text = normalize_newlines(email_text)
        lang = detect_language(email_text)

        self.status_var.set("返信を生成しています…")
        self.root.update_idletasks()

        try:
            reply = self.generator.generate(email_text, summary, lang)
        except Exception as e:  # pragma: no cover - 実行時依存
            logger.exception("返信生成中にエラーが発生しました")
            messagebox.showerror("エラー", f"返信生成に失敗しました: {e}")
            self.status_var.set("エラーが発生しました")
            return

        set_text_to_clipboard(reply)
        self.status_var.set("返信を生成し、クリップボードにコピーしました。メールクライアントに貼り付けてください。")
        messagebox.showinfo("完了", "返信をクリップボードにコピーしました。")

    def on_clear(self) -> None:
        self.email_text.delete("1.0", tk.END)
        self.summary_text.delete("1.0", tk.END)
        self.status_var.set("入力をクリアしました")

    # 実行 -------------------------------------------------------------
    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    config = load_config(base_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        filename=str(base_dir / "mail_reply_generator.log"),
        filemode="a",
    )

    app = MailReplyGUI(config)
    app.run()


if __name__ == "__main__":  # pragma: no cover
    main()
