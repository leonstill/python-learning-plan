# 第 4 章 · 函数

---

## 4.1 函数的定义与调用

函数是**一段有名字的可复用代码块**。它有三大作用：

1. **避免重复**：同一段逻辑不用到处复制粘贴
2. **隐藏细节**：调用者只需知道函数做什么，不用关心怎么做
3. **便于维护**：修改一处，所有调用生效

### 定义与调用

```python
def greet(name):
    """向指定的人打招呼"""       # 文档字符串（docstring），写在这个位置
    print(f"你好，{name}！")

greet("小明")    # 你好，小明！
greet("小红")    # 你好，小红！
```

- `def` 是定义函数的关键字
- `greet` 是函数名（命名规则和变量一样：小写英文 + 下划线）
- `name` 是参数（形参），调用时传入的值叫实参
- 缩进部分是函数体
- 三引号包起来的第一行字符串是 docstring，用 `help(greet)` 可以查看

### 返回值

函数可以给调用者"返回"一个结果：

```python
def add(a, b):
    return a + b

result = add(3, 5)   # result = 8
```

- `return` 后面是返回的值
- 函数遇到 `return` 立即结束，`return` 后面的代码不会执行
- 没有 `return` 的函数默认返回 `None`

### 先定义，后调用

函数必须**先定义再调用**。调用一个还没定义的函数会报 `NameError`。

---

### ⭐ 练习 4.1

1. 写一个 `is_even(n)` 函数，判断一个数是否为偶数，返回 `True` 或 `False`。
2. 写一个 `max_of_three(a, b, c)` 函数，返回三个数中最大的那个。

---

## 4.2 参数与返回值

Python 函数的参数机制非常灵活。

### 位置参数（最常用）

```python
def divide(a, b):
    return a / b

divide(10, 2)   # a=10, b=2（按位置对应）
divide(2, 10)   # a=2, b=10 —— 顺序很重要！
```

### 默认参数

```python
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("小明")                     # 你好，小明！
greet("Tom", greeting="Hello")    # Hello，Tom！
```

有默认值的参数必须放在没有默认值的参数后面：`def f(a, b=1)` 正确，`def f(a=1, b)` 错误。

### 关键词参数

调用函数时可以按名字传参，不依赖位置：

```python
def order(price, quantity, discount=0):
    return price * quantity * (1 - discount)

order(quantity=3, price=100, discount=0.1)   # 打乱顺序也没关系
```

### 可变参数：*args 和 **kwargs

```python
# *args：接收任意数量的位置参数，打包成元组
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4, 5)   # 15

# **kwargs：接收任意数量的关键词参数，打包成字典
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="小明", age=18, city="北京")
```

### 返回多个值

```python
def min_max(nums):
    return min(nums), max(nums)    # 实际上返回了一个元组

lo, hi = min_max([3, 1, 7, 4])     # 解包接收
```

---

### ⭐ 练习 4.2

1. 写一个 `safe_divide(a, b)` 函数，当 `b` 为 0 时不报错，返回 `"除数不能为0"`。
2. 写一个函数，接收任意数量的单词（用可变参数），返回一个字符串，每个单词首字母大写，用空格连接。

---

## 4.3 作用域与命名空间

### 局部变量与全局变量

```python
x = 10            # 全局变量

def demo():
    y = 5         # 局部变量（只能在函数内使用）
    print(x)      # 可以读取全局变量
    print(y)

demo()
print(x)          # 10 — 正常
print(y)          # ❌ NameError — y 在函数外不可见
```

### LEGB 规则

Python 查找变量时，按这个顺序：

1. **L**ocal — 函数内部
2. **E**nclosing — 外层函数
3. **G**lobal — 模块全局
4. **B**uilt-in — Python 内置

### 在函数内修改全局变量

```python
count = 0

def increment():
    global count      # 声明要修改全局变量
    count += 1
```

**少用 `global`**。如果函数需要外部数据，用参数传进去，用返回值传出来。大量使用全局变量会让代码难以理解和调试。

### nonlocal：修改外层函数的变量

```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1       # 修改的是 outer 里的 x
    inner()
    print(x)          # 11
```

这里 `inner` 是一个**闭包（closure）**——它"记住"了外层函数 `outer` 的变量 `x`，即使 `outer` 已经执行完毕。`nonlocal` 关键字让闭包可以修改（而不仅仅是读取）外层变量。

---

