

## 下载安装

+ Windows <br>
  [npm](https://nodejs.org/zh-cn/download)： Node.js 默认的包管理器。<br>
  [pnpm](https://pnpm.io/zh/installation)：管理 Node.js 项目的依赖。
```shell
# npm
# 下载安装包 https://nodejs.org/dist/v24.11.1/node-v24.11.1-x64.msi
# 验证 Node.js 版本：
node -v # "v24.11.1".
# 验证 npm 版本：
npm -v # "11.6.2".

# pnpm
powerShell> Invoke-WebRequest https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression
# PNPM_HOME=C:\Users\chubin.zheng\AppData\Local\pnpm
PS> pnpm -v
# 10.24.0
```
报错：
```
PS > npm
npm : 无法加载文件 E:\Program Files\nodejs\npm.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅 https:/go.microsof
t.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
所在位置 行:1 字符: 1
+ npm
+ ~~~
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```
=> 以管理员身份打开 PowerShell，并设置执行策略为 RemoteSigned（推荐）
```shell
Set-ExecutionPolicy RemoteSigned
```