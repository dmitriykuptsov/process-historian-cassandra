#!/usr/bin/env bash

set -e

echo "🔄 Updating system..."
sudo apt update -y

echo "📦 Installing required packages..."
sudo apt install -y ca-certificates curl gnupg

echo "🔐 Adding Docker GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "📦 Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "🔄 Updating package list..."
sudo apt update -y

echo "🐳 Installing Docker Engine + Compose plugin..."
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "🚀 Enabling Docker..."
sudo systemctl enable docker
sudo systemctl start docker

echo "👤 Adding current user to docker group..."
sudo usermod -aG docker $USER

echo "✅ Installation complete!"
echo "⚠️ IMPORTANT: Log out and back in (or run: newgrp docker)"
echo "👉 Test with: docker compose version"
