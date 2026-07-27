# 第 6 章 · 文件操作与异常处理

---

## 6.1 文件的读写

程序处理的数据不能只在内存里——需要**持久化**到磁盘。Python 操作文件很简单。

### 打开文件

```python
f = open("data.txt", "r", encoding="utf-8")
content = f.read()
f.close()
```

`open()` 的三个参数：

| 参数 | 值 | 含义 |
|------|-----|------|
| 文件名 | `"data.txt"` | 文件路径（相对或绝对） |
| 模式 | `"r"` | r=读, w=写（覆盖）, a=追加, r+=读写 |
| 编码 | `"utf-8"` | 读写中文务必指定！ |

### 用 with...as（最佳实践）

手动 `close()` 容易忘（尤其代码出异常时）。`with` 语句会自动关闭文件，**这应该是你唯一的写法**：

```python
# 读文件
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 一次性读完
    # 或逐行读
    for line in f:
        print(line.strip())

# 写文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行\n")
```

### 读取方法对比

```python
f.read()          # 一次性读全部内容，返回字符串
f.readline()      # 读一行，包含换行符
f.readlines()     # 读全部行，返回列表
# 逐行迭代（推荐，大文件也不怕内存爆）
for line in f:
    process(line)
```

**写文件注意**：`"w"` 模式会**清空原文件**再写入。想保留原内容用 `"a"`（追加模式）。

---

### ⭐ 练习 6.1

1. 创建一个文件 `hello.txt`，写入三行文字，然后重新打开读取并打印全部内容。
2. 写一个程序，读取一个文本文件，统计它有多少行、多少个单词、多少个字符。

---

## 6.2 文件与目录操作

`os` 和 `os.path` 模块提供了文件和目录的操作能力。

```python
import os
import shutil

# --- 路径 ---
os.path.abspath("data.txt")        # 获取绝对路径
os.path.basename("/a/b/c.txt")     # 'c.txt'
os.path.dirname("/a/b/c.txt")      # '/a/b'
os.path.splitext("data.csv")       # ('data', '.csv')

# --- 目录 ---
os.mkdir("new_folder")             # 创建目录（父目录必须存在）
os.makedirs("a/b/c", exist_ok=True)  # 递归创建，exist_ok 避免重复创建报错
os.listdir(".")                    # 列出目录内容
os.getcwd()                        # 当前工作目录
os.chdir("/path/to/dir")           # 切换工作目录

# --- 文件/目录操作 ---
os.rename("old.txt", "new.txt")    # 重命名
os.remove("temp.txt")              # 删除文件
os.rmdir("empty_folder")           # 删除空目录
shutil.rmtree("folder")            # 删除目录及其所有内容（危险，谨慎使用）
shutil.copy("src.txt", "dst.txt")  # 复制文件
shutil.move("file.txt", "dir/")    # 移动文件

# --- 检查 ---
os.path.exists("file.txt")         # 是否存在
os.path.isfile("file.txt")         # 是否是文件
os.path.isdir("folder")            # 是否是目录
```

### pathlib：更现代的路径操作

Python 3.4+ 推荐用 `pathlib` 替代 `os.path`，语法更直观：

```python
from pathlib import Path

p = Path("data/report.txt")

p.exists()                    # 是否存在
p.is_file()                   # 是否是文件
p.name                        # 'report.txt'
p.stem                        # 'report'（不带扩展名的文件名）
p.suffix                      # '.txt'
p.parent                      # Path('data')
p.with_suffix(".csv")         # Path('data/report.csv')

# 读写
content = p.read_text(encoding="utf-8")
p.write_text("Hello", encoding="utf-8")

# 遍历
for f in Path(".").glob("*.py"):   # 所有 .py 文件
    print(f)
```

---

### ⭐ 练习 6.2

1. 用 `pathlib.Path` 在当前目录下创建一个文件夹 `test_dir`，在里面创建 `a.txt` 和 `b.txt` 两个空文件。
2. 用 `glob` 列出当前目录下所有 `.py` 文件。

---

## 6.3 什么是异常

程序运行时遇到的问题叫**异常**（Exception）。如果不处理，程序会直接崩溃并打印一堆红色的"Traceback"。

### 常见异常类型

```python
# ZeroDivisionError：除以零
1 / 0

# TypeError：类型不对
"hello" + 42

# ValueError：值不合适
int("abc")

# IndexError：列表索引越界
nums = [1, 2, 3]
nums[10]

# KeyError：字典键不存在
info = {"name": "小明"}
info["age"]

# FileNotFoundError：文件不存在
open("不存在的文件.txt")

# AttributeError：对象没有这个属性
"hello".non_existent_method()
```

### 异常传播

发生异常时，它会一层层向上抛，直到有代码处理它，或者程序崩溃：

```python
def level3():
    return 1 / 0      # 这里炸了

def level2():
    return level3()   # 往上抛

def level1():
    return level2()   # 再往上抛

level1()  # 最终在这里崩溃
```

理解异常传播有助于理解 Python 的错误信息——Traceback 会完整列出从出错位置到最后调用的路径。

---

### ⭐ 练习 6.3

1. 写三行代码，故意触发三种不同的异常，观察错误信息。
2. 看看这段代码会抛出什么异常，为什么：

