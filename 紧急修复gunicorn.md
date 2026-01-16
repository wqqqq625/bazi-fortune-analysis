# 🚨 紧急修复 Gunicorn 错误

## 问题

Render 仍然显示错误：
```
gunicorn: error: unrecognized arguments: --host 0.0.0.0 --port 10000
```

这说明 Render 的 Settings 中还在使用旧的 Start Command。

## ✅ 立即修复（在 Render 中）

### 步骤1：进入 Render 设置

1. 登录 https://render.com
2. 找到你的 Web Service（`bazi-fortune-analysis`）
3. 点击进入详情页
4. 点击左侧的 **"Settings"** 标签

### 步骤2：修改 Start Command

1. 找到 **"Start Command"** 字段
2. **删除** 当前的内容（可能是 `gunicorn app:app --host 0.0.0.0 --port $PORT`）
3. **输入** 正确的命令：
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```
4. 点击 **"Save Changes"** 按钮

### 步骤3：等待重新部署

- Render 会自动检测到更改并重新部署
- 等待 1-2 分钟
- 查看 "Logs" 标签确认是否成功

## 📝 正确的命令对比

### ❌ 错误（当前使用的）
```
gunicorn app:app --host 0.0.0.0 --port $PORT
```

### ✅ 正确（应该使用的）
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

## 🔍 如何确认修复成功

1. 在 Render 的 "Logs" 标签中
2. 应该看到类似这样的日志：
   ```
   [INFO] Starting gunicorn 21.2.0
   [INFO] Listening at: http://0.0.0.0:10000
   [INFO] Using worker: sync
   [INFO] Booting worker with pid: X
   ```
3. 没有错误信息
4. 网站可以正常访问

## ⚠️ 如果还是不行

如果修改后还是报错，检查：

1. **确认命令完全正确**
   - 没有多余的空格
   - 使用 `--bind` 而不是 `--host --port`
   - `$PORT` 前面是冒号 `:`

2. **清除缓存重新部署**
   - 在 Settings 中点击 "Clear build cache"
   - 然后点击 "Manual Deploy" → "Deploy latest commit"

3. **检查 Procfile**
   - 确保本地 Procfile 内容是：`web: gunicorn app:app --bind 0.0.0.0:$PORT`
   - 推送更新：`git add Procfile && git commit -m "Fix" && git push`

## 🎯 快速操作

**在 Render 的 Settings 页面：**

1. 找到 "Start Command"
2. 改为：`gunicorn app:app --bind 0.0.0.0:$PORT`
3. 保存
4. 等待部署完成

**就这么简单！**

