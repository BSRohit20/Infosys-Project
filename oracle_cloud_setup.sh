#!/bin/bash

# Update packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv nginx

# Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up systemd service
cat > infosys.service << EOF
[Unit]
Description=Infosys Application
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)/app
ExecStart=$(pwd)/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo mv infosys.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start infosys
sudo systemctl enable infosys

# Configure Nginx as a reverse proxy
cat > nginx_config << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo mv nginx_config /etc/nginx/sites-available/infosys
sudo ln -s /etc/nginx/sites-available/infosys /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