```python
data = {"a": [1, 2, 3], "b": [4, 5]}
print(data["b"][3])
```

---

## 6.4 try / except / finally

用 `try/except` 来**捕获并处理**异常，防止程序崩溃。

### 基本结构

```python
try:
    num = int(input("请输入一个数字："))
    result = 100 / num
    print(f"结果是：{result}")
except ValueError:
    print("输入的不是有效数字！")
except ZeroDivisionError:
    print("除数不能为 0！")
except Exception as e:
    print(f"未知错误：{e}")
```

- `try` 块放可能出问题的代码
- `except 异常类型` 捕获指定类型的异常
- `Exception` 是所有异常的基类，`except Exception` 能捕获大多数异常
- `as e` 可以获取异常对象，查看详细信息

### else 和 finally

```python
try:
    f = open("data.txt", "r", encoding="utf-8")
except FileNotFoundError:
    print("文件不存在，请检查路径")
else:
    # 只有 try 成功时才执行
    content = f.read()
    f.close()
    print(f"读取了 {len(content)} 个字符")
finally:
    # 无论是否异常，一定执行
    print("操作结束")
```

`finally` 常用于释放资源——但如果你用了 `with`，就不需要手动 `finally` 关闭文件了。

### 什么时候该捕获异常

- ✅ **用户输入可能不正确** — 捕获并友好提示
- ✅ **网络请求可能失败** — 捕获并重试或降级
- ❌ **不要用 except 掩盖逻辑错误** — 异常暴露 bugs，吞掉它只会让调试更难
- ❌ **不要写 `except:` 不指定类型** — 这会连 `KeyboardInterrupt`（Ctrl+C）都吃掉

---

### ⭐ 练习 6.4

1. 写一个函数 `read_number()`，让用户输入数字，如果输入非数字则提示重来，直到正确为止（用循环 + try/except）。
2. 写一个安全文件读取函数 `safe_read(path)`，文件存在就返回内容，不存在返回空字符串，不给上层抛异常。

---

## 6.5 自定义异常

当 Python 内置异常不足以表达你的错误类型时，可以自定义异常。

### 定义和使用

```python
class InsufficientBalanceError(Exception):
    """余额不足"""
    pass

class InvalidAmountError(Exception):
    """金额无效（负数或零）"""
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"金额 {amount} 无效，必须为正数")

# 使用
def withdraw(balance, amount):
    if amount <= 0:
        raise InvalidAmountError(amount)
    if amount > balance:
        raise InsufficientBalanceError(f"余额 {balance}，无法取出 {amount}")
    return balance - amount

try:
    new_balance = withdraw(100, 200)
except InsufficientBalanceError as e:
    print(f"取款失败：{e}")
except InvalidAmountError as e:
    print(f"金额错误：{e}")
```

`raise` 用于手动抛出异常。自定义异常和内置异常用法完全一样——它们都是 `Exception` 的子类。

### 为什么要自定义异常

- **语义清晰**：`InsufficientBalanceError` 比 `ValueError` 更准确，调用者一看就知道发生了什么
- **方便针对性捕获**：调用者可以 `except InsufficientBalanceError` 只处理这一种情况
- **携带额外信息**：可以在异常类中添加属性（如 `amount`），方便调试和恢复

---

### ⭐ 练习 6.5

1. 定义一个 `PasswordTooShortError` 异常，要求密码长度至少为 6 位，不符合时抛出。
2. 写一个 `register(username, password)` 函数，检查用户名不为空、密码长度足够，任一不满足就抛出对应的自定义异常。

---

## 🌟 章末练习

**日志分析工具**

假设有一个服务器日志文件 `access.log`，每行格式为：
```
2024-01-15 14:23:01 INFO [user:张三] 登录成功
2024-01-15 14:24:05 ERROR [user:李四] 连接超时
2024-01-15 14:25:10 WARNING [user:张三] 密码即将过期
2024-01-15 14:26:33 INFO [user:王五] 登录成功
```
（实际需求中每行可能不同，可以自己设定格式）

要求：

1. **读取日志**：用 `with open()` 读取 `access.log`，如果文件不存在则友好提示并退出
2. **统计概要**：
   - 总行数
   - 不同用户数（用集合）
   - INFO / WARNING / ERROR 各多少条（用字典统计）
3. **搜索功能**：
   - 按用户名搜索该用户的所有日志行
   - 按级别搜索（INFO/WARNING/ERROR）
4. **结果输出**：将统计结果写入 `report.txt`
5. **异常处理**：捕获文件读写可能的异常，友好的错误提示

框架提示：
```python
def parse_line(line):
    """解析一行日志，返回 {time, level, user, message}"""
    # 可以简单的用 split 或者用 re（第9章会讲）

def analyze_log(filepath):
    """分析日志文件，返回统计字典"""
    stats = {"total": 0, "users": set(), "levels": {}}
    # ...
    return stats

def main():
    try:
        stats = analyze_log("access.log")
        # 输出统计...
    except FileNotFoundError:
        print("日志文件不存在")
    except Exception as e:
        print(f"处理出错：{e}")

if __name__ == "__main__":
    main()
```
