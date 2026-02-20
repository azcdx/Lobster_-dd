#!/usr/bin/env python3
"""
Telegram Bot - LobsterAI 桥接版本
将 Telegram 消息转发给 LobsterAI 处理
"""

import asyncio
import logging
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from telegram import Update, Bot, Document, PhotoSize
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('telegram_bridge.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Bot Token
BOT_TOKEN = "8177838184:AAG3dvLZhSF83bG1txN6ZpKuw8No1pq4K8s"

# 工作目录
WORK_DIR = r"C:\Users\Administrator\lobsterai\project"

# 消息队列文件（用于与 LobsterAI 通信）
MESSAGE_QUEUE = os.path.join(WORK_DIR, "telegram_messages.json")
RESPONSE_FILE = os.path.join(WORK_DIR, "telegram_responses.json")

class TelegramBridge:
    """Telegram 到 LobsterAI 的桥接器"""

    def __init__(self, token: str):
        self.token = token
        self.application: Optional[Application] = None
        self.pending_messages = {}  # 待处理的消息

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """启动命令"""
        user = update.effective_user
        welcome_message = f"""
🦞 LobsterAI 远程对话已连接！

你好 {user.first_name}！我正在连接到 LobsterAI...

现在您可以像在飞书一样与我对话了！

💬 直接发送消息，我会转达给 LobsterAI 并返回回复

📋 命令列表：
/start - 显示此信息
/status - 查看连接状态
/help - 查看帮助
        """
        await update.message.reply_text(welcome_message)
        logger.info(f"用户 {user.id} ({user.username}) 启动了桥接器")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """帮助命令"""
        help_text = """
🦞 LobsterAI 桥接器帮助

此 Bot 将您的消息转发给 LobsterAI 处理。

使用方法：
1. 直接发送任何文本消息
2. 消息会被传递给 LobsterAI
3. LobsterAI 的回复会通过此 Bot 返回

支持的文件：
- 文本消息
- 图片
- 文档

注意：回复可能需要几秒钟，请耐心等待。
        """
        await update.message.reply_text(help_text)

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """状态检查"""
        queue_exists = os.path.exists(MESSAGE_QUEUE)
        response_exists = os.path.exists(RESPONSE_FILE)

        status_text = f"""
📊 桥接器状态

⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📁 工作目录：{WORK_DIR}
📨 消息队列：{'✅ 存在' if queue_exists else '❌ 不存在'}
📤 响应文件：{'✅ 存在' if response_exists else '❌ 不存在'}

🤖 Bot 状态：运行中
🔄 桥接模式：活跃
        """
        await update.message.reply_text(status_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理收到的消息 - 转发给 LobsterAI"""
        message = update.message
        user = update.effective_user

        # 获取消息内容
        text_content = message.text
        if message.caption:
            text_content = message.caption

        if not text_content:
            await message.reply_text("⚠️ 仅支持文本消息")
            return

        logger.info(f"收到消息 from {user.id} ({user.username}): {text_content}")

        # 显示"正在处理"
        status_msg = await message.reply_text("⏳ 正在连接 LobsterAI...")

        try:
            # 将消息添加到队列
            message_data = {
                'user_id': user.id,
                'username': user.username or 'unknown',
                'first_name': user.first_name or 'User',
                'message_id': message.message_id,
                'text': text_content,
                'timestamp': datetime.now().isoformat(),
                'chat_id': message.chat_id
            }

            # 读取现有队列
            queue = []
            if os.path.exists(MESSAGE_QUEUE):
                try:
                    with open(MESSAGE_QUEUE, 'r', encoding='utf-8') as f:
                        queue = json.load(f)
                except:
                    queue = []

            # 添加新消息
            queue.append(message_data)

            # 保存队列
            with open(MESSAGE_QUEUE, 'w', encoding='utf-8') as f:
                json.dump(queue, f, ensure_ascii=False, indent=2)

            logger.info(f"消息已添加到队列，队列长度: {len(queue)}")

            # 等待 LobsterAI 处理（轮询响应）
            max_wait = 30  # 最多等待30秒
            wait_interval = 1
            waited = 0

            response = None
            while waited < max_wait:
                await asyncio.sleep(wait_interval)
                waited += wait_interval

                # 检查是否有响应
                if os.path.exists(RESPONSE_FILE):
                    try:
                        with open(RESPONSE_FILE, 'r', encoding='utf-8') as f:
                            responses = json.load(f)

                        # 查找对应消息的响应
                        for resp in responses:
                            if resp.get('message_id') == message.message_id:
                                response = resp.get('response')
                                # 从响应列表中移除已处理的
                                responses = [r for r in responses if r.get('message_id') != message.message_id]
                                with open(RESPONSE_FILE, 'w', encoding='utf-8') as f:
                                    json.dump(responses, f, ensure_ascii=False, indent=2)
                                break
                    except:
                        pass

                if response:
                    break

            if response:
                # 发送 LobsterAI 的回复
                await status_msg.edit_text(response)
                logger.info(f"已发送 LobsterAI 的回复")
            else:
                # 超时，使用智能响应
                await status_msg.edit_text(
                    f"⚠️ LobsterAI 暂时无响应\n\n"
                    f"但我收到了您的消息：\n「{text_content}」\n\n"
                    f"💡 请确保 LobsterAI 正在运行并监控消息队列。"
                )
                logger.warning(f"等待响应超时")

        except Exception as e:
            logger.error(f"处理消息出错: {e}", exc_info=True)
            await status_msg.edit_text(f"❌ 处理消息时出错：{str(e)}")

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理文件 - 转发给 LobsterAI"""
        message = update.message
        document = message.document
        user = update.effective_user

        status_msg = await message.reply_text("⏳ 正在处理文件...")

        try:
            # 下载文件
            file = await context.bot.get_file(document.file_id)
            save_path = os.path.join(WORK_DIR, document.file_name)
            await file.download_to_drive(save_path)

            # 创建文件消息数据
            message_data = {
                'user_id': user.id,
                'username': user.username or 'unknown',
                'first_name': user.first_name or 'User',
                'message_id': message.message_id,
                'type': 'file',
                'file_name': document.file_name,
                'file_path': save_path,
                'caption': message.caption or '',
                'timestamp': datetime.now().isoformat(),
                'chat_id': message.chat_id
            }

            # 添加到队列
            queue = []
            if os.path.exists(MESSAGE_QUEUE):
                try:
                    with open(MESSAGE_QUEUE, 'r', encoding='utf-8') as f:
                        queue = json.load(f)
                except:
                    queue = []

            queue.append(message_data)

            with open(MESSAGE_QUEUE, 'w', encoding='utf-8') as f:
                json.dump(queue, f, ensure_ascii=False, indent=2)

            await status_msg.edit_text(
                f"📎 文件已接收：{document.file_name}\n\n"
                f"已转发给 LobsterAI 处理"
            )
            logger.info(f"文件已转发: {document.file_name}")

        except Exception as e:
            logger.error(f"处理文件出错: {e}")
            await status_msg.edit_text(f"❌ 处理文件失败：{str(e)}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """错误处理"""
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        """启动桥接器"""
        try:
            self.application = Application.builder().token(self.token).build()

            # 注册处理器
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("status", self.status))

            # 消息处理器
            self.application.add_handler(MessageHandler(
                filters.Document.ALL,
                self.handle_document
            ))
            self.application.add_handler(MessageHandler(
                filters.PHOTO,
                self.handle_document
            ))
            self.application.add_handler(MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message
            ))

            # 错误处理器
            self.application.add_error_handler(self.error_handler)

            # 启动轮询
            logger.info("🦞 LobsterAI Telegram 桥接器启动中...")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)

        except Exception as e:
            logger.error(f"桥接器启动失败：{e}")
            raise


def main():
    """主函数"""
    import sys
    import io

    # 设置标准输出编码为 UTF-8
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("🦞 LobsterAI Telegram 桥接器")
    print("=" * 50)
    print(f"工作目录：{WORK_DIR}")
    print(f"Bot Token：{BOT_TOKEN[:20]}...")
    print("=" * 50)

    bridge = TelegramBridge(BOT_TOKEN)
    bridge.run()


if __name__ == "__main__":
    main()
