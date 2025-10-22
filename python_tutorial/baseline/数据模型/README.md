
## 类型化字典（Typed dictionaries）

`TypedDict` 是Python 3.8版本中引入的，通过typing模块提供，用于创建具有固定键和各自类型值的字典类型。TypedDict使得静态类型检查器能够更准确地处理字典对象，从而为使用字典存储结构化数据的场景提供了类型安全。

+ **仅支持字符串键**<br>
  `TypedDict` 只能用于键为字符串（`str`）类型的字典；实际值必须是 `dict` 类型的实例，不能是其子类。<br>
+ **字段（项）有明确类型**<br>
  每个键都有对应的值类型声明。例如：<br>
  ```python
  class User(TypedDict):
      name: str
      age: int
  ```
  表示这个字典必须包含 `'name'`（字符串）和 `'age'`（整数）两个键。
+ **字段可以是“必需”或“可选”**<br>
  默认情况下，所有字段都是**必需的**，创建实例时必须提供。<br>
  可通过 `NotRequired[]` 或设置 `total=False` 将字段设为可选。例如：<br>
  ```python
  class Address(TypedDict, total=False):
      street: NotRequired[str]
      city: NotRequired[str]
  ```
+ **字段可以是只读（ReadOnly）**<br>
  使用 `ReadOnly[T]` 可以标记某个字段不允许被修改，这在防止意外修改数据时很有用。
+ **结构化类型（Duck Typing）**<br>
  `TypedDict` 是基于结构的类型：只要两个 `TypedDict` 的字段完全一致，它们就被认为是兼容的，即使没有继承关系。<br>
  支持继承：可以从其他 `TypedDict` 继承字段，便于复用；也支持泛型，可以创建通用的类型模板。
+ **不支持运行时类型检查**<br>
  完全用于`静态类型检查`，不会在运行运行时报错或验证。<br>
  不能使用 `isinstance(obj, MyTypedDict)` 来判断类型；类型检查由静态分析工具（如 `mypy`）在开发阶段完成。

### 语法与使用
有两种语法形式：**基于类的语法**（class-based syntax）和**函数式语法**（functional syntax）。

+ 基于类的语法
```pyton
class User(TypedDict):
    name: str
    age: int
```
+ 函数式语法
```pyton
User1 = TypedDict('User1', {'name': str, 'age': int})
```
+ 使用 TypedDict 类型
```python
u1: User1 = {'name': 'Alice', 'age': 19}
u2: User1 = User1(name='Edward', age=12)
u3: User1 = get_user1({'name': 'Bob', 'age': 18})
u4: User1 = dict(name='Eric', age=55)
```

### 综合示例
```python
from typing import TypedDict
from typing_extensions import NotRequired


class User(TypedDict):
    name: str
    age: int


class Address(TypedDict, total=False):
    street: NotRequired[str]
    city: NotRequired[str]


class AdminUser(User):
    permissions: list[str]
    address: Address


def test01() -> None:
    u1: User = {"name": "Alice", "age": 30}
    u3: User = {"name": "Carol"}  # ❌ error: Missing key "age" for TypedDict "User"  [typeddict-item]


def test02() -> None:
    a1: Address = {"street": "粤海街道", "city": "深圳市"}
    a2: Address = {"city": "深圳市"}  # total=False：默认字段都是可选；所以不会报错


def test_admin_user() -> None:
    a2: Address = {"city": "深圳市"}
    # <class 'dict'>
    admin1: AdminUser = {"name": "Dana", "age": 40, "permissions": ["read", "write"], "address": a2}

    # ❌ error: Missing key "age" for TypedDict "AdminUser"  [typeddict-item]
    admin2: AdminUser = {"name": "Dana", "permissions": ["read", "write"], "address": a2}
```



[typeddict-Pyton官方文档](https://typing.python.org/en/latest/spec/typeddict.html) <br>
[Python 数据模型详解：Pydantic 与 TypedDict 的对比与实战](https://zhuanlan.zhihu.com/p/1962258529646780899) <br>