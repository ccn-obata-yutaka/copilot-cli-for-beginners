![第05章: Skills システム](images/chapter-header.png)

> **Copilot が、チームのベストプラクティスを毎回説明しなくても自動で適用してくれたらどうでしょう？**

この章では、Agent Skills について学びます。Agent Skills は、関連するタスクで Copilot が自動的に読み込む指示のフォルダです。agents が Copilot の*考え方*を変えるのに対し、skills はタスクを*どう完了するか*という具体的な方法を教えます。セキュリティについて質問したときに Copilot が適用する security-audit skill を作成し、一貫したコード品質を保つためのチーム標準のレビュー基準を構築し、さらに Copilot CLI、VS Code、GitHub Copilot cloud agent 全体で skills がどう機能するかを学びます。

## 🎯 学習目標

この章の終わりまでに、次のことができるようになります。

- Agent Skills の仕組みと使いどきを理解する
- SKILL.md ファイルでカスタム skill を作成する
- 共有リポジトリのコミュニティ skill を使う
- skills、agents、MCP の使い分けを理解する

> ⏱️ **所要時間**: 約55分（読書20分 + 実践35分）

---

## 🧩 実世界のたとえ: 電動工具

一般的なドリルも便利ですが、専用のアタッチメントを付けるとさらに強力になります。
<img src="images/power-tools-analogy.png" alt="Power Tools - Skills Extend Copilot's Capabilities" width="800"/>

skills も同じです。用途に応じてドリルビットを交換するように、Copilot にもさまざまなタスク向けの skill を追加できます。

| スキルのアタッチメント | 目的 |
|------------|---------|
| `commit` | 一貫した commit message を生成する |
| `security-audit` | OWASP 脆弱性をチェックする |
| `generate-tests` | 網羅的な pytest テストを作成する |
| `code-checklist` | チームのコード品質基準を適用する |

*skills は、Copilot の機能を拡張する専用アタッチメントです*

---

# Skills の仕組み

<img src="images/how-skills-work.png" alt="光る RPG 風の skill アイコンが光の軌跡でつながり、Copilot skills を表している図" width="800"/>

skills とは何か、なぜ重要なのか、そして agents や MCP とどう違うのかを学びます。

---

## *Skills が初めてですか？* まずはこちらから！

1. **利用できる skills を確認する:**
   ```bash
   copilot
   > /skills list
   ```
   CLI に付属する **built-in skills**、プロジェクト内の skills、個人フォルダの skills を含め、Copilot が見つけられるすべての skills が表示されます。

   > 💡 **built-in skills**: Copilot CLI には、あらかじめ skills が組み込まれています。たとえば `customizing-copilot-cloud-agents-environment` skill は、Copilot cloud agent の環境をカスタマイズするためのガイドを提供します。これらを使うために何かを作成したりインストールしたりする必要はありません。利用可能なものは `/skills list` で確認できます。

2. **実際の skill file を見る:** 提供済みの [code-checklist SKILL.md](../.github/skills/code-checklist/SKILL.md) を見て、パターンを確認しましょう。YAML frontmatter と markdown の指示だけで構成されています。

3. **基本概念を理解する:** skills は、prompt が skill の description に一致したときに Copilot が*自動的*に読み込む、タスク固有の指示です。手動で有効化する必要はなく、自然に依頼するだけで使えます。

## Skills を理解する

Agent Skills は、指示、scripts、resources を含む folders で、task に関連するときに Copilot が**自動で読み込む**ものです。Copilot は prompt を読み、該当する skill があるか確認し、関連する指示を自動で適用します。

```bash
copilot

> Check books.py against our quality checklist
# これは "code-checklist" skill に一致すると Copilot が判断し
# Python 向けの quality checklist を自動で適用します

> Generate tests for the BookCollection class
# Copilot が "pytest-gen" skill を読み込み
# 好みの test structure を適用します

> What are the code quality issues in this file?
# Copilot が "code-checklist" skill を読み込み
# team standards に照らして確認します
```

> 💡 **Key Insight**: skills は、prompt が skill の description に一致すると**automatically triggered** されます。自然に依頼するだけで、Copilot が裏側で関連 skills を適用します。次に説明するように、skills を直接呼び出すこともできます。

