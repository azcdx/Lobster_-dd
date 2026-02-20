#!/usr/bin/env python3
"""
LobsterAI Telegram 监听器
监听 Telegram 消息队列并处理
"""

import json
import os
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
WORK_DIR = r"C:\Users\Administrator\lobsterai\project"
MESSAGE_QUEUE = os.path.join(WORK_DIR, "telegram_messages.json")
RESPONSE_FILE = os.path.join(WORK_DIR, "telegram_responses.json")

class LobsterAI_Monitor:
    """LobsterAI 消息监控器"""

    def __init__(self):
        self.running = True

    def check_messages(self):
        """检查新消息"""
        if not os.path.exists(MESSAGE_QUEUE):
            return []

        try:
            with open(MESSAGE_QUEUE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            return messages
        except:
            return []

    def clear_queue(self):
        """清空消息队列"""
        try:
            with open(MESSAGE_QUEUE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        except:
            pass

    def send_response(self, message_id, response):
        """发送响应到 Telegram"""
        responses = []
        if os.path.exists(RESPONSE_FILE):
            try:
                with open(RESPONSE_FILE, 'r', encoding='utf-8') as f:
                    responses = json.load(f)
            except:
                responses = []

        response_data = {
            'message_id': message_id,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }

        responses.append(response_data)

        with open(RESPONSE_FILE, 'w', encoding='utf-8') as f:
            json.dump(responses, f, ensure_ascii=False, indent=2)

    def process_message(self, msg):
        """处理单条消息 - 这里可以调用 LobsterAI"""
        user_name = msg.get('first_name', 'User')
        text = msg.get('text', '')
        msg_id = msg.get('message_id')

        print(f"\n{'='*60}")
        print(f"📩 收到 Telegram 消息")
        print(f"{'='*60}")
        print(f"用户: {user_name}")
        print(f"内容: {text}")
        print(f"时间: {msg.get('timestamp', '')}")
        print(f"{'='*60}\n")

        # TODO: 这里应该调用 LobsterAI 的处理逻辑
        # 目前使用简单的响应
        response = f"🦞 LobsterAI 收到了您的消息：\n\n{text}\n\n正在处理中...（请等待完整集成）"

        return response

    def run(self):
        """运行监控器"""
        print("🦞 LobsterAI Telegram 监听器启动")
        print("=" * 60)
        print(f"工作目录: {WORK_DIR}")
        print(f"消息队列: {MESSAGE_QUEUE}")
        print(f"响应文件: {RESPONSE_FILE}")
        print("=" * 60)
        print("\n监听中... (Ctrl+C 停止)\n")

        try:
            while self.running:
                # 检查新消息
                messages = self.check_messages()

                if messages:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 发现 {len(messages)} 条新消息")

                    # 处理所有消息
                    for msg in messages:
                        try:
                            # 处理消息
                            response = self.process_message(msg)

                            # 发送响应
                            msg_id = msg.get('message_id')
                            if msg_id:
                                self.send_response(msg_id, response)
                                print(f"✅ 响应已发送")

                            # 等待一下避免处理太快
                            time.sleep(0.5)

                        except Exception as e:
                            print(f"❌ 处理消息出错: {e}")

                    # 清空队列
                    self.clear_queue()

                # 等待一段时间再检查
                time.sleep(2)

        except KeyboardInterrupt:
            print("\n\n监听器已停止")

def main():
    import sys
    import io

    # 设置编码
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    monitor = LobsterAI_Monitor()
    monitor.run()

if __name__ == "__main__":
    main()
