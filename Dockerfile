# Use a lightweight Python base image
FROM python:3.14-slim

# Copy the pre-compiled uv binary from Astral's official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency management files first (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures the lockfile is strictly respected
# --no-dev ensures testing tools like pytest are omitted from production
RUN uv sync --frozen --no-dev

# Copy the rest of the application code
COPY app ./app

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]