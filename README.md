# Agent MCP

Create a LLM Agent using a local MCP as tools. Both the MCP and the Agent are available through a single API.

## Usage

1. **Build the Docker image**:
   ```bash
   make build
   ```

2. **Run the Docker container**:
   ```bash
   docker run --rm -it \
         -p 8000:8000 \
         -e OPENAI_API_KEY=<your_openai_api_key> \
         -e HOST=0.0.0.0 \
         agent-mcp
   ```

3. **Access the API**:
    - The API will be available at `http://localhost:8000`.

    Example:
    ```bash
    curl -X POST http://localhost:8000/v1/response \
        -H "Content-Type: application/json" \
        -d '{"input":"what do people think about the second most featured product ?"}'
    ```
