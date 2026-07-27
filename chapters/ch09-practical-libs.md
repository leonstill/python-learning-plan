# 第 9 章 · 常用库实战

---

## 9.1 datetime：时间处理

处理时间是编程中最常见的需求之一，也是一个出名的"坑"——时区、闰年、夏令时……好在 Python 的 `datetime` 模块足够好用。

### 获取当前时间

```python
from datetime import datetime, date, timedelta

now = datetime.now()           # 当前日期和时间
today = date.today()           # 只有日期
print(now)                     # 2024-07-15 14:30:22.123456
print(today)                   # 2024-07-15
```

### 日期时间运算

```python
# 日期加减
tomorrow = today + timedelta(days=1)
yesterday = today - timedelta(days=1)
one_hour_later = now + timedelta(hours=1)

# 日期差
days_passed = tomorrow - yesterday    # timedelta(days=2)
print(days_passed.days)               # 2

# 比较
print(tomorrow > today)               # True
```

### 字符串 ↔ 日期互转

```python
# 字符串 → 日期
birthday = datetime.strptime("2000-08-15", "%Y-%m-%d")

# 日期 → 字符串
formatted = now.strftime("%Y年%m月%d日 %H:%M:%S")
print(formatted)   # 2024年07月15日 14:30:22
```

常用格式符：`%Y`(四位年)、`%m`(月)、`%d`(日)、`%H`(时24)、`%M`(分)、`%S`(秒)、`%A`(星期几)。

### 实用示例：计算年龄

```python
def calculate_age(birth_date_str):
    birth = datetime.strptime(birth_date_str, "%Y-%m-%d")
    today = date.today()
    age = today.year - birth.year
    # 如果今年的生日还没到，年龄减 1
    if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
        age -= 1
    return age

print(calculate_age("2000-08-15"))   # 结果取决于当前年份（例如在 2024 年为 23 或 24）
```

---

### ⭐ 练习 9.1

1. 输入你的出生日期，计算你来到这个世界多少天。
2. 写一个函数，接收两个日期字符串，返回它们之间相隔多少天（忽略时间部分）。

---

## 9.2 re：正则表达式

正则表达式是用于匹配和提取文本模式的"迷你语言"，强大但语法晦涩。`re` 是 Python 的正则模块。

### 核心函数

```python
import re

text = "联系电话：138-0000-1234，备用：139-1111-5678"

# search：找第一个匹配
match = re.search(r"\d{3}-\d{4}-\d{4}", text)
print(match.group())                 # 138-0000-1234

# findall：找所有匹配
phones = re.findall(r"\d{3}-\d{4}-\d{4}", text)
print(phones)                        # ['138-0000-1234', '139-1111-5678']

# match：从开头匹配（和 search 不同）
print(re.match(r"abc", "abcdef"))    # <re.Match>
print(re.match(r"abc", "xabcdef"))   # None（不是从开头）

# sub：替换
masked = re.sub(r"\d{3}-\d{4}-\d{4}", "***-****-****", text)
print(masked)   # 联系电话：***-****-****，备用：***-****-****

# split：用正则切分
re.split(r"[,;，；]", "苹果,香蕉；橘子，西瓜")   # ['苹果', '香蕉', '橘子', '西瓜']
```

### 常用模式速查

| 模式 | 含义 | 示例 |
|------|------|------|
| `\d` | 数字 | `\d{3}` = 三位数字 |
| `\w` | 字母/数字/下划线 | `\w+` = 一个或多个单词字符 |
| `\s` | 空白字符 | `\s*` = 零个或多个空白 |
| `.` | 任意字符 | `a.c` → abc, a1c, a_c |
| `+` | 1个以上 | `\d+` = 一个或多个数字 |
| `*` | 0个以上 | `\s*` = 可选空白 |
| `?` | 0或1个 | `https?` → http 或 https |
| `[]` | 字符类 | `[aeiou]` = 任意元音字母 |
| `[^]` | 否定字符类 | `[^0-9]` = 非数字 |
| `()` | 分组捕获 | `(\d{3})-(\d{4})` 分成两组 |
| `^` | 开头 | `^Hello` |
| `$` | 结尾 | `world$` |

### 原始字符串

正则前面加 `r`（`r"\d+"`）表示**原始字符串**，让反斜杠保持原样。不用 `r` 的话，`\d` 中的 `\` 会被 Python 先转义——导致各种诡异 bug。**写正则永远加 `r`。**

### 分组捕获

```python
match = re.search(r"(\d{3})-(\d{4})-(\d{4})", "138-0000-1234")
print(match.group(0))   # 138-0000-1234（完整匹配）
print(match.group(1))   # 138（第一个括号）
print(match.group(2))   # 0000（第二个括号）
print(match.groups())   # ('138', '0000', '1234')
```

---

### ⭐ 练习 9.2

1. 写一个正则表达式，判断一个字符串是否是有效的邮箱地址（简单的规则：`xxx@xx.xx` 即可）。
2. 从字符串 `"订单号：20240715-003 金额：¥299.50 订单号：20240715-004 金额：¥45.00"`中用正则提取所有订单号和金额。

---

## 9.3 json：数据序列化

JSON 是目前最通用的数据交换格式。`json` 模块实现 Python 对象和 JSON 之间的互转。

### 基本用法

```python
import json