### ⭐ 练习 4.3

1. 运行下面的代码，预测输出结果并解释：

```python
x = 5
def change():
    x = 10
    print(x)
change()
print(x)
```

2. 写一个计数器函数 `make_counter()`，每次调用它返回一个比上次大 1 的数字（提示：用嵌套函数和 `nonlocal`）。

---

## 4.4 lambda 表达式

`lambda` 是一种创建**匿名函数**的快捷方式，用于需要一个简单函数但不想正式定义它的场景。

```python
# 普通写法
def square(x):
    return x * x

# lambda 写法
square = lambda x: x * x
```

语法：`lambda 参数: 返回值表达式`。只能包含一个表达式，不能有赋值、循环等复杂逻辑。

### 典型用途：作为排序/过滤的回调

```python
students = [
    {"name": "小明", "score": 85},
    {"name": "小红", "score": 92},
    {"name": "小刚", "score": 78}
]

# 按成绩排序
students.sort(key=lambda s: s["score"])
# lambda s: s["score"] 就是"告诉我每个学生的排序依据"

# 配合 filter / map
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))   # [2, 4, 6]
doubled = list(map(lambda x: x * 2, nums))          # [2, 4, 6, 8, 10, 12]
```

> `lambda` 只是语法糖。如果一个逻辑超过一行，就应该用 `def` 正式定义一个函数，这样可读性更好。

---

### ⭐ 练习 4.4

1. 用 `lambda` 和 `sorted()` 将字符串列表 `["apple", "banana", "kiwi", "grape"]` 按单词长度排序。
2. 用 `filter()` 和 `lambda`，从列表 `[15, 22, 8, 37, 41, 11]` 中筛选出大于 20 的数。

---

## 4.5 递归函数

递归就是**函数调用自己**。适合解决可以分解成"更小规模同类问题"的任务。

### 经典例子：阶乘

```
n! = n × (n-1) × (n-2) × ... × 1
5! = 5 × 4 × 3 × 2 × 1 = 120
```

递归思路：`n! = n × (n-1)!`，而 `(n-1)! = (n-1) × (n-2)!`……直到 `1! = 1`。

```python
def factorial(n):
    if n == 1:              # 基线条件：最小问题直接求解
        return 1
    return n * factorial(n - 1)  # 递归调用：问题规模缩小

print(factorial(5))   # 120
```

### 递归的两个必备要素

1. **基线条件**：什么时候停止递归（没有它，函数会无限调用直到栈溢出）
2. **递归条件**：把问题拆成更小的子问题

### 递归 vs 循环

```python
# 同样的阶乘，用循环写
def factorial_loop(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

大多数情况下循环更直观、效率更高。但某些问题（遍历树结构、分治算法）用递归更自然。

### 递归的代价

Python 默认递归深度限制约为 1000 层。`factorial(10000)` 会报 `RecursionError`。深度递归在实际工程中用得不多，但理解递归思想有助于后续学算法。

---

### ⭐ 练习 4.5

1. 写一个递归函数 `fibonacci(n)` 计算第 n 个斐波那契数（`fib(1)=1, fib(2)=1, fib(n)=fib(n-1)+fib(n-2)`）。
2. 用递归实现字符串反转。思考：基线条件是什么？递归条件是什么？

---

## 🌟 章末练习

**打造一个小型工具库**

创建文件 `utils.py`，在里面实现以下函数，然后在另一个文件中导入调用验证：

| 函数 | 功能 |
|------|------|
| `clamp(value, lo, hi)` | 将 value 限制在 [lo, hi] 区间内 |
| `distance(p1, p2)` | 计算两点 (x1,y1) 和 (x2,y2) 的欧氏距离 |
| `title_case(s)` | 将字符串中的每个单词首字母大写（自己实现，不用 `.title()`） |
| `group_by(items, key_func)` | 按 `key_func` 的结果将列表分组，返回字典 |
| `flatten(nested)` | 将嵌套列表（如 `[[1,2],[3,[4,5]]]`）递归展平为一维列表 |

`group_by` 示例：
```python
students = [
    {"name": "小明", "grade": "A"},
    {"name": "小红", "grade": "B"},
    {"name": "小刚", "grade": "A"},
]
group_by(students, lambda s: s["grade"])
# → {"A": [小明, 小刚], "B": [小红]}
```

这个练习将综合运用参数传递、返回值、lambda、递归等本章所学内容。
