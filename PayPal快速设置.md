# 💳 PayPal 快速设置指南

## ✅ 已完成

我已经将支付系统从 Stripe 改为 PayPal！

## 🚀 快速设置（5分钟）

### 第一步：创建 PayPal 应用

1. **访问 PayPal Developer**
   - 打开 https://developer.paypal.com
   - 使用 PayPal 账号登录（如果没有，先注册）

2. **创建应用**
   - 点击 "My Apps & Credentials"
   - 点击 "Create App"
   - **App Name**: `Bazi Fortune Analysis`
   - 点击 "Create App"

3. **复制 Credentials**
   - 你会看到 **Client ID** 和 **Secret**
   - 点击 "Show" 查看 Secret
   - **复制这两个值**

### 第二步：在 Render 中设置

1. **进入 Render Web Service**
   - 点击 "Environment" 标签

2. **添加环境变量**

   **第一个：**
   - Key: `PAYPAL_CLIENT_ID`
   - Value: 你的 Client ID

   **第二个：**
   - Key: `PAYPAL_CLIENT_SECRET`
   - Value: 你的 Secret

   **第三个：**
   - Key: `PAYPAL_MODE`
   - Value: `sandbox`（测试时）

3. **保存**
   - 点击 "Save Changes"
   - Render 会自动重新部署

### 第三步：推送代码

```bash
cd "/Users/kiukiu/Five Elements Test"
git add .
git commit -m "Switch to PayPal payment"
git push
```

## 🧪 测试

### 使用 PayPal 测试账号

1. **在 PayPal Developer Dashboard**
   - 点击 "Accounts" → "Sandbox"
   - 使用默认测试账号，或创建新的测试账号

2. **测试流程**
   - 访问你的网站
   - 提交分析
   - 点击支付按钮
   - 使用 PayPal 测试账号登录
   - 确认支付
   - 应该自动创建账号并登录

## ✅ 完成！

设置完成后就可以接受 PayPal 支付了！

