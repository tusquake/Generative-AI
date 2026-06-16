FROM python:3.11-alpine

WORKDIR /workspace

# Install common testing utilities
RUN pip install --no-cache-dir pytest requests pydantic httpx

# Disable standard python file buffering
ENV PYTHONUNBUFFERED=1

CMD ["sh"]
