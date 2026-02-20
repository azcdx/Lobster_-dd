#!/usr/bin/env python3
"""
LobsterAI Telegram Bot
双向通信和任务执行系统
"""

import asyncio
import logging
import subprocess
import os
import sys
from datetime import datetime
from typing import Optional
from telegram import Update, Bot, Document, PhotoSize
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('telegram_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Bot Token
BOT_TOKEN = "8177838184:AAG3dvLZhSF83bG1txN6ZpKuw8No1pq4K8s"

# 工作目录
WORK_DIR = r"C:\Users\Administrator\lobsterai\project"

class TelegramBotManager:
    """Telegram Bot 管理器"""

    def __init__(self, token: str):
        self.token = token
        self.application: Optional[Application] = None
        self.authorized_users = set()  # 授权用户集合

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """启动命令 - /start"""
        user = update.effective_user
        welcome_message = f"""
🦞 LobsterAI Bot 已启动！

你好 {user.first_name}！我是您的全场景个人助理。

📋 可用命令：
/start - 显示此帮助信息
/help - 查看详细帮助
/status - 查看系统状态
/exec <命令> - 执行系统命令
/file <文件名> - 发送文件
/cd <目录> - 切换工作目录
/pwd - 显示当前工作目录
/ls - 列出当前目录文件

💬 您也可以直接发送消息，我会尽力响应！

当前工作目录：{WORK_DIR}
        """
        await update.message.reply_text(welcome_message)
        logger.info(f"用户 {user.id} ({user.username}) 启动了 bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """帮助命令 - /help"""
        help_text = """
🦞 LobsterAI 详细帮助

📁 文件操作：
• /ls [目录] - 列出文件
• /pwd - 显示当前目录
• /cd <目录> - 切换目录
• /file <文件名> - 发送文件给您
• /save <文件名> - 保存接收的文件

💻 系统命令：
• /exec <命令> - 执行系统命令
• /status - 查看系统状态
• /env - 查看环境变量

📊 数据处理：
• /analyze <文件> - 分析数据文件
• /plot <文件> - 生成图表

📧 其他功能：
• /weather <城市> - 查询天气
• /search <关键词> - 网络搜索
• /time - 显示当前时间

💡 提示：
- 发送文件给我，我会保存到工作目录
- 发送图片，我可以分析内容
- 直接发送文本消息，我会智能响应
        """
        await update.message.reply_text(help_text)

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """系统状态 - /status"""
        try:
            # 获取系统信息
            cpu_usage = os.popen('wmic cpu get loadpercentage').read()
            disk_usage = os.popen('wmic logicaldisk get size,freespace,caption').read()

            status_text = f"""
📊 系统状态

⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📁 工作目录：{WORK_DIR}
🖥️ CPU使用率：{cpu_usage}
💾 磁盘使用：
{disk_usage}

🤖 Bot 状态：运行中
✅ 所有系统正常
            """
            await update.message.reply_text(status_text)
        except Exception as e:
            await update.message.reply_text(f"❌ 获取状态失败：{str(e)}")

    async def exec_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """执行命令 - /exec <命令>"""
        if not context.args:
            await update.message.reply_text("❌ 请提供要执行的命令\n例如：/exec dir")
            return

        command = ' '.join(context.args)
        await update.message.reply_text(f"⏳ 执行命令：{command}")

        try:
            # 在 Windows 下执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=WORK_DIR,
                timeout=30
            )

            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "✅ 命令执行完成，无输出"

            # 如果输出太长，分段发送
            if len(output) > 4000:
                chunks = [output[i:i+4000] for i in range(0, len(output), 4000)]
                for chunk in chunks:
                    await update.message.reply_text(f"```\n{chunk}\n```", parse_mode='Markdown')
            else:
                await update.message.reply_text(f"```\n{output}\n```", parse_mode='Markdown')

        except subprocess.TimeoutExpired:
            await update.message.reply_text("❌ 命令执行超时（30秒）")
        except Exception as e:
            await update.message.reply_text(f"❌ 执行失败：{str(e)}")

    async def pwd_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """显示当前目录 - /pwd"""
        await update.message.reply_text(f"📁 当前工作目录：\n{WORK_DIR}")

    async def ls_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """列出文件 - /ls"""
        try:
            args = context.args
            target_dir = ' '.join(args) if args else WORK_DIR

            if not os.path.isabs(target_dir):
                target_dir = os.path.join(WORK_DIR, target_dir)

            if not os.path.exists(target_dir):
                await update.message.reply_text(f"❌ 目录不存在：{target_dir}")
                return

            files = os.listdir(target_dir)
            if not files:
                await update.message.reply_text(f"📁 目录为空：{target_dir}")
                return

            # 格式化文件列表
            file_list = []
            for f in sorted(files):
                full_path = os.path.join(target_dir, f)
                if os.path.isdir(full_path):
                    file_list.append(f"📁 {f}/")
                else:
                    size = os.path.getsize(full_path)
                    file_list.append(f"📄 {f} ({self._format_size(size)})")

            response = f"📂 目录内容：{target_dir}\n\n" + "\n".join(file_list[:50])  # 限制显示数量
            if len(files) > 50:
                response += f"\n\n... 还有 {len(files) - 50} 个文件"

            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text(f"❌ 列出文件失败：{str(e)}")

    async def send_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """发送文件 - /file <文件名>"""
        if not context.args:
            await update.message.reply_text("❌ 请提供文件名\n例如：/file document.pdf")
            return

        filename = ' '.join(context.args)
        filepath = os.path.join(WORK_DIR, filename)

        if not os.path.exists(filepath):
            await update.message.reply_text(f"❌ 文件不存在：{filename}")
            return

        try:
            await update.message.reply_document(
                document=open(filepath, 'rb'),
                caption=f"📄 {filename}"
            )
            logger.info(f"发送文件：{filepath}")
        except Exception as e:
            await update.message.reply_text(f"❌ 发送文件失败：{str(e)}")

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理接收的文件"""
        document: Document = update.message.document
        user = update.effective_user

        await update.message.reply_text(f"⏳ 正在保存文件：{document.file_name}")

        try:
            # 下载文件
            file = await context.bot.get_file(document.file_id)
            save_path = os.path.join(WORK_DIR, document.file_name)
            await file.download_to_drive(save_path)

            file_size = self._format_size(document.file_size)
            await update.message.reply_text(
                f"✅ 文件已保存\n"
                f"📄 名称：{document.file_name}\n"
                f"📏 大小：{file_size}\n"
                f"📁 路径：{save_path}"
            )
            logger.info(f"用户 {user.id} 上传文件：{save_path}")

        except Exception as e:
            await update.message.reply_text(f"❌ 保存文件失败：{str(e)}")

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理接收的图片"""
        photo: PhotoSize = update.message.photo[-1]  # 获取最大尺寸
        user = update.effective_user

        await update.message.reply_text("⏳ 正在保存图片...")

        try:
            # 下载图片
            file = await context.bot.get_file(photo.file_id)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"photo_{user.id}_{timestamp}.jpg"
            save_path = os.path.join(WORK_DIR, filename)
            await file.download_to_drive(save_path)

            await update.message.reply_text(
                f"✅ 图片已保存\n"
                f"📷 名称：{filename}\n"
                f"📁 路径：{save_path}"
            )
            logger.info(f"用户 {user.id} 上传图片：{save_path}")

        except Exception as e:
            await update.message.reply_text(f"❌ 保存图片失败：{str(e)}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理普通文本消息"""
        message = update.message.text
        user = update.effective_user

        logger.info(f"收到消息 from {user.id}: {message}")

        # 智能响应
        response = self._generate_response(message)
        await update.message.reply_text(response)

    def _generate_response(self, message: str) -> str:
        """生成智能响应"""
        message_lower = message.lower()

        # 时间相关
        if any(word in message_lower for word in ['时间', '几点', 'time', '时刻']):
            return f"⏰ 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 问候
        if any(word in message_lower for word in ['你好', 'hello', 'hi', '嗨']):
            return "👋 你好！我是 LobsterAI，很高兴为您服务！\n\n发送 /help 查看我能做什么"

        # 功能询问
        if any(word in message_lower for word in ['能做什么', '功能', 'help', '帮助']):
            return "🦞 我可以帮您：\n\n• 执行系统命令\n• 传输文件\n• 查询系统状态\n• 分析数据\n• 生成图表\n• 搜索信息\n• 自动化任务\n\n发送 /help 查看详细命令列表"

        # 默认响应
        return f"🤔 收到您的消息：{message}\n\n💡 提示：\n• 发送 /help 查看可用命令\n• 或使用 /exec 执行具体命令"

    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """错误处理"""
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        """启动 Bot"""
        try:
            # 创建 Application
            self.application = Application.builder().token(self.token).build()

            # 注册处理器
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("status", self.status))
            self.application.add_handler(CommandHandler("exec", self.exec_command))
            self.application.add_handler(CommandHandler("pwd", self.pwd_command))
            self.application.add_handler(CommandHandler("ls", self.ls_command))
            self.application.add_handler(CommandHandler("file", self.send_file))

            # 消息处理器
            self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
            self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

            # 错误处理器
            self.application.add_error_handler(self.error_handler)

            # 启动轮询
            logger.info("🦞 LobsterAI Bot 启动中...")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)

        except Exception as e:
            logger.error(f"Bot 启动失败：{e}")
            raise


def main():
    """主函数"""
    import sys
    import io

    # 设置标准输出编码为 UTF-8
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("🦞 LobsterAI Telegram Bot")
    print("=" * 50)
    print(f"工作目录：{WORK_DIR}")
    print(f"Bot Token：{BOT_TOKEN[:20]}...")
    print("=" * 50)

    bot_manager = TelegramBotManager(BOT_TOKEN)
    bot_manager.run()


if __name__ == "__main__":
    main()
