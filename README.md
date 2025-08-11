# TOTP生成器

这是一个基于时间的一次性密码（TOTP）生成工具，提供命令行和图形界面两种版本。

## 功能特性

- 支持标准base32格式密钥
- 实时生成6位TOTP验证码
- 30秒有效期倒计时显示
- 自动验证OTP有效性

## 使用方式

### 图形界面版本（推荐）

1. 下载 `dist/TOTPGenerator.exe`
2. 双击运行程序
3. 输入您的base32密钥
4. 点击"生成OTP"按钮

### 命令行版本

```bash
python generate_otp.py
```

### 源码运行

```bash
# 安装依赖
pip install pyotp

# 运行图形界面
python totp_gui.py

# 运行命令行版本
python generate_otp.py
```

## 打包方法

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包为EXE
pyinstaller --onefile --noconsole --name TOTPGenerator totp_gui.py
```

> 提示：程序不存储任何密钥信息，确保您的密钥安全