> 🧰 **Ready-to-use templates**: そのままコピーして試せるシンプルな skills は、[.github/skills](../.github/skills/) folder を確認してください。

### スラッシュコマンドで直接呼び出す

skills は auto-trigger が基本ですが、name を slash command として使って**直接呼び出す**こともできます。

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

これにより、特定の skill を確実に使いたいときに明示的に指定できます。

> 📝 **skills vs agents Invocation**: skill invocation と agent invocation を混同しないでください。
> - **skills**: `/skill-name <prompt>`、たとえば `/code-checklist Check this file`
> - **agents**: `/agent`（一覧から選択）または `copilot --agent <name>`（command line）
>
> skill と同名の agent（たとえば "code-reviewer"）がある場合、`/code-reviewer` は**skill** を呼び出し、agent は呼び出しません。

### Skill が使われたか確認するには？

Copilot に直接聞けばわかります。

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### Skills・Agents・MCP の違い

skills は GitHub Copilot の拡張モデルの一部にすぎません。agents や MCP servers と比べると次のようになります。

> *MCP はまだ深く気にしなくて大丈夫です。[Chapter 06](../06-mcp-servers/) で扱います。ここでは、skills が全体像の中でどう位置づけられるかを見るために載せています。*

<img src="images/skills-agents-mcp-comparison.png" alt="Agents、Skills、MCP Servers の違いと、それらがワークフローでどう組み合わさるかを示す比較図" width="800"/>

| 機能 | 役割 | 使う場面 |
|---------|--------------|-------------|
| **Agents** | AI の考え方を変える | 多くの task にまたがる専門知識が必要なとき |
| **Skills** | Task 固有の指示を与える | 手順が明確で繰り返し行う task のとき |
| **MCP** | 外部サービスにつなぐ | API から live data が必要なとき |

広い専門性には agents、特定 task の指示には skills、外部 data には MCP を使います。agent は conversation の中で one or more skills を使えます。たとえば code review を依頼すると、`security-audit` skill と `code-checklist` skill の両方を自動で適用することがあります。

> 📚 **Learn More**: skill formats と best practices の完全な参照は、公式の [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) documentation を参照してください。

---

## 手動プロンプトから自動の専門性へ

skills の作り方に入る前に、まずは *なぜ* 学ぶ価値があるのかを見てみましょう。consistency の向上が見えると、「どうやるか」も理解しやすくなります。

### Before Skills: 一貫しない review

コード review のたびに、何かを見落としてしまうことがあります。

```bash
copilot

> Review this code for issues
# generic review - team 固有の concerns を見落とすかもしれない
```

あるいは、毎回長い prompt を書くことになります。

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

時間: 入力に **30秒以上**。一貫性: **記憶に依存**。

### After Skills: 自動で best practices

`code-checklist` skill を入れておけば、自然に依頼するだけです。

```bash
copilot

> Check the book collection code for quality issues
```

**裏側で起きていること**:
1. Copilot が prompt 内の "code quality" と "issues" を認識する
2. skill description を確認し、`code-checklist` skill が一致すると見つける
3. team の quality checklist を自動で読み込む
4. 列挙しなくてもすべてのチェックを適用する

<img src="images/skill-auto-discovery-flow.png" alt="Skills の自動起動の流れを示す 4 ステップ図" width="800"/>

*自然に依頼するだけで大丈夫です。Copilot が prompt を適切な skill に一致させ、自動で適用します。*

**Output**:
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**違い**: チームの標準が、毎回、入力しなくても自動で適用されます。

---

<details>
<summary>🎬 動作を見る!</summary>

![Skill Trigger Demo](images/skill-trigger-demo.gif)

*デモの出力は異なる場合があります。表示される内容は model、tools、response によって変わります。*

</details>

---

## チーム規模で一貫性を保つ: Team PR Review skill

チームに 10 項目の PR checklist があるとします。skill がなければ、開発者は毎回その 10 項目を覚えておく必要があり、誰かが 1 つ忘れてしまいがちです。`pr-review` skill があれば、チーム全員が一貫した review を受けられます。

```bash
copilot

> Can you review this PR?
```

Copilot はチームの `pr-review` skill を自動で読み込み、10 項目すべてを確認します。

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**強み**: チーム全員が同じ standard を自動で適用できます。新しいメンバーも checklist を暗記する必要がなく、skill が代わりに処理します。

