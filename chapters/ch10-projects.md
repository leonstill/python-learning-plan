# 第 10 章 · 综合项目

本章将前面学到的所有知识融会贯通，用三个实战项目检验你的学习成果。每个项目给出**架构分析**和**关键代码**，完整实现留给你自己动手完成。

---

## 10.1 项目一：命令行待办事项工具

### 需求描述

一个在命令行下运行的待办事项管理器（TODO List），支持增删改查和持久化。

| 功能 | 命令 | 说明 |
|------|------|------|
| 添加任务 | `add 内容` | 可指定优先级 `--priority high\|medium\|low` |
| 查看所有 | `list` | 按优先级排序，显示序号 |
| 查看分类 | `list --status done\|todo` | 筛选已完成/未完成的任务 |
| 标记完成 | `done 序号` | 将任务标记为已完成 |
| 删除任务 | `delete 序号` | 确认后删除 |
| 退出 | `quit` | 自动保存到文件 |

### 架构设计

```
todo_app/
├── __init__.py
├── models.py        # 数据模型：Task 类
├── storage.py       # 数据持久化：JSON 文件读写
├── commands.py      # 命令处理：解析命令、执行业务逻辑
└── main.py          # 入口：命令行交互循环
```

**分层**：
- `models.py` — 数据层。只关心"任务是什么"，不关心怎么存、怎么显示。
- `storage.py` — 持久化层。负责把任务列表存到 JSON 文件和读回来。
- `commands.py` — 业务逻辑层。接收解析后的命令参数，执行增删改查。
- `main.py` — 表示层/入口。命令行交互循环，解析用户输入，调用 commands。

### 关键代码

**数据模型**（`models.py`）：

```python
from datetime import datetime
from enum import Enum

class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class Task:
    """待办任务的数据模型"""
    def __init__(self, id: int, content: str, priority: Priority = Priority.MEDIUM):
        self.id = id
        self.content = content
        self.priority = priority
        self.done = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def mark_done(self):
        self.done = True
        self.completed_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """序列化为字典，用于 JSON 存储"""
        return {
            "id": self.id,
            "content": self.content,
            "priority": self.priority.name,
            "done": self.done,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        """从字典反序列化"""
        task = cls(
            id=d["id"],
            content=d["content"],
            priority=Priority[d["priority"]],
        )
        task.done = d["done"]
        task.created_at = d["created_at"]
        task.completed_at = d.get("completed_at")
        return task
```

**持久化层**（`storage.py`）：

```python
import json
from pathlib import Path
from models import Task

DATA_FILE = Path("tasks.json")

def load_tasks() -> list[Task]:
    """从 JSON 文件加载任务列表"""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(d) for d in data]

def save_tasks(tasks: list[Task]):
    """将任务列表保存到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
```

**命令处理**（`commands.py` 核心框架）：

```python
from models import Task, Priority
from storage import load_tasks, save_tasks

tasks = []    # 当前内存中的任务列表

def init():
    """启动时加载数据"""
    global tasks
    tasks = load_tasks()

def add_task(content: str, priority: str = "MEDIUM"):
    new_id = max([t.id for t in tasks], default=0) + 1
    task = Task(new_id, content, Priority[priority.upper()])
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ 已添加任务 #{new_id}：{content}")

def list_tasks(status: str = None):
    """列出任务。status 为 'done'/'todo'/None"""
    filtered = tasks
    if status == "done":
        filtered = [t for t in tasks if t.done]
    elif status == "todo":
        filtered = [t for t in tasks if not t.done]

    # 按优先级排序
    filtered.sort(key=lambda t: t.priority.value)

    if not filtered:
        print("📭 没有相关任务")
        return

    for t in filtered:
        status_icon = "✅" if t.done else "⬜"
        priority_icon = {Priority.HIGH: "🔴", Priority.MEDIUM: "🟡", Priority.LOW: "🟢"}
        print(f"  {status_icon} [{t.id}] {priority_icon[t.priority]} {t.content}")

def mark_done(task_id: int):
    for t in tasks:
        if t.id == task_id:
            t.mark_done()
            save_tasks(tasks)
            print(f"✅ 任务 #{task_id} 已完成！")
            return
    print(f"❌ 未找到任务 #{task_id}")

def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    save_tasks(tasks)
    print(f"🗑 任务 #{task_id} 已删除")
```

