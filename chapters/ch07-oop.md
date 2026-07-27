# 第 7 章 · 面向对象编程

---

## 7.1 类与对象

**类**是描述具有相同属性和行为的一类事物的模板；**对象**是这个模板的一个具体实例。

打个比方："猫"是一个类——有毛色、年龄等属性，有叫、跑等行为。你家的"小花"是一个对象——它是"猫"这个类的一个具体实例。

### 定义一个类

```python
class Dog:
    """狗类"""

    def __init__(self, name, age):
        self.name = name      # 实例属性：每只狗有自己的名字
        self.age = age

    def bark(self):
        print(f"{self.name}：汪汪！")

    def birthday(self):
        self.age += 1
        print(f"{self.name} 今年 {self.age} 岁了")
```

### 创建和使用对象

```python
# 创建实例（自动调用 __init__）
wangcai = Dog("旺财", 3)
xiaobai = Dog("小白", 1)

# 访问属性
print(wangcai.name)     # "旺财"
print(xiaobai.age)      # 1

# 调用方法
wangcai.bark()          # 旺财：汪汪！
wangcai.birthday()      # 旺财 今年 4 岁了
```

### 关键概念

- **`__init__`**：构造方法，创建对象时自动调用，用于初始化属性。第一个参数 `self` 指向当前实例。
- **`self`**：代表实例本身。在方法定义中必须是第一个参数，调用时 Python 自动传递，你不需要手动传。
- **实例属性**：通过 `self.xxx` 定义的属性，每个对象独立拥有。
- **方法**：定义在类里的函数，第一个参数必须是 `self`。

---

### ⭐ 练习 7.1

1. 定义一个 `Book` 类，包含 `title`（书名）、`author`（作者）、`pages`（页数）三个属性，以及 `describe()` 方法打印书籍信息。
2. 创建两本 `Book` 实例，分别调用 `describe()`。

---

## 7.2 属性与方法

### 实例属性 vs 类属性

```python
class Student:
    school = "一中"        # 类属性：所有实例共享

    def __init__(self, name):
        self.name = name   # 实例属性：每个实例独立

s1 = Student("小明")
s2 = Student("小红")

print(s1.school)   # 一中
print(s2.school)   # 一中
Student.school = "二中"     # 修改类属性
print(s1.school)   # 二中（都变了）
print(s2.school)   # 二中
```

类属性适合存放所有实例共享的数据，如学校名称、默认配置等。

### 实例方法、类方法、静态方法

```python
class Demo:
    class_var = "类变量"

    def instance_method(self):
        """实例方法：最常用，能访问实例和类的数据"""
        return f"实例方法，通过 self 访问"

    @classmethod
    def class_method(cls):
        """类方法：用 @classmethod 装饰，第一个参数是类本身(cls)"""
        return f"类方法, class_var = {cls.class_var}"

    @staticmethod
    def static_method():
        """静态方法：就是放在类里的普通函数，不访问实例和类"""
        return "静态方法，不需要 self 或 cls"

# 调用
d = Demo()
d.instance_method()           # 通过实例调用
Demo.class_method()           # 通过类调用，不需要实例
Demo.static_method()          # 通过类调用
```

- **实例方法**（90%的情况）：操作实例数据
- **类方法**：常用于"工厂方法"（创建不同配置的实例）
- **静态方法**：逻辑上属于这个类，但不依赖实例或类变量

---

### ⭐ 练习 7.2

1. 给 `Student` 类添加一个类属性 `count`，统计创建了多少个 `Student` 实例（在 `__init__` 里自增）。
2. 用 `@classmethod` 实现一个 `Student.from_string("小明,18")` 工厂方法，从逗号分隔的字符串创建实例。

---

## 7.3 继承与多态

### 继承

一个类可以"继承"另一个类的属性和方法，避免代码重复。

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} 发出了声音")

class Cat(Animal):       # Cat 继承 Animal
    def speak(self):     # 重写（override）父类方法
        print(f"{self.name}：喵喵～")

class Dog(Animal):
    def speak(self):
        print(f"{self.name}：汪汪！")

    def fetch(self):     # 新增方法
        print(f"{self.name} 把球叼回来了")
```

- `class Cat(Animal)`：`Animal` 是父类（基类），`Cat` 是子类（派生类）
- 子类自动拥有父类的**所有属性和方法**
- 子类可以**重写**父类的方法，实现自己的版本
- 子类可以**新增**父类没有的方法

### super()：调用父类方法

```python
class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)   # 调用父类的 __init__，设置 name
        self.color = color       # 再添加自己的属性

    def speak(self):
        super().speak()          # 先执行父类的 speak
        print(f"它是{self.color}色的猫")
