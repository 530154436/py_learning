# -*- coding: utf-8 -*-
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


def test_functional():
    User1 = TypedDict('User1', {'name': str, 'age': int})
    def get_user1(user: User1) -> User1: return user

    u1: User1 = {'name': 'Alice', 'age': 19}
    u2: User1 = User1(name='Edward', age=12)
    u3: User1 = get_user1({'name': 'Bob', 'age': 18})
    u4: User1 = dict(name='Eric', age=55)
    print(type(u1))  # <class 'dict'>
    print(u1)
    print(u2)
    print(u3)
    print(u4)


if __name__ == "__main__":
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "-m", "mypy", __file__], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ mypy: No type errors!")
    else:
        print(result.stdout)
        print(result.stderr)
    test_functional()