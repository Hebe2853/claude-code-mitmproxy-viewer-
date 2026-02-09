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

## Usage

### Process TXT Files to JSON

```bash
python process.py
# Select option 1: Convert txt files to JSON
```

This processes all `.txt` files in subdirectories (步骤1-5) and creates corresponding `.json` files.

### Merge JSON Files

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

### View Data

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
