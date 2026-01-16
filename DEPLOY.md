# Todo 应用部署指南

本文档详细介绍如何在本地和云端部署这个 Todo 应用。

---

## 🐳 Docker 一键部署（推荐）

这是最简单的部署方式，不需要手动安装 Python 或 PostgreSQL。

### 1. 安装 Docker
确保你的电脑或服务器已安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/) 或 Docker Engine。

### 2. 启动服务
```bash
docker-compose up -d
```

### 3. 访问应用
打开浏览器访问：http://localhost:8080

### 4. 停止服务
```bash
docker-compose down
```

---

## 📁 项目结构

```
TESTonline/
├── app.py              # Flask 应用主入口
├── models.py           # 数据库模型
├── requirements.txt    # Python 依赖
├── .gitignore          # Git 忽略文件
├── static/
│   ├── style.css       # 样式文件
│   └── script.js       # 前端交互
└── templates/
    └── index.html      # 主页面模板
```

---

## 🖥️ 本地运行

### 1. 安装 Python 依赖

```bash
cd /Users/mac/Desktop/小程序/TESTonline
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：**http://127.0.0.1:5000**

---

## ☁️ Railway 部署（平台即服务）

[Railway](https://railway.app) 是一个简单易用的平台即服务，支持一键部署。

### 步骤

1. **注册 Railway 账号**
   - 访问 https://railway.app 并使用 GitHub 登录

2. **创建新项目**
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 授权 Railway 访问你的 GitHub

3. **上传代码到 GitHub**
   ```bash
   cd /Users/mac/Desktop/小程序/TESTonline
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/todo-app.git
   git push -u origin main
   ```

4. **在 Railway 选择仓库**
   - 选择你刚创建的仓库
   - Railway 会自动检测 Python 项目并部署

5. **添加 PostgreSQL 数据库**
   - 在项目仪表板点击 "New" → "Database" → "PostgreSQL"
   - Railway 会自动设置 `DATABASE_URL` 环境变量

6. **配置启动命令**
   - 点击你的服务 → "Settings" → "Deploy"
   - 设置 Start Command: `gunicorn app:app`

7. **获取域名**
   - 点击 "Settings" → "Networking" → "Generate Domain"
   - 你的应用就可以通过公网访问了！

---

## 🌐 云服务器部署（阿里云/腾讯云）

### 前置条件

- 一台云服务器（推荐 Ubuntu 22.04）
- 服务器已安装 Python 3.8+
- 已配置安全组开放 80 端口

### 步骤

#### 1. 连接服务器

```bash
ssh root@你的服务器IP
```

#### 2. 安装系统依赖

```bash
apt update
apt install python3-pip python3-venv nginx -y
```

#### 3. 上传代码

将本地代码上传到服务器：
```bash
scp -r /Users/mac/Desktop/小程序/TESTonline root@你的服务器IP:/var/www/
```

#### 4. 创建虚拟环境并安装依赖

```bash
cd /var/www/TESTonline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. 测试运行

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

访问 `http://你的服务器IP:5000` 确认应用正常运行。

#### 6. 配置 Systemd 服务

创建服务文件：
```bash
nano /etc/systemd/system/todo.service
```

内容：
```ini
[Unit]
Description=Todo Flask App
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/TESTonline
Environment="PATH=/var/www/TESTonline/venv/bin"
ExecStart=/var/www/TESTonline/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
systemctl daemon-reload
systemctl start todo
systemctl enable todo
```

#### 7. 配置 Nginx 反向代理

创建 Nginx 配置：
```bash
nano /etc/nginx/sites-available/todo
```

内容：
```nginx
server {
    listen 80;
    server_name 你的域名或IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/TESTonline/static;
    }
}
```

启用配置：
```bash
ln -s /etc/nginx/sites-available/todo /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 8. 完成！

现在可以通过 `http://你的域名或IP` 访问应用了。

---

## 🔒 生产环境建议

1. **使用 PostgreSQL 替代 SQLite**
   ```bash
   export DATABASE_URL="postgresql://用户名:密码@主机:5432/数据库名"
   ```

2. **配置 HTTPS**
   - 使用 [Let's Encrypt](https://letsencrypt.org/) 免费 SSL 证书
   - 或使用云服务商的 CDN/SSL 服务

3. **设置环境变量**
   - 不要在代码中硬编码敏感信息
   - 使用 `.env` 文件管理配置

---

## 🆘 常见问题

### Q: 应用启动失败？
检查 Python 版本和依赖是否安装正确：
```bash
python3 --version
pip list
```

### Q: 数据库连接失败？
确保 `DATABASE_URL` 环境变量设置正确。

### Q: 端口被占用？
```bash
lsof -i :5000
kill -9 <PID>
```
