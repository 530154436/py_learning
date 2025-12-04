
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

### 2、常用命令

```shell
# 管理 Python 版本
uv python list  
# cpython-3.15.0a2-windows-x86_64-none                 <download available>
# cpython-3.12.10-windows-x86_64-none                  C:\Users\AppData\Local\Programs\Python\Python312\python.exe

# 初始化新项目
uv init my_project

# 添加依赖（自动更新 pyproject.toml 和 uv.lock）
uv add requests

# 同步环境（根据 uv.lock 安装依赖）
uv sync           # 仅主依赖
uv sync --active  # 若已激活其他虚拟环境（如 E:\PythonEnvs\myenv），需加`--active`：

# 运行脚本（自动使用项目环境）
uv run main.py

# 创建虚拟环境（可指定 Python）
uv venv --python 3.12 .venv

# 构建与发布
uv build
uv publish

# 查看依赖树
uv tree

# 导出为 requirements.txt
uv export > requirements.txt

# 清理缓存
uv cache clean
```

## 参考引用
[1] [新一代Python管理UV完全使用指南](https://zhuanlan.zhihu.com/p/1897568987136640818)<br>
[2] [uv官网](https://docs.astral.sh/uv/getting-started/installation/)<br>