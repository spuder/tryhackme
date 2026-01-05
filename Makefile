# Makefile to manage the Parrot Security container environment using Apple's 'container' command

# Define the container command for the new Apple 'container' tool
CONTAINER_CMD = container
IMAGE_NAME = parrotsec/security
CONTAINER_NAME = parrot-security

# Phony target to avoid conflicts with a file named 'kali'
.PHONY: kali all stop clean

# Default target
all: kali

# Main target to set up the Kali Linux container
kali:
	@echo "\033[0;32m--- Checking for $(CONTAINER_CMD) command ---\033[0m"
	@if ! command -v $(CONTAINER_CMD) >/dev/null; then \
		echo "Error: '$(CONTAINER_CMD)' command not found."; \
		echo "Please ensure the new Apple container runtime is installed and in your PATH."; \
		exit 1; \
	fi
	@echo "'$(CONTAINER_CMD)' is installed."

	@echo "\n\033[0;32m--- Checking if $(CONTAINER_CMD) system is running ---\033[0m"
	@if ! $(CONTAINER_CMD) system status >/dev/null 2>&1; then \
		echo "Warning: '$(CONTAINER_CMD)' system is not running. Attempting to start it..."; \
		$(CONTAINER_CMD) system start; \
		echo "Waiting for the system to initialize..."; \
		while ! $(CONTAINER_CMD) system status >/dev/null 2>&1; do \
			sleep 5; \
		done; \
		echo "'$(CONTAINER_CMD)' system started successfully."; \
	else \
		echo "'$(CONTAINER_CMD)' system is already running."; \
	fi

	@echo "\n\033[0;32m--- Pulling $(IMAGE_NAME) image ---\033[0m"
	@$(CONTAINER_CMD) image pull $(IMAGE_NAME)

	@echo "\n\033[0;32m--- Checking for running $(CONTAINER_NAME) container ---\033[0m"
	@if $(CONTAINER_CMD) list --quiet | grep -q "^$(CONTAINER_NAME)$$"; then \
		echo "Container '$(CONTAINER_NAME)' is already running."; \
	elif $(CONTAINER_CMD) list --all --quiet | grep -q "^$(CONTAINER_NAME)$$"; then \
		echo "Found a stopped container. Starting it..."; \
		$(CONTAINER_CMD) start $(CONTAINER_NAME); \
	else \
		echo "No existing container found. Creating and starting a new one..."; \
		$(CONTAINER_CMD) run -dt --name $(CONTAINER_NAME) \
			--network host \
			-v $(PWD):/workspace \
			-w /workspace \
			$(IMAGE_NAME); \
	fi

	@echo "\n\033[0;32m--------------------------------------------------\033[0m"
	@echo "\033[0;32mSetup complete.\033[0m"
	@echo "To open a shell in the running container, use the command:"
	@echo "  $(CONTAINER_CMD) exec -it $(CONTAINER_NAME) /bin/bash"
	@echo "\033[0;32m--------------------------------------------------\033[0m"

# Target to stop the container
stop:
	@echo "\033[0;32m--- Stopping container '$(CONTAINER_NAME)' ---\033[0m"
	@$(CONTAINER_CMD) stop $(CONTAINER_NAME)

# Target to remove the container
clean:
	@echo "\033[0;32m--- Removing container '$(CONTAINER_NAME)' ---\033[0m"
	@$(CONTAINER_CMD) delete $(CONTAINER_NAME)
