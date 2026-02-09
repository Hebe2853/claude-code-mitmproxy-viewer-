# Claude Delta Viewer

A tool for processing and visualizing Claude AI conversation streams captured via mitmproxy.

## Features

- **Process SSE Delta Events**: Converts raw SSE streams with `text_delta`, `thinking_delta`, and `input_json_delta` events into structured JSON
- **Merge Multiple Conversations**: Combine conversation data from multiple folders into a single JSON file
- **Interactive HTML Viewer**: Beautiful dark-themed viewer with collapsible 3-level hierarchy (Keys → Lists → Entries)
- **Filter & Search**: Filter by entry type (Text/Thinking/Tool Use) and search across all content
- **Markdown & Code Highlighting**: Automatic markdown rendering and syntax highlighting for code blocks

## Project Structure

```
├── process.py          # Main processing script
├── viewer.html         # Interactive data viewer
├── merged.json         # Output merged data (generated)
├── 步骤1/              # Source data folders
├── 步骤2/
├── 步骤3/
├── 步骤4/
└── 步骤5/
```

## Prerequisites

### mitmproxy Installation & Setup

> **TODO:** Add mitmproxy installation and configuration instructions here.

<!-- MITMPROXY SETUP START -->
<!--
Example sections to add:

#### Installation

```bash
# macOS
brew install mitmproxy

# Linux
pip install mitmproxy

# Windows
choco install mitmproxy
```

#### Configuration

1. Start mitmproxy:
   ```bash
   mitmproxy
   # or mitmweb for web UI
   ```

2. Install CA certificate (https://mitm.it)

3. Configure browser/system proxy to 127.0.0.1:8080

4. Add custom addon script to capture Claude API streams (TODO: provide example)

#### Capturing Claude Conversations

1. Start mitmproxy with your addon
2. Use Claude AI while proxy is active
3. Save captured streams to txt files in project folders
-->
<!-- MITMPROXY SETUP END -->

## Usage

### 1. Capture Data with mitmproxy

> **TODO:** Add detailed steps for capturing Claude API streams

<!-- CAPTURE STEPS START -->
<!--
1. Start mitmproxy with Claude stream capture addon
2. Organize captured streams into subdirectories (步骤1/, 步骤2/, etc.)
3. Save each conversation as a separate .txt file
-->
<!-- CAPTURE STEPS END -->

### 2. Process TXT Files to JSON

```bash
python process.py
# Select option 1: Convert txt files to JSON
```

This processes all `.txt` files in subdirectories (步骤1-5) and creates corresponding `.json` files.

### 3. Merge JSON Files

```bash
python process.py
# Select option 2: Merge all JSON files in subfolders
```

This merges all JSON files into a single `merged.json` file with the structure:

```json
{
  "步骤1": [
    [
      {"type": "thinking", "content": "..."},
      {"type": "text", "content": "..."},
      {"type": "tool_use", "delta": {...}}
    ],
    [...]
  ],
  "步骤2": [...]
}
```

### 4. View Data

Open `viewer.html` in a browser and select `merged.json` to visualize the data.

## Data Format

### Input (TXT Files)

Raw SSE event streams:
```
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "..."}}
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "..."}}
```

### Output (JSON Files)

Consolidated entries:
```json
[
  {"type": "thinking", "content": "..."},
  {"type": "text", "content": "..."},
  {"type": "tool_use", "delta": {"type": "input_json_delta", "partial_json": "..."}}
]
```

## Viewer Features

- **3-Level Hierarchy**:
  - Level 1: Key blocks (e.g., "步骤1", "步骤2") - Blue header
  - Level 2: List blocks - Gray header
  - Level 3: Entry blocks - Type badges (Text/Thinking/Tool Use)

- **Entry Types**:
  - `text`: Rendered with markdown support
  - `thinking`: Italicized with purple accent
  - `tool_use`: Formatted JSON with syntax highlighting

## Requirements

- Python 3.7+
- Modern web browser (for viewer)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
