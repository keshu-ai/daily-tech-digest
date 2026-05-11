#!/usr/bin/env python3
import feedparser
import requests
from datetime import datetime
import re
import sys
from collections import OrderedDict

DEFAULT_SOURCES = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://openai.com/blog/rss.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.wired.com/feed/rss",
    "https://www.artificialintelligence-news.com/feed/",
    "https://www.woshipm.com/feed",
    "https://www.ifanr.com/feed",
    "https://sspai.com/feed",
    "https://36kr.com/feed",
    "https://www.199it.com/feed",
    "https://www.jiqizhixin.com/rss",
    "https://www.qbitai.com/rss",
    "https://www.geekpark.net/rss"
]

KEYWORDS = [
    "AI", "人工智能", "大模型", "GPT", "OpenAI", "Claude", "Gemini", "LLM", "AGI",
    "机器学习", "深度学习", "神经网络", "自然语言处理", "NLP", "计算机视觉", "CV",
    "多模态", "Transformer", "提示词", "Prompt", "RAG", "向量数据库", "知识图谱",
    "AIGC", "生成式AI", "ChatGPT", "Copilot", "智能助手", "AI写作", "AI绘画",
    "AI视频", "AI音乐", "数字人", "虚拟主播", "智能客服", "自动驾驶", "机器人",
    "AI芯片", "GPU", "CUDA", "英伟达", "NVIDIA", "算力", "智算中心", "AI infra",
    "MLOps", "模型训练", "微调", "Fine-tuning", "RLHF", "模型蒸馏", "模型量化",
    "科技", "互联网", "创投", "融资", "IPO", "独角兽", "技术", "开源", "GitHub",
    "程序员", "开发者", "工程师", "产品经理", "运营", "数字化", "转型", "SaaS",
    "云计算", "云原生", "边缘计算", "物联网", "IoT", "5G", "Web3", "区块链"
]