**入口**（`main.py`）：

```python
import sys
from commands import init, add_task, list_tasks, mark_done, delete_task

def main():
    init()
    print("📋 待办事项管理器")
    print("输入 help 查看命令")

    while True:
        try:
            raw = input("\n>>> ").strip()
            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()

            if cmd == "quit":
                print("👋 再见！")
                break
            elif cmd == "list":
                status = None
                if "--status" in raw:
                    status = parts[parts.index("--status") + 1]
                list_tasks(status)
            elif cmd == "add":
                content = " ".join(parts[1:])
                priority = "MEDIUM"
                if "--priority" in raw:
                    idx = parts.index("--priority")
                    priority = parts[idx + 1]
                    content = content.replace(f"--priority {priority}", "").strip()
                add_task(content, priority)
            elif cmd == "done":
                mark_done(int(parts[1]))
            elif cmd == "delete":
                delete_task(int(parts[1]))
            elif cmd == "help":
                print("add <内容> [--priority high|medium|low]")
                print("list [--status done|todo]")
                print("done <序号> | delete <序号> | quit")
            else:
                print(f"未知命令: {cmd}（输入 help 查看帮助）")

        except (ValueError, IndexError) as e:
            print(f"命令格式错误：{e}")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break

if __name__ == "__main__":
    main()
```

### 关键设计要点

- **序列化/反序列化**：`to_dict()` / `from_dict()` 是数据模型的基础方法，让存储和业务逻辑解耦。
- **枚举（Enum）**：优先级用 `Enum` 限定可选值，避免字符串拼写错误。
- **`pathlib.Path`**：跨平台友好的路径处理。
- **列表推导式**：`list_tasks` 中的过滤和排序大量用到了第 8 章的知识。

---

### ⭐ 练习 10.1

1. 补全上面的代码，实现完整的 `commands.py`（包括所有边界情况：删除不存在的任务、重复标记完成等）。
2. 额外功能：添加 `edit 序号 新内容` 命令，支持修改任务描述。
3. 额外功能：添加 `sort --by date|priority` 切换排序方式。

---

## 10.2 项目二：简易网页爬虫

### 需求描述

爬取指定网页的标题和正文内容，并将结果保存为文件。

| 功能 | 说明 |
|------|------|
| 爬取单页 | 输入 URL，提取标题和所有段落文本 |
| 保存结果 | 保存为 `.txt` 或 `.md` 文件 |
| 批量爬取 | 从文件读取 URL 列表，逐个爬取 |
| 速率限制 | 请求间隔不小于 1 秒，避免被封 |

### 架构设计

```
simple_crawler/
├── __init__.py
├── fetcher.py       # HTTP 请求 + 重试（封装 requests）
├── parser.py        # HTML 解析（提取标题、段落）
├── storage.py       # 结果持久化
└── main.py          # 入口 + 命令行参数
```

**选库分析**：

HTML 的解析有几种选择：

| 方案 | 优点 | 缺点 |
|------|------|------|
| **BeautifulSoup** (`bs4`) | 容错性强，API 友好，文档好 | 速度一般 |
| `lxml` | 速度快，支持 XPath | 对破损 HTML 容错差 |
| 正则表达式 | 不额外安装 | 解析 HTML 很脆弱，各种 edge case |

**推荐 BeautifulSoup**，适合学习。`pip install beautifulsoup4 requests`。

### 关键代码

**请求模块**（`fetcher.py`）：

