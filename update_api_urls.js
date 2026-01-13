/**
 * 脚本：更新所有 HTML 文件中的 API URL
 * 使用方法：node update_api_urls.js <backend-url>
 * 例如：node update_api_urls.js https://bazi-api.onrender.com
 */

const fs = require('fs');
const path = require('path');

const backendUrl = process.argv[2] || 'http://localhost:5001';

const htmlFiles = ['index.html', 'login.html', 'result.html'];

htmlFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // 替换所有 localhost:5001 为新的后端 URL
        content = content.replace(/http:\/\/localhost:5001/g, backendUrl);
        content = content.replace(/localhost:5001/g, backendUrl.replace(/^https?:\/\//, ''));
        
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✅ Updated ${file}`);
    } else {
        console.log(`⚠️  File not found: ${file}`);
    }
});

console.log(`\n✨ All API URLs updated to: ${backendUrl}`);