# 英文标题翻译映射（无API版）
TRANSLATIONS = {
    # AI/科技核心词
    'AI': 'AI', 'Artificial Intelligence': '人工智能', 'Machine Learning': '机器学习',
    'Deep Learning': '深度学习', 'Neural Network': '神经网络', 'AGI': 'AGI',
    'Large Language Model': '大语言模型', 'LLM': 'LLM', 'GPT': 'GPT',
    'Chatbot': '聊天机器人', 'OpenAI': 'OpenAI', 'Anthropic': 'Anthropic',
    'Claude': 'Claude', 'Gemini': 'Gemini', 'Google': '谷歌', 'Microsoft': '微软',
    'Apple': '苹果', 'Tesla': '特斯拉', 'Meta': 'Meta', 'Amazon': '亚马逊',
    'Elon Musk': '埃隆·马斯克', 'Sam Altman': '山姆·奥特曼', 'xAI': 'xAI',
    'Nvidia': '英伟达', 'NVIDIA': '英伟达', 'GPU': 'GPU', 'Chip': '芯片',
    'Model': '模型', 'Models': '模型', 'Agent': '智能体', 'Agents': '智能体',
    'Multimodal': '多模态', 'Multipath': '多路径', 'Training': '训练',
    'Inference': '推理', 'Supercomputer': '超级计算机', 'Networking': '网络',
    'Protocol': '协议', 'System': '系统', 'Card': '说明',

    # 事件动作
    'Valuation': '估值', 'Raises': '融资', 'Funding': '融资', 'Secures': '获得',
    'Acquires': '收购', 'Acquisition': '收购', 'Merger': '合并', 'Merges': '合并',
    'Partnership': '合作', 'Collaborates': '合作', 'Collaboration': '合作',
    'Launches': '发布', 'Launch': '发布', 'Released': '发布', 'Release': '发布',
    'Announces': '宣布', 'Announced': '宣布', 'Introduces': '推出', 'Reveals': '揭示',
    'Plans': '计划', 'Reveals': '公开', 'Unveils': '发布', 'Breakthrough': '突破',
    'Transforms': '变革', 'Enables': '使能', 'Improves': '提升', 'Advances': '推进',

    # 商业财经
    'Billion': '亿', 'Million': '百万', 'Dollar': '美元', 'Investment': '投资',
    'Invests': '投资', 'Investor': '投资者', 'Startup': '创业公司', 'IPO': '上市',
    'Public': '公开', 'Private': '私有', 'Market': '市场', 'Enterprise': '企业',
    'Business': '商业', 'Company': '公司', 'Tech': '科技', 'Technology': '技术',
    'Digital': '数字化', 'Cloud': '云', 'Platform': '平台', 'Service': '服务',
    'Product': '产品', 'Revenue': '营收', 'Profit': '盈利', 'Growth': '增长',

    # 研究分析
    'Study': '研究', 'Research': '研究', 'Analysis': '分析', 'Report': '报告',
    'Survey': '调研', 'Finds': '发现', 'Results': '结果', 'Data': '数据',
    'Framework': '框架', 'Method': '方法', 'Approach': '方法', 'Strategy': '策略',

    # 产品功能
    'Feature': '功能', 'Update': '更新', 'Version': '版本', 'Instant': '即时',
    'Smarter': '更智能', 'Clearer': '更清晰', 'Personalized': '个性化',
    'Performance': '性能', 'Speed': '速度', 'Efficiency': '效率', 'Quality': '质量',

    # 热门话题
    'Trial': '审判', 'Lawsuit': '诉讼', 'Demo': '演示', 'Event': '活动',
    'Conference': '大会', 'Week': '周', 'Day': '日', 'Year': '年', 'Annual': '年度',
    'Insights': '洞察', 'Perspective': '视角', 'Future': '未来', 'Trend': '趋势',

    # 常见词
    'New': '新', 'Latest': '最新', 'First': '首个', 'Best': '最佳', 'Top': '顶级',
    'Global': '全球', 'World': '世界', 'China': '中国', 'US': '美国', 'UK': '英国',
    'European': '欧洲', 'Asia': '亚洲', 'International': '国际', 'Domestic': '国内',
    'Network': '网络', 'Networks': '网络', 'Scale': '规模', 'Large': '大型', 'Small': '小型',
    'Medium': '中型', 'Enterprise': '企业', 'Consumer': '消费者', 'User': '用户',
    'Developer': '开发者', 'Engineer': '工程师', 'Team': '团队', 'Building': '建设',
    'Ways': '方式', 'Way': '方式', 'Buy': '购买', 'Sell': '销售', 'Get': '获取',
    'Use': '使用', 'Using': '使用', 'Make': '制作', 'Help': '帮助', 'Learn': '学习',
    'Understand': '理解', 'Know': '知道', 'See': '看到', 'Look': '看', 'Watch': '观看',
    'Read': '阅读', 'Write': '写作', 'Create': '创建', 'Build': '构建', 'Building': '构建',
    'Start': '开始', 'Stop': '停止', 'End': '结束', 'Begin': '开始', 'Continues': '继续',
    'Now': '现在', 'Then': '然后', 'After': '之后', 'Before': '之前', 'Next': '下一个',
    'Last': '上一个', 'This': '这个', 'That': '那个', 'These': '这些', 'Those': '那些',
    'All': '所有', 'Some': '一些', 'Many': '许多', 'Much': '很多', 'More': '更多',
    'Other': '其他', 'Another': '另一个', 'With': '和', 'Without': '没有', 'For': '为了',
    'From': '来自', 'Into': '进入', 'Over': '覆盖', 'Under': '下面', 'About': '关于',
    'According': '根据', 'Against': '反对', 'Among': '其中', 'Between': '之间', 'Through': '通过',
    'During': '期间', 'Including': '包括', 'Available': '可用', 'Unable': '无法', 'Unable': '无法',
    'Able': '能够', 'Can': '可以', 'Could': '可能', 'Would': '将会', 'Should': '应该',
    'Might': '可能', 'Will': '将', 'Must': '必须', 'May': '可能', 'Just': '只是',
    'Only': '只有', 'Even': '甚至', 'Also': '也', 'Still': '仍然', 'Yet': '仍然',
    'Already': '已经', 'Always': '总是', 'Never': '从不', 'Sometimes': '有时', 'Often': '经常',
    'Usually': '通常', 'Really': '真正', 'Very': '非常', 'Most': '最多', 'Very': '非常',
    'So': '所以', 'Because': '因为', 'Since': '自从', 'While': '当', 'Although': '虽然',
    'However': '然而', 'Therefore': '因此', 'Thus': '因此', 'Hence': '故', 'Otherwise': '否则',
    'Instead': '相反', 'Rather': '相当', 'Enough': '足够', 'Rather': '相当', 'Pretty': '相当',
    'How': '如何', 'What': '什么', 'When': '何时', 'Where': '在哪里', 'Which': '哪个',
    'Who': '谁', 'Why': '为什么', 'Here': '这里', 'There': '那里', 'Every': '每个',
    'Each': '每个', 'Both': '两个', 'Few': '几个', 'Most': '大多数', 'Other': '其他',
    'Such': '这样的', 'Same': '相同', 'Different': '不同', 'Like': '像', 'Unlike': '不像',
    'The': '', 'A': '', 'An': '', 'Is': '是', 'Are': '是', 'Was': '是', 'Were': '是',
    'Be': '是', 'Been': '是', 'Being': '是', 'Have': '有', 'Has': '有', 'Had': '有',
    'Do': '做', 'Does': '做', 'Did': '做', 'Done': '完成', 'Making': '制作',
    'Getting': '获取', 'Giving': '给予', 'Saying': '说', 'Going': '去', 'Coming': '来',
    'Taking': '拿', 'Putting': '放', 'Setting': '设置', ' Letting': '让', 'Letting': '让',
    'Running': '运行', 'Walking': '走', 'Playing': '玩', 'Working': '工作', 'Looking': '看',
    'Thinking': '思考', 'Feeling': '感觉', 'Wanting': '想要', 'Needing': '需要',
    'Trying': '尝试', 'Asking': '问', 'Finding': '发现', 'Telling': '告诉',
    'Year': '年', 'Day': '日', 'Week': '周', 'Month': '月', 'Hour': '小时',
    'Time': '时间', 'Day': '天', 'Morning': '早上', 'Evening': '晚上', 'Night': '夜晚',
    'Today': '今天', 'Tomorrow': '明天', 'Yesterday': '昨天', 'Online': '在线',
    'Offline': '离线', 'Together': '一起', 'Apart': '分开', 'Almost': '几乎', 'Nearly': '几乎',
    'Easy': '简单', 'Hard': '困难', 'Simple': '简单', 'Complex': '复杂', 'Fast': '快',
    'Slow': '慢', 'Quick': '快', 'Rapid': '快速', 'Better': '更好', 'Worse': '更差',
    'Higher': '更高', 'Lower': '更低', 'Larger': '更大', 'Smaller': '更小', 'Longer': '更长',
    'Shorter': '更短', 'Bigger': '更大', 'Little': '小', 'Big': '大', 'Small': '小',
    'Old': '旧', 'Young': '年轻', 'White': '白', 'Black': '黑', 'Red': '红', 'Blue': '蓝',
    'Green': '绿', 'Yellow': '黄', 'Strong': '强', 'Weak': '弱', 'Rich': '富', 'Poor': '穷',
}

