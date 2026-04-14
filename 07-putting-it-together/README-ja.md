![第07章: Putting It All Together](images/chapter-header.png)

> **ここですべてがつながります。1回のセッションで、アイデアから merged PR まで進めましょう。**

この章では、これまで学んだ内容を実際のワークフローとしてまとめます。multi-agent での協働、security issue を事前に見つける pre-commit hooks、Copilot を CI/CD pipeline に組み込む方法、そして feature idea から merged PR までを1つの terminal session で進める流れを扱います。ここで GitHub Copilot CLI は本当の意味での force multiplier になります。

> 💡 **補足**: この章は、ここまでの内容をまとめて使う方法を示します。**productive になるのに agents、skills、MCP は必須ではありません（ただし非常に便利です）。** 基本のワークフロー — describe, plan, implement, test, review, ship — は Chapter 00-03 の built-in features だけでも実行できます。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- agents、skills、MCP (Model Context Protocol) を統合したワークフローを組み合わせる
- multi-tool の考え方で complete feature を作る
- hooks を使った基本的な automation を設定する
- professional development の best practices を適用する

> ⏱️ **想定時間**: 約75分（読書15分 + ハンズオン60分）

---

## 🧩 実世界のたとえ: Orchestra

<img src="images/orchestra-analogy.png" alt="Orchestra Analogy - Unified Workflow" width="800"/>

symposium orchestra には多くの section があります。
- **Strings** は土台を支えます（core workflow のようなものです）
- **Brass** は力強さを加えます（specialized expertise を持つ agents のようなものです）
- **Woodwinds** は色合いを加えます（capability を広げる skills のようなものです）
- **Percussion** は rhythm を保ちます（external systems につながる MCP のようなものです）

それぞれ単体では限られた音しか出せません。ですが、うまく指揮すれば、ひとつになって素晴らしいものを生み出します。

**この章はまさにそれを教えるものです！**<br>
*orchestra の conductor のように、agents、skills、MCP を統合した unified workflow を組み立てます*

まずは、コードを変更し、tests を生成し、review して、PR を作るシナリオを1回の session で追ってみましょう。

---

## Idea to Merged PR in One Session

