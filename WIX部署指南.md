# 🚀 Wix 部署指南

## 📋 方案选择

由于 Wix 不支持直接运行 Python/Flask 后端，我们有两种方案：

### 方案A：后端部署到云服务 + 前端部署到 Wix（推荐用于 Wix）
- **后端**：部署到云服务（Render, Railway, Heroku 等）
- **前端**：部署到 Wix，通过 API 调用后端
- **优点**：可以利用 Wix 的页面设计和 SEO 功能
- **缺点**：需要维护两个平台

### 方案B：全栈部署到云服务（更简单，推荐）
- **全栈**：部署到 Render, Railway, Vercel 等
- **优点**：简单，一个平台管理所有内容
- **缺点**：不使用 Wix 的页面设计功能

---

## 🎯 方案A：后端云服务 + Wix 前端

### 第一步：部署后端到云服务

#### 选项1：使用 Render（免费，推荐）

1. **准备部署文件**

创建 `Procfile`（如果没有）：
```
web: gunicorn app:app
```

创建 `runtime.txt`：
```
python-3.11.0
```

2. **在 Render 上部署**

   a. 访问 https://render.com 并注册账号
   
   b. 点击 "New +" → "Web Service"
   
   c. 连接你的 GitHub 仓库（或直接上传代码）
   
   d. 配置：
      - **Name**: `bazi-api`（或你喜欢的名字）
      - **Environment**: `Python 3`
      - **Build Command**: `pip install -r requirements.txt`
      - **Start Command**: `gunicorn app:app --host 0.0.0.0 --port $PORT`
      - **Environment Variables**: 
        - `DEEPSEEK_API_KEY`: 你的 DeepSeek API Key
   
   e. 点击 "Create Web Service"
   
   f. 等待部署完成，你会得到一个 URL，比如：`https://bazi-api.onrender.com`

3. **更新 requirements.txt**

确保包含 `gunicorn`：
```
Flask==3.0.0
flask-cors==4.0.0
openai==1.12.0
gunicorn==21.2.0
```

#### 选项2：使用 Railway（简单）

1. 访问 https://railway.app
2. 点击 "New Project" → "Deploy from GitHub"
3. 选择你的仓库
4. Railway 会自动检测 Python 项目
5. 添加环境变量 `DEEPSEEK_API_KEY`
6. 部署完成后会得到一个 URL

---

### 第二步：在 Wix 上部署前端

#### 方法1：使用 Wix Velo（推荐）

1. **创建 Wix 网站**
   - 访问 https://www.wix.com
   - 创建一个新网站
   - 选择 "Start from Scratch" 或使用模板

2. **添加自定义页面**
   - 在 Wix 编辑器中，点击 "Add" → "Page" → "Blank Page"
   - 命名为 "Bazi Analysis"

3. **使用 Wix Velo 添加代码**
   
   a. 点击右上角 "Dev Mode" 开启开发者模式
   
   b. 在左侧面板找到 "Code" 标签
   
   c. 创建新文件 `public/index.html`（或直接在页面中添加 HTML）
   
   d. 修改你的 `index.html`，更新 API 地址：
   
   ```javascript
   // 将所有的 http://localhost:5001 改为你的后端 URL
   const API_BASE_URL = 'https://your-backend-url.onrender.com';
   
   // 例如：
   const response = await fetch(`${API_BASE_URL}/api/calculate`, {
       // ...
   });
   ```

4. **添加 HTML 代码到 Wix 页面**
   
   a. 在 Wix 编辑器中，添加 "HTML iframe" 元素
   
   b. 或者使用 Velo 的 `$w.onReady()` 函数动态加载内容
   
   c. 更好的方法：使用 Wix 的 "Embed Code" 功能

#### 方法2：使用 Wix 的 HTML 嵌入功能

1. **准备前端文件**
   - 修改 `index.html` 中的所有 API 调用，将 `http://localhost:5001` 改为你的后端 URL
   - 同样修改 `login.html` 和 `result.html`