```

### 多态

"多态"的意思是：不同类的对象，可以对**同一个方法名**做出**不同的响应**。调用者不用关心对象具体是什么类型，只管调用。

```python
def make_sound(animal):
    animal.speak()      # 不管传进来的是什么动物，统一调用 speak

make_sound(Cat("小花"))    # 小花：喵喵～
make_sound(Dog("旺财"))    # 旺财：汪汪！
```

这就是多态的核心价值——**同一接口，不同行为**。你以后添加新动物（如 `Pig`），只要它实现了 `speak()`，`make_sound` 不用改就能直接用。

---

### ⭐ 练习 7.3

1. 定义一个 `Vehicle`（交通工具）类，子类 `Car` 和 `Bike`。`Vehicle` 有个 `run()` 方法，两个子类各自重写。
2. 用 `isinstance(obj, cls)` 检查一个实例的类型。`isinstance()` 是 Python 内置函数，判断对象是否属于某个类（包括其父类）。例如 `isinstance(Car(), Vehicle)` 返回 `True`，因为 `Car` 是 `Vehicle` 的子类。

---

## 7.4 封装与访问控制

封装是指**把数据和行为打包在一起，并控制外部能访问哪些**。

### Python 的"私有"约定

Python 没有真正强制性的 private，而是靠命名约定：

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner           # 公有属性
        self._protected = balance    # 一个下划线："受保护的"，约定不要直接访问
        self.__private = "secret"    # 两个下划线：名称会被改写（name mangling）

    def deposit(self, amount):
        if amount > 0:
            self._protected += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._protected:
            self._protected -= amount
            return True
        return False

    def get_balance(self):           # getter：安全地获取余额
        return self._protected


acc = BankAccount("小明", 1000)
acc.deposit(500)                     # ✅ 通过方法修改
print(acc.get_balance())             # 1500
# acc._protected = -100              # ❌ 绕过了检查，但这是反约定的
# print(acc.__private)               # ❌ AttributeError
# print(acc._BankAccount__private)   # 可以这样访问，但不要这么做
```

### 访问控制的本质

- **`_name`**（单下划线）：约定这是内部实现，外部不要直接访问。你可以访问，但后果自负。
- **`__name`**（双下划线）：Python 会将其重命名为 `_ClassName__name`，防止子类意外覆盖。

Python 的设计哲学是 **"大家都是成年人"**——与其强行限制，不如用约定和文档说明什么是公开 API。把校验逻辑放在方法里（如 `deposit`、`withdraw`），让外部通过方法来操作数据，这才是 Pythonic 的封装。

---

### ⭐ 练习 7.4

1. 设计一个 `Temperature` 类，用 `__celsius` 私有属性存储温度（摄氏度），提供 `to_fahrenheit()` 方法转换为华氏度。
2. 为什么通过方法修改属性比直接赋值更好？举一个实际场景说明。

---

## 7.5 魔术方法

"魔术方法"是 Python 中前后有双下划线的方法（如 `__init__`），它们让自定义类的行为像内置类型一样自然。

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):               # print() 时的显示
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):              # 调试/交互模式下的显示
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):        # + 运算符
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):         # == 比较
        return self.x == other.x and self.y == other.y

    def __len__(self):               # len()
        return 2

    def __getitem__(self, index):    # 索引访问 vec[0]
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"索引 {index} 超出范围，Vector 只有 0 和 1")

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)        # Vector(4, 6)
print(v1 == v2)       # False
print(v1[1])          # 2
```

### 常用魔术方法速查

| 方法 | 触发条件 |
|------|----------|
| `__init__` | 创建实例 |
| `__str__` | `print()`、`str()` |
| `__repr__` | 交互环境、`repr()` |
| `__len__` | `len()` |
| `__add__` | `+` 运算符 |
| `__eq__` | `==` 比较 |
| `__lt__` | `<` 比较（排序用） |
| `__getitem__` | `obj[index]` |
| `__contains__` | `x in obj` |
| `__call__` | 把实例当函数调用 `obj()` |

魔术方法让你的类"融入" Python 生态——比如实现了 `__lt__` 后，排序（`sorted()`）就能直接用了。

---

### ⭐ 练习 7.5

1. 定义 `Fraction`（分数）类，实现 `__str__`（显示为 `a/b`）、`__add__` 和 `__eq__` 方法。
2. 定义 `Playlist`（播放列表）类，内部存一个歌曲列表，实现 `__len__`、`__getitem__` 和 `__contains__`，让它用起来像内置列表。

---

## 7.6 @property 与描述符

`@property` 让你把方法调用伪装成属性访问——既能像访问属性一样简洁，又能执行方法中的逻辑。

### 不用 @property 的问题

```python
class Person:
    def __init__(self, name):
        self.name = name
        self._age = 18

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value

