# syntax=docker/dockerfile:1

# Base image provided by Ollama that already includes the Ollama CLI and runtime.
FROM ollama/ollama:latest

# Provide a simple entrypoint that starts the Ollama server and then
# pulls required models (if missing) before keeping the server running.
#
# This avoids build-time `ollama pull` failures (which require a running server)
# while still ensuring the container is ready to serve with the desired models.

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 11434

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