2. **在 Wix 中添加**
   - 在页面中添加 "Embed Code" 元素
   - 将 HTML 代码粘贴进去
   - 或者使用 iframe 嵌入

3. **上传静态文件**
   - 在 Wix 的 "Media" 中上传 CSS/JS 文件（如果需要）
   - 或者将所有代码内联到 HTML 中

---

## 🎯 方案B：全栈部署到云服务（更简单）

### 使用 Render（推荐）

1. **准备部署文件**

确保项目根目录有：
- `requirements.txt`
- `Procfile`（内容：`web: gunicorn app:app`）
- `runtime.txt`（内容：`python-3.11.0`）

2. **修改 app.py**

确保静态文件服务已配置（应该已经有了）：
```python
app = Flask(__name__, static_folder='.', static_url_path='')
```

3. **在 Render 上部署**

   a. 访问 https://render.com
   
   b. 点击 "New +" → "Web Service"
   
   c. 连接 GitHub 仓库
   
   d. 配置：
      - **Name**: `bazi-fortune-analysis`
      - **Environment**: `Python 3`
      - **Build Command**: `pip install -r requirements.txt`
      - **Start Command**: `gunicorn app:app --host 0.0.0.0 --port $PORT`
      - **Environment Variables**: 
        - `DEEPSEEK_API_KEY`: 你的 API Key
   
   e. 点击 "Create Web Service"
   
   f. 等待部署完成

4. **访问你的网站**

部署完成后，你会得到一个 URL，比如：
`https://bazi-fortune-analysis.onrender.com`

直接访问这个 URL 就可以使用你的网站了！

---

## 📝 需要修改的代码

### 1. 更新 API 地址

在所有 HTML 文件中，将：
```javascript
const API_URL = 'http://localhost:5001';
```

改为：
```javascript
const API_URL = 'https://your-backend-url.onrender.com';
```

### 2. 添加 CORS 配置（如果还没有）

确保 `app.py` 中有：
```python
CORS(app, supports_credentials=True, origins=["*"])
```

### 3. 修改端口配置

在 `app.py` 中，确保使用环境变量：
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
```

---

## 🔧 快速部署脚本

创建一个 `deploy.sh` 文件：

```bash
#!/bin/bash
# 更新所有 HTML 文件中的 API URL
BACKEND_URL="https://your-backend-url.onrender.com"

# 替换所有 localhost:5001 为实际的后端 URL
find . -name "*.html" -type f -exec sed -i '' "s|http://localhost:5001|${BACKEND_URL}|g" {} \;

echo "API URLs updated to: ${BACKEND_URL}"
```

---

## ⚠️ 注意事项

1. **免费服务限制**
   - Render 免费版：15 分钟无活动后休眠，首次访问需要几秒唤醒
   - Railway 免费版：有使用限制
   - 考虑升级到付费版以获得更好的性能

2. **环境变量**
   - 确保在云服务平台上设置了 `DEEPSEEK_API_KEY`
   - 不要将 API Key 提交到 GitHub

3. **域名**
   - 免费服务通常提供子域名
   - 可以绑定自定义域名（需要配置 DNS）

4. **HTTPS**
   - 云服务通常自动提供 HTTPS
   - 确保所有 API 调用使用 HTTPS

---

## 🎨 Wix 特定建议

如果你坚持使用 Wix：

1. **使用 Wix 的 API 集成**
   - 在 Wix 中设置 "External API" 连接
   - 配置你的后端 API URL

2. **使用 Wix Velo**
   - 可以编写 JavaScript 调用你的后端 API
   - 使用 `fetch()` 或 `wix-fetch` 模块

3. **页面设计**
   - 使用 Wix 的页面编辑器设计界面
   - 通过 Velo 代码连接后端功能

---

## 💡 推荐方案

**我推荐使用方案B（全栈部署到 Render）**，因为：
- ✅ 更简单，一个平台管理所有内容
- ✅ 不需要修改太多代码
- ✅ 更容易维护
- ✅ 性能更好（不需要跨域请求）

如果你需要 Wix 的 SEO 和页面设计功能，可以使用方案A。

---

需要我帮你准备部署文件吗？