# Python → JSON 字符串（序列化）
data = {
    "name": "小明",
    "age": 18,
    "scores": [85, 90, 92],
    "married": False
}

json_str = json.dumps(data, ensure_ascii=False)
print(json_str)
# {"name": "小明", "age": 18, "scores": [85, 90, 92], "married": false}

# JSON 字符串 → Python（反序列化）
parsed = json.loads(json_str)
print(parsed["name"])    # 小明
```

- `json.dumps()` — Python 对象 → JSON **字符串**
- `json.loads()` — JSON **字符串** → Python 对象
- `ensure_ascii=False` — 保留中文，不转成大 `\uXXXX`

### 文件读写

```python
# 写入 JSON 文件
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    # indent=2 让输出格式化，有缩进，方便阅读

# 读取 JSON 文件
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
```

### 类型对照

| Python | JSON |
|--------|------|
| `dict` | `object` |
| `list` | `array` |
| `str` | `string` |
| `int/float` | `number` |
| `True/False` | `true/false` |
| `None` | `null` |

注意 Python 的 `tuple` 序列化后会变成 JSON array，反序列化后回到 `list`。

---

### ⭐ 练习 9.3

1. 创建一个 Python 字典，包含你的个人信息（姓名、年龄、爱好列表等），用 `dumps` 转成 JSON 并打印。
2. 将上面的 JSON 写入一个文件，然后从该文件中重新读取并解析回 Python 对象。

---

## 9.4 requests：网络请求

`requests` 是 Python 最受欢迎的第三方库（`pip install requests`），让你用极少代码发送 HTTP 请求。

> HTTP 请求是浏览器和服务器之间的通信方式。浏览器输入网址按回车，本质上就是发了一个 GET 请求。

### GET 请求

```python
import requests

# 简单请求
response = requests.get("https://api.github.com")
print(response.status_code)        # 200 表示成功
print(response.text[:200])         # 响应内容（字符串）

# 解析 JSON 响应
data = response.json()             # 直接把 JSON 响应转成 Python 对象
print(data.keys())

# 带参数的请求
response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "python tutorial", "sort": "stars"}
)
result = response.json()
print(f"共找到 {result['total_count']} 个仓库")

# 自定义请求头
headers = {"User-Agent": "My-App/1.0"}
response = requests.get("https://api.github.com", headers=headers)
```

### POST 请求

```python
# 发送 JSON 数据
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "小明", "message": "你好"}
)
print(response.json())
```

### 错误处理

```python
try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()    # 4xx 或 5xx 时抛异常
    data = response.json()
except requests.exceptions.Timeout:
    print("请求超时，请检查网络")
except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")
```

**几个好习惯**：总是设置 `timeout`、检查状态码、用 `try/except` 处理网络异常。

---

### ⭐ 练习 9.4

1. 用 `requests` 获取 `https://api.github.com/users/python` 的信息，打印用户名、仓库数量、粉丝数。
2. 写一个函数，接收一个 URL，尝试 GET 请求，成功返回内容长度，失败返回错误信息。

---

## 9.5 unittest：单元测试

写测试是"今天多花 10 分钟，以后省下 10 小时"的投资。Python 自带 `unittest` 模块。

### 基本用法

首先有一个要测试的模块 `calculator.py`：

```python
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

创建测试文件 `test_calculator.py`：

```python
import unittest
from calculator import add, divide

