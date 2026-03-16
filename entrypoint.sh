#!/bin/sh

# Configure Ollama server binding in a Docker-friendly way.
# Ollama uses OLLAMA_HOST, not --host/--port flags.
: "${OLLAMA_HOST:=0.0.0.0:11434}"

# Start the Ollama server in the background so the CLI can talk to it.
ollama serve &

# Wait for the server to accept connections.
# We use a small retry loop because the server can take a moment to start.
for i in 1 2 3 4 5; do
  if ollama list >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

# Ensure the required models are available.
# If the model is already present, `ollama pull` is a no-op.
ollama pull ibm/granite-docling:258m || true
ollama pull ibm/granite3.3-vision:2b || true

# Wait for the server process so the container stays running.
wait
