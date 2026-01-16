
请继续在 Workbench 中执行以下命令，完成最后一步！

## 🚀 第六步：配置 Nginx（最后一步）

```bash
# 1. 创建 Nginx 配置文件
cat <<EOF > /etc/nginx/conf.d/todo.conf
server {
    listen 80;
    server_name _;  # 监听所有域名/IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/TODO-app/static;
    }
}
EOF

# 2. 移除默认配置（如果有）
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak 2>/dev/null

# 3. 测试配置并重启 Nginx
nginx -t && systemctl restart nginx && systemctl enable nginx
```

---

## 🎉 恭喜！部署完成！

现在，请打开浏览器访问你的公网 IP：

👉 **http://8.141.85.192**

你应该能看到你的待办事项应用了！

如果有任何问题（比如打不开），请告诉我，可能需要检查阿里云的安全组设置。
