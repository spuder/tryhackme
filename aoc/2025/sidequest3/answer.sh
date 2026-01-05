#!/bin/bash

# Prompt for MACHINE_IP if not defined
if [ -z "$MACHINE_IP" ]; then
    read -p "Enter MACHINE_IP: " MACHINE_IP
fi

# Prompt for ATTACKER_IP if not defined
if [ -z "$ATTACKER_IP" ]; then
    read -p "Enter ATTACKER_IP: " ATTACKER_IP
fi

# Add entries to /etc/hosts
echo "Adding entries to /etc/hosts..."
sudo bash -c "cat >> /etc/hosts << EOF
$MACHINE_IP     dns-manager.hopaitech.thm
$MACHINE_IP     ns1.hopaitech.thm
$MACHINE_IP     ticketing-system.hopaitech.thm
$MACHINE_IP     url-analyzer.hopaitech.thm
EOF"

# Check if /etc/resolv.conf is a symlink
if [ -L /etc/resolv.conf ]; then
    echo "/etc/resolv.conf is a symlink, removing it..."
    sudo rm /etc/resolv.conf
fi

# Create new /etc/resolv.conf with proper permissions
echo "Configuring /etc/resolv.conf..."
sudo bash -c "echo 'nameserver $MACHINE_IP' > /etc/resolv.conf"
sudo bash -c "echo 'search hopaitech.thm' >> /etc/resolv.conf"
sudo bash -c "echo 'nameserver 1.1.1.1      # fallback public DNS' >> /etc/resolv.conf"
sudo bash -c "echo 'nameserver 8.8.8.8      # extra fallback' >> /etc/resolv.conf"
sudo chmod 644 /etc/resolv.conf

echo "Configuration complete!"
