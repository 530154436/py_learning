## uv
> 官网：https://docs.astral.sh/uv/getting-started/installation/

`uv`是新一代的Python项目管理工具，由 Astral（Ruff 的开发者）打造，比 pip 快 10–100 倍，全平台支持。核心功能：

| 功能          | 描述                             | 替代工具                     |
|-------------|--------------------------------|--------------------------|
| **包管理**     | 安装/升级/卸载包，完全兼容 `pip` 接口        | `pip`, `pip-tools`       |
| **虚拟环境**    | 创建和管理隔离环境                      | `venv`, `virtualenv`     |
| 依赖锁定        | 生成 `uv.lock` 确保可重现构建           | `poetry`, `pip-tools`    |
| Python 版本管理 | 自动下载、切换多个 Python 版本            | `pyenv`, `asdf`          |
| 项目初始化       | `uv init` 生成标准项目结构             | 手动创建 / Cookiecutter      |
| 脚本运行        | `uv run` 直接执行脚本（自动加载依赖）        | `poetry run`, `pipx run` |
| 工具管理        | 安装全局 CLI 工具（如 `ruff`, `black`） | `pipx`                   |
| **构建与发布**   | 打包 wheel/sdist 并发布到 PyPI       | `build` + `twine`        |
| 工作区支持       | 类似 Rust Cargo，支持多包大型项目         | —                        |


### 1、下载安装
+ Windows 10
```shell
# 下载并安装uv
powershell -ExecutionPolicy ByPass -c {$env:UV_INSTALL_DIR = "E:\DevSoftware\uv";irm https://astral.sh/uv/install.ps1 | iex}

# 设置环境变量
set Path=E:\DevSoftware\uv;%Path%   (cmd)
$env:Path = "E:\DevSoftware\uv;$env:Path"   (powershell)

# 验证是否安装成功 uv 0.9.15 (5eafae332 2025-12-02)
cmd > uv self version
```

+ PyCharm2025.2.2 配置uv [Configure a uv environment](https://www.jetbrains.com/help/pycharm/uv.html)
```
1. 打开 Settings / Preferences，路径：`File → Settings`（Windows/Linux）或 `PyCharm → Settings`（macOS）
2. 导航到 Python Interpreter 设置，在左侧菜单中展开：Python → Interpreter
3. 添加新的解释器：点击右上角的 "Add Interpreter" 按钮
4. 选择解释器类型：在弹出窗口中，将 Type 下拉菜单设置为：uv
5. 配置 `uv` 路径：例如 E:\DevSoftware\uv\uv.exe
6. 设置虚拟环境：选择 "Select existing" 并指定项目中的 `.venv` 目录：E:\PythonProjects\llm-application\.venv
7. 完成配置：点击 OK 保存，PyCharm 将自动加载 `uv` 管理的依赖包列表
```

### 2、常用操作
#### 2.1 初始化、虚拟环境、构建和发布
```shell
# 管理 Python 版本
uv python list  
# cpython-3.15.0a2-windows-x86_64-none                 <download available>
# cpython-3.12.10-windows-x86_64-none                  C:\Users\AppData\Local\Programs\Python\Python312\python.exe

# 初始化新项目
uv init --python 3.12 
uv python list

# 创建、激活虚拟环境
uv venv --python 3.12 .venv
.venv\Scripts\activate
uv python pin 3.12

# 清理缓存
uv cache clean

# 构建与发布
uv build
uv publish

# 导出为 requirements.txt
uv export > requirements.txt

# 导出为 uv.lock
uv lock
```

#### 2.2 管理依赖
项目的依赖在几个字段中定义：
+ project.dependencies：已发布的依赖项。
+ project.optional-dependencies：已发布的可选依赖项或“附加项”。
+ dependency-groups：用于开发的本地依赖项。 
+ tool.uv.sources：开发期间依赖项的备用源。
```toml
# pyproject.toml
[project]
name = "llm-application"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.28.1",
]

# 索引
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true

# 工作区成员
[tool.uv.workspace]
members = [
    "project-llmtoolkits",
]
[tool.uv.sources]
llmtoolkits = { workspace = true, editable = true }

# 开发依赖组
[dependency-groups]
dev = [
    "gradio>=6.0.2",
    # 可编辑依赖
    "llmtoolkits",
]
```
添加、删除、查看依赖项
```shell
# 添加依赖后，将在 project.dependencies 字段中添加一个条目
uv add httpx

# 删除依赖
uv remove httpx

# 查看依赖
uv pip list

# 查看依赖树
uv tree
```
添加开发依赖组
```shell
# 开发依赖项是仅限本地的，在发布到 PyPI 或其他索引时，不会包含在项目需求中。因此，开发依赖项不包含在 [project] 表中。
uv add --dev gradio
```
添加工作区成员（可编辑依赖）
```shell
uv add --dev --editable ./project-llmtoolkits/
```
环境是自动同步的，但也可以使用 `uv sync` 显式同步
```shell
# 同步环境（安装所有第三方包）
uv sync --active           # 若已激活其他虚拟环境（如 E:\PythonEnvs\myenv），需加`--active`：
# 同步开发依赖组
uv sync --active --dev     # 安装 dev 组
uv sync --active --no-dev  # 排除 dev 组
```
当清空`project.dependencies `后同步，则可以删除所有依赖
```shell
# pyproject.toml
[project]
dependencies = [] # ← 清空主依赖

# 同步环境（卸载所有第三方包）
uv sync --active
```

## 参考引用
[1] [新一代Python管理UV完全使用指南](https://zhuanlan.zhihu.com/p/1897568987136640818)<br>
[2] [uv官网](https://docs.astral.sh/uv/getting-started/installation/)<br>
[3] [uv中文文档-管理依赖](https://uv.oaix.tech/concepts/projects/dependencies/#_16)<br>
