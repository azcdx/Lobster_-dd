# LobsterAI Telegram Bot 使用说明

## 🎯 功能概述

我已经为您创建了一个功能完整的 Telegram Bot，实现以下功能：

### ✅ 核心功能

**1. 命令执行**
- `/exec <命令>` - 执行系统命令
- `/status` - 查看系统状态
- `/pwd` - 显示当前工作目录
- `/ls [目录]` - 列出文件

**2. 文件传输**
- `/file <文件名>` - 发送文件给您
- 接收您发送的文件并自动保存
- 支持图片、文档等各种格式

**3. 智能对话**
- 直接发送文本消息，我会智能响应
- 支持时间查询、问候语、功能询问等
- 可以自然语言交互

**4. 系统管理**
- `/start` - 启动 bot 并查看欢迎信息
- `/help` - 查看详细帮助
- `/cd <目录>` - 切换工作目录
- `/env` - 查看环境变量

**5. 高级功能**
- `/analyze <文件>` - 分析数据文件
- `/plot <文件>` - 生成图表
- `/weather <城市>` - 查询天气
- `/search <关键词>` - 网络搜索

## 🚀 快速启动

### 方法 1：使用启动脚本（推荐）

双击运行 `start_bot.bat` 文件，脚本会自动：
1. 检查 Python 环境
2. 安装所需依赖
3. 启动 Bot

### 方法 2：手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Bot
python telegram_bot.py
```

## 📱 在 Telegram 中使用

1. **找到您的 Bot**：
   - 在 Telegram 搜索框中输入您的 Bot 用户名
   - 或直接访问：`https://t.me/您的Bot用户名`

2. **发送 `/start` 开始**：
   ```
   /start
   ```

3. **尝试一些命令**：
   ```
   /status          # 查看系统状态
   /ls              # 列出当前目录文件
   /exec dir        # 执行 dir 命令
   你好             # 发送消息测试对话
   ```

## 📁 文件说明

- **[telegram_bot.py](file:///C:\Users\Administrator\lobsterai\project\telegram_bot.py)** - Bot 主程序
- **[start_bot.bat](file:///C:\Users\Administrator\lobsterai\project\start_bot.bat)** - Windows 启动脚本
- **[requirements.txt](file:///C:\Users\Administrator\lobsterai\project\requirements.txt)** - Python 依赖列表
- **telegram_bot.log** - 运行日志（自动生成）

## 🔄 后台运行

如果想让 Bot 在后台持续运行：

### Windows 使用 Task Scheduler
1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：启动时
4. 操作：启动程序 `start_bot.bat`

### 使用 nohup（Linux/WSL）
```bash
nohup python telegram_bot.py > bot.log 2>&1 &
```

## 🛠️ 配置说明

### 修改工作目录
编辑 `telegram_bot.py` 中的 `WORK_DIR` 变量：
```python
WORK_DIR = r"您的自定义路径"
```

### 添加授权用户
在代码中添加允许使用 Bot 的用户 ID：
```python
self.authorized_users = {123456789, 987654321}  # 添加您的 Telegram User ID
```

获取 User ID 的方法：
1. 发送 `/start` 给您的 Bot
2. 查看 `telegram_bot.log` 文件
3. 找到类似 `用户 123456789` 的记录

## 📊 使用示例

### 示例 1：远程执行命令
```
您: /exec python --version
Bot: Python 3.12.0
```

### 示例 2：文件传输
```
您: /file report.pdf
Bot: [发送 report.pdf 文件]
```

### 示例 3：接收文件
```
您: [发送 document.txt]
Bot: ✅ 文件已保存
    📄 名称：document.txt
    📏 大小：1.23 KB
    📁 路径：C:\Users\Administrator\lobsterai\project\document.txt
```

### 示例 4：智能对话
```
您: 现在几点了？
Bot: ⏰ 当前时间：2026-02-20 00:39:01
```

## 🔒 安全建议

1. **保护 Bot Token**：不要将 Token 分享给他人
2. **设置用户白名单**：限制只有特定用户可以使用
3. **命令限制**：谨慎使用 `/exec` 命令，避免执行危险操作
4. **日志监控**：定期检查 `telegram_bot.log` 了解使用情况

## 🐛 故障排查

### Bot 无法启动
- 检查网络连接
- 确认 Bot Token 正确
- 查看 `telegram_bot.log` 错误信息

### 命令无响应
- 检查是否使用了正确的前缀 `/`
- 查看日志中的错误信息

### 文件传输失败
- 确认文件路径正确
- 检查文件权限
- 确认文件大小不超过 Telegram 限制（50MB）

## 📞 技术支持

如需帮助或发现问题：
1. 查看日志文件 `telegram_bot.log`
2. 检查 Bot Token 是否正确
3. 确认网络连接正常

---

🦞 **LobsterAI** - 您的全场景个人助理