# 重要性评分关键词
IMPORTANCE_KEYWORDS = {
    'critical': ['billion', 'acquisition', 'merger', 'ipo', '收购', '合并', '上市', '融资'],
    'high': ['launch', 'announces', 'introduces', 'release', '发布', '推出', '宣布', '重磅', '革命'],
    'medium': ['study', 'research', 'report', 'analysis', 'research', '研究', '报告', '分析', '趋势'],
}

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = re.sub(r'\s+', ' ', cleantext)
    return cleantext.strip()

def fetch_feed(url):
    try:
        resp = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        feed = feedparser.parse(resp.content)
        return feed
    except Exception as e:
        print(f"<!-- 抓取 {url} 失败: {str(e)} -->")
        return None

def is_relevant(title, summary):
    content = f"{title} {summary}".lower()
    for kw in KEYWORDS:
        if kw.lower() in content:
            return True
    return False

def is_within_72h(pub_date_str):
    if not pub_date_str:
        return True
    try:
        from datetime import timedelta
        formats = [
            "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S", "%a, %d %b %Y %H:%M:%S GMT", "%Y-%m-%d",
        ]
        pub_dt = None
        for fmt in formats:
            try:
                pub_dt = datetime.strptime(pub_date_str.strip(), fmt)
                break
            except:
                continue
        if pub_dt is None:
            try:
                parsed = feedparser._parse_date(pub_date_str)
                if parsed:
                    pub_dt = datetime(*parsed[:6])
            except:
                pass
        if pub_dt is None:
            return True
        if pub_dt.tzinfo is None:
            pub_dt = pub_dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
        now = datetime.now(pub_dt.tzinfo)
        diff = now - pub_dt
        return diff <= timedelta(hours=72)
    except:
        return True

