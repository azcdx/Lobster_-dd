#!/bin/bash
# LobsterAI 配置和记忆备份脚本

set -e

echo "=== LobsterAI 配置和记忆备份 ==="
echo ""

# 定义源目录和目标目录
LOBSTERAI_APPDATA="$APPDATA/LobsterAI"
BACKUP_DIR="$PWD/backup-config"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "📁 备份目标目录: $BACKUP_DIR"
echo "⏰ 时间戳: $TIMESTAMP"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份函数
backup_file() {
    local src="$1"
    local dest="$2"
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        echo "✅ 已备份: $(basename "$src")"
    else
        echo "⚠️  跳过（不存在）: $(basename "$src")"
    fi
}

backup_dir() {
    local src="$1"
    local dest="$2"
    if [ -d "$src" ]; then
        cp -r "$src" "$dest"
        echo "✅ 已备份目录: $(basename "$src")"
    else
        echo "⚠️  跳过（不存在）: $(basename "$src")"
    fi
}

echo "📋 开始备份关键文件..."
echo ""

# 1. 数据库文件（包含用户记忆、配置等）
echo "1️⃣ 备份数据库..."
backup_file "$LOBSTERAI_APPDATA/lobsterai.sqlite" "$BACKUP_DIR/lobsterai.sqlite"
backup_file "$LOBSTERAI_APPDATA/DIPS" "$BACKUP_DIR/DIPS"

# 2. 配置文件
echo ""
echo "2️⃣ 备份配置文件..."
backup_file "$LOBSTERAI_APPDATA/Preferences" "$BACKUP_DIR/Preferences"
backup_file "$LOBSTERAI_APPDATA/Local State" "$BACKUP_DIR/Local State"

# 3. SKILLs 配置
echo ""
echo "3️⃣ 备份 SKILLs 配置..."
backup_dir "$LOBSTERAI_APPDATA/SKILLs" "$BACKUP_DIR/SKILLs"

# 4. Cowork 配置和脚本
echo ""
echo "4️⃣ 备份 Cowork 配置..."
backup_dir "$LOBSTERAI_APPDATA/cowork/bin" "$BACKUP_DIR/cowork-bin"
backup_dir "$LOBSTERAI_APPDATA/cowork/sandbox" "$BACKUP_DIR/cowork-sandbox"

# 5. 邮件配置（如果存在）
echo ""
echo "5️⃣ 备份邮件配置..."
IMAP_SMTP_SKILL="E:/实例/LobsterAI/SKILLs/imap-smtp-email"
if [ -f "$IMAP_SMTP_SKILL/.env" ]; then
    backup_file "$IMAP_SMTP_SKILL/.env" "$BACKUP_DIR/email-config.env"
    echo "⚠️  注意: email-config.env 包含敏感信息，请勿推送到公开仓库"
else
    echo "ℹ️  未找到邮件配置文件"
fi

# 6. 创建元数据文件
echo ""
echo "6️⃣ 创建备份元数据..."
cat > "$BACKUP_DIR/backup-info.json" << EOF
{
  "backupDate": "$(date -Iseconds)",
  "timestamp": "$TIMESTAMP",
  "hostname": "$(hostname)",
  "username": "$USER",
  "lobsteraiVersion": "0.1.16"
}
EOF
echo "✅ 已创建备份元数据"

# 7. 生成备份清单
echo ""
echo "7️⃣ 生成备份清单..."
cat > "$BACKUP_DIR/FILE_LIST.txt" << EOF
LobsterAI 配置和记忆备份文件清单
=====================================
备份时间: $(date)
备份时间戳: $TIMESTAMP
主机名: $(hostname)
用户: $USER

重要文件说明:
-----------
1. lobsterai.sqlite - 主数据库（包含对话历史、用户记忆、定时任务等）
2. DIPS - 偏好设置数据库
3. Preferences - Electron 应用偏好设置
4. Local State - 本地状态配置
5. SKILLs/ - 技能配置目录
6. cowork-bin/ - Cowork 运行时环境
7. cowork-sandbox/ - 沙箱配置
8. email-config.env - 邮件配置（敏感信息）

恢复说明:
---------
1. 将这些文件复制到新电脑的相同位置
2. Windows: C:\Users\<你的用户名>\AppData\Roaming\LobsterAI\
3. 确保 LobsterAI 应用已关闭
4. 复制文件后重启应用

注意事项:
---------
- lobsterai.sqlite 包含所有重要数据，请妥善保管
- email-config.env 包含密码，不要分享或上传到公开仓库
- 建议定期备份，特别是在重要配置更改后
EOF

echo "✅ 已创建备份清单"
echo ""
echo "🎉 备份完成！"
echo ""
echo "📊 备份统计:"
du -sh "$BACKUP_DIR" 2>/dev/null || echo "  总大小: 计算中..."
echo ""
echo "📂 备份位置: $BACKUP_DIR"
echo ""
echo "💡 下一步:"
echo "1. 检查备份文件: ls -la '$BACKUP_DIR'"
echo "2. 提交到 Git: git add backup-config/ && git commit -m '备份配置和记忆'"
echo "3. 推送到远程仓库: git push origin main"
echo ""
echo "⚠️  重要提醒:"
echo "- 如果包含 email-config.env，请将其添加到 .gitignore"
echo "- 不要将包含密码的文件推送到公开仓库"
