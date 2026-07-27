# 第 2 章 · 流程控制

---

## 2.1 条件判断：if / elif / else

程序大多数时候不只是从上到下顺序执行——它需要**根据条件做不同的选择**。这就像你出门前看天气：下雨带伞，不下雨不带。

### 基本语法

```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

执行过程：从上到下依次检查每个条件，**第一个为 True 的分支被执行，其余跳过**。如果所有条件都为 False，执行 `else`（`else` 是可选的）。

### 关键细节

- **缩进是语法**：条件后面的代码块必须缩进（推荐 4 个空格）。缩进不一致会直接报 `IndentationError`。
- **冒号不能少**：`if`、`elif`、`else` 后必须有冒号。
- **`elif` 可以有多个，也可以没有**。

### 嵌套条件

条件里面可以再写条件：

```python
age = 25
has_ticket = True

if age >= 18:
    if has_ticket:
        print("可以入场")
    else:
        print("请先购票")
else:
    print("未成年不可入场")
```

### 条件表达式（三元表达式）

简单的 if-else 可以写成一行：

```python
result = "通过" if score >= 60 else "不通过"
# 等价于：
# if score >= 60:
#     result = "通过"
# else:
#     result = "不通过"
```

---

### ⭐ 练习 2.1

1. 输入一个年份，判断是否为闰年。规则：能被 4 整除但不能被 100 整除，**或者**能被 400 整除。
2. 输入三个数字，用 if-elif 找出最大的那个。

---

## 2.2 while 循环

循环让你**重复执行一段代码**。`while` 的规则很简单：**只要条件为 True，就一直循环**。

```python
count = 1
while count <= 5:
    print(f"第{count}次")
    count += 1    # 每次把 count 加 1，否则会无限循环！

# 输出：
# 第1次
# 第2次
# 第3次
# 第4次
# 第5次
```

### 无限循环与退出

```python
while True:
    answer = input("输入 quit 退出：")
    if answer == "quit":
        break          # break 立即跳出循环
```

`while True` 是一个很常见的写法，表示"一直做，直到条件满足时手动退出"。**配合 `break` 使用，否则就是死循环。**

### 累加模式

```python
# 计算 1 到 100 的和
total = 0
i = 1
while i <= 100:
    total += i
    i += 1
print(total)   # 5050
```

---

### ⭐ 练习 2.2

1. 用 while 循环打印 1 到 20 之间的所有偶数。
2. 用户不断输入数字，输入 0 时停止，最后输出所有数字的总和。

---

## 2.3 for 循环

`for` 循环是 Python 中最常用的循环形式。它**逐个取出序列中的元素**，对每个元素执行循环体。

```python
# 遍历字符串
for char in "Python":
    print(char)     # 依次打印 P y t h o n

# 遍历列表
fruits = ["苹果", "香蕉", "橘子"]
for fruit in fruits:
    print(f"我喜欢吃{fruit}")
```

### range()：生成数字序列

```python
range(5)          # → 0, 1, 2, 3, 4（从 0 开始，不含 5）
range(2, 6)       # → 2, 3, 4, 5（从 2 开始，到 6 之前）
range(1, 10, 2)   # → 1, 3, 5, 7, 9（步长为 2）

for i in range(3):
    print(i)      # 0 1 2
```

`range()` 和 `for` 是黄金搭档，循环 N 次的写法是 `for i in range(N):`。

### enumerate()：同时获取索引和值

```python
names = ["张三", "李四", "王五"]
for i, name in enumerate(names):
    print(f"{i}: {name}")
# 0: 张三
# 1: 李四
# 2: 王五
```

### for vs while 的选择

- 知道要循环多少次 → 用 `for`
- 不知道次数，依赖某个条件 → 用 `while`

---

### ⭐ 练习 2.3

1. 用 for 循环计算 1×2×3×...×10 的结果。
2. 给定列表 `scores = [78, 92, 85, 66, 73, 91]`，用 for 循环统计及格（≥60）的人数。

---

## 2.4 break 与 continue

`break` 和 `continue` 是循环中的两个控制开关。

### break：立即退出整个循环

```python
for i in range(10):
    if i == 5:
        break         # i 等于 5 时，循环直接结束
    print(i)
# 输出：0 1 2 3 4
```

典型场景——**在列表中找元素，找到了就停**：

```python
names = ["张三", "李四", "王五", "赵六"]
for name in names:
    if name == "王五":
        print("找到了！")
        break
```

### continue：跳过本轮，继续下一轮

```python
for i in range(5):
    if i == 2:
        continue      # i 等于 2 时，跳过 print，进入下一轮
    print(i)
# 输出：0 1 3 4
```

典型场景——**跳过不符合条件的数据**：

```python
# 只打印偶数
for i in range(10):
    if i % 2 != 0:
        continue
    print(i)           # 0 2 4 6 8
```

### for...else：循环正常结束才执行

```python
for i in range(3):
    print(i)
else:
    print("循环正常结束，没被 break 打断")
```

如果循环被 `break` 打断，`else` 不会执行。这个特性常用来做**搜索失败处理**：

```python
for name in names:
    if name == "target":
        print("找到")
        break
else:
    print("没找到")   # 只有 break 没触发时才执行
```

---

### ⭐ 练习 2.4

1. 写代码找出 2~50 中第一个能被 7 整除的数，找到就停止。
2. 遍历 1~20，打印所有不是 3 的倍数的数（用 continue 跳过 3 的倍数）。

---

## 2.5 嵌套与综合运用

循环可以放在另一个循环里面。

### 九九乘法表

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()   # 换行
```

外层 `i` 控制行（1到9），内层 `j` 控制每行中的列（1到i）。`\t` 是制表符，让输出对齐。

### 遍历嵌套列表

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:       # 先取每一行
    for item in row:     # 再取行中的每个元素
        print(item, end=" ")
    print()
```

### 综合示例：简易登录

```python
correct_password = "abc123"
max_attempts = 3

for attempt in range(1, max_attempts + 1):
    password = input(f"请输入密码（第{attempt}次）：")
    if password == correct_password:
        print("登录成功！")
        break
else:
    print("密码错误次数过多，账户被锁定")
```

---

### ⭐ 练习 2.5

1. 用嵌套循环打印下面的图案：
   ```
   *
   **
   ***
   ****
   *****
   ```
2. 模拟一个猜数字游戏：预设一个答案（比如 42），每次用户输入后提示"太大"或"太小"，猜中结束并显示次数。

---

## 🌟 章末练习

**制作一个成绩管理系统（命令行版）。**

功能要求：
1. 预设一个学生成绩字典：`{"张三":85, "李四":92, "王五":67, ...}`（至少 5 个学生）
2. 提供菜单：1-查看所有成绩  2-添加学生  3-查询某个学生  4-统计（平均分/最高分/最低分/及格率）  5-退出
3. 用 while 循环保持菜单运行，用户选 5 才退出
4. 统计功能需要遍历所有成绩进行计算

参考框架：
```
========= 成绩管理系统 =========
1. 查看所有成绩
2. 添加学生
3. 查询学生
4. 成绩统计
5. 退出
================================
```

> 提示：你还未学到字典操作（第 3 章），可以先用两个列表分别存姓名和成绩，学完第 3 章后再改回字典实现。