```python
import time
import requests
from typing import Optional

class Fetcher:
    """HTTP 请求器，内置重试和速率限制"""

    def __init__(self, timeout: int = 10, retries: int = 3, delay: float = 1.0):
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self._last_request_time = 0

    def _rate_limit(self):
        """确保两次请求间隔不少于 delay 秒"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request_time = time.time()

    def fetch(self, url: str) -> Optional[str]:
        """获取网页 HTML，失败返回 None"""
        for attempt in range(1, self.retries + 1):
            self._rate_limit()
            try:
                response = requests.get(
                    url,
                    timeout=self.timeout,
                    headers={"User-Agent": "SimpleCrawler/1.0 (Learning)"}
                )
                response.raise_for_status()
                response.encoding = response.apparent_encoding  # 自动检测编码
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"[尝试 {attempt}/{self.retries}] {url} 失败: {e}")
                if attempt == self.retries:
                    return None
                time.sleep(2 ** attempt)   # 指数退避：2s, 4s, 8s...
        return None
```

**解析模块**（`parser.py`）：

```python
from bs4 import BeautifulSoup
from typing import Optional
from dataclasses import dataclass, asdict

@dataclass
class PageContent:
    """解析后的网页内容"""
    url: str
    title: str
    paragraphs: list[str]
    word_count: int

def parse(html: str, url: str) -> PageContent:
    """从 HTML 中提取标题和正文"""
    soup = BeautifulSoup(html, "html.parser")

    # 标题：优先 <title> 标签，其次 <h1>
    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)
    elif soup.h1:
        title = soup.h1.get_text(strip=True)

    # 移除无关标签
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # 提取所有段落文本
    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 30:    # 过滤太短的"假"段落
            paragraphs.append(text)

    word_count = sum(len(p) for p in paragraphs)
    return PageContent(url=url, title=title, paragraphs=paragraphs, word_count=word_count)
```

**批量爬取流程**（`main.py` 核心流程）：

```python
def crawl_batch(urls: list[str], output_dir: str = "output"):
    """批量爬取并保存"""
    fetcher = Fetcher(delay=1.0)
    results = []

    for url in urls:
        html = fetcher.fetch(url)
        if html is None:
            results.append({"url": url, "status": "失败"})
            continue

        content = parse(html, url)

        # 保存为 Markdown 文件
        filename = slugify(content.title) or "untitled"
        filepath = Path(output_dir) / f"{filename}.md"
        save_as_markdown(content, filepath)

        results.append({"url": url, "status": "成功", "file": str(filepath)})

    # 输出汇总
    print(f"\n📊 汇总：{len(results)} 个 URL")
    success = [r for r in results if r["status"] == "成功"]
    print(f"  成功：{len(success)}，失败：{len(results) - len(success)}")
    return results
```

### 关键设计要点

- **速率限制**（`_rate_limit`）：爬虫的基本礼仪，也是自我保护——发太快容易被封 IP。
- **指数退避**：重试间隔逐渐延长（2s → 4s → 8s），给服务器恢复时间。
- **编码自动检测**：`apparent_encoding` 用 chardet 推测网页编码，避免中文乱码。
- **`dataclass`**：`@dataclass` 是 Python 3.7+ 的特性，自动生成 `__init__`、`__repr__` 等，适合做纯数据模型。
- **HTML 清洗**：移除 script/style/nav/footer 等无关标签，避免噪音。

---

### ⭐ 练习 10.2

1. 实现 `save_as_markdown()` 函数，将 `PageContent` 保存为格式良好的 Markdown 文件。
2. 添加 `--depth 2` 支持——爬取页面内的链接（同域名），实现简单的二级深度爬取。
3. 思考：如何避免重复爬取同一个 URL？如果网页 A 链接到 B，B 又链接到 A 怎么办？

---

## 10.3 项目三：数据分析入门

### 需求描述

读取一个 CSV 数据文件，进行清洗、统计和可视化，最后输出分析报告。

这里以一个假设的销售数据为例：`sales.csv` 包含字段 `日期,商品,类别,单价,数量,销售额`。

