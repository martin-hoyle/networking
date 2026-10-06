#!/bin/bash
set -e

echo
echo "Gathering user information..."
echo
read -p "Enter your Git username: " git_username
read -p "Enter your Git email: " git_email
echo

read -p "Use default Python directory ~/develop/python? [Y/n]: " answer

if [ "$answer" = "Y" ]; then
    python_dir="$HOME/develop/python"
else
    read -p "Enter Python directory: " python_dir
fi

echo
echo "Generate an ED25519 key"

sleep 5

ssh-keygen -t ed25519 -C "$git_email"

eval "$(ssh-agent -s)"
# Add your key:
ssh-add ~/.ssh/id_ed25519
# Your public key is:
cat ~/.ssh/id_ed25519.pub

echo
echo "Installing essential packages..."
echo
sleep 5

sudo dnf update -y

sudo dnf install -y \
  wireshark \
  wireshark-cli \
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
  bind-utils \
  traceroute \
  mtr \
  tcpdump \
  openssh-clients \
  sshpass \
  python3 \
  python3-pip \
  python3-devel \
  pipx \
  gcc \
  gcc-c++ \
  make \
  ca-certificates \
  gnupg2 \
  netcat \
  socat \
  whois \
  telnet \
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

# Check:
git config --list

sleep 5

echo
echo "Installing VS Code"
echo

sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

sudo tee /etc/yum.repos.d/vscode.repo > /dev/null <<'EOF'
[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
autorefresh=1
type=rpm-md
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
EOF

sudo dnf check-update || true
sudo dnf install -y code

sleep 5

echo
echo "Installing useful VS Code addons"
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

# For your particular background:
code --install-extension esphome.esphome-vscode

echo
echo "Installing Docker"
echo

sleep 5

sudo dnf -y install dnf-plugins-core

sudo dnf config-manager \
  --add-repo \
  https://download.docker.com/linux/rhel/docker-ce.repo

sudo dnf install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

# Allow your normal user to use Docker
sudo usermod -aG docker "$USER"

# Enable and start Docker
sudo systemctl enable --now docker

echo
echo "Docker installed."
echo "Log out and back in before running Docker without sudo."

sleep 5

echo
echo "Setting up ~/develop/python with venv"
echo

sleep 5

pipx ensurepath

pipx install ansible

export PATH="$HOME/.local/bin:$PATH"

mkdir -p "$python_dir"
cd "$python_dir"

#mkdir -p ~/develop/python

#cd ~/develop/python

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
echo "Installing HashiCorp's official repository"
echo

sleep 5

sudo dnf config-manager \
  --add-repo \
  https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo

sudo dnf install -y terraform

terraform version

sleep 5

echo
echo "Installing kubectl"
echo

sleep 5

cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo > /dev/null
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.34/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.34/rpm/repodata/repomd.xml.key
EOF

sudo dnf install -y kubectl

# Check:
kubectl version --client

echo
echo "Installing Helm"
echo

sleep 5

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
  | bash

# Check:
helm version

echo
echo "Running Autoremove"
echo

sleep 5

sudo dnf autoremove -y

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
echo "Ansible"
ansible --version

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
echo "Pipx packages"
pipx list

echo
echo "Git configuration"
git config --list
```
