# 🔧 修复 "Failed to fetch" 错误

## 问题原因

前端代码中还在使用 `http://localhost:5001`，需要改为你的 Render URL。

## ✅ 解决方案

### 方法1：使用相对路径（推荐，最简单）

如果你的前端和后端在同一个域名下（都在 Render），可以使用相对路径。

### 方法2：使用 Render URL

需要将所有的 `http://localhost:5001` 替换为你的 Render URL。

---

## 🎯 快速修复步骤

### 第一步：获取你的 Render URL

你的 Render URL 应该是类似：
```
https://bazi-fortune-analysis.onrender.com
```
或者
```
https://你的服务名.onrender.com
```

### 第二步：更新所有 HTML 文件

需要修改 3 个文件：
1. `index.html`
2. `login.html`
3. `result.html`

将所有的：
```javascript
'http://localhost:5001'
```

改为：
```javascript
'https://你的RenderURL.onrender.com'
```

或者使用相对路径（如果前后端同域名）：
```javascript
''  // 空字符串，使用相对路径
```

---

## 📝 具体修改位置

### index.html

找到：
```javascript
const calculateResponse = await fetch('http://localhost:5001/api/calculate', {
```

改为：
```javascript
const calculateResponse = await fetch('https://你的RenderURL.onrender.com/api/calculate', {
```

### login.html

找到：
```javascript
const response = await fetch('http://localhost:5001/api/login', {
```

改为：
```javascript
const response = await fetch('https://你的RenderURL.onrender.com/api/login', {
```

### result.html

找到所有：
```javascript
fetch('http://localhost:5001/api/...', {
```

改为：
```javascript
fetch('https://你的RenderURL.onrender.com/api/...', {
```

---

## ⚡ 更简单的方法：使用相对路径

如果你的前端和后端都在同一个 Render 服务上（通过 Flask 的静态文件服务），可以使用相对路径：

将所有：
```javascript
'http://localhost:5001'
```

改为：
```javascript
''  // 空字符串
```

这样会自动使用当前域名。

---

## 🔍 如何确认修复成功

1. 修改后，推送代码到 GitHub：
   ```bash
   git add .
   git commit -m "Update API URLs to Render"
   git push
   ```

2. Render 会自动重新部署

3. 刷新浏览器，清除缓存（Cmd+Shift+R 或 Ctrl+Shift+R）

4. 再次点击 "Analyze" 按钮

5. 应该可以正常工作了！

---

## ⚠️ 如果还是不行

检查：
1. Render 的 URL 是否正确
2. CORS 配置是否正确（应该已经配置了）
3. 浏览器控制台（F12）查看具体错误信息
4. Render 的 Logs 查看后端是否有错误

