#!/bin/bash
set -e

echo
echo "Gathering user information..."
echo
read -p "Enter your Git username: " git_username
read -p "Enter your Git email: " git_email


echo "Generate an ED25519 key"

sleep 5

ssh-keygen -t ed25519 -C "$git_email"

eval "$(ssh-agent -s)"
#Add your key:
ssh-add ~/.ssh/id_ed25519
#Your public key is:
cat ~/.ssh/id_ed25519.pub


echo
echo "Installing essential packages..."
echo
sleep 5

sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  wireshark \
  tshark \
  nmap \
  iperf3 \
  git \
  curl \
  wget \
  unzip \
  zip \
  jq \
  tree \
  vim \
  nano \
  tmux \
  htop \
  ncdu \
  net-tools \
  dnsutils \
  traceroute \
  mtr \
  tcpdump \
  openssh-client \
  sshpass \
  python3 \
  python3-pip \
  python3-venv \
  pipx \
  build-essential \
  ca-certificates \
  gnupg \
  lsb-release \
  software-properties-common \
  apt-transport-https \
  netcat-openbsd \
  socat \
  whois \
  telnet \
  vlan \
  bridge-utils

echo
echo "Setting up Git"
echo
sleep 5

git config --global user.name "$git_username"
git config --global user.email "$git_email"
git config --global core.editor "code --wait"
git config --global core.autocrlf input
git config --global init.defaultBranch main
git config --global pull.rebase false
#Check:
git config --list
   
sleep 5

echo
echo "Installing VS Code"
echo

wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/packages.microsoft.gpg > /dev/null

echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
  | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null


sudo apt update
sudo apt install -y code

sleep 5

echo
echo "Installing usfull VS addons"
echo

code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-azuretools.vscode-docker
code --install-extension redhat.vscode-yaml
code --install-extension eamodio.gitlens
code --install-extension ms-python.python
code --install-extension redhat.ansible
code --install-extension hashicorp.terraform
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension timonwong.shellcheck
#For your particular background, I'd also add:
code --install-extension esphome.esphome-vscode

echo "Installing Docker"

sleep 5

sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/keyrings/docker.gpg

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


# Allow your normal user to use Docker
sudo usermod -aG docker $USER

# Restart Docker
sudo systemctl restart docker

# Test Docker
#docker run hello-world

echo
echo "Docker installed."
echo "Log out and back in before running Docker without sudo."

sleep 5

echo
echo "Setting up ~/develop/python with venv"
echo

sleep 5

sudo apt install -y pipx
pipx ensurepath

pipx install ansible

export PATH="$HOME/.local/bin:$PATH"

mkdir -p ~/develop/python

cd ~/develop/python
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

pip install \
  requests \
  pyyaml \
  jinja2 \
  netmiko \
  paramiko \
  napalm

sleep 5

echo
echo "Install HashiCorp's official repository"
echo

sleep 5

wget -O- https://apt.releases.hashicorp.com/gpg \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update
sudo apt install -y terraform

terraform version

sleep 5

echo
echo "installing kubectl"
echo

sleep 5

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key \
  | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /' \
  | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update
sudo apt install -y kubectl
#Check:
kubectl version --client

echo
echo "Installing Helm"
echo

sleep 5

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
  | bash
#Check:
#helm version

echo
echo "Running Autoremove"
echo
sleep 5

sudo apt autoremove -y

echo
echo "Gathering Version information"
echo

echo "Git"
git --version
echo
echo "Docker"
docker --version
echo
echo "Docker Compose"
docker compose version
echo
echo "Python"
python3 --version
echo
#echo "Ansible"
#ansible --version
echo
echo "Terraform"
terraform version
echo
echo "Kubectl"
kubectl version --client
echo
echo "Helm"
helm version
echo
echo "SSH"
ssh -V
echo
echo "Nmap"
nmap --version
echo
echo
echo "Pipx packages"
pipx list
echo
echo
echo "Git configuration"
git config --list