---

# カスタム Skills を作る

<img src="images/creating-managing-skills.png" alt="人とロボットの手が、skill を表す光る LEGO のようなブロックの壁を組み立てている図" width="800"/>

SKILL.md ファイルから自分の skill を作りましょう。

---

## Skill の場所

skills は `.github/skills/`（project-specific）または `~/.copilot/skills/`（user level）に保存されます。

### Copilot が skills を見つける方法

Copilot は次の場所を自動的にスキャンして skills を探します。

| Location | Scope |
|----------|-------|
| `.github/skills/` | Project-specific（git で team と共有） |
| `~/.copilot/skills/` | User-specific（個人用の skill） |

### Skill の構造

各 skill は、`SKILL.md` file を持つ専用 folder に置きます。必要に応じて scripts、examples、その他の resources を含めることもできます。

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Required: skill の定義と instructions
    ├── examples/          # Optional: Copilot が参照できる example files
    │   └── sample.py
    └── scripts/           # Optional: skill が使える scripts
        └── validate.sh
```

> 💡 **Tip**: directory name は SKILL.md frontmatter の `name` と一致させる必要があります（lowercase + hyphen）。

### SKILL.md Format

skills は、YAML frontmatter を含むシンプルな markdown format を使います。

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML Properties:**

| Property | Required | Description |
|----------|----------|-------------|
| `name` | **Yes** | Unique identifier（lowercase, spaces は hyphen） |
| `description` | **Yes** | skill が何をするか、Copilot がいつ使うべきか |
| `license` | No | この skill に適用される license |

> 📖 **Official docs**: [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### 最初の skill を作る

OWASP Top 10 vulnerabilities をチェックする security audit skill を作ってみましょう。

```bash
# skill directory を作成
mkdir -p .github/skills/security-audit

# SKILL.md file を作成
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# skill を試す（skills は prompt に基づいて自動で読み込まれる）
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot は "security vulnerabilities" が skill に一致すると判断し
# OWASP checklist を自動で適用します
```

**Expected output**（結果は異なります）:

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## 良い skill description の書き方

SKILL.md の `description` field はとても重要です。Copilot が skill を読み込むかどうかを判断する基準だからです。

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **Tip**: 普段の言い方に合う keyword を含めましょう。たとえば「security review」と言うなら、description にも "security review" を入れます。

### Skills と agents を組み合わせる

skills と agents は一緒に使えます。agent が専門性を提供し、skill が具体的な instructions を提供します。

```bash
# code-reviewer agent から始める
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer agent の専門性が
# code-checklist skill の checklist と組み合わさります
```

---

# Skills の管理と共有

インストール済みの skills を見つけ、コミュニティの skills を探し、自分の skills を共有しましょう。

<img src="images/managing-sharing-skills.png" alt="discover, use, create, share のサイクルを示す、CLI skills の管理と共有の図" width="800" />

---

## `/skills` command で skills を管理する

`/skills` command を使って、インストール済みの skills を管理できます。

| Command | 役割 |
|---------|--------------|
| `/skills list` | すべての installed skills を表示する |
| `/skills info <name>` | 特定の skill の詳細を表示する |
| `/skills add <name>` | skill を有効にする（repository や marketplace から） |
| `/skills remove <name>` | skill を無効化または uninstall する |
| `/skills reload` | SKILL.md を編集した後に skills を再読み込みする |

> 💡 **Remember**: prompt ごとに skill を「有効化」する必要はありません。インストール済みであれば、skills は prompt が description に一致したときに**自動的に起動**します。これらの command は、使うためではなく、利用可能な skill を管理するためのものです。

### Skills を表示する例

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>See it in action!</summary>

![List Skills Demo](images/list-skills-demo.gif)

*デモの出力は異なる場合があります。表示される内容は model、tools、response によって変わります。*

</details>

---

### `/skills reload` を使うタイミング

skill の SKILL.md file を作成または編集したら、Copilot を再起動せずに変更を取り込むために `/skills reload` を実行します。

```bash
# skill file を編集
# その後 Copilot で:
> /skills reload
Skills reloaded successfully.
```

> 💡 **Good to know**: `/compact` で conversation history を要約しても、skills は引き続き有効です。compact 後に reload する必要はありません。

---

## コミュニティ skills を見つけて使う

### Plugins を使って skills をインストールする

> 💡 **plugins とは？** plugins は、skills、agents、MCP server configuration をまとめて含められるインストール可能な package です。Copilot CLI の「app store」拡張のようなものだと考えてください。

`/plugin` command で、こうした package を探したりインストールしたりできます。

```bash
copilot

