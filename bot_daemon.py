#!/usr/bin/env python3
"""
LobsterAI Telegram Bot - 守护进程版本
自动监控和重启 Bot
"""

import os
import sys
import time
import subprocess
import signal
import logging
from pathlib import Path

# 配置
WORK_DIR = r"C:\Users\Administrator\lobsterai\project"
BOT_SCRIPT = os.path.join(WORK_DIR, "telegram_bot.py")
LOG_FILE = os.path.join(WORK_DIR, "telegram_bot.log")
DAEMON_LOG = os.path.join(WORK_DIR, "bot_daemon.log")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DAEMON_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BotDaemon:
    """Bot 守护进程"""

    def __init__(self):
        self.bot_process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 50  # 最大重启次数

    def start_bot(self):
        """启动 Bot 进程"""
        try:
            logger.info(f"启动 Bot (第 {self.restart_count + 1} 次)...")
            self.bot_process = subprocess.Popen(
                [sys.executable, BOT_SCRIPT],
                cwd=WORK_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            logger.info(f"Bot PID: {self.bot_process.pid}")
            return True
        except Exception as e:
            logger.error(f"启动失败: {e}")
            return False

    def stop_bot(self):
        """停止 Bot 进程"""
        if self.bot_process and self.bot_process.poll() is None:
            logger.info("停止 Bot...")
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("强制杀死 Bot 进程")
                self.bot_process.kill()

    def check_bot_health(self):
        """检查 Bot 健康状态"""
        if not self.bot_process:
            return False

        # 检查进程是否还在运行
        if self.bot_process.poll() is not None:
            logger.warning(f"Bot 进程已退出 (退出码: {self.bot_process.returncode})")
            return False

        # 检查日志文件是否有最新活动
        if os.path.exists(LOG_FILE):
            try:
                stat = os.stat(LOG_FILE)
                last_modified = stat.st_mtime
                current_time = time.time()
                idle_time = current_time - last_modified

                # 如果超过 60 秒没有活动，可能有问题
                if idle_time > 60:
                    logger.warning(f"Bot 可能卡住 (日志 {int(idle_time)} 秒未更新)")
                    return False
            except Exception as e:
                logger.error(f"检查日志失败: {e}")

        return True

    def run(self):
        """运行守护进程"""
        logger.info("🦞 LobsterAI Bot 守护进程启动")
        logger.info(f"工作目录: {WORK_DIR}")

        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        while self.running and self.restart_count < self.max_restarts:
            # 启动 Bot
            if not self.start_bot():
                logger.error("无法启动 Bot，等待 10 秒后重试...")
                time.sleep(10)
                continue

            # 监控 Bot
            health_check_interval = 30  # 每 30 秒检查一次
            last_check = time.time()

            while self.running:
                try:
                    # 检查进程状态
                    if self.bot_process.poll() is not None:
                        logger.warning("Bot 进程意外退出")
                        break

                    # 定期健康检查
                    current_time = time.time()
                    if current_time - last_check >= health_check_interval:
                        if not self.check_bot_health():
                            logger.warning("健康检查失败，重启 Bot")
                            self.stop_bot()
                            break
                        last_check = current_time

                    # 等待一段时间
                    time.sleep(5)

                except KeyboardInterrupt:
                    logger.info("收到中断信号")
                    self.running = False
                    break
                except Exception as e:
                    logger.error(f"监控出错: {e}")
                    time.sleep(5)

            # 停止 Bot
            self.stop_bot()

            # 如果还在运行，准备重启
            if self.running:
                self.restart_count += 1
                wait_time = min(5 * self.restart_count, 60)  # 递增等待时间
                logger.info(f"{wait_time} 秒后重启...")
                time.sleep(wait_time)

        self.stop_bot()
        logger.info("守护进程退出")

    def signal_handler(self, signum, frame):
        """信号处理器"""
        logger.info(f"收到信号 {signum}，准备退出...")
        self.running = False


def main():
    """主函数"""
    import sys
    import io

    # 设置标准输出编码为 UTF-8
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    daemon = BotDaemon()

    try:
        daemon.run()
    except KeyboardInterrupt:
        logger.info("用户中断")
    except Exception as e:
        logger.error(f"守护进程错误: {e}")
        raise


if __name__ == "__main__":
    main()