def is_english(text):
    if not text:
        return False
    english_count = sum(1 for c in text if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == ' ')
    return english_count / len(text) > 0.5 if len(text) > 0 else False

def translate_title(title):
    """翻译英文标题为中文（无API版）"""
    return title

def get_source_name(url):
    source_map = {
        'techcrunch.com': 'TechCrunch', 'technologyreview.com': 'MIT科技评论',
        'openai.com': 'OpenAI', 'venturebeat.com': 'VentureBeat',
        'arstechnica.com': 'Ars Technica', 'wired.com': 'Wired',
        'artificialintelligence-news.com': 'AI News',
        'woshipm.com': '人人都是产品经理', 'ifanr.com': '爱范儿',
        'sspai.com': '少数派', '36kr.com': '36氪', '199it.com': '199IT',
        'jiqizhixin.com': '机器之心', 'qbitai.com': '量子位',
        'geekpark.net': '极客公园',
    }
    for domain, name in source_map.items():
        if domain in url:
            return name
    return '其他'

def score_article(title, summary):
    """给文章打分，返回 (分数, 等级)"""
    text = f"{title} {summary}".lower()
    score = 0

    # AI相关基础分
    ai_keywords = ['gpt', 'openai', 'llm', '大模型', '人工智能', 'agi', 'claude', 'gemini', 'anthropic']
    for kw in ai_keywords:
        if kw.lower() in text:
            score += 2

    # 重大事件关键词
    for kw in IMPORTANCE_KEYWORDS['critical']:
        if kw.lower() in text:
            score += 5
    for kw in IMPORTANCE_KEYWORDS['high']:
        if kw.lower() in text:
            score += 3
    for kw in IMPORTANCE_KEYWORDS['medium']:
        if kw.lower() in text:
            score += 1

    # 金额大值
    if any(m in text for m in ['$1b', '10亿', 'billion', '1.16b', '20亿', '380m']):
        score += 3

    # 评级
    if score >= 8:
        return score, '🔥🔥🔥'
    elif score >= 5:
        return score, '🔥🔥'
    elif score >= 3:
        return score, '🔥'
    else:
        return score, '📌'

