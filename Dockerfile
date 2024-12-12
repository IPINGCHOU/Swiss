# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    zsh \
    git \
    curl \
    unzip

# Create a vscode user with Zsh as the default shell
RUN useradd -m -s /bin/zsh vscode

# Install system-wide tools as root
USER root
RUN pip install --no-cache-dir poetry==1.7.1 && \
    mkdir -p /home/vscode/.local/bin && \
    chown -R vscode:vscode /home/vscode/.local

RUN poetry config virtualenvs.in-project true

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Add build arguments
ARG GIT_USER_EMAIL
ARG GIT_USER_NAME

# Switch to the vscode user
USER vscode
WORKDIR /home/vscode

# Install Oh My Zsh and plugins
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /home/vscode/.oh-my-zsh/custom/themes/powerlevel10k && \
    git clone https://github.com/zsh-users/zsh-autosuggestions /home/vscode/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /home/vscode/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
    echo "source /home/vscode/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> /home/vscode/.zshrc && \
    echo "source /home/vscode/.oh-my-zsh/custom/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh" >> /home/vscode/.zshrc && \
    echo "ZSH_THEME=\"powerlevel10k/powerlevel10k\"" >> /home/vscode/.zshrc && \
    echo "plugins=(git zsh-autosuggestions zsh-syntax-highlighting)" >> /home/vscode/.zshrc

# Add poetry to PATH and configure
ENV PATH="/home/vscode/.local/bin:$PATH"

# Copy project files
COPY --chown=vscode:vscode pyproject.toml ./

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Configure Git globally if credentials are provided
RUN if [ ! -z "$GIT_USER_EMAIL" ] && [ ! -z "$GIT_USER_NAME" ]; then \
    git config --global user.email "${GIT_USER_EMAIL}" && \
    git config --global user.name "${GIT_USER_NAME}"; \
    fi

# Command to run when the container starts
CMD ["zsh"]