# 🔧 修复 Gunicorn 错误

## ❌ 错误信息

```
gunicorn: error: unrecognized arguments: --host 0.0.0.0 --port 10000
```

## ✅ 问题原因

Gunicorn 不支持 `--host` 和 `--port` 参数，应该使用 `--bind`（或 `-b`）来指定地址和端口。

## 🔧 解决方案

### 方法1：使用 Procfile（推荐）

`Procfile` 已经修复为：
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### 方法2：在 Render 中修改 Start Command

在 Render 的 Web Service 设置中：

1. 点击 "Settings" 标签
2. 找到 "Start Command"
3. 修改为：
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```
4. 点击 "Save Changes"
5. Render 会自动重新部署

## 📝 正确的 Gunicorn 语法

### 错误写法 ❌
```
gunicorn app:app --host 0.0.0.0 --port $PORT
```

### 正确写法 ✅
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

或者使用简写：
```
gunicorn app:app -b 0.0.0.0:$PORT
```

## 🎯 其他常用 Gunicorn 选项

如果需要更多配置，可以添加：

```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

- `--workers`: 工作进程数（通常设为 CPU 核心数 × 2 + 1）
- `--timeout`: 超时时间（秒）
- `--access-logfile`: 访问日志文件
- `--error-logfile`: 错误日志文件

## ✅ 修复后

1. 保存更改
2. 在 Render 中重新部署
3. 应该可以正常启动了！