> /plugin list
# installed plugins を表示する

> /plugin marketplace
# 利用可能な plugins を閲覧する

> /plugin install <plugin-name>
# marketplace から plugin をインストールする
```

plugins には複数の機能をまとめて含められます。1 つの plugin に、連携して動く関連 skills、agents、MCP server configuration が入っていることがあります。

### Community Skill Repositories

あらかじめ用意された skills は、community repository からも利用できます。

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - skills documentation と example を含む、GitHub Copilot の公式リソース

### Community Skill を手動でインストールする

GitHub repository にある skill を見つけたら、その folder を skills directory にコピーします。

```bash
# awesome-copilot repository を clone
git clone https://github.com/github/awesome-copilot.git /tmp/awesome-copilot

# 特定の skill を project にコピー
cp -r /tmp/awesome-copilot/skills/code-checklist .github/skills/

# あるいは全 project で使う personal skill としてコピー
cp -r /tmp/awesome-copilot/skills/code-checklist ~/.copilot/skills/
```

> ⚠️ **install 前に確認する**: skill を project にコピーする前に、必ず `SKILL.md` を読んでください。skills は Copilot の動作を指示するため、悪意のある skill は危険な command を実行させたり、予期しない code 変更を行わせたりする可能性があります。

---

# 実践

<img src="../images/practice.png" alt="コード、ランプ、コーヒーカップ、ヘッドホンが並ぶ学習準備の整った作業机" width="800"/>

学んだことを実践して、自分の skills を作成・検証しましょう。

---

## ▶️ 自分で試す

### さらに skills を作る

ここでは、異なるパターンを示す 2 つの skill を紹介します。上の「最初の skill を作る」で使った `mkdir` + `cat` の流れに従うか、適切な場所にコピーして貼り付けてください。追加の例は [.github/skills](../.github/skills) にあります。

### pytest Test Generation Skill

codebase 全体で一貫した pytest 構成を保つための skill です。

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### Team PR Review Skill

team 全体で一貫した PR review standard を適用する skill です。

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### さらに学ぶ

1. **Skill Creation Challenge**: `quick-review` skill を作って、3 項目の checklist にしてみましょう。
   - Bare except clauses
   - Missing type hints
   - Unclear variable names

   次のように依頼して試します: "Do a quick review of books.py"

2. **Skill Comparison**: 詳細な security review prompt を手で書く時間を測ってみましょう。次に "Check for security issues in this file" とだけ依頼して、security-audit skill が自動で読み込まれる様子を比べます。どれくらい時間を節約できましたか？

3. **Team Skill Challenge**: 自分の team の code review checklist を考えてみましょう。skill にできる項目を 3 つ書き出してください。

**Self-Check**: `description` field がなぜ重要か説明できれば、skills を理解できています（Copilot が skill を読み込むかどうかを判断するためです）。

---

## 📝 課題

### Main Challenge: Book Summary skill を作る

上の例では `pytest-gen` と `pr-review` skills を作成しました。次は、別の種類の skill を作ってみましょう。データから整形済み output を生成する skill です。

1. 現在の skills を確認する: Copilot を起動して `/skills list` を実行します。`ls .github/skills/` で project skills を見たり、`ls ~/.copilot/skills/` で personal skills を見たりすることもできます。
2. `.github/skills/book-summary/SKILL.md` に `book-summary` skill を作成し、book collection の markdown summary を整形して出力するようにします。
3. skill には次の内容を含めます。
   - 明確な name と description（description は一致判定で重要です）
   - 具体的な formatting rules（たとえば title、author、year、read status の markdown table）
   - 出力の convention（たとえば read status に ✅/❌ を使う、year で sort する）
4. skill を試す: `@samples/book-app-project/data.json Summarize the books in this collection`
5. `/skills list` を確認して、skill が auto-trigger されることを確かめる
6. `/book-summary Summarize the books in this collection` で直接呼び出してみる

**Success criteria**: `book-summary` skill が動作し、book collection について尋ねると Copilot が自動で適用すること。

<details>
<summary>💡 ヒント（クリックで展開）</summary>

**Starter template**: `.github/skills/book-summary/SKILL.md` を作成します。

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**Test it:**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# skill should auto-trigger based on the description match
```