| 功能 | 说明 |
|------|------|
| 数据读取 | 读取 CSV，自动处理编码和缺失值 |
| 数据清洗 | 去除异常值、填充缺失、类型转换 |
| 统计分析 | 按类别汇总、月度趋势、商品排行 |
| 数据可视化 | 生成柱状图和折线图（可选，见下文） |
| 报告生成 | 输出 Markdown 格式的分析报告 |

### 架构设计

```
data_analysis/
├── __init__.py
├── reader.py        # 数据读取与清洗
├── analysis.py      # 统计分析函数
├── report.py        # 报告生成
└── main.py          # 入口
```

**可视化方案选择**：

| 方案 | 安装 | 适用场景 |
|------|------|----------|
| **matplotlib** | `pip install matplotlib` | 经典方案，功能全面 |
| plotly | `pip install plotly` | 交互式图表 |
| 纯文本（terminaltables） | `pip install terminaltables` | 如果不想引入重量依赖 |

轻量场景选 matplotlib，或简单用表格输出结果。下面用 matplotlib。

### 关键代码

**数据读取与清洗**（`reader.py`）：

```python
import csv
from collections import namedtuple
from datetime import datetime

# 用 namedtuple 定义一行数据的结构（比 dataclass 更轻量）
SaleRecord = namedtuple("SaleRecord", ["date", "product", "category", "price", "quantity", "revenue"])

def load_csv(filepath: str) -> list[SaleRecord]:
    """读取并清洗 CSV 数据"""
    records = []

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = SaleRecord(
                    date=datetime.strptime(row["日期"], "%Y-%m-%d").date(),
                    product=row["商品"].strip(),
                    category=row["类别"].strip(),
                    price=float(row["单价"]),
                    quantity=int(row["数量"]),
                    revenue=float(row["销售额"]),
                )
                # 数据校验：跳过异常值
                if record.price <= 0 or record.quantity <= 0 or record.revenue < 0:
                    continue
                records.append(record)
            except (ValueError, KeyError) as e:
                print(f"跳过异常行：{row} → {e}")
                continue

    print(f"✅ 共读取 {len(records)} 条有效记录")
    return records
```

**统计分析**（`analysis.py` 核心函数）：

```python
from collections import defaultdict
from reader import SaleRecord

def summary_by_category(records: list[SaleRecord]) -> dict:
    """按类别汇总销售额"""
    result = defaultdict(float)
    for r in records:
        result[r.category] += r.revenue
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

def monthly_trend(records: list[SaleRecord]) -> dict:
    """月度销售额趋势"""
    result = defaultdict(float)
    for r in records:
        key = r.date.strftime("%Y-%m")
        result[key] += r.revenue
    return dict(sorted(result.items()))

def top_products(records: list[SaleRecord], n: int = 10) -> list[tuple]:
    """销售额 Top-N 商品"""
    result = defaultdict(float)
    for r in records:
        result[r.product] += r.revenue
    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:n]

def stats_summary(records: list[SaleRecord]) -> dict:
    """整体统计指标"""
    revenues = [r.revenue for r in records]
    return {
        "总销售额": sum(revenues),
        "平均单笔": sum(revenues) / len(revenues) if revenues else 0,
        "最高单笔": max(revenues) if revenues else 0,
        "总订单数": len(records),
        "商品种类": len(set(r.product for r in records)),
        "日期范围": f"{min(r.date for r in records)} ~ {max(r.date for r in records)}",
    }
```

**可视化**（`analysis.py` 中的绘图函数）：