p = Person("小明")
p.set_age(25)               # 调用方法…啰嗦
print(p.get_age())
```

### 用 @property 改进

```python
class Person:
    def __init__(self, name):
        self.name = name
        self._age = 18

    @property
    def age(self):                    # getter：p.age 触发
        return self._age

    @age.setter
    def age(self, value):             # setter：p.age = xx 触发
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value

p = Person("小明")
p.age = 25          # 直接赋值，但走的是 @age.setter 方法
print(p.age)        # 25，直接读取，但走的是 @property 方法
# p.age = -5        # ValueError: 年龄不能为负数
```

语法更简洁了，但校验逻辑一个不少。这就是 `@property` 的魅力——**外部使用简单，内部逻辑完整**。

### 只读属性

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):              # 没有 @area.setter，只读！
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)    # 78.53975
# c.area = 100   # ❌ AttributeError
```

---

### ⭐ 练习 7.6

1. 给 `Person` 类添加一个 `display_name` 属性（`@property`），自动返回 `{name}（{age}岁）`。
2. 定义一个 `Temperature` 类，内部用开尔文存储，通过 `@property` 提供摄氏度和华氏度的读写接口。

---

## 7.7 枚举（Enum）

当一组变量只有有限的几个可选值时，用 `Enum` 比用字符串常量更安全、更清晰。

```python
from enum import Enum

class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

# 使用
task_priority = Priority.HIGH

print(task_priority)            # Priority.HIGH
print(task_priority.name)       # 'HIGH'
print(task_priority.value)      # 1

# 比较
print(task_priority == Priority.HIGH)   # True
print(task_priority == "HIGH")          # False —— 不会和字符串混淆

# 从字符串创建
p = Priority["HIGH"]            # Priority.HIGH
p = Priority(2)                 # Priority.MEDIUM
```

**为什么要用 Enum 而不是字符串？**

- **防止拼写错误**：`Priority.HIG` 会立即报 `AttributeError`，而字符串 `"hig"` 悄悄变成了 bug
- **IDE 自动补全**：输入 `Priority.` 后 IDE 列出所有选项
- **语义清晰**：看到 `Priority.HIGH` 就知道只有这几个值，不会和别的字符串搞混

### auto()：自动编号

```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()      # 1
    GREEN = auto()    # 2
    BLUE = auto()     # 3
```

当你不在意具体数值，只需要区分不同成员时，用 `auto()` 最省事。

---

### ⭐ 练习 7.7

1. 定义一个 `OrderStatus` 枚举，包含 `PENDING`、`SHIPPED`、`DELIVERED`、`CANCELLED` 四个状态。
2. 写一个 `Order` 类，用 `OrderStatus` 枚举作为订单状态属性，并提供 `update_status()` 方法切换状态。

---

## 🌟 章末练习

设计以下类结构：

```
BankAccount（基类）
├── name, account_number, _balance（属性）
├── deposit(amount), withdraw(amount)（方法）
├── balance（@property，只读）
└── __str__：返回 "账户[xxx]余额: xxx"

SavingsAccount（继承 BankAccount）
├── interest_rate（利率属性）
├── add_interest()：计算并添加利息
└── withdraw()：重写，有最低余额限制（比如余额不能低于 100）

CreditAccount（继承 BankAccount）
├── credit_limit（透支额度）
└── withdraw()：重写，允许透支但不超过 credit_limit
```

测试代码示例：
```python
acc1 = SavingsAccount("小明", "001", 1000, interest_rate=0.03)
acc1.deposit(500)
acc1.add_interest()
acc1.withdraw(2000)   # 应该失败：取款后余额低于100

acc2 = CreditAccount("小红", "002", 500, credit_limit=1000)
acc2.withdraw(1200)   # 成功：透支700，在额度内
acc2.withdraw(500)    # 失败：超过额度

accounts = [acc1, acc2]
for acc in accounts:
    print(acc)        # 多态：不同类型显示各自的信息
```

要求：充分运用本章所学的继承、封装、`@property`、魔术方法、多态等面向对象知识。
