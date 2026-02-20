# 本地会话 Telegram 同步 - 更新说明

## 🎯 新增功能

现在**所有本地会话的消息都会自动同步到 Telegram**！

### 实现方式

在 `main.ts` 的 `message` 事件监听器中添加了 Telegram 同步逻辑：

```typescript
coworkRunner.on('message', (sessionId: string, message: any) => {
  // ... 原有的代码 ...

  // 新增：同步到 Telegram（如果是文本消息）
  if (message.type === 'text' && message.content) {
    try {
      const manager = getIMGatewayManager();
      if (manager) {
        manager.sendToTelegram(message.content).catch((error) => {
          console.error('[Main] Failed to sync to Telegram:', error);
        });
      }
    } catch (error) {
      console.debug('[Main] IMGatewayManager not available for Telegram sync');
    }
  }
});
```

## ✅ 效果

- 💻 你在本地（电脑端）的所有对话
- 📱 会自动同步到 Telegram
- 🔄 完整的双向同步，无断层

## 🚀 需要重启应用

代码已编译完成，需要重启 LobsterAI 应用才能生效！