```python
import matplotlib.pyplot as plt
from collections import Counter

def plot_category_pie(category_data: dict, output_path: str = "category_pie.png"):
    """绘制类别占比饼图"""
    # 设置中文字体
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 饼图
    ax1.pie(category_data.values(), labels=category_data.keys(),
            autopct="%1.1f%%", startangle=90)
    ax1.set_title("各类别销售额占比")

    # 柱状图
    ax2.bar(category_data.keys(), category_data.values())
    ax2.set_title("各类别销售额")
    ax2.set_ylabel("销售额（元）")
    ax2.tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"📊 图表已保存至 {output_path}")

def plot_monthly_trend(trend_data: dict, output_path: str = "trend.png"):
    """绘制月度趋势折线图"""
    plt.figure(figsize=(10, 5))
    months = list(trend_data.keys())
    values = list(trend_data.values())
    plt.plot(months, values, marker="o", linewidth=2, markersize=6)
    plt.title("月度销售额趋势")
    plt.xlabel("月份")
    plt.ylabel("销售额（元）")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
```

**报告生成**（`report.py` 框架）：

```python
def generate_report(stats, category_data, trend_data, top10, output_path="report.md"):
    """生成 Markdown 格式的分析报告"""
    lines = [
        "# 📊 销售数据分析报告",
        f"生成日期：{datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## 一、整体概览",
        "| 指标 | 数值 |",
        "|------|------|",
    ]
    for key, value in stats.items():
        if isinstance(value, float):
            lines.append(f"| {key} | {value:,.2f} |")
        else:
            lines.append(f"| {key} | {value} |")

    lines += [
        "",
        "## 二、类别分析",
        "| 类别 | 销售额 |",
        "|------|--------|",
    ]
    for cat, revenue in category_data.items():
        lines.append(f"| {cat} | {revenue:,.2f} |")

    lines += [
        "",
        "## 三、月度趋势",
        "| 月份 | 销售额 |",
        "|------|--------|",
    ]
    for month, revenue in trend_data.items():
        lines.append(f"| {month} | {revenue:,.2f} |")

    lines += [
        "",
        "## 四、热销商品 Top 10",
        "| 排名 | 商品 | 销售额 |",
        "|------|------|--------|",
    ]
    for i, (product, revenue) in enumerate(top10, 1):
        lines.append(f"| {i} | {product} | {revenue:,.2f} |")

    lines += [
        "",
        "## 五、可视化",
        "![类别占比](category_pie.png)",
        "![月度趋势](trend.png)",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📄 报告已生成：{output_path}")
```

### 关键设计要点

- **`collections.defaultdict`**：统计汇总的神器，不用每次检查键是否已存在。
- **`collections.namedtuple`**：比普通元组有名字，比类轻量。适合表示表格里的一行。
- **函数式管道**：数据流是 `读取 → 清洗 → 分析 → 图表 → 报告`，每个环节是纯函数，互相独立。
- **编码处理**：`utf-8-sig` 处理 Excel 导出的 CSV 可能带的 BOM 头。
- **matplotlib 中文**：设置 `font.sans-serif` 解决中文乱码，是 Windows 环境的典型问题。

---

### ⭐ 练习 10.3

1. 自己生成一份模拟 CSV 数据（或用代码 `random` 生成），然后用上面的代码做分析，输出报告。
2. 添加一个分析功能：计算每个商品在各类别中的"销售额占比"（该商品在所属类别中的贡献率）。
3. 扩展：如果数据里有 `区域` 字段，如何按区域做对比分析？尝试实现。

---

## 🌟 结语：下一步学什么

恭喜你完成这 10 章的学习！你现在已经掌握了 Python 的核心知识。如果继续深入，以下几条路线供参考：

| 方向 | 下一步学什么 |
|------|-------------|
| **Web 开发** | Flask / FastAPI → Django → 数据库（SQLAlchemy） → 部署 |
| **数据分析** | pandas → NumPy → SQL → Jupyter → Tableau/Power BI |
| **AI / 机器学习** | NumPy → pandas → scikit-learn → PyTorch / TensorFlow |
| **自动化运维** | 脚本化日常工作 → subprocess → Ansible → Docker → CI/CD |
| **爬虫进阶** | Scrapy 框架 → 反爬策略 → 分布式爬虫 → 数据清洗 |

无论选哪条路，**多写代码**永远是最高效的学习方式。祝你编程愉快！🚀