class TestCalculator(unittest.TestCase):

    def test_add_positive(self):
        self.assertEqual(add(3, 5), 8)

    def test_add_negative(self):
        self.assertEqual(add(-3, 5), 2)
        self.assertEqual(add(-3, -5), -8)

    def test_divide_normal(self):
        self.assertAlmostEqual(divide(10, 3), 3.33333, places=4)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):   # 期待抛出 ValueError
            divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```

运行：`python test_calculator.py`

### 常用断言

| 断言方法 | 用途 |
|----------|------|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `x is True` |
| `assertFalse(x)` | `x is False` |
| `assertIn(item, container)` | `item in container` |
| `assertRaises(Error, func)` | func 抛出指定异常 |
| `assertAlmostEqual(a, b)` | 浮点数近似相等 |

### setUp 与 tearDown：公共的准备和清理

如果多个测试有相同的准备工作（比如都要创建一个临时文件），可以放在 `setUp` 和 `tearDown` 里——每个测试方法执行前后自动调用：

```python
import os
import unittest


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        """每个测试方法运行前自动调用"""
        self.test_file = "temp_test.txt"
        with open(self.test_file, "w") as f:
            f.write("test data")

    def tearDown(self):
        """每个测试方法运行后自动调用（无论测试是否失败）"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_read_file(self):
        with open(self.test_file, "r") as f:
            self.assertEqual(f.read(), "test data")

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.test_file))
```

### 测试的原则

- **一个测试只测一件事**：`test_divide_normal` 不负责测"除零"
- **测试命名要描述场景**：`test_divide_by_zero` 一看就知道测什么
- **先写测试再写功能（TDD）** 是个理想状态，但至少功能写完后**立刻补测试**
- **修改代码后跑一遍测试**——哪个测试挂了，你就知道哪里出了问题

> `unittest` 是标准库中的测试框架。社区中还有一个更流行的第三方选择 **pytest**（`pip install pytest`），语法更简洁（普通函数加 `assert` 即可，无需继承 `TestCase`），遇到时可以了解一下。

---

### ⭐ 练习 9.5

1. 给之前写的 `utils.py` 中的函数写一套 `unittest` 测试。至少用上三种不同的断言方法。
2. 故意在测试里写一个错误断言，运行看看失败的测试长什么样。

---

## 9.6 logging：专业的日志记录

教程前面一直用 `print()` 输出信息，这对小脚本够用。但在正式项目中，你需要 `logging`——它能控制输出级别、写入文件、带上时间戳和模块名。

### 基本用法

```python
import logging

# 配置日志级别和格式（只需在程序入口配置一次）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 使用不同级别输出日志
logging.debug("调试信息：变量 x = 42")      # 默认不显示
logging.info("服务器启动成功，端口 8080")
logging.warning("磁盘空间不足，剩余 5%")
logging.error("连接数据库失败")
logging.critical("系统即将崩溃！")
```

输出示例：
```
2024-07-15 14:30:22 [INFO] 服务器启动成功，端口 8080
2024-07-15 14:30:25 [WARNING] 磁盘空间不足，剩余 5%
2024-07-15 14:30:28 [ERROR] 连接数据库失败
2024-07-15 14:30:30 [CRITICAL] 系统即将崩溃！
```

### 五个级别

| 级别 | 用途 |
|------|------|
| `DEBUG` | 开发调试用的详细信息 |
| `INFO` | 正常的运行状态记录 |
| `WARNING` | 有潜在问题但不影响运行 |
| `ERROR` | 出错了，部分功能不可用 |
| `CRITICAL` | 严重错误，程序可能无法继续 |

`basicConfig` 中设置 `level=logging.INFO` 意味着只显示 INFO 及以上级别的日志（DEBUG 被过滤）。

### 写入文件

```python
logging.basicConfig(
    filename="app.log",        # 输出到文件而不是屏幕
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
```

### logging 比 print 好在哪？

- **控制级别**：上线时设为 WARNING，不删代码就静默了 DEBUG/INFO
- **自动附带元信息**：时间戳、模块名、行号等不用手动拼接
- **输出目标灵活**：可以同时输出到文件、控制台、远程服务器
- **不阻塞**：`print()` 写 stdout，可能被重定向或缓存干扰

---

### ⭐ 练习 9.6

1. 配置 `logging`，将 INFO 及以上日志写入 `app.log`，同时保持在控制台输出。
2. 把之前写的猜数字游戏中的 `print()` 提示替换为合适的 `logging` 级别。

---

## 🌟 章末练习

**天气查询小工具**

结合本章所学，做一个命令行天气查询器：

1. 使用的 API：`https://api.open-meteo.com`（免费天气 API，无需注册）

2. 功能要求：
   - 用户输入城市名称和经纬度（或直接输入经纬度）
   - 调用 API 获取当前天气和未来 3 天预报
   - 用 `requests` 发送请求，用 `json` 解析返回数据
   - 用 `datetime` 格式化日期显示
   - 用文件或 JSON 保存查询历史

3. API 示例（北京，纬度 39.9，经度 116.4）：
   ```
   https://api.open-meteo.com/v1/forecast?latitude=39.9&longitude=116.4&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Shanghai
   ```

4. 输出格式参考：
   ```
   🏙 北京 天气预报
   ─────────────────────
   当前天气：晴  |  温度：28°C

   📅 未来三天：
   2024-07-15  晴     最高 32°C / 最低 22°C
   2024-07-16  多云   最高 30°C / 最低 21°C
   2024-07-17  小雨   最高 27°C / 最低 20°C
   ```

5. 查询历史以 JSON 格式保存在 `weather_history.json`，之后查询时可查看历史。

> 提示：Open-Meteo 的 weathercode 需要查表转换（0=晴，1/2/3=多云，61/63/65=小雨等）。Open-Meteo 还提供城市搜索 API，试试找找看。
