![第06章: MCP サーバー](images/chapter-header.png)

> **Copilot が GitHub のイシューを読んだり、データベースを確認したり、ターミナルから PR を作成したりできたら、どうなるでしょう？**

これまで Copilot が扱えるのは、`@` で直接参照したファイル、会話の履歴、そして学習済みのデータだけでした。しかし、自分で GitHub リポジトリを確認したり、プロジェクトのファイルを調べたり、ライブラリの最新ドキュメントを検索したりできたら、どうなるでしょう？

それを実現するのが **MCP（Model Context Protocol）** です。MCP は Copilot を外部サービスに接続し、リアルタイムの実世界データへのアクセスを可能にする仕組みです。Copilot が接続する各サービスのことを「MCP サーバー」と呼びます。この章では、いくつかの接続を設定して、MCP が Copilot をどれほど強力にするかを実際に体験します。

> 💡 **MCP をご存知の方へ**: [クイックスタート](#-built-in-github-mcp-を使ってみよう) に進んで動作確認と設定を始めましょう。

## 🎯 学習目標

この章の終わりまでに、次のことができるようになります。

- MCP とは何か、なぜ重要かを理解する
- `/mcp` コマンドで MCP サーバーを管理する
- GitHub、filesystem、ドキュメント用の MCP サーバーを設定する
- book app プロジェクトで MCP を活用したワークフローを使う
- カスタム MCP サーバーをいつ・どう作るかを知る（オプション）

> ⏱️ **所要時間**: 約50分（読書15分 + 実践35分）

---

## 🧩 実世界のたとえ: ブラウザ拡張機能

<img src="images/browser-extensions-analogy.png" alt="MCP Servers are like Browser Extensions" width="800"/>

MCP サーバーはブラウザの拡張機能に似ています。ブラウザそのままでもウェブページは表示できますが、拡張機能を使うことで追加のサービスに接続できるようになります。

| ブラウザ拡張機能 | 接続先 | MCP での対応 |
|----------------|--------|------------|
| パスワードマネージャー | パスワード保管庫 | **GitHub MCP** → リポジトリ、イシュー、PR |
| Grammarly | 文章解析サービス | **Context7 MCP** → ライブラリドキュメント |
| ファイルマネージャー | クラウドストレージ | **Filesystem MCP** → ローカルプロジェクトファイル |

拡張機能なしでもブラウザは役に立ちますが、拡張機能があればより強力になります。MCP サーバーも Copilot に対して同じ効果をもたらします。GitHub のイシューを読んだり、ファイルシステムを探索したり、最新のドキュメントを取得したりと、リアルなデータソースに Copilot を接続します。

***MCP サーバーは Copilot を外の世界—GitHub、リポジトリ、ドキュメントなど—に接続します***

> 💡 **重要なポイント**: MCP なしの場合、Copilot は `@` で明示的に共有したファイルしか見られません。MCP があれば、プロジェクトを自律的に探索したり、GitHub リポジトリを確認したり、ドキュメントを検索したりできます。すべて自動で行われます。

---

<img src="images/quick-start-mcp.png" alt="Power cable connecting with bright electrical spark surrounded by floating tech icons representing MCP server connections" width="800"/>

# クイックスタート: 30秒で MCP を体験

## Built-in GitHub MCP を使ってみよう
何も設定しなくても、今すぐ MCP を体験できます。
GitHub MCP サーバーはデフォルトで組み込まれています。試してみましょう：

```bash
copilot
> List the recent commits in this repository
```

Copilot が実際のコミットデータを返してきたら、MCP が動いている証拠です。それが GitHub MCP サーバーで、あなたの代わりに GitHub にアクセスしています。でも GitHub は*一つの*サーバーに過ぎません。この章では、さらに多くのサーバー（ファイルシステムアクセス、最新ドキュメントなど）を追加して、Copilot をさらに便利にする方法を学びます。

---

## `/mcp show` コマンド

`/mcp show` を使うと、設定されている MCP サーバーの一覧と有効化状況を確認できます：

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub サーバーしか表示されない場合**: それは正常です！追加の MCP サーバーをまだ設定していなければ、GitHub のみが表示されます。次のセクションで追加していきます。

> 📚 **MCP 管理コマンドをすべて確認したい場合**: サーバーはチャット内の `/mcp` スラッシュコマンドか、ターミナルから直接 `copilot mcp` で管理できます。この章の末尾にある[コマンドリファレンス](#-追加の-mcp-コマンド)をご覧ください。

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![MCP Status Demo](images/mcp-status-demo.gif)

*デモの出力は異なる場合があります。使用するモデル、ツール、応答内容はここに示したものと異なります。*

</details>

---

## MCP があると何が変わるの？

実際のところ、MCP があるとこう違います：

**MCP なし:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**MCP あり:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP によって Copilot は実際の開発環境を把握できるようになります。

> 📚 **公式ドキュメント**: MCP が GitHub Copilot とどう連携するかを詳しく知りたい方は [About MCP](https://docs.github.com/copilot/concepts/context/mcp) をご覧ください。

---

# MCP サーバーの設定

<img src="images/configuring-mcp-servers.png" alt="Hands adjusting knobs and sliders on a professional audio mixing board representing MCP server configuration" width="800"/>

MCP の動作を確認したところで、追加のサーバーを設定しましょう。このセクションでは設定ファイルの書き方と新しいサーバーの追加方法を説明します。

---

## MCP 設定ファイル

MCP サーバーは `~/.copilot/mcp-config.json`（ユーザーレベル、すべてのプロジェクトに適用）または `.vscode/mcp.json`（プロジェクトレベル、現在のワークスペースのみに適用）で設定します。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*ほとんどの MCP サーバーは npm パッケージとして配布されており、`npx` コマンドで実行します。*

<details>
<summary>💡 <strong>JSON を初めて触る方へ</strong>: 各フィールドの意味はこちら</summary>

| フィールド | 意味 |
|-----------|------|
| `"mcpServers"` | すべての MCP サーバー設定を格納するコンテナ |
| `"server-name"` | 自分で決める名前（例: "github"、"filesystem"） |
| `"type": "local"` | サーバーが自分のマシン上で動く |
| `"command": "npx"` | 実行するプログラム（npx は npm パッケージを実行する） |
| `"args": [...]` | コマンドに渡す引数 |
| `"tools": ["*"]` | このサーバーのすべてのツールを許可する |

**JSON の重要なルール:**
- 文字列にはダブルクォート `"` を使う（シングルクォートは不可）
- 最後の項目の後にカンマを付けない
- 有効な JSON でなければならない（不安な場合は [JSON バリデーター](https://jsonlint.com/) を利用）

</details>

---

## MCP サーバーの追加

GitHub MCP サーバーは組み込みで設定不要です。以下に追加できるサーバーを紹介します。**興味のあるものを選ぶか、順番に試してみましょう。**

| やりたいこと | 移動先 |
|---|---|
| Copilot にプロジェクトファイルを見てもらう | [Filesystem サーバー](#filesystem-server) |
| 最新のライブラリドキュメントを取得する | [Context7 サーバー](#context7-server-documentation) |
| オプションの応用（カスタムサーバー、web_fetch） | [応用編](#beyond-the-basics) |

<details>
<summary><strong>Filesystem サーバー</strong> - Copilot にプロジェクトファイルを探索させる</summary>
<a id="filesystem-server"></a>

### Filesystem サーバー

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` パスについて**: `.` は「カレントディレクトリ」を意味します。Copilot は起動した場所を基準にファイルにアクセスします。Codespace では、これはワークスペースのルートになります。`/workspaces/copilot-cli-for-beginners` のような絶対パスでも構いません。

これを `~/.copilot/mcp-config.json` に追加して Copilot を再起動してください。

</details>

<details>
<summary><strong>Context7 サーバー</strong> - 最新のライブラリドキュメントを取得する</summary>
<a id="context7-server-documentation"></a>

### Context7 サーバー（ドキュメント）

Context7 は、人気のフレームワークやライブラリの最新ドキュメントへのアクセスを Copilot に提供します。古くなっているかもしれない学習データに頼るのではなく、実際の現行ドキュメントを取得します。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **コードはローカルに保持**

これを `~/.copilot/mcp-config.json` に追加して Copilot を再起動してください。

</details>

<details>
<summary><strong>応用編</strong> - カスタムサーバーとウェブアクセス（オプション）</summary>
<a id="beyond-the-basics"></a>

これらは、上記のコアサーバーに慣れた後で試せるオプションです。

### Microsoft Learn MCP サーバー

これまで紹介してきた MCP サーバー（filesystem、Context7）はすべて自分のマシン上で動きます。しかし MCP サーバーはリモートでも動作できます。つまり Copilot CLI に URL を教えるだけで、あとは自動で処理されます。`npx` も `python` も、ローカルプロセスも、インストールすべき依存関係も不要です。

[Microsoft Learn MCP Server](https://github.com/microsoftdocs/mcp) はその好例です。Copilot CLI に公式 Microsoft ドキュメント（Azure、Microsoft Foundry などの AI トピック、.NET、Microsoft 365 など）への直接アクセスを提供し、モデルの学習データに頼らずにドキュメントを検索したり、全ページを取得したり、公式コードサンプルを探したりできます。

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **ローカルインストール不要**

**`/plugin install` でクイックインストール:**

JSON 設定ファイルを手動で編集する代わりに、1コマンドでインストールできます：

```bash
copilot

> /plugin install microsoftdocs/mcp
```

これによりサーバーと関連する agent skills が自動的に追加されます。インストールされる skills は以下のとおりです：

- **microsoft-docs**: コンセプト、チュートリアル、ファクトの検索
- **microsoft-code-reference**: API 検索、コードサンプル、トラブルシューティング
- **microsoft-skill-creator**: Microsoft テクノロジーに関するカスタム skill を生成するメタスキル

**使用例:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 詳細: [Microsoft Learn MCP Server の概要](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch` によるウェブアクセス

Copilot CLI には、任意の URL からコンテンツを取得できる組み込みの `web_fetch` ツールが含まれています。ターミナルを離れることなく README や API ドキュメント、リリースノートを参照するのに便利です。MCP サーバーは不要です。

アクセス可能な URL は `~/.copilot/config.json`（Copilot の一般設定）で制御できます。これは MCP サーバー定義を記述する `~/.copilot/mcp-config.json` とは別のファイルです。

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**使用例:**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### カスタム MCP サーバーの構築

自分の API、データベース、社内ツールに Copilot を接続したいですか？Python でカスタム MCP サーバーを構築できます。事前構築済みサーバー（GitHub、filesystem、Context7）でほとんどのユースケースはカバーできるため、これは完全にオプションです。

📖 book app を例にした完全なウォークスルーは [カスタム MCP サーバーガイド](mcp-custom-server.md) をご覧ください。

📚 背景知識については [MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners) を参照してください。

</details>

<a id="complete-configuration-file"></a>

### 設定ファイルの完成形

filesystem と Context7 サーバーを含む `mcp-config.json` の完全な例です：

> 💡 **注意:** GitHub MCP は組み込みです。設定ファイルに追加する必要はありません。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

グローバルに使うには `~/.copilot/mcp-config.json` として、プロジェクト固有の設定には `.vscode/mcp.json` として保存してください。

---

# MCP サーバーを使う

MCP サーバーの設定ができたところで、実際に何ができるか見ていきましょう。

<img src="images/using-mcp-servers.png" alt="Using MCP Servers - Hub-and-spoke diagram showing a Developer CLI connected to GitHub, Filesystem, Context7, and Custom/Web Fetch servers" width="800" />

---

## サーバーの使用例

**気になるサーバーを選んで試すか、順番に進めましょう。**

| 試したいこと | 移動先 |
|---|---|
| GitHub のリポジトリ、イシュー、PR | [GitHub サーバー](#github-server-built-in) |
| プロジェクトファイルの閲覧 | [Filesystem サーバーの使用](#filesystem-server-usage) |
| ライブラリドキュメントの検索 | [Context7 サーバーの使用](#context7-server-usage) |
| カスタムサーバー、Microsoft Learn MCP、web_fetch の使用 | [応用編の使用例](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub サーバー（組み込み）</strong> - リポジトリ、イシュー、PR などにアクセス</summary>
<a id="github-server-built-in"></a>

### GitHub サーバー（組み込み）

GitHub MCP サーバーは**組み込み**です。Copilot にログインしていれば（初期設定時に行ったはずです）、すでに使えます。設定は不要です！

> 💡 **動かない場合**: `/login` を実行して GitHub で再認証してください。

<details>
<summary><strong>Dev Container での認証</strong></summary>

- **GitHub Codespaces**（推奨）: 認証は自動です。`gh` CLI が Codespace のトークンを継承します。何もしなくて OK。
- **ローカル dev container（Docker）**: コンテナ起動後に `gh auth login` を実行し、Copilot を再起動してください。

**認証のトラブルシューティング:**
```bash
# 認証済みかどうかを確認する
gh auth status

# 未認証の場合はログインする
gh auth login

# GitHub MCP が接続されていることを確認する
copilot
> /mcp show
```

</details>

| 機能 | 例 |
|------|----|
| **リポジトリ情報** | コミット、ブランチ、コントリビューターを表示 |
| **イシュー** | イシューの一覧表示、作成、検索、コメント |
| **プルリクエスト** | PR の表示、差分確認、PR 作成、ステータス確認 |
| **コード検索** | リポジトリ横断でコードを検索 |
| **Actions** | ワークフローの実行状況とステータスを確認 |

```bash
copilot

# このリポジトリの最近の活動を確認する
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# リポジトリ構造を調べる
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# リポジトリ横断でコードパターンを検索する
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **自分のフォークで作業している場合**: このコースリポジトリをフォークしていれば、イシューの作成やプルリクエストなどの書き込み操作も試せます。以降の演習で実践します。

> ⚠️ **結果が表示されない場合**: GitHub MCP はリモート（github.com 上）のリポジトリを対象に動作します。ローカルファイルだけでなく、リモートが設定されているか `git remote -v` で確認してください。

</details>

<details>
<summary><strong>Filesystem サーバー</strong> - プロジェクトファイルの閲覧と分析</summary>
<a id="filesystem-server-usage"></a>

### Filesystem サーバー

設定すると、filesystem MCP は Copilot が自動的に使えるツールを提供します：

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7 サーバー</strong> - ライブラリドキュメントを検索する</summary>
<a id="context7-server-usage"></a>

### Context7 サーバー

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot now knows the official pytest patterns
# and can apply them to samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>応用編</strong> - カスタムサーバーと web_fetch の使用例</summary>
<a id="beyond-the-basics-usage"></a>

### 応用編

**カスタム MCP サーバー**: [カスタム MCP サーバーガイド](mcp-custom-server.md) に従って book-lookup サーバーを構築した場合、ブックコレクションに直接クエリを実行できます：

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**: [Microsoft Learn MCP サーバー](#microsoft-learn-mcp-サーバー)をインストールした場合、公式 Microsoft ドキュメントを直接検索できます：

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**: 組み込みの `web_fetch` ツールを使って任意の URL からコンテンツを取得します：

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## マルチサーバーワークフロー

これらのワークフローが、開発者が「もうこれなしでは仕事できない」と言う理由です。各例では、1つのセッションで複数の MCP サーバーを組み合わせています。

<img src="images/issue-to-pr-workflow.png" alt="Issue to PR Workflow using MCP - Shows the complete flow from getting a GitHub issue through creating a pull request" width="800"/>

*完全な MCP ワークフロー: GitHub MCP がリポジトリデータを取得し、Filesystem MCP がコードを見つけ、Context7 MCP がベストプラクティスを提供し、Copilot が分析を担当する*

以下の各例は独立しています。**気になるものを選ぶか、すべて読み進めましょう。**

| 見たいこと | 移動先 |
|---|---|
| 複数サーバーの連携 | [マルチサーバー探索](#multi-server-exploration) |
| イシューから PR まで一気に | [Issue-to-PR ワークフロー](#issue-to-pr-workflow) |
| プロジェクトの健全性を素早く確認 | [ヘルスダッシュボード](#health-dashboard) |

<details>
<summary><strong>マルチサーバー探索</strong> - filesystem、GitHub、Context7 を1つのセッションで組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数の MCP サーバーで Book App を探索する

```bash
copilot

# Step 1: filesystem MCP を使って book app を探索する
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Step 2: GitHub MCP を使って最近の変更を確認する
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Step 3: Context7 MCP でベストプラクティスを調べる
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Step 4: 推奨事項をまとめる
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 MCP ワークフローを実際に見てみましょう！</summary>

![MCP Workflow Demo](images/mcp-workflow-demo.gif)

*デモの出力は異なる場合があります。使用するモデル、ツール、応答内容はここに示したものと異なります。*

</details>

**結果**: コード探索 → 変更履歴の確認 → ベストプラクティスの検索 → 改善案の提示。**3つの MCP サーバーを組み合わせて、すべて1つのターミナルセッションから実現します。**

</details>

<details>
<summary><strong>Issue-to-PR ワークフロー</strong> - ターミナルを離れずに GitHub イシューからプルリクエストを作成する</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue-to-PR ワークフロー（自分のリポジトリで）

書き込み権限のある自分のフォークまたはリポジトリで最も効果的です：

> 💡 **今すぐ試せなくても大丈夫です。** 読み取り専用のクローンでは、課題で練習します。今はフローを理解するために読み進めましょう。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**コピー＆ペーストなし。コンテキストの切り替えなし。1つのターミナルセッションで完結。**

</details>

<details>
<summary><strong>ヘルスダッシュボード</strong> - 複数サーバーを使ったプロジェクトの素早い健全性チェック</summary>
<a id="health-dashboard"></a>

#### Book App ヘルスダッシュボード

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**結果**: 複数のデータソースを数秒で集約。手動でやるなら grep を実行して、行数を数えて、git log を確認して、テストファイルを参照して…と15分以上かかる作業です。

</details>

---

# 演習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

**🎉 基本はマスターしました！** MCP が何か、サーバーの設定方法、実際のワークフローを理解できました。次は自分で試してみましょう。

---

## ▶️ 自分でやってみよう

今度はあなたの番です！book app プロジェクトで MCP サーバーを使う練習をしましょう。

### 演習 1: MCP のステータスを確認する

まず、どの MCP サーバーが使えるか確認しましょう：

```bash
copilot

> /mcp show
```

GitHub サーバーが有効として表示されるはずです。表示されない場合は `/login` を実行して認証してください。

---

### 演習 2: Filesystem MCP で Book App を探索する

filesystem サーバーを設定済みの場合、それを使って book app を探索してみましょう：

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**期待される結果**: Copilot が `book_app.py`、`books.py`、`utils.py` を関数とともに一覧表示します。

> 💡 **filesystem MCP をまだ設定していない場合**: 上記の[設定ファイルの完成形](#complete-configuration-file)セクションから設定ファイルを作成してください。その後 Copilot を再起動します。

---

### 演習 3: GitHub MCP でリポジトリ履歴を照会する

組み込みの GitHub MCP を使って、このコースリポジトリを探索しましょう：

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**期待される結果**: Copilot が GitHub リモートから最近のコミットメッセージとブランチ名を表示します。

> ⚠️ **Codespace を使っている場合**: 認証が自動で引き継がれるため、これは自動的に動作します。ローカルクローンの場合は `gh auth status` でログイン済みかどうかを確認してください。

---

### 演習 4: 複数の MCP サーバーを組み合わせる

filesystem と GitHub MCP を1つのセッションで組み合わせてみましょう：

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**期待される結果**: Copilot が JSON ファイルを読み取り（filesystem MCP）、"The Hobbit"、"1984"、"Dune"、"To Kill a Mockingbird"、"Mysterious Book" の5冊を一覧表示した後、GitHub でコミット履歴を照会します。

**理解度チェック**: 「Check my repo's commit history」という依頼が、手動で `git log` を実行して結果をプロンプトに貼り付けるよりなぜ優れているかを説明できたら、MCP を理解できた証拠です。

---

## 📝 課題

### メインチャレンジ: Book App の MCP 探索

book app プロジェクトで MCP サーバーを組み合わせて使ってみましょう。1つの Copilot セッションで以下を完了してください：

1. **MCP が動作していることを確認する**: `/mcp show` を実行して GitHub サーバーが有効になっていることを確認する
2. **filesystem MCP を設定する**（まだの場合）: filesystem サーバー設定を含む `~/.copilot/mcp-config.json` を作成する
3. **コードを探索する**: filesystem サーバーを使って Copilot に以下を依頼する
   - `samples/book-app-project/books.py` のすべての関数を一覧表示する
   - `samples/book-app-project/utils.py` で型ヒントが欠けている関数を確認する
   - `samples/book-app-project/data.json` を読み取り、データ品質の問題を特定する（ヒント: 最後のエントリを確認）
4. **リポジトリの活動を確認する**: GitHub MCP を使って Copilot に以下を依頼する
   - `samples/book-app-project/` のファイルに触れた最近のコミットを一覧表示する
   - 未解決のイシューやプルリクエストがあるか確認する
5. **サーバーを組み合わせる**: 1つのプロンプトで Copilot に以下を依頼する
   - `samples/book-app-project/tests/test_books.py` のテストファイルを読み取る
   - テスト済みの関数と `books.py` のすべての関数を比較する
   - 不足しているテストカバレッジをまとめる

**成功の基準**: filesystem と GitHub MCP のデータを1つの Copilot セッションでシームレスに組み合わせられ、各 MCP サーバーが応答にどう貢献したかを説明できる。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**ステップ 1: MCP を確認する**
```bash
copilot
> /mcp show
# "github" が有効と表示されるはず
# 表示されない場合は: /login
```

**ステップ 2: 設定ファイルを作成する**

上記の[設定ファイルの完成形](#complete-configuration-file)セクションの JSON を `~/.copilot/mcp-config.json` として保存してください。

**ステップ 3: 探すべきデータ品質の問題**

`data.json` の最後の書籍はこちらです：
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
著者が空で year が 0。これがデータ品質の問題です！

**ステップ 5: テストカバレッジの比較**

`test_books.py` のテストがカバーしているのは `add_book`、`mark_as_read`、`remove_book`、`get_unread_books`、`find_book_by_title` です。`load_books`、`save_books`、`list_books` などの関数には直接のテストがありません。`book_app.py` の CLI 関数と `utils.py` のヘルパー関数にはテストがまったくありません。

**MCP が動作しない場合**: 設定ファイルを編集した後に Copilot を再起動してください。

</details>

### ボーナスチャレンジ: カスタム MCP サーバーを構築する

さらに深く掘り下げてみましょう。[カスタム MCP サーバーガイド](mcp-custom-server.md) に従って、任意の API に接続する独自の MCP サーバーを Python で構築してみましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起きるか | 対処法 |
|--------|------------|--------|
| GitHub MCP が組み込みだと知らない | 手動でインストール・設定しようとする | GitHub MCP はデフォルトで組み込まれています。試してみましょう: "List the recent commits in this repo" |
| 設定ファイルの場所が違う | MCP 設定を見つけられない、または編集できない | ユーザーレベルの設定は `~/.copilot/mcp-config.json`、プロジェクトレベルは `.vscode/mcp.json` |
| 設定ファイルの JSON が無効 | MCP サーバーの読み込みに失敗する | `/mcp show` で設定を確認し、JSON 構文を検証する |
| MCP サーバーの認証を忘れる | "Authentication failed" エラー | 一部の MCP は個別の認証が必要です。各サーバーの要件を確認してください |

### トラブルシューティング

**「MCP server not found」の場合** - 以下を確認してください：
1. npm パッケージが存在すること: `npm view @modelcontextprotocol/server-github`
2. 設定ファイルが有効な JSON であること
3. サーバー名が設定と一致していること

現在の設定を確認するには `/mcp show` を使ってください。

**「GitHub authentication failed」の場合** - 組み込みの GitHub MCP は `/login` の認証情報を使います。試してみましょう：

```bash
copilot
> /login
```

これで GitHub との再認証が行われます。問題が続く場合は、GitHub アカウントがアクセスしようとしているリポジトリに必要な権限を持っているか確認してください。

**「MCP server failed to start」の場合** - サーバーのログを確認してください：
```bash
# サーバーコマンドを手動で実行してエラーを確認する
npx -y @modelcontextprotocol/server-github
```

**MCP ツールが使えない場合** - サーバーが有効になっているか確認してください：
```bash
copilot

> /mcp show
# サーバーが一覧に表示され、有効になっているか確認する
```

サーバーが無効になっている場合は、再有効化の方法について以下の[追加の `/mcp` コマンド](#-追加の-mcp-コマンド)を参照してください。

</details>

---

<details>
<summary>📚 <strong>追加の MCP コマンド</strong>（クリックして展開）</summary>
<a id="-追加の-mcp-コマンド"></a>

MCP サーバーを管理する方法は2つあります: **チャットセッション内のスラッシュコマンド**を使う方法と、**ターミナルから直接 `copilot mcp` コマンド**を使う方法（チャットセッション不要）です。

### オプション 1: スラッシュコマンド（チャットセッション内）

`copilot` の中にいるときに使えます：

| コマンド | 機能 |
|---------|------|
| `/mcp show` | 設定済みの MCP サーバーとそのステータスを表示 |
| `/mcp add` | 新しいサーバーを対話形式で追加 |
| `/mcp edit <server-name>` | 既存のサーバー設定を編集 |
| `/mcp enable <server-name>` | 無効なサーバーを有効化（セッションをまたいで持続） |
| `/mcp disable <server-name>` | サーバーを無効化（セッションをまたいで持続） |
| `/mcp delete <server-name>` | サーバーを完全に削除 |
| `/mcp auth <server-name>` | OAuth を使う MCP サーバーで再認証（アカウント切り替え後など） |

### オプション 2: `copilot mcp` コマンド（ターミナルから）

チャットセッションを開始せずに、ターミナルから直接 MCP サーバーを管理することもできます：

```bash
# 設定済みの MCP サーバーをすべて一覧表示する
copilot mcp list

# サーバーを有効化する
copilot mcp enable filesystem

# サーバーを無効化する
copilot mcp disable context7
```

> 💡 **どちらを使う？** チャットセッション中は `/mcp` スラッシュコマンドを使いましょう。セッションを始める前にサーバー設定を素早く確認・変更したい場合は、ターミナルから `copilot mcp` を使いましょう。

このコースでは `/mcp show` で十分です。他のコマンドは、サーバーが増えてきた際の管理に役立ちます。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **MCP** は Copilot を外部サービス（GitHub、filesystem、ドキュメント）に接続する
2. **GitHub MCP は組み込み** - `/login` するだけで設定不要
3. **Filesystem と Context7** は `~/.copilot/mcp-config.json` で設定する
4. **マルチサーバーワークフロー** では1つのセッションで複数のデータソースを組み合わせられる
5. **2つの管理方法**: チャット内の `/mcp` スラッシュコマンドか、ターミナルから `copilot mcp`
6. **カスタムサーバー** で任意の API に接続できる（オプション、付録ガイドに記載）

> 📋 **クイックリファレンス**: コマンドとショートカットの完全な一覧は [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) をご覧ください。

---

## ➡️ 次のステップ

これですべての構成要素が揃いました: モード、コンテキスト、ワークフロー、agents、skills、そして MCP。いよいよすべてを組み合わせる時です。

**[第07章: 総まとめ](../07-putting-it-together/README.md)** では以下を学びます：

- agents、skills、MCP を統合ワークフローで組み合わせる
- アイデアからマージされた PR までの完全な機能開発
- フックによる自動化
- チーム環境でのベストプラクティス

---

**[← 第05章に戻る](../05-skills/README.md)** | **[第07章に進む →](../07-putting-it-together/README.md)**
