# 第 8 章 · 高级特性

---

## 8.1 列表推导式与生成器表达式

列表推导式是 Python 最标志性的语法之一——用一行代码完成"遍历 + 过滤 + 转换"。

### 列表推导式

```python
# 传统写法：把 1~10 的平方放入列表
squares = []
for i in range(1, 11):
    squares.append(i ** 2)

# 列表推导式
squares = [i ** 2 for i in range(1, 11)]
# → [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

语法：`[表达式 for 变量 in 可迭代对象 if 条件]`

```python
# 带过滤：只保留偶数的平方
[i ** 2 for i in range(1, 11) if i % 2 == 0]
# → [4, 16, 36, 64, 100]

# 嵌套：展开二维列表
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
[item for row in matrix for item in row]
# → [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 条件表达式：偶数平方，奇数不变
[i ** 2 if i % 2 == 0 else i for i in range(1, 9)]
# → [1, 4, 3, 16, 5, 36, 7, 64]
```

### 字典和集合推导式

```python
# 字典推导式
{name: len(name) for name in ["张三", "李四", "王小明"]}
# → {'张三': 2, '李四': 2, '王小明': 3}

# 集合推导式
{i % 3 for i in range(20)}
# → {0, 1, 2}
```

### 生成器表达式

把方括号换成圆括号，就是**生成器表达式**——不会一次性生成所有数据，而是"用多少生成多少"，内存友好：

```python
sum(i ** 2 for i in range(1, 1000001))   # 不创建百万元素的列表
```

> 推导式可以让代码非常简洁，但不要走极端。如果逻辑超过三四层嵌套，拆成普通 `for` 循环可读性更好。

---

### ⭐ 练习 8.1

1. 用列表推导式生成 1~50 中所有能被 3 或 5 整除的数的列表。
2. 给定 `words = ["apple", "banana", "kiwi"]`，用字典推导式生成 `{单词: 长度}` 的字典。

---

## 8.2 迭代器与可迭代对象

你已经用了很久的迭代，现在是时候揭开它的面纱了。

### 概念辨析

- **可迭代对象（Iterable）**：能用 `for` 遍历的东西（列表、元组、字符串、集合、文件…），因为它有 `__iter__()` 方法
- **迭代器（Iterator）**：记住"遍历到哪了"的对象，有 `__next__()` 方法，调用一次返回下一个元素，耗尽时抛出 `StopIteration`

```python
nums = [1, 2, 3]

# 手动使用迭代器
it = iter(nums)          # 通过 iter() 获取迭代器
print(next(it))          # 1
print(next(it))          # 2
print(next(it))          # 3
print(next(it))          # StopIteration！

# for 循环的本质就是：
# it = iter(obj)
# while True:
#     try:
#         item = next(it)
#         ...处理 item...
#     except StopIteration:
#         break
```

### 自定义迭代器

```python
class Countdown:
    """从 n 倒数到 1 的迭代器"""
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self          # 迭代器自身就是自己的 __iter__

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        current = self.n
        self.n -= 1
        return current

for num in Countdown(5):
    print(num)               # 5 4 3 2 1
```

### 生成器（yield）：更简单的迭代器

```python
def countdown(n):
    """和上面的 Countdown 类完全等价"""
    while n > 0:
        yield n            # 暂停，返回 n，下次调用从此处继续
        n -= 1

for num in countdown(5):
    print(num)
```

`yield` 把函数变成了生成器——函数执行到 `yield` 暂停，交出值；下次 `next()` 调用时，从暂停的地方继续执行。**生成器是创建迭代器的最简单方式。**

> 什么时候用生成器？当你需要处理大量数据但不想一次全部加载到内存时——比如逐行读大文件、生成无限序列。

---

### ⭐ 练习 8.2

1. 写一个生成器 `fib_gen(n)`，逐个生成前 n 个斐波那契数（用 `yield`）。
2. 写一个 `even_numbers(iterable)` 生成器，接收一个可迭代对象，只输出其中的偶数。

---

## 8.3 装饰器

装饰器让你在**不修改函数源码**的情况下，给函数添加额外功能。

### 问题引入

```python
# 你有一个已经工作函数
def greet(name):
    return f"你好，{name}"

