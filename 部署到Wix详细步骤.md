# 📘 部署到 Wix - 详细步骤

## 🎯 推荐方案：全栈部署到 Render（最简单）

由于 Wix 不支持 Python 后端，我**强烈推荐**先将整个应用部署到 Render，然后在 Wix 中嵌入或链接。

---

## 🚀 第一步：部署到 Render（5分钟）

### 1. 准备 GitHub 仓库

1. 在 GitHub 上创建一个新仓库
2. 将你的项目代码推送到 GitHub：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git push -u origin main
   ```

### 2. 在 Render 上部署

1. **访问 Render**
   - 打开 https://render.com
   - 点击 "Get Started for Free" 注册账号（可以用 GitHub 账号登录）

2. **创建 Web Service**
   - 登录后，点击 "New +" → "Web Service"
   - 选择 "Connect GitHub" 并授权
   - 选择你的仓库

3. **配置部署**
   - **Name**: `bazi-fortune-analysis`（或你喜欢的名字）
   - **Environment**: `Python 3`
   - **Region**: 选择离你最近的区域
   - **Branch**: `main`（或你的主分支）
   - **Root Directory**: 留空（如果代码在根目录）
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --host 0.0.0.0 --port $PORT`

4. **设置环境变量**
   - 点击 "Environment" 标签
   - 添加环境变量：
     - **Key**: `DEEPSEEK_API_KEY`
     - **Value**: `sk-ce5f3d16c611492ca98a3fda8e77dc17`（你的 API Key）
   - 点击 "Save Changes"

5. **开始部署**
   - 点击 "Create Web Service"
   - 等待 2-5 分钟，部署会自动完成
   - 部署成功后，你会得到一个 URL，比如：`https://bazi-fortune-analysis.onrender.com`

6. **测试部署**
   - 在浏览器中访问你的 URL
   - 应该能看到网站首页

---

## 🎨 第二步：在 Wix 中集成

### 方法1：直接链接（最简单）

1. **在 Wix 中创建页面**
   - 登录 Wix 编辑器
   - 添加一个新页面，命名为 "Bazi Analysis"
   - 添加一个按钮或链接
   - 设置链接为你的 Render URL：`https://bazi-fortune-analysis.onrender.com`

2. **完成！**
   - 用户点击按钮就会跳转到你的应用

### 方法2：使用 iframe 嵌入（推荐）

1. **在 Wix 页面中添加 HTML 元素**
   - 在 Wix 编辑器中，点击 "Add" → "More" → "Embed Code" → "HTML iframe"
   - 或者添加 "Embed" → "HTML Code"

2. **添加 iframe 代码**
   ```html
   <iframe 
       src="https://bazi-fortune-analysis.onrender.com" 
       width="100%" 
       height="800px" 
       frameborder="0"
       style="border: none;">
   </iframe>
   ```

3. **调整样式**
   - 在 Wix 中调整 iframe 的大小和位置
   - 确保响应式设计

### 方法3：使用 Wix Velo 调用 API（高级）

如果你想要更深度集成，可以使用 Wix Velo：

1. **开启开发者模式**
   - 在 Wix 编辑器中，点击右上角 "Dev Mode"

2. **创建页面代码**
   - 在左侧面板找到 "Code" 标签
   - 创建新文件 `public/main.js`

3. **添加代码**
   ```javascript
   import wixFetch from 'wix-fetch';

   $w.onReady(function () {
       // 你的后端 API URL
       const API_URL = 'https://bazi-fortune-analysis.onrender.com';
       
       // 调用 API 的示例
       $w('#submitButton').onClick(() => {
           wixFetch.fetch(`${API_URL}/api/calculate`, {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify({
                   nickname: $w('#nicknameInput').value,
                   birthDate: $w('#birthDateInput').value
               })
           })
           .then(response => response.json())
           .then(data => {
               // 处理返回的数据
               $w('#resultText').text = JSON.stringify(data);
           });
       });
   });
   ```

4. **设计页面**
   - 使用 Wix 的页面编辑器设计界面
   - 添加输入框、按钮等元素
   - 通过代码连接后端 API

---

## 🔧 重要配置

### 1. 更新 CORS 设置

确保 `app.py` 中的 CORS 配置允许 Wix 域名：

```python
CORS(app, supports_credentials=True, origins=[
    "https://your-wix-site.wixsite.com",
    "https://yourdomain.com",
    "*"  # 开发时可以使用，生产环境建议限制
])
```

### 2. 环境变量

在 Render 的环境变量中设置：
- `DEEPSEEK_API_KEY`: 你的 DeepSeek API Key
- `FLASK_ENV`: `production`（生产环境）

### 3. 自定义域名（可选）

1. **在 Render 中绑定域名**
   - 在 Render 的 Web Service 设置中
   - 点击 "Custom Domains"
   - 添加你的域名
   - 按照提示配置 DNS

2. **在 Wix 中使用自定义域名**
   - 在 Wix 设置中配置域名
   - 确保 DNS 配置正确

---

## ⚠️ 注意事项

### Render 免费版限制

1. **休眠机制**
   - 15 分钟无活动后会自动休眠
   - 首次访问需要几秒唤醒时间
   - 考虑升级到付费版（$7/月）以保持常驻

2. **性能**
   - 免费版资源有限
   - 如果访问量大，建议升级

### 安全建议

1. **API Key 安全**
   - 不要将 API Key 提交到 GitHub
   - 使用环境变量存储
   - 考虑使用 `.env` 文件（但不要提交）

2. **HTTPS**
   - Render 自动提供 HTTPS
   - 确保所有 API 调用使用 HTTPS

---

## 🎯 推荐工作流程

### 开发阶段
1. 本地开发：`python3 app.py`（使用 localhost:5001）
2. 测试功能

### 部署阶段
1. 推送到 GitHub
2. Render 自动部署
3. 测试生产环境

### Wix 集成
1. 使用 iframe 嵌入（最简单）
2. 或使用 Velo 深度集成（如果需要）

---

## 📞 需要帮助？

如果遇到问题：
1. 检查 Render 的部署日志
2. 检查浏览器控制台的错误
3. 确保 API URL 正确
4. 检查 CORS 配置

---

## ✅ 检查清单

部署前确认：
- [ ] `requirements.txt` 包含所有依赖
- [ ] `Procfile` 存在且正确
- [ ] `runtime.txt` 指定了 Python 版本
- [ ] 环境变量已设置
- [ ] 代码已推送到 GitHub
- [ ] Render 部署成功
- [ ] 可以访问网站
- [ ] API 调用正常
- [ ] Wix 集成完成

---

**完成这些步骤后，你的网站就可以在 Wix 中使用了！** 🎉

