# 💳 Stripe 支付设置指南

## 📋 设置步骤

### 第一步：创建 Stripe 账号

1. 访问 https://stripe.com
2. 点击 "Sign up" 注册账号
3. 填写你的信息（邮箱、密码等）
4. 验证邮箱

### 第二步：获取 API Keys

1. **登录 Stripe Dashboard**
   - 访问 https://dashboard.stripe.com
   - 登录你的账号

2. **切换到测试模式（开发时）**
   - 在右上角，确保 "Test mode" 开关是打开的（显示 "Test mode"）
   - 这样可以使用测试卡号，不会产生真实费用

3. **获取 API Keys**
   - 点击左侧菜单 "Developers" → "API keys"
   - 你会看到两把钥匙：
     - **Publishable key** (pk_test_...)
     - **Secret key** (sk_test_...)
   - 点击 "Reveal test key" 查看 Secret key
   - **复制这两个 key**

### 第三步：在 Render 中设置环境变量

1. **登录 Render**
   - 访问 https://render.com
   - 进入你的 Web Service

2. **添加环境变量**
   - 点击 "Environment" 标签
   - 添加以下两个环境变量：

   **第一个：**
   - **Key**: `STRIPE_SECRET_KEY`
   - **Value**: `sk_test_...`（你的 Stripe Secret Key）

   **第二个：**
   - **Key**: `STRIPE_PUBLISHABLE_KEY`
   - **Value**: `pk_test_...`（你的 Stripe Publishable Key）

3. **保存并重新部署**
   - 点击 "Save Changes"
   - Render 会自动重新部署

### 第四步：测试支付

1. **使用测试卡号**
   - 卡号：`4242 4242 4242 4242`
   - 过期日期：任何未来的日期（如 12/25）
   - CVC：任何 3 位数字（如 123）
   - 邮编：任何 5 位数字（如 12345）

2. **测试流程**
   - 访问你的网站
   - 提交分析
   - 点击 "Unlock Full Report - $2.99"
   - 使用测试卡号支付
   - 应该会自动创建账号并登录

### 第五步：切换到生产模式（上线时）

1. **在 Stripe Dashboard**
   - 关闭 "Test mode" 开关
   - 切换到 "Live mode"

2. **获取生产环境的 Keys**
   - 点击 "Developers" → "API keys"
   - 现在显示的是 Live keys（没有 test 前缀）
   - 复制新的 Secret key 和 Publishable key

3. **更新 Render 环境变量**
   - 将 `STRIPE_SECRET_KEY` 更新为 Live Secret Key
   - 将 `STRIPE_PUBLISHABLE_KEY` 更新为 Live Publishable Key
   - 保存并重新部署

## ⚠️ 重要提示

### 安全
- **永远不要**将 Secret Key 提交到 GitHub
- 只使用环境变量存储
- Secret Key 应该保密，只有服务器知道

### 测试 vs 生产
- **测试模式**：使用 `sk_test_...` 和 `pk_test_...`
- **生产模式**：使用 `sk_live_...` 和 `pk_live_...`
- 测试模式不会产生真实费用

### Webhook（可选，用于更高级的功能）

如果需要处理支付后的异步通知，可以设置 Webhook：
1. 在 Stripe Dashboard → "Developers" → "Webhooks"
2. 添加 endpoint：`https://你的域名.com/api/webhook`
3. 选择事件：`checkout.session.completed`
4. 复制 Webhook signing secret
5. 添加到环境变量：`STRIPE_WEBHOOK_SECRET`

## ✅ 检查清单

- [ ] 创建了 Stripe 账号
- [ ] 获取了测试环境的 API Keys
- [ ] 在 Render 中设置了环境变量
- [ ] 测试支付流程成功
- [ ] 支付后能自动创建账号
- [ ] 支付后能自动登录
- [ ] 能看到完整报告

## 🎉 完成！

设置完成后，用户就可以通过支付 $2.99 来解锁完整报告了！