def generate_digest(custom_sources=None):
    sources = DEFAULT_SOURCES.copy()
    if custom_sources:
        sources.extend(custom_sources)

    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    date_id = today.strftime("%Y-%m-%d")

    output = f"""---
title: {date_str} 科技日报
date: {date_id}
tags:
  - 科技资讯
  - 日报
  - AI
created: {today.strftime("%H:%M:%S")}
---

# 📰 {date_str} 科技资讯日报

> [!INFO] 数据来源
> 本日报汇总自 {len(sources)} 个 RSS 源，筛选近 72 小时内的 AI/科技热点资讯。

"""

    seen_urls = set()
    articles = []

    for url in sources:
        feed = fetch_feed(url)
        if not feed or not feed.entries:
            continue
        for entry in feed.entries[:5]:
            title = entry.get('title', '无标题')
            link = entry.get('link', '')
            if not link or link in seen_urls:
                continue
            seen_urls.add(link)
            summary = entry.get('description', entry.get('summary', ''))
            summary = clean_html(summary)
            if len(summary) > 200:
                summary = summary[:200] + "..."
            pub_date = entry.get('published', '')
            if not is_within_72h(pub_date):
                continue
            is_ai = is_relevant(title, summary)
            source = get_source_name(link)
            article_score, rating = score_article(title, summary)
            articles.append({
                'title': title,
                'summary': summary,
                'link': link,
                'source': source,
                'is_ai': is_ai,
                'score': article_score,
                'rating': rating
            })

    # 按评分排序
    articles.sort(key=lambda x: x['score'], reverse=True)

    # 深度洞察部分
    top_articles = articles[:5]
    ai_articles = [a for a in articles if a['is_ai']]
    other_articles = [a for a in articles if not a['is_ai']]

    # 洞察概要
    critical_count = sum(1 for a in articles if a['rating'] == '🔥🔥🔥')
    high_count = sum(1 for a in articles if a['rating'] == '🔥🔥')
    medium_count = sum(1 for a in articles if a['rating'] == '🔥')

    # 今日洞察表格
    output += f"""> [!ABSTRACT]- 今日洞察
> 共筛选 **{len(articles)}** 篇资讯，其中 **🔥🔥🔥 重磅** {critical_count} 篇、**🔥🔥 重点** {high_count} 篇、**🔥 值得关注** {medium_count} 篇。

| 等级 | 标题 | 来源 | 链接 |
|:---:|---|---|:---:|
"""

    for item in articles[:18]:
        title = item['title']
        if is_english(title):
            title = translate_title(title)
        # 截断长标题
        if len(title) > 40:
            title = title[:40] + '...'
        # 移除markdown特殊字符
        title = title.replace('|', '\\|').replace('\n', ' ')
        # 生成Obsidian可点击链接
        link_text = item['link']
        output += f"| {item['rating']} | {title} | {item['source']} | [🔗]({link_text}) |\n"

    output += "\n---\n\n"

    # AI领域
    if ai_articles:
        output += "## 🤖 AI 领域\n\n"
        for idx, item in enumerate(ai_articles[:10], 1):
            title = item['title']
            if is_english(title):
                title = translate_title(title)
            output += f"""### {idx}. {title} {item['rating']}

> [!ABSTRACT]+ 摘要
> {item['summary']}

- 🔗 [原文]({item['link']}) · {item['source']}

---

"""

    # 其他科技动态
    if other_articles:
        output += "## 💡 其他科技动态\n\n"
        for idx, item in enumerate(other_articles[:8], 1):
            title = item['title']
            if is_english(title):
                title = translate_title(title)
            output += f"""### {idx}. {title} {item['rating']}

> [!ABSTRACT]+ 摘要
> {item['summary']}

- 🔗 [原文]({item['link']}) · {item['source']}

---

"""

    # 底部来源列表
    output += """## 📚 订阅源列表

> [!TIP]+ 订阅源
> - TechCrunch AI · MIT 科技评论 · OpenAI · VentureBeat · The Verge
> - 人人都是产品经理 · 虎嗅 · 爱范儿 · 少数派 · 36氪
> - 199IT · 机器之心 · 量子位

"""

    return output

if __name__ == "__main__":
    custom_sources = sys.argv[1:] if len(sys.argv) > 1 else None
    digest = generate_digest(custom_sources)
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"科技日报_{today}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(digest)
    print(f"日报已生成: {output_file}")