editor、terminal、test runner、GitHub UI を行ったり来たりして、そのたびに context を失う代わりに、1つの terminal session ですべての tool をまとめて使えます。このパターンは後ほど [Integration Pattern](#the-integration-pattern) で分解します。

```bash
# Start Copilot in interactive mode
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot creates high-level plan...

# SWITCH TO PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# SWITCH TO PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# IMPLEMENT
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TEST
> Generate comprehensive tests for the new feature

# Multiple tests are generated similar to the following:
# - Happy path (3 tests) — filters correctly, excludes read, includes unread
# - Edge cases (4 tests) — empty collection, all read, none read, single book
# - Parametrized (5 cases) — varying read/unread ratios via @pytest.mark.parametrize
# - Integration (4 tests) — interplay with mark_as_read, remove_book, add_book, and data integrity

# Review the changes
> /review

# If review passes, use /pr to operate on the pull request for the current branch
> /pr [view|create|fix|auto]

# Or ask naturally if you want Copilot to draft it from the terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**従来のやり方**: editor、terminal、test runner、GitHub UI を何度も切り替える必要があり、そのたびに context が途切れます。

**重要なポイント**: あなたは architect のように specialist に指示を出しています。細かい作業は彼らが担当し、あなたは全体像を担っています。

> 💡 **さらに進めるなら**: このような大きな複数ステップの plan では、`/fleet` を使って independent な subtask を並列に処理できます。詳細は [official docs](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet) を参照してください。

---

# Additional Workflows

<img src="images/combined-workflows.png" alt="People assembling a colorful giant jigsaw puzzle with gears, representing how agents, skills, and MCP combine into unified workflows" width="800"/>

Chapter 04-06 を終えた方向けに、agents、skills、MCP がどのように力を増幅するかを示す workflows です。

## The Integration Pattern

すべてを組み合わせるときの mental model は次のとおりです。

<img src="images/integration-pattern.png" alt="The Integration Pattern - A 4-phase workflow: Gather Context (MCP), Analyze and Plan (Agents), Execute (Skills + Manual), Complete (MCP)" width="800"/>

---

## Workflow 1: Bug Investigation and Fix

full tool integration を使った現実的な bug fixing:

```bash
copilot

# PHASE 1: Understand the bug from GitHub (MCP provides this)
> Get the details of issue #1

# Learn: "find_by_author doesn't work with partial names"

# PHASE 2: Research best practice (deep research with web + GitHub sources)
> /research Best practices for Python case-insensitive string matching

# PHASE 3: Find related code
> @samples/book-app-project/books.py Show me the find_by_author method

# PHASE 4: Get expert analysis
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching

# Agent identifies: Method uses exact equality instead of substring matching

# PHASE 5: Fix with agent guidance
> Implement the fix using lowercase comparison and 'in' operator

# PHASE 6: Generate tests
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# PHASE 7: Commit and PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## Workflow 2: Code Review Automation (Optional)

> 💡 **この section は optional です。** pre-commit hooks は teams には便利ですが、productive になるために必須ではありません。始めたばかりなら後回しでも大丈夫です。
>
> ⚠️ **Performance note**: この hook は staged file ごとに `copilot -p` を呼び出すため、1ファイルあたり数秒かかります。大きな commit では critical な file に絞るか、`/review` で手動 review するのがおすすめです。

**git hook** は Git が特定のタイミングで自動実行する script です。たとえば commit の直前です。これを使うと、commit 前に自動で Copilot review を走らせられます。

```bash
# Create a pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    # --allow-all auto-approves file reads/writes so the hook can run unattended.
    # Only use this in automated scripts. In interactive sessions, let Copilot ask for permission.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOS users**: `timeout` command は macOS には標準で入っていません。`brew install coreutils` で入れるか、`timeout 60` を外して使ってください。

> 📚 **Official Documentation**: [Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) と [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) を参照してください。
>
> 💡 **Built-in alternative**: Copilot CLI には `copilot hooks` という built-in hooks system もあり、pre-commit などの event で自動実行できます。上の manual git hook は柔軟性が高く、built-in system は設定が簡単です。どちらが合うかは docs を見て判断してください。

今ではすべての commit で quick security review が走ります。

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Output:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## Workflow 3: Onboarding to a New Codebase

新しい project に入ったときは、context、agents、MCP を組み合わせると素早く立ち上がれます。

```bash
# Start Copilot in interactive mode
copilot

# PHASE 1: Get the big picture with context
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# PHASE 2: Understand a specific flow
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# PHASE 3: Get expert analysis with an agent
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# PHASE 4: Find something to work on (MCP provides GitHub access)
> List open issues labeled "good first issue"

# PHASE 5: Start contributing
> Pick the simplest open issue and outline a plan to fix it
```

この workflow は `@` context、agents、MCP を1つの session にまとめたもので、まさに前半で説明した integration pattern そのものです。

---

# Best Practices & Automation

workflows をより効果的にする patterns と習慣です。

---

## Best Practices

### 1. Start with Context Before Analysis

analysis を頼む前に、まず context を集めましょう。

```bash
# Good
> Get the details of issue #42
> /agent
# Select python-reviewer
> Analyze this issue

# Less effective
> /agent
# Select python-reviewer
> Fix login bug
# Agent doesn't have issue context
```

### 2. Know the Difference: Agents, Skills, and Custom Instructions

それぞれの tool には得意分野があります。

```bash
# Agents: Specialized personas you explicitly activate
> /agent
# Select python-reviewer
> Review this authentication code for security issues

# Skills: Modular capabilities that auto-activate when your prompt
# matches the skill's description (you must create them first — see Ch 05)
> Generate comprehensive tests for this code
# If you have a testing skill configured, it activates automatically

# Custom instructions (.github/copilot-instructions.md): Always-on
# guidance that applies to every session without switching or triggering
```

> 💡 **Key point**: Agents と skills はどちらも code を分析し、生成できます。違いは **activation の仕組み** です。agents は明示的に `/agent` で切り替え、skills は prompt に反応して自動で有効になり、custom instructions は常に適用されます。

### 3. Keep Sessions Focused

`/rename` で session に名前を付け、`/exit` で明確に終わらせましょう。

```bash
# Good: One feature per session
> /rename list-unread-feature
# Work on list unread
> /exit

copilot
> /rename export-csv-feature
# Work on CSV export
> /exit

# Less effective: Everything in one long session
```

### 4. Make Workflows Reusable with Copilot

workflow を wiki に書くだけでなく、repo 内に直接埋め込むと Copilot が活用できます。

- **Custom instructions** (`.github/copilot-instructions.md`): coding standard、architecture rule、build/test/deploy 手順を常に適用する guidance
- **Prompt files** (`.github/prompts/`): code review、component generation、PR description などに使える reusable な parameterized prompt
- **Custom agents** (`.github/agents/`): security reviewer や docs writer のような specialized persona を `/agent` で起動できるようにする
- **Custom skills** (`.github/skills/`): 条件に応じて自動で有効になる step-by-step の workflow instructions

> 💡 **効果**: 新しい team member も、あなたの workflow をそのまま使えます。head の中ではなく、repo の中にあるからです。

---

## Bonus: Production Patterns

これらは optional ですが、professional な環境では役立ちます。

### PR Description Generator

```bash
# Generate comprehensive PR descriptions
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD Integration

既存の CI/CD pipeline がある team では、GitHub Actions を使って pull request ごとに Copilot review を自動化できます。review comment の自動投稿や critical issue のフィルタリングも可能です。

> 📖 **Learn more**: 完全な GitHub Actions workflow、configuration option、troubleshooting は [CI/CD Integration](../appendices/ci-cd-integration.md) を参照してください。

---

# Practice

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

complete workflow を実践してみましょう。

---

## ▶️ Try It Yourself

demo を終えたら、次の variation を試してみてください。

1. **End-to-End Challenge**: 小さな feature（たとえば "list unread books" や "export to CSV"）を選び、full workflow を使います。
   - `/plan` で計画する
   - agents（python-reviewer, pytest-helper）で design する
   - implement する
   - tests を生成する
   - PR を作成する

2. **Automation Challenge**: Code Review Automation workflow の pre-commit hook を設定します。file path vulnerability を意図的に含む commit を作ってみてください。止められるでしょうか？

3. **Your Production Workflow**: あなたがよく行う作業向けに自分だけの workflow を設計し、checklist として書き出します。skills、agents、hooks で自動化できる部分はどこでしょうか？

**Self-Check**: agents、skills、MCP がどう連携し、いつどれを使うのかを colleague に説明できれば、この章をマスターしたと言えます。

---

## 📝 Assignment

### Main Challenge: End-to-End Feature

ハンズオンの例では "list unread books" feature を作りました。今度は別の feature、**search books by year range** を使って full workflow を練習しましょう。

1. Copilot を起動して context を集める: `@samples/book-app-project/books.py`
2. `/plan Add a "search by year" command that lets users find books published between two years`
3. `BookCollection` に `find_by_year_range(start_year, end_year)` method を実装する
4. `book_app.py` に `handle_search_year()` function を追加し、start/end year を入力させる
5. tests を生成する: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. `/review` で review する
7. README を更新する: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. commit message を生成する

workflow を進めながら記録してください。

**Success criteria**: planning、implementation、tests、documentation、review を含め、idea から commit までを Copilot CLI で完了できること。

> 💡 **Bonus**: Chapter 04 の agents を設定しているなら、custom agents を作って使ってみましょう。たとえば、implementation review 用の error-handler agent や README 更新用の doc-writer agent です。

<details>
<summary>💡 Hints (click to expand)</summary>

**["Idea to Merged PR"](#idea-to-merged-pr-in-one-session) の例** をたどってみてください。主な手順は次のとおりです。

1. `@samples/book-app-project/books.py` で context を集める
2. `/plan Add a "search by year" command` で計画する
3. method と command handler を実装する
4. edge case（invalid input、empty results、reversed range）を含む tests を生成する
5. `/review` で review する
6. `@samples/book-app-project/README.md` で README を更新する
7. `-p` で commit message を生成する

**考えるべき edge case**:
- `2000` と `1990` のように reversed range を入力したらどうするか？
- 範囲に一致する本が1冊もない場合は？
- 数値でない input を入れたら？

**ポイントは、idea → context → plan → implement → test → document → commit の full workflow を練習することです。**

</details>

---

<details>
<summary>🔧 <strong>Common Mistakes</strong> (click to expand)</summary>

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| いきなり implementation に進む | 後で修正コストの高い design issue を見逃す | まず `/plan` で方針を整理する |
| 1つの tool だけで済ませる | 遅くなり、結果も浅くなる | Agent で analysis → Skill で execution → MCP で integration |
| review せずに commit する | security issue や bug が混ざる | 常に `/review` を実行するか、[pre-commit hook](#workflow-2-code-review-automation-optional) を使う |
| workflow を team と共有しない | 各自が毎回やり直すことになる | shared な agents、skills、instructions にまとめる |

</details>

---

# Summary

## 🔑 Key Takeaways

1. **Integration > Isolation**: tool を組み合わせると効果が最大化される
2. **Context first**: analysis の前に必要な context を必ず集める
3. **Agents analyze, Skills execute**: 役割に合った tool を使う
4. **Automate repetition**: hooks や scripts で効率が大きく上がる
5. **Document workflows**: 共有可能な pattern は team 全体に利益をもたらす

> 📋 **Quick Reference**: 完全な command と shortcut の一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## 🎓 Course Complete!

おめでとうございます！次の内容を学びました。

| Chapter | What You Learned |
|---------|-------------------|
| 00 | Copilot CLI の installation と Quick Start |
| 01 | 3つの interaction mode |
| 02 | `@` syntax による context management |
| 03 | Development workflows |
| 04 | Specialized agents |
| 05 | Extensible skills |
| 06 | MCP による external connections |
| 07 | Unified production workflows |

これで、GitHub Copilot CLI を development workflow の genuine force multiplier として使う準備が整いました。

## ➡️ What's Next

学びはここで終わりではありません。

1. **Practice daily**: 実際の仕事で Copilot CLI を使う
2. **Build custom tools**: 自分の needs に合わせた agents や skills を作る
3. **Share knowledge**: team に workflow を広める
4. **Stay updated**: GitHub Copilot の新機能を追う

### Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Community Skills](https://github.com/topics/copilot-skill)

---

**よくできました！さあ、何か素晴らしいものを作りましょう。**

**[← Back to Chapter 06](../06-mcp-servers/README.md)** | **[Return to Course Home →](../README.md)**
