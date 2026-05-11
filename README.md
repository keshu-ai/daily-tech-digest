# Daily Tech Digest - 每日科技资讯摘要

一个基于 **Claude Code Skill** 的自动化工具，从多个国内外科技 RSS 源抓取内容，智能筛选 AI/科技热点，生成排版精美的 Obsidian 日报。

---

## 目录

- [功能特性](#功能特性)
- [效果预览](#效果预览)
- [快速开始](#快速开始)
  - [作为 Claude Code Skill 安装](#作为-claude-code-skill-安装)
  - [独立 Python 脚本运行](#独立-python-脚本运行)
- [触发方式](#触发方式)
- [配置说明](#配置说明)
  - [自定义 RSS 源](#自定义-rss-源)
  - [权限配置](#权限配置)
- [输出格式](#输出格式)
- [在主流 AI Agent 工具中使用](#在主流-ai-agent-工具中使用)
  - [Claude Code](#claude-code)
  - [OpenClaw](#openclaw)
  - [Codex (OpenAI)](#codex-openai)
- [RSS 源列表](#rss-源列表)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 功能特性

- **多源聚合** — 同时从 15+ 个国内外科技 RSS 源抓取内容
- **智能筛选** — 基于关键词匹配自动识别 AI/科技相关内容
- **热度评分** — 根据事件重要性自动打分排序（重磅/重点/关注）
- **72 小时窗口** — 只抓取最近 72 小时内的新鲜内容
- **自动去重** — 基于 URL 去重，避免重复资讯
- **Obsidian 原生** — 输出带 frontmatter、callout、可折叠区块的标准 Obsidian Markdown
- **零 API 依赖** — 不需要任何付费 API Key，纯 RSS 抓取

## 效果预览

生成的日报包含：

```
📰 2026年05月06日 科技资讯日报

┌─────────────────────────────────┐
│ 今日洞察                          │
│ 共筛选 42 篇，🔥🔥🔥 重磅 3 篇     │
├──────┬────────────┬───────┬─────┤
│ 等级  │ 标题        │ 来源   │ 链接 │
│ 🔥🔥🔥│ OpenAI 发布..│ OpenAI │  🔗  │
│ 🔥🔥  │ 谷歌推出...  │ 36氪   │  🔗  │
└──────┴────────────┴───────┴─────┘

🤖 AI 领域 （详细摘要 + 原文链接）
💡 其他科技动态
📚 订阅源列表
```

---

## 快速开始

### 作为 Claude Code Skill 安装

**方式一：通过 `skills-lock.json` 安装（推荐）**

在你的项目根目录 `skills-lock.json` 中添加：

```json
{
  "daily-tech-digest": {
    "github": "keshu-ai/daily-tech-digest",
    "ref": "main"
  }
}
```

然后运行：

```bash
npx skills install
```

**方式二：手动安装**

1. 将 `.claude/skills/daily-tech-digest/` 目录复制到你项目的 `.claude/skills/` 下
2. 将 `settings.example.json` 中的权限合并到你的 `.claude/settings.local.json`
3. 安装 Python 依赖：

```bash
pip install -r requirements.txt
```

**使用：**

安装后在 Claude Code 中直接对话即可触发：

```
> 生成今日科技日报
> 帮我抓取今天的 AI 新闻
> daily tech digest
```

### 独立 Python 脚本运行

不使用 Claude Code，也可以直接运行 Python 脚本：

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/daily-tech-digest.git
cd daily-tech-digest

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行（使用默认 RSS 源）
python .claude/skills/daily-tech-digest/scripts/generate_digest.py

# 4. 运行（添加自定义源）
python .claude/skills/daily-tech-digest/scripts/generate_digest.py https://example.com/rss.xml
```

生成文件：`科技日报_YYYYMMDD.md`

---

## 触发方式

安装后，在对话中直接说：

```
生成今日科技日报
帮我抓取今天的 AI 新闻
daily tech digest
```

也可以直接调用 skill：
```
/daily-tech-digest
```

---

### 自定义 RSS 源

编辑 `.claude/skills/daily-tech-digest/references/sources.list`，每行一个 RSS 地址：

```
# 国际科技源
https://techcrunch.com/category/artificial-intelligence/feed/
https://openai.com/blog/rss.xml

# 国内科技源
https://36kr.com/feed
https://www.jiqizhixin.com/rss

# 添加你自己的源
https://your-favorite-site.com/rss.xml
```

也可以直接修改 `generate_digest.py` 中的 `DEFAULT_SOURCES` 列表。

### 权限配置

如果使用 Claude Code，需要在 `.claude/settings.local.json` 中配置 WebFetch 权限，参考 `settings.example.json`。

---

## 输出格式

| 区块 | 内容 |
|------|------|
| **Frontmatter** | 标题、日期、标签（科技资讯/日报/AI） |
| **今日洞察** | 总览表格，按热度排序的前 18 条资讯 |
| **AI 领域** | AI/大模型相关资讯详情（最多 10 条） |
| **其他科技动态** | 泛科技类资讯（最多 8 条） |
| **订阅源列表** | 来源网站列表 |

每条资讯包含：标题、热度等级、可折叠摘要、原文链接、来源网站。

---

## 在主流 AI Agent 工具中使用

本技能的核心是一个 Python 脚本 + RSS 配置文件，支持在以下 AI Agent 工具中使用：

### Claude Code

> **原生支持** — 这是本项目的主要使用场景。

Claude Code 是 Anthropic 官方的 CLI 工具，支持 Skill 系统，可以直接安装使用。

**安装方式：**
```bash
# 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 在项目目录运行
claude
```

**Skill 安装：** 参见上方 [快速开始](#作为-claude-code-skill-安装) 部分。

**触发方式：** 在对话中直接说"生成科技日报"或"daily tech digest"。

**特点：**
- 原生 Skill 系统，安装即用
- 自动权限管理
- 支持定时任务（`/loop` 命令）
- 可与 Obsidian 笔记系统深度集成

---

### OpenClaw

> **通过 Skill 目录集成**

[OpenClaw](https://openclaw.ai) 是另一个支持 Skill 系统的 AI Agent 工具。

**安装步骤：**

1. 克隆仓库到本地
2. 将 `.claude/skills/daily-tech-digest/` 复制到 OpenClaw 的 skills 目录下（通常为 `~/.openclaw/skills/`）
3. 安装 Python 依赖：

```bash
pip install feedparser requests
```

**配置权限：**

在 `~/.openclaw/settings.local.json` 中添加 WebFetch 权限，参考 `settings.example.json`。

**使用：** 在 OpenClaw 对话中直接触发 skill。

---

### Codex (OpenAI)

> **通过 Custom Instructions 集成**

[Codex](https://openai.com/codex) 是 OpenAI 推出的 AI 编程助手。

**手动集成：**

1. 将 `scripts/generate_digest.py` 和 `references/sources.list` 复制到项目根目录
2. 安装依赖：

```bash
pip install feedparser requests
```

**通过 Custom Instructions 配置：**

在 Codex 的 Custom Instructions 或项目配置中添加：

```
当用户要求生成科技日报时，执行以下命令：
python generate_digest.py
```

脚本会在当前目录生成 `科技日报_YYYYMMDD.md`。

---

## RSS 源列表

### 国际源

| 来源 | RSS 地址 | 方向 |
|------|---------|------|
| TechCrunch AI | `techcrunch.com/.../feed/` | AI 新闻 |
| MIT 科技评论 | `technologyreview.com/.../feed/` | AI 前沿 |
| OpenAI 官方博客 | `openai.com/blog/rss.xml` | 模型发布 |
| VentureBeat AI | `venturebeat.com/.../feed/` | AI 产业 |
| Ars Technica | `feeds.arstechnica.com/...` | 科技综合 |
| Wired | `wired.com/feed/rss` | 科技文化 |
| AI News | `artificialintelligence-news.com/feed/` | AI 专业 |

### 国内源

| 来源 | RSS 地址 | 方向 |
|------|---------|------|
| 人人都是产品经理 | `woshipm.com/feed` | 产品/互联网 |
| 爱范儿 | `ifanr.com/feed` | 消费科技 |
| 少数派 | `sspai.com/feed` | 效率/工具 |
| 36氪 | `36kr.com/feed` | 创投/商业 |
| 199IT | `199it.com/feed` | 数据报告 |
| 机器之心 | `jiqizhixin.com/rss` | AI 学术 |
| 量子位 | `qbitai.com/rss` | AI 产业 |
| 极客公园 | `geekpark.net/rss` | 科技创新 |

---

## 常见问题

### Q: 某些 RSS 源抓取失败？

网络环境不同，部分国际源可能需要代理。可以在 `generate_digest.py` 的 `fetch_feed` 函数中配置代理：

```python
resp = requests.get(url, timeout=10, proxies={
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
})
```

### Q: 如何添加新的 RSS 源？

编辑 `references/sources.list` 文件，每行添加一个 RSS URL。同时在 `generate_digest.py` 的 `get_source_name` 函数中添加源名称映射。

### Q: 输出文件在哪里？

默认在当前工作目录下生成 `科技日报_YYYYMMDD.md`。如果在 Obsidian vault 中运行，文件会直接出现在笔记中。

### Q: 支持定时自动运行吗？

- **Claude Code**: 使用 `/loop 24h 生成科技日报` 设置定时任务
- **系统级**: 使用 cron (Linux/Mac) 或任务计划程序 (Windows)
- **GitHub Actions**: 可以配置定时 workflow 自动运行

### Q: Python 版本要求？

Python 3.8+，推荐 3.10 及以上。

---

## 贡献指南

欢迎提交 PR 和 Issue！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/new-rss-source`
3. 提交更改：`git commit -m "add: 新增 RSS 源"`
4. 推送分支：`git push origin feature/new-rss-source`
5. 创建 Pull Request

**可以贡献的方向：**
- 新增优质 RSS 源
- 优化关键词匹配算法
- 添加新的输出格式支持
- 改进翻译功能
- 国际化支持

---

## 许可证

[MIT License](LICENSE)
