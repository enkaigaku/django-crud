# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy uv configuration files
WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen: Sync with uv.lock
# --no-dev: Do not install dev dependencies
# --no-install-project: Do not install the project itself yet
RUN uv sync --frozen --no-dev --no-install-project

# Final stage
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start the application with Gunicorn
CMD ["gunicorn", "dvd_rental.wsgi:application", "--bind", "0.0.0.0:8000"]