# 你现在想：每次调用 greet 时打印一条日志
# 不想改 greet 的代码，因为还有很多其他函数也需要这个功能
```

### 装饰器原理

装饰器本质上是一个**接收函数、返回新函数的函数**。假设你在 `log_utils.py` 中写了一个装饰器，另一个文件 `app.py` 使用它：

**`log_utils.py`**（装饰器定义）：

```python
def log_call(func):
    """装饰器：打印函数调用信息"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}，参数：{args}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 返回：{result}")
        return result
    return wrapper
```

**`app.py`**（使用装饰器）：

```python
from log_utils import log_call

@log_call                      # 等价于 greet = log_call(greet)
def greet(name):
    """向指定的人打招呼"""
    return f"你好，{name}"

print(greet("小明"))
# [LOG] 调用 greet，参数：('小明',)
# [LOG] greet 返回：你好，小明
# 你好，小明
```

日志功能正常工作。但有一个隐蔽的问题：

```python
print(greet.__name__)    # 输出：wrapper（不是 "greet"！）
print(greet.__doc__)     # 输出：None（不是 "向指定的人打招呼"！）
```

这里涉及 Python 中每个函数自带的两个元数据：

- **`__name__`**：函数的名字。定义时确定，但被装饰后会变成 wrapper 的名字。
- **`__doc__`**：函数的文档字符串。即函数体内第一行 `"""..."""` 的内容。

这两个属性看似没用，但很多工具依赖它们：IDE 的提示信息、自动生成文档、调试时的 traceback 显示，甚至 `help(greet)` 也会受影响。当装饰器和被装饰函数不在同一个文件时（这是最常见的情况），丢了 `__name__` 的 `greet` 会让调试变得困难——报错时 traceback 里显示的是 `wrapper` 而不是 `greet`。

### @wraps：修复这个问题

用 `functools.wraps` 一行就能解决：

```python
from functools import wraps

def log_call(func):
    """装饰器：打印函数调用信息"""
    @wraps(func)             # 把 func 的 __name__、__doc__ 复制到 wrapper 上
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}，参数：{args}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 返回：{result}")
        return result
    return wrapper
```

现在 `greet.__name__` 恢复为 `"greet"`，`greet.__doc__` 恢复为 `"向指定的人打招呼"`。写装饰器时加上 `@wraps(func)` 是一个好习惯。

### 常见应用

**计时器**：
```python
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时：{time.time() - start:.3f}s")
        return result
    return wrapper
```

**带参数的装饰器**（三层嵌套）：
```python
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def roll_dice():
    import random
    return random.randint(1, 6)

print(roll_dice())   # [3, 6, 1]（三次结果）
```

---

### ⭐ 练习 8.3

1. 写一个 `@retry(n)` 装饰器：函数执行出错时自动重试 n 次，全部失败才把最后的异常抛出来。
2. 用 `@timer` 装饰器测量 `sum(range(1000000))` 的执行时间。

---

## 8.4 缓存装饰器：@lru_cache

标准库 `functools` 提供了一个现成的缓存装饰器 `@lru_cache`，能自动记住函数的计算结果，相同参数直接返回缓存值。省去了手写缓存字典的麻烦。

```python
from functools import lru_cache

@lru_cache(maxsize=128)     # 最多缓存 128 组结果
def fibonacci(n):
    """返回第 n 个斐波那契数（fib(1)=1, fib(2)=1，与第 4 章练习一致）"""
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))        # 瞬间出结果！没有缓存时这几乎算不出来
```

没加 `@lru_cache` 时，递归的 `fibonacci(100)` 会产生约 `2^100` 次函数调用，根本跑不完。加了缓存后，每个 `n` 只计算一次，复杂度降到 `O(n)`。

### 常用参数

- `maxsize`：缓存上限。超过后按 LRU（最近最少使用）策略淘汰旧条目。设为 `None` 表示无限制。
- `typed`：设为 `True` 时，`f(1)` 和 `f(1.0)` 视为不同参数分别缓存。

Python 3.9+ 还提供了更简单的 `@cache`（等价于 `@lru_cache(maxsize=None)`），适合不在意内存的场景：

```python
from functools import cache

@cache
def expensive_calc(x):
    ...
```

### 适用场景

- ✅ 纯函数（相同输入总是产生相同输出）
- ✅ 递归函数（斐波那契、动态规划）
- ✅ 开销大的计算/数据库查询
- ❌ 有副作用的函数（读写文件、发网络请求）
- ❌ 依赖外部状态的函数（当前时间、全局变量）

---

### ⭐ 练习 8.4

1. 用 `@lru_cache` 实现一个高效的斐波那契函数，对比加缓存前后 `fibonacci(35)` 的执行时间。
2. 用 `@cache` 缓存一个"计算字符串中不同字符数量"的函数，测试同一字符串多次调用的效果。

---

## 8.5 上下文管理器

你已经用过了上下文管理器——`with open(...) as f:`。它保证无论代码块是否发生异常，资源都能被正确释放。

### 用类实现

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):             # with 进入时调用
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file             # as 后面拿到的就是这个返回值

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 无论是否异常都调用，关闭资源
        self.file.close()
        if exc_type:
            print(f"发生了异常：{exc_val}")
        return False    # False = 不吞异常；True = 吞掉异常

with FileManager("test.txt", "w") as f:
    f.write("Hello")
```

### 用 contextlib 实现（更简单）

```python
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    try:
        f = open(filename, mode, encoding="utf-8")
        yield f            # yield 前 = __enter__；yield 后 = __exit__
    finally:
        f.close()

with file_manager("test.txt", "w") as f:
    f.write("Hello")
```

### 典型应用

- 文件操作（`open`）
- 数据库连接
- 锁的获取与释放
- 临时目录（`tempfile.TemporaryDirectory`）
- 测试中的 `pytest.raises` 和 `unittest.mock.patch`

---

### ⭐ 练习 8.5

1. 写一个 `timer` 上下文管理器，进入时记录时间，退出时打印"代码块执行了 X 秒"。
2. 用 `contextmanager` 装饰器实现一个简单的数据库事务模拟（进入时打印"开始事务"，正常退出打印"提交"，异常打印"回滚"）。

---

## 8.6 类型提示

Python 是动态类型语言，但从 3.5 开始支持**可选的类型提示**，帮助 IDE 提供自动补全和静态检查。

### 基本用法

```python
def greet(name: str) -> str:
    return f"你好，{name}"

def divide(a: float, b: float) -> float:
    return a / b

def process(items: list[int]) -> dict[str, int]:
    """接收整数列表，返回每个数及其平方"""
    return {str(x): x ** 2 for x in items}
```

- `变量: 类型` 标注参数类型
- `-> 类型` 标注返回值类型
- **运行时 Python 并不会强制检查**——类型提示纯粹是"提示"，不影响运行

### 常用类型

```python
from typing import Optional, Union, Any

# 可选类型：可能是 str，也可能是 None
def get_name(user_id: int) -> Optional[str]:
    ...

# 联合类型：可能是 str 或 int
def process(value: Union[str, int]) -> str:
    ...

# 任意类型
def debug(obj: Any) -> None:
    ...

# 3.10+ 可以更简洁地写：
# str | None  代替  Optional[str]
# str | int   代替  Union[str, int]
```

### 静态类型检查器

```bash
pip install mypy
mypy your_script.py
```

`mypy` 会**静态分析**你的代码，找出类型不匹配的地方，而不运行代码。这在大型项目中非常有用。

### 该不该用

- ✅ **大中型项目**：类型提示 + mypy 能显著减少低级 bug
- ✅ **公开的库/API**：类型提示是活文档，使用者不用猜
- ➖ **小脚本/原型**：可加可不加，收益不大
- ❌ **不要为了类型提示牺牲灵活性**：Python 的强项就是动态，不是所有场景都适合类型化

---

### ⭐ 练习 8.6

1. 给以下函数添加类型提示：
```python
def find_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None
```

2. 安装 mypy，对它检查你之前写的代码，看看有什么提示。

---

## 🌟 章末练习

**实现一个简单的"计时缓存"**

要求结合本章高级特性实现：

1. **创建一个 `@cache_with_timeout(seconds)` 装饰器**：
   - 第一次调用函数时，正常计算并返回结果，同时把结果记录到缓存中
   - 在 `seconds` 秒内再次用相同参数调用，直接返回缓存值，不重新计算
   - 超过时间后，下次调用重新计算并更新缓存
   - 用 `time.time()` 记录时间

2. **创建一个 `LogContext` 上下文管理器**：
   - 进入时打印 `[开始] 操作名`，退出时打印 `[结束] 操作名 - 耗时: X.XXs`
   - 如果发生异常，打印 `[失败] 操作名 - 错误信息`，然后让异常继续传播

测试代码示例：
```python
import time

@cache_with_timeout(5)      # 5秒缓存
def expensive_calc(x):
    print(f"正在计算 {x}...")   # 观察这个只打印了几次
    time.sleep(1)               # 模拟耗时操作
    return x * x

print(expensive_calc(10))    # 计算并缓存
print(expensive_calc(10))    # 命中缓存（不打印"正在计算"）
time.sleep(6)
print(expensive_calc(10))    # 缓存过期，重新计算

with LogContext("数据处理"):
    time.sleep(0.5)          # [开始] 数据处理 → … → [结束] 数据处理 - 耗时: 0.50s
```
