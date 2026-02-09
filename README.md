# Claude Code Reverse Proxy Analysis

This project demonstrates how to set up a reverse proxy for Claude Code, capture actual API requests/responses, and analyze Claude Code's internal system prompts and workflow.

> **⚠️ Disclaimer**: This is an educational/research project for understanding how AI coding assistants work internally. Please respect Anthropic's Terms of Service.

## Background

Claude Code is Anthropic's AI-powered coding assistant. By setting up a reverse proxy with mitmproxy, we can:

1. **Intercept and inspect** the actual API requests and responses
2. **Analyze system prompts** that guide Claude's behavior
3. **Understand the workflow** of how Claude processes coding tasks
4. **Study delta streaming** for real-time token generation

## Project Structure

```
claude-code-mitmproxy-viewer/
├── addons/
│   └── claude_capture.py    # mitmproxy addon for capturing streams
├── process.py                # Process raw SSE streams to JSON
├── viewer.html               # Interactive data viewer
├── merged.json              # Merged output (generated)
├── 分析步骤设计.md           # Analysis workflow design (Chinese)
├── 步骤1/                   # Captured conversations - Step 1
├── 步骤2/                   # Captured conversations - Step 2
├── 步骤3/                   # Captured conversations - Step 3
├── 步骤4/                   # Captured conversations - Step 4
└── 步骤5/                   # Captured conversations - Step 5
```

## Quick Start

### 1. Install mitmproxy

```bash
# macOS
brew install mitmproxy

# Linux
pip install mitmproxy

# Windows
choco install mitmproxy
```

### 2. Configure mitmproxy Addon

Create `addons/claude_capture.py`:

```python
#!/usr/bin/env python3
"""
mitmproxy addon to capture Claude API streaming responses.
"""

from mitmproxy import http
import json
import os
from pathlib import Path

class ClaudeCapture:
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "步骤1"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.file_counter = 0

    def request(self, flow: http.HTTPFlow) -> None:
        # Check if this is a Claude API request
        if "antrpc.com" in flow.request.pretty_host or "claude.ai" in flow.request.pretty_host:
            # Log request details
            print(f"[REQUEST] {flow.request.method} {flow.request.path}")

    def response(self, flow: http.HTTPFlow) -> None:
        # Capture streaming responses
        if "antrpc.com" in flow.request.pretty_host:
            content = flow.response.text
            if content and "data:" in content:
                # Save to file
                output_file = self.output_dir / f"req{self.file_counter + 1}.txt"
                output_file.write_text(content)
                self.file_counter += 1
                print(f"[CAPTURED] Saved to {output_file.name}")

addons = [ClaudeCapture()]
```

### 3. Start mitmproxy

```bash
# Start with the addon
mitmproxy -s addons/claude_capture.py -p 8080

# Or use mitmweb for web interface
mitmweb -s addons/claude_capture.py -p 8080
```

### 4. Configure Proxy

1. **Install CA Certificate**: Visit https://mitm.it and install the certificate
2. **Configure System Proxy**: Set to `127.0.0.1:8080`
3. **Configure Claude Code**:
   ```bash
   export HTTPS_PROXY=http://127.0.0.1:8080
   export HTTP_PROXY=http://127.0.0.1:8080
   ```

### 5. Use Claude Code

Run Claude Code while mitmproxy is active. The addon will automatically capture streaming responses to the `步骤1/` folder.

## Processing Captured Data

### Convert SSE Streams to JSON

```bash
python process.py
# Select option 1
```

This processes raw SSE streams into structured JSON:

```json
[
  {"type": "thinking", "content": "User wants to..."},
  {"type": "text", "content": "I'll help you..."},
  {"type": "tool_use", "delta": {"type": "input_json_delta", ...}}
]
```

### Merge All Conversations

```bash
python process.py
# Select option 2
```

Merges all JSON files into `merged.json`:

```json
{
  "步骤1": [[...], [...]],
  "步骤2": [[...], [...]]
}
```

### View in Browser

Open `viewer.html` and select `merged.json` for interactive visualization.

## Delta Event Types

| Type | Description |
|------|-------------|
| `text_delta` | Text content tokens |
| `thinking_delta` | Internal reasoning tokens |
| `input_json_delta` | Tool use parameters (partial JSON) |

## Analysis Workflow

Following [分析步骤设计.md](分析步骤设计.md), this project organizes captures into steps:

- **步骤1**: Basic conversation capture
- **步骤2**: Multi-turn conversations
- **步骤3**: Code execution scenarios
- **步骤4**: File operations
- **步骤5**: Complex workflows

Each step helps understand different aspects of Claude Code's behavior.

## Viewer Features

- **3-Level Hierarchy**: Steps → Conversations → Entries
- **Type Filtering**: Filter by Text/Thinking/Tool Use
- **Full-text Search**: Search across all content
- **Markdown Rendering**: Automatic formatting
- **Code Highlighting**: Syntax highlighting for code blocks
- **JSON Inspection**: Formatted display of tool use data

## Learnings

By analyzing the captured data, you can observe:

1. **System Prompts**: How Claude is instructed to behave
2. **Tool Definitions**: Available tools and their schemas
3. **Thinking Patterns**: Internal reasoning before responses
4. **Delta Streaming**: How tokens are streamed in real-time
5. **Multi-step Reasoning**: How Claude plans and executes tasks

## Requirements

- Python 3.7+
- mitmproxy
- Modern web browser

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [mitmproxy Documentation](https://docs.mitmproxy.org/)
- [Anthropic API Documentation](https://docs.anthropic.com/)