**If it doesn't trigger:** `/skills reload` を試してから、もう一度依頼します。

</details>

### Bonus Challenge: Commit Message Skill

1. 一貫した format で conventional commit messages を生成する `commit-message` skill を作る
2. 変更を stage してから "Generate a commit message for my staged changes" と依頼して試す
3. skill を documentation 付きで GitHub に公開し、`copilot-skill` topic を付ける

---

<details>
<summary>🔧 <strong>よくある間違いと troubleshooting</strong>（クリックで展開）</summary>

### よくある間違い

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| `SKILL.md` 以外の名前にする | skill が認識されない | file 名は必ず `SKILL.md` にする |
| `description` field が曖昧 | skill が自動で読み込まれない | description に具体的な trigger words を入れる |
| frontmatter に `name` または `description` がない | skill が読み込めない | YAML frontmatter に両方追加する |
| folder の場所が違う | skill が見つからない | `.github/skills/skill-name/`（project）または `~/.copilot/skills/skill-name/`（personal）を使う |

### トラブルシューティング

**skill が使われない** - 期待どおりに Copilot が skill を使わない場合:

1. **description を確認する**: 依頼の仕方と合っていますか？
   ```markdown
   # Bad: あいまいすぎる
   description: Reviews code

   # Good: trigger words を含める
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **file の場所を確認する**:
   ```bash
   # Project skills
   ls .github/skills/

   # User skills
   ls ~/.copilot/skills/
   ```

3. **SKILL.md format を確認する**: frontmatter が必要です。
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**skill が表示されない** - folder structure を確認します。
```
.github/skills/
└── my-skill/           # Folder name
    └── SKILL.md        # Must be exactly SKILL.md (case-sensitive)
```

`SKILL.md` を作成・編集したあとは、`/skills reload` を実行して変更を取り込みます。

**skill が読み込まれたか確認する** - Copilot に直接聞きます。
```bash
> What skills do you have available for checking code quality?
# Copilot will describe relevant skills it found
```

**本当に動いているかどうかを確認するには？**

1. **output format を確認する**: skill が `[CRITICAL]` などの出力 format を指定しているなら、それが返ってくるか確認する
2. **直接聞く**: response を受け取ったあとに "Did you use any skills for that?" と聞く
3. **あり・なしで比較する**: `--no-custom-instructions` を付けて同じ prompt を試し、違いを見る
   ```bash
   # With skills
   copilot --allow-all -p "Review @file.py for security issues"

   # Without skills (baseline comparison)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **特定の checks を探す**: skill に「functions over 50 lines」のような具体的な checks が入っているなら、それが output に出るか確認する

</details>

---

# まとめ

## 🔑 重要なポイント

1. **skills は自動**: prompt が skill の description に一致すると Copilot が読み込む
2. **直接呼び出しも可能**: `/skill-name` で skill を slash command として呼び出せる
3. **SKILL.md format**: YAML frontmatter（name、description、任意で license）＋ markdown instructions
4. **場所が重要**: `.github/skills/` は project/team 共有、`~/.copilot/skills/` は personal 用
5. **description が鍵**: 普段の質問の仕方に合う description を書く

> 📋 **Quick Reference**: コマンドと shortcut の完全な一覧は、[GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次へ

skills は、auto-loaded instructions で Copilot の機能を広げます。では、外部 services に接続したい場合はどうでしょう？ そこで MCP の出番です。

**[Chapter 06: MCP Servers](../06-mcp-servers/README.md)** では、次の内容を学びます。

- MCP（Model Context Protocol）とは何か
- GitHub、filesystem、documentation services への接続
- MCP servers の設定
- Multi-server workflow

---

**[← Back to Chapter 04](../04-agents-custom-instructions/README.md)** | **[Continue to Chapter 06 →](../06-mcp-servers/README.md)**
