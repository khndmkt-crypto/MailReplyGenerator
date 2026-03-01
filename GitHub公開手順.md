# MailReplyGenerator を GitHub で公開する手順

## 公開の2つの方法

| 方法 | 内容 | 向いている場合 |
|------|------|----------------|
| **A. MacAutomator の一部として** | MacAutomator 全体を1つのリポジトリで push する。MailReplyGenerator はその中に含まれる | 他のツール（LaunchProject 等）もまとめて公開したい |
| **B. 単独リポジトリとして** | MailReplyGenerator だけのリポジトリを作り、このフォルダの中身だけを push する | MailReplyGenerator だけを独立したプロジェクトとして公開したい |

---

## 方法A vs 方法B：メリット・デメリット

| 観点 | 方法A（MacAutomator の一部） | 方法B（単独リポジトリ） |
|------|------------------------------|--------------------------|
| **管理の手間** | **メリット**: リポジトリは1つだけ。push も1回で全ツールが更新される。 | **デメリット**: リポジトリが増える。MacAutomator と MailReplyGenerator の両方で変更を反映する手間がかかることがある。 |
| **発見されやすさ** | **デメリット**: 「メール返信ツール」で探す人には、MacAutomator という名前では見つけにくい。 | **メリット**: リポジトリ名が「MailReplyGenerator」なので、検索・共有しやすい。 |
| **スター・フォーク** | **デメリット**: スターは MacAutomator 全体につく。MailReplyGenerator 単体の人気は分かりにくい。 | **メリット**: このツール専用のスター・フォーク数で人気が分かる。 |
| **依存・説明** | **メリット**: 他のツール（LaunchProject 等）と一緒に「論文・講演用自動化ツール群」として説明しやすい。 | **デメリット**: 単体なので、MacAutomator の文脈は README で補足する必要がある。 |
| **クローンして使う人** | **デメリット**: 全ツールを clone することになり、使わないツールのファイルも一緒についてくる。 | **メリット**: 必要な人だけ「MailReplyGenerator だけ」を clone でき、軽い。 |
| **更新の一貫性** | **メリット**: 1リポジトリなので、.gitignore・LICENSE・共通ルールの更新が一括で済む。 | **デメリット**: 単独リポジトリを別に作ると、後から MacAutomator 側を更新しても自動では反映されない。 |
| **将来の分離** | **デメリット**: のちに「MailReplyGenerator だけ別リポジトリにしたい」となると、subtree 分割などの作業が必要。 | **メリット**: 最初から分離しているので、その手間は不要。 |
| **ライセンス** | 1つの LICENSE を MacAutomator 全体で共有。 | MailReplyGenerator 専用のライセンスを設定できる。 |

**まとめ**

- **まずは MacAutomator 全体を公開し、後から必要なら MailReplyGenerator を単独でも公開する**（A を先にやって、B は必要に応じて）という進め方も可能です。
- **「メール返信生成ツール」としてだけ宣伝・共有したい**なら、方法Bの単独リポジトリの方が向いています。

---

## 方法A: MacAutomator の一部として公開する

MacAutomator を GitHub に push すれば、MailReplyGenerator も含めて公開されます。

1. **MacAutomator ルート**の手順に従う: [MacAutomator_GitHub管理手順.md](../MacAutomator_GitHub管理手順.md)
2. `config.json` は MacAutomator ルートの `.gitignore` で除外されているため、GitHub には `config.json.example` のみが含まれる
3. ほかは追加作業なし

---

## 方法B: MailReplyGenerator だけを単独リポジトリとして公開する

### B-1. GitHub でリポジトリを作成

1. GitHub で **New repository** をクリック
2. **Repository name**: `MailReplyGenerator` など
3. **Public** を選択
4. **Add a README file** はチェックしない（ローカルから push するため）
5. **Add a license**: オープンソースにするなら **MIT License** を選択（後から追加も可）
6. **Create repository**
7. 表示される URL（HTTPS または SSH）を控える

### B-2. ローカルで単独リポジトリを用意して push

**手順（コピーで新規リポジトリを作る場合）:**

```bash
# 作業用ディレクトリに移動（例: デスクトップ）
cd ~/Desktop

# フォルダをコピー（config.json と .log は .gitignore で除外されるので含めなくてよい）
cp -r /Users/hkanemoto/Cursor/MacAutomator/MailReplyGenerator MailReplyGenerator-repo
cd MailReplyGenerator-repo

# 機密・不要ファイルを削除（コピー先に含まれている場合）
rm -f config.json mail_reply_generator.log

# Git リポジトリとして初期化
git init
git add .
git commit -m "Initial commit: MailReplyGenerator"

# リモートを追加（URL はあなたのリポジトリに置き換え）
git remote add origin https://github.com/あなたのユーザー名/MailReplyGenerator.git

# メインブランチを main にして push
git branch -M main
git push -u origin main
```

**HTTPS** の場合は初回に GitHub の認証（Personal Access Token 等）が求められます。**SSH** を使う場合は:

```bash
git remote add origin git@github.com:あなたのユーザー名/MailReplyGenerator.git
```

### B-3. 公開前に確認すること

- [ ] `config.json` がリポジトリに含まれていない（`.gitignore` で除外）
- [ ] `config.json.example` が含まれている（利用者がコピーして使う）
- [ ] README の「ライセンス」欄を、追加した LICENSE に合わせて修正する（例: MIT を選んだ場合）

---

## README の「ライセンス」表記について

現在の README には「このプロジェクトは個人利用を目的としています。」とあります。  
GitHub で MIT 等のライセンスファイルを追加した場合は、README のライセンス欄を次のように変更すると分かりやすいです。

```markdown
## ライセンス

MIT License。詳細は [LICENSE](./LICENSE) を参照してください。
```

---

*作成: 2026-03-01*
