# 第 5 章 · 模块与包

---

## 5.1 模块的导入与使用

当代码变多时，不可能把所有函数写在同一个文件里。Python 用**模块**来组织代码——一个 `.py` 文件就是一个模块。

### import 的几种写法

```python
# 方式一：导入整个模块
import math
print(math.sqrt(16))     # 4.0（用 模块名.函数名 调用）

# 方式二：只导入需要的部分
from math import sqrt, pi
print(sqrt(16))          # 4.0（直接使用，不需要前缀）
print(pi)                # 3.14159...

# 方式三：导入并取别名（解决重名问题）
import math as m
print(m.sqrt(16))

# 方式四：导入全部（不推荐）
from math import *       # 会污染命名空间，不知道导入了什么
```

### 推荐做法

- **首选 `import 模块名`**：调用时前缀清晰，知道函数来自哪里
- 只有当函数名很长或频繁调用时才用 `from 模块 import 函数`

### Python 查找模块的顺序

当你 `import` 一个模块，Python 按这个顺序找：

1. 当前目录
2. `PYTHONPATH` 环境变量中的目录
3. 标准库目录
4. 第三方包安装目录（site-packages）

可以用 `sys.path` 查看完整搜索路径：

```python
import sys
print(sys.path)
```

---

### ⭐ 练习 5.1

1. 用 `import random` 然后调用 `random.randint(1, 100)` 生成一个 1~100 的随机数，多运行几次观察。
2. 查一下 `math` 模块还有哪些常用函数（如 `ceil`、`floor`、`pow`），各写一个例子。

---

## 5.2 自定义模块

你写的 `.py` 文件，可以直接被另一个文件导入。

### 创建一个模块

`calculator.py`：

```python
"""一个简单的计算器模块"""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "错误：除数不能为 0"
    return a / b

# 测试代码
if __name__ == "__main__":
    print(add(1, 2))        # 只有直接运行此文件时才执行
    print("计算器模块测试完成")
```

`main.py`：

```python
from calculator import add, divide

print(add(3, 5))      # 8
print(divide(10, 2))  # 5.0
```

### `if __name__ == "__main__"` 是什么

这是 Python 中最重要的惯用法之一：

- 当一个 `.py` 文件被直接运行时，`__name__` 的值是 `"__main__"`
- 当它被作为模块导入时，`__name__` 的值是模块文件名（如 `"calculator"`）

所以 `if __name__ == "__main__":` 下面的代码只在直接运行时执行，导入时不执行。这让你可以在同一个文件里既写模块代码，又写测试代码。

---

### ⭐ 练习 5.2

1. 将第 4 章章末练习写的函数整理到 `utils.py` 中，用 `if __name__ == "__main__":` 加一段测试代码。
2. 新建 `main.py`，导入 `utils` 中的函数并调用验证。

---

## 5.3 包与包管理（pip）

### 什么是包

当模块更多时，可以用文件夹组织成**包**（package）。包就是一个包含 `__init__.py` 的文件夹。

```
mypackage/
├── __init__.py          # 标识这是一个包（3.3+ 可以省略，但建议保留）
├── math_utils.py
├── string_utils.py
└── data/
    ├── __init__.py
    └── io_utils.py
```

使用：

```python
from mypackage.math_utils import add
from mypackage.data.io_utils import read_file
```

`__init__.py` 可以为空，也可以在包被导入时执行初始化代码。你可以通过它在包级别暴露出常用接口。

### pip：Python 的包管理器

pip 用来安装和管理第三方包，这些包来自 [PyPI](https://pypi.org)（Python Package Index）。

```bash
# 安装
pip install requests

# 安装指定版本
pip install requests==2.28.0

# 查看已安装的包
pip list

# 卸载
pip uninstall requests

# 导出当前环境依赖
pip freeze > requirements.txt

# 批量安装依赖
pip install -r requirements.txt
```

### 虚拟环境（重要！）

不同项目可能需要同一包的不同版本。虚拟环境给每个项目一个独立的环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活（Windows）
venv\Scripts\activate

# 激活（Mac/Linux）
source venv/bin/activate

# 退出
deactivate
```

**养成习惯：每个项目一个虚拟环境。** 这样项目之间不会互相干扰，`requirements.txt` 也只记录本项目需要的依赖。

---

### ⭐ 练习 5.3

1. 创建一个虚拟环境，激活后在环境中 `pip install requests`，然后用 `pip list` 确认安装成功。
2. 用 `pip freeze > requirements.txt` 导出依赖，打开文件看看里面有什么。

---

## 5.4 常用标准库概览

Python 自带了大量实用的模块——这就是所谓的"电池已包含"。以下是最常用的几个。

### os — 操作系统接口

```python
import os
os.getcwd()            # 当前工作目录
os.listdir(".")        # 列出目录内容
os.path.join("a", "b", "c")    # 跨平台的路径拼接 → "a/b/c"
os.path.exists("test.txt")     # 文件是否存在
os.path.splitext("data.csv")   # ('data', '.csv')（分离扩展名）
```

### sys — 系统相关参数

```python
import sys
sys.argv              # 命令行参数列表
sys.exit(0)           # 退出程序
print(sys.version)    # Python 版本信息
```

### random — 随机数

```python
import random
random.random()           # [0, 1) 之间的随机浮点数
random.randint(1, 6)      # [1, 6] 之间的随机整数
random.choice(["苹果", "香蕉", "橘子"])  # 随机选一个
random.shuffle(deck)      # 原地打乱列表
```

### collections — 实用容器

```python
from collections import Counter, defaultdict

# Counter：一键统计
Counter("abracadabra")     # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# defaultdict：给不存在的键一个默认值
scores = defaultdict(list)  # 访问不存在的键时，自动创建空列表
scores["数学"].append(90)
```

### itertools — 迭代工具

```python
import itertools
itertools.permutations([1, 2, 3])     # 所有排列
itertools.combinations([1, 2, 3], 2)  # 所有组合（选 2 个）
itertools.product("AB", "12")          # 笛卡尔积 → A1, A2, B1, B2
```

更多模块（`datetime`、`re`、`json` 等）会在第 9 章详细展开。

---

### ⭐ 练习 5.4

1. 用 `os.path.join` 拼接一个路径，然后用 `os.path.exists` 检查它是否存在。
2. 用 `random.sample(range(1, 34), 6)` 模拟双色球红球选号。

---

## 🌟 章末练习

**命令行猜数字游戏（增强版）**

结合本章模块化和标准库，完成以下要求：

1. 创建包结构：
   ```
   guess_game/
   ├── __init__.py
   ├── game.py          # 游戏逻辑（生成答案、判断大小、计分）
   ├── utils.py         # 工具函数（读取/保存历史成绩）
   └── main.py          # 入口：命令行交互
   ```

2. 功能要求：
   - 随机生成 1-100 之间的答案（用 `random`）
   - 用户输入猜测，提示"太大"/"太小"，猜中后显示次数
   - 根据次数打分：1次100分，2-3次80分，4-6次60分，更多40分
   - 将每次游戏的成绩保存到 `history.txt`（用文件操作，可以等到第 6 章再实现）
   - 支持命令行参数 `--level easy` 控制难度（1-50 / 1-100 / 1-200）

3. 运行方式：
   ```bash
   python -m guess_game.main
   # 或者
   python -m guess_game.main --level hard
   ```
