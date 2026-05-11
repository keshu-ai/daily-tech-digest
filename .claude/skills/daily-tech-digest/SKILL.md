---
name: daily-tech-digest
description: 每日科技资讯摘要生成工具，自动从多个科技RSS源抓取内容，筛选AI/科技相关热点，生成排版美观的日报，包含原文链接。使用场景：当用户需要获取每日科技新闻、科技热点汇总、AI行业动态时触发。
---
# Daily Tech Digest 每日科技摘要

## 功能说明
自动从多个国内外科技 RSS 源抓取最新内容，筛选科技/AI 相关热点信息，生成排版美观的每日科技日报，包含资讯摘要和原文链接。

## 已配置默认 RSS 源

### 国际科技源
1. TechCrunch AI: https://techcrunch.com/category/artificial-intelligence/feed/
2. MIT 科技评论 AI: https://www.technologyreview.com/topic/artificial-intelligence/feed/
3. OpenAI 官方博客: https://openai.com/blog/rss.xml
4. 谷歌 AI 官方博客: https://ai.googleblog.com/atom.xml

### 国内科技源
1. 人人都是产品经理: https://www.woshipm.com/feed
2. 虎嗅网: https://www.huxiu.com/rss/0.xml
3. 爱范儿: https://www.ifanr.com/feed
4. 少数派: https://sspai.com/feed
5. 36氪: https://36kr.com/feed
6. 199IT 互联网数据中心: https://www.199it.com/feed
7. 机器之心: https://www.jiqizhixin.com/rss
8. 量子位: https://www.qbitai.com/rss

## 使用方法

### 生成默认日报
```bash
python scripts/generate_digest.py
```

### 自定义源
```bash
python scripts/generate_digest.py https://example.com/rss.xml
```

## 输出格式

生成文件: `科技日报_YYYYMMDD.md`

包含:
- **Frontmatter**: 标题、日期、标签等元数据
- **数据来源**: RSS 源数量统计
- **AI 领域**: 筛选出的 AI/大模型相关资讯（最多 10 条）
- **其他科技动态**: 泛科技类资讯（最多 8 条）
- **订阅源列表**: 来源网站列表

每条资讯包含:
- 标题（含英文翻译）
- 可折叠摘要（`>[!ABSTRACT]+`）
- 原文链接（Obsidian 可直接打开的 Markdown 链接格式）

## 脚本说明

`scripts/generate_digest.py` - 自动抓取 RSS 内容、去重、筛选、排版的核心脚本

## 参考配置

`references/sources.list` - 可编辑此文件自定义默认 RSS 源列表，每行一个地址
