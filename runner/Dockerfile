FROM ubuntu:22.04

# Don't ask for user input during install
ENV DEBIAN_FRONTEND=noninteractive

# Install the basics + docker repository prerequisites
RUN apt-get update && apt-get install -y \
    curl git jq sudo unzip ca-certificates \
    apt-transport-https gnupg lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI and Docker Compose plugin
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Create docker group (if not exists)
RUN groupadd -f docker

# Install Node.js 24 (matches the node24 runtime used by actions/checkout@v5 and newer actions)
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create a safe non-root user called "runner" and add to docker group
RUN useradd -m -s /bin/bash runner \
    && usermod -aG docker runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Download the GitHub Actions runner app
# v2.328.0+ is required for node24 support (used by actions/checkout@v5, etc.)
ENV RUNNER_VERSION=2.333.0
WORKDIR /home/runner

# Detect architecture and download the correct runner binary
RUN ARCH=$(uname -m) \
    && if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then RUNNER_ARCH="arm64"; else RUNNER_ARCH="x64"; fi \
    && echo ">>> Building for arch: $ARCH → runner arch: $RUNNER_ARCH" \
    && curl -fsSL -o runner.tar.gz \
    "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" \
    && tar xzf runner.tar.gz \
    && rm runner.tar.gz \
    && ./bin/installdependencies.sh \
    # Verify the key binary exists — fails the build immediately if arch was wrong
    && test -f ./bin/Runner.Listener || (echo "ERROR: Runner.Listener missing — wrong architecture downloaded!" && exit 1)

# Copy our startup script into the container
COPY start.sh /home/runner/start.sh
RUN chmod +x /home/runner/start.sh \
    && chown -R runner:runner /home/runner

# Switch to non-root user for security
USER runner

# When the container starts, run start.sh
ENTRYPOINT ["/home/runner/start.sh"]