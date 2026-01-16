# 💳 PayPal 支付设置指南

## 📋 设置步骤

### 第一步：创建 PayPal 账号

1. 访问 https://www.paypal.com
2. 点击 "Sign Up" 注册账号
3. 选择 "Business Account"（商业账号，用于接收付款）
   - 或者选择 "Personal Account"（个人账号，也可以接收付款）
4. 填写信息并验证邮箱

### 第二步：获取 PayPal API Credentials

1. **登录 PayPal Developer Dashboard**
   - 访问 https://developer.paypal.com
   - 使用你的 PayPal 账号登录

2. **创建应用**
   - 点击 "My Apps & Credentials"
   - 点击 "Create App"
   - **App Name**: `Bazi Fortune Analysis`（或你喜欢的名字）
   - **Merchant**: 选择你的账号
   - 点击 "Create App"

3. **获取 API Credentials**
   - 创建后，你会看到：
     - **Client ID**（客户端 ID）
     - **Secret**（密钥）- 点击 "Show" 查看
   - **复制这两个值**

4. **选择环境**
   - **Sandbox**（测试环境）- 用于测试，不会产生真实费用
   - **Live**（生产环境）- 用于正式上线

### 第三步：在 Render 中设置环境变量

1. **登录 Render**
   - 访问 https://render.com
   - 进入你的 Web Service

2. **添加环境变量**
   - 点击 "Environment" 标签
   - 添加以下环境变量：

   **第一个：**
   - **Key**: `PAYPAL_CLIENT_ID`
   - **Value**: 你的 PayPal Client ID（从 Developer Dashboard 复制）

   **第二个：**
   - **Key**: `PAYPAL_CLIENT_SECRET`
   - **Value**: 你的 PayPal Secret（从 Developer Dashboard 复制）

   **第三个：**
   - **Key**: `PAYPAL_MODE`
   - **Value**: `sandbox`（测试时）或 `live`（生产时）

3. **保存并重新部署**
   - 点击 "Save Changes"
   - Render 会自动重新部署

### 第四步：推送代码

```bash
cd "/Users/kiukiu/Five Elements Test"
git add .
git commit -m "Switch from Stripe to PayPal payment"
git push
```

## 🧪 测试支付

### 使用 PayPal 测试账号

在 Sandbox 模式下，你可以创建测试账号：

1. **在 PayPal Developer Dashboard**
   - 点击 "Accounts" → "Sandbox" → "Create account"
   - 创建买家（Buyer）和卖家（Seller）测试账号
   - 或者使用默认测试账号

2. **测试账号信息**
   - PayPal 会提供测试邮箱和密码
   - 使用这些账号登录 PayPal 测试环境

### 测试流程

1. 访问你的网站
2. 提交分析请求
3. 点击 "💳 Unlock Full Report - $2.99"
4. 跳转到支付页面
5. 点击 "Pay $2.99 to Unlock"
6. 跳转到 PayPal 登录页面
7. 使用测试账号登录
8. 确认支付
9. 支付成功后：
   - 自动创建账号
   - 自动登录
   - 显示账号信息
   - 自动跳转到结果页面
   - 可以看到完整报告

## 💰 支付流程

1. **用户点击支付按钮**
   - 跳转到 `payment.html`
   - 显示价格和功能列表

2. **用户点击 "Pay $2.99 to Unlock"**
   - 调用 `/api/create-payment`
   - 创建 PayPal 支付
   - 获取 PayPal 支付链接

3. **跳转到 PayPal**
   - 用户登录 PayPal
   - 确认支付

4. **支付成功回调**
   - PayPal 重定向到 `/payment-success`
   - 验证支付状态
   - 自动生成用户名和密码
   - 保存到 USERS 数据库
   - 自动登录
   - 重定向到结果页面，显示完整报告

## ⚠️ 重要提示

### Sandbox vs Live

**Sandbox（测试环境）：**
- 使用测试账号
- 不会产生真实费用
- 用于开发和测试

**Live（生产环境）：**
1. 在 PayPal Developer Dashboard 切换到 Live
2. 获取 Live 环境的 Client ID 和 Secret
3. 更新 Render 环境变量：
   - `PAYPAL_CLIENT_ID` → Live Client ID
   - `PAYPAL_CLIENT_SECRET` → Live Secret
   - `PAYPAL_MODE` → `live`
4. 重新部署

### 安全

- ✅ Client Secret 只存储在环境变量中
- ✅ 不会提交到 GitHub
- ✅ 使用 PayPal 的安全支付页面
- ✅ 不处理信用卡信息

### PayPal 费用

- PayPal 会收取交易手续费（通常约 2.9% + $0.30）
- 实际到账金额会略少于 $2.99

## ✅ 检查清单

- [ ] 创建了 PayPal 账号
- [ ] 在 Developer Dashboard 创建了应用
- [ ] 获取了 Sandbox 环境的 Client ID 和 Secret
- [ ] 在 Render 中设置了环境变量
- [ ] 推送了代码
- [ ] Render 重新部署成功
- [ ] 测试支付流程
- [ ] 支付成功后能自动登录
- [ ] 能看到完整报告

## 🎉 完成！

设置完成后，用户就可以通过 PayPal 支付 $2.99 来解锁完整报告了！

## 📞 需要帮助？

如果遇到问题：
1. 检查 PayPal Developer Dashboard 中的应用状态
2. 检查 Render 的环境变量是否正确
3. 查看 Render Logs 中的错误信息
4. 确保 PayPal 账号已激活

