"""
Python 学习计划 Web 阅读程序
启动后访问 http://localhost:5000
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

from flask import Flask, render_template, request, jsonify, abort
import mistune

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
CHAPTERS_DIR = Path(__file__).parent / "chapters"
app = Flask(__name__)


# ---------------------------------------------------------------------------
# Markdown → HTML 渲染（使用 mistune 渲染后，为标题添加锚点 id）
# ---------------------------------------------------------------------------
_md_parser = mistune.create_markdown(
    renderer=mistune.HTMLRenderer(),
    plugins=[mistune.plugins.table.table],
)


def render_markdown(text: str) -> str:
    """将 Markdown 文本渲染为 HTML，并为标题添加锚点 id"""
    html = _md_parser(text)

    # 后处理：为 <h1>/<h2> 添加 id 锚点
    def add_anchor(m):
        tag_level = m.group(1)
        title_text = m.group(2)
        anchor = re.sub(r"[^\w一-鿿\-]", "", title_text.replace(" ", "-").replace("/", "-"))
        return f'<h{tag_level} id="{anchor}">{title_text}</h{tag_level}>'

    html = re.sub(
        r"<h([12])>(.+?)</h[12]>",
        add_anchor,
        html,
    )
    return html


# ---------------------------------------------------------------------------
# 章节元数据
# ---------------------------------------------------------------------------
CHAPTERS = [
    {"file": "ch01-intro.md",           "title": "第 1 章 · Python 入门"},
    {"file": "ch02-control-flow.md",    "title": "第 2 章 · 流程控制"},
    {"file": "ch03-data-structures.md", "title": "第 3 章 · 数据结构"},
    {"file": "ch04-functions.md",       "title": "第 4 章 · 函数"},
    {"file": "ch05-modules-packages.md","title": "第 5 章 · 模块与包"},
    {"file": "ch06-files-exceptions.md","title": "第 6 章 · 文件操作与异常处理"},
    {"file": "ch07-oop.md",             "title": "第 7 章 · 面向对象编程"},
    {"file": "ch08-advanced.md",        "title": "第 8 章 · 高级特性"},
    {"file": "ch09-practical-libs.md",  "title": "第 9 章 · 常用库实战"},
    {"file": "ch10-projects.md",        "title": "第 10 章 · 综合项目"},
]


def get_chapter_meta(filename: str) -> dict | None:
    """根据文件名获取章节元数据"""
    for ch in CHAPTERS:
        if ch["file"] == filename:
            return ch
    return None


# ---------------------------------------------------------------------------
# 章节节解析（提取每章的二级标题，用于首页索引）
# ---------------------------------------------------------------------------
def parse_sections(md_text: str) -> list[dict]:
    """从 markdown 文本中提取所有 ## 标题及其锚点"""
    sections = []
    for m in re.finditer(r"^##\s+(.+)$", md_text, re.MULTILINE):
        title = m.group(1).strip()
        anchor = re.sub(r"[^\w一-鿿\-]", "", title.replace(" ", "-").replace("/", "-"))
        sections.append({"title": title, "anchor": anchor})
    return sections


# ---------------------------------------------------------------------------
# 全文搜索引擎
# ---------------------------------------------------------------------------
class SearchEngine:
    """内存全文搜索引擎"""

    def __init__(self):
        self.index: dict[str, list[dict]] = defaultdict(list)
        # index 结构：{词 → [{chapter, chapter_title, section, line_num, line_text}, ...]}
        self._build()

    def _tokenize(self, text: str) -> list[str]:
        """分词：提取中文单字和英文单词"""
        tokens = []
        # 英文单词
        for m in re.finditer(r"[a-zA-Z_]\w*", text.lower()):
            tokens.append(m.group())
        # 中文单字组成的中文词（连续中文字符作为一个词）
        for m in re.finditer(r"[一-鿿]+", text):
            word = m.group()
            # 将连续中文按 2-gram 拆分以提升搜索精度
            if len(word) <= 3:
                tokens.append(word)
            else:
                for i in range(len(word) - 1):
                    tokens.append(word[i:i+2])
                tokens.append(word)  # 同时保留完整词
        return tokens

    def _build(self):
        """构建全文索引"""
        for ch in CHAPTERS:
            filepath = CHAPTERS_DIR / ch["file"]
            if not filepath.exists():
                continue
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")
            current_section = ch["title"]
            in_code_block = False

            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()

                # 跟踪代码块状态
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue

                if in_code_block:
                    continue  # 跳过代码块内的所有行

                # 跟踪当前二级标题
                if stripped.startswith("## "):
                    current_section = stripped[3:].strip()
                # 也跟踪一级标题
                elif stripped.startswith("# "):
                    current_section = stripped[2:].strip()

                if not stripped:
                    continue  # 跳过空行

                tokens = self._tokenize(stripped)
                for token in tokens:
                    self.index[token].append({
                        "chapter": ch["file"],
                        "chapter_title": ch["title"],
                        "section": current_section,
                        "line_num": line_num,
                        "line_text": stripped[:120],  # 截取前 120 字符
                    })

    def search(self, query: str, limit: int = 20) -> list[dict]:
        """搜索并返回结果列表"""
        if not query.strip():
            return []

        tokens = self._tokenize(query)
        if not tokens:
            return []

        # 收集所有匹配行及其分数
        scored: dict[tuple, dict] = {}  # key = (chapter, line_num)

        for token in tokens:
            for entry in self.index.get(token, []):
                key = (entry["chapter"], entry["line_num"])
                if key in scored:
                    scored[key]["score"] += 1
                else:
                    scored[key] = {**entry, "score": 1}

        # 按分数降序排列
        results = sorted(scored.values(), key=lambda x: x["score"], reverse=True)

        # 同一章节同一小节去重（只保留最高分的行），但保留不同行
        seen = set()
        deduped = []
        for r in results:
            key = (r["chapter"], r["line_num"])
            if key not in seen:
                seen.add(key)
                deduped.append(r)

        return deduped[:limit]


# 全局搜索引擎实例（启动时构建）
search_engine = SearchEngine()


# ---------------------------------------------------------------------------
# Flask 路由
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """首页：章节索引 + 搜索栏"""
    chapters_with_sections = []
    for ch in CHAPTERS:
        filepath = CHAPTERS_DIR / ch["file"]
        if filepath.exists():
            sections = parse_sections(filepath.read_text(encoding="utf-8"))
        else:
            sections = []
        chapters_with_sections.append({**ch, "sections": sections})

    return render_template("index.html", chapters=chapters_with_sections)


@app.route("/chapter/<filename>")
def chapter(filename: str):
    """章节阅读页"""
    ch = get_chapter_meta(filename)
    if not ch:
        abort(404)

    filepath = CHAPTERS_DIR / filename
    if not filepath.exists():
        abort(404)

    md_content = filepath.read_text(encoding="utf-8")
    html_content = render_markdown(md_content)

    # 上一章 / 下一章
    idx = next((i for i, c in enumerate(CHAPTERS) if c["file"] == filename), -1)
    prev_ch = CHAPTERS[idx - 1] if idx > 0 else None
    next_ch = CHAPTERS[idx + 1] if idx < len(CHAPTERS) - 1 else None

    return render_template(
        "chapter.html",
        chapter=ch,
        content=html_content,
        prev_ch=prev_ch,
        next_ch=next_ch,
    )


@app.route("/api/search")
def api_search():
    """搜索 API，返回 JSON"""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": [], "query": ""})

    results = search_engine.search(query)

    # 为每个结果生成跳转链接
    for r in results:
        section_anchor = re.sub(
            r"[^\w一-鿿\-]",
            "",
            r["section"].replace(" ", "-").replace("/", "-"),
        )
        r["link"] = f"/chapter/{r['chapter']}#{section_anchor}"

    return jsonify({"results": results, "query": query, "total": len(results)})


# ---------------------------------------------------------------------------
# 404 处理
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("chapter.html",
                           chapter={"title": "404 - 页面未找到", "file": ""},
                           content="<p>该章节不存在，<a href='/'>返回首页</a></p>",
                           prev_ch=None, next_ch=None), 404


# ---------------------------------------------------------------------------
# 启动
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Windows 终端 GBK 编码不兼容某些字符，用纯 ASCII
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 50)
    print("  [Python 学习计划] Web 阅读程序")
    print("  访问地址：http://localhost:5000")
    print("  按 Ctrl+C 停止服务")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
