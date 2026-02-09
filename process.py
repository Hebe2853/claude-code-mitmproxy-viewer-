#!/usr/bin/env python3
"""
Process txt files in private-doc directory and convert delta data to JSON format.

This script traverses each folder under private-doc, reads each txt file,
and consolidates text_delta, thinking_delta, and input_json_delta into
complete entries, then writes to a JSON file with the same name.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any


def natural_sort_key(text: str) -> List:
    """Generate a key for natural sorting (e.g., req1, req2, ..., req10, req11).

    Args:
        text: String to generate sorting key for

    Returns:
        List with string and numeric parts for proper sorting
    """
    # Convert to string if Path object
    if isinstance(text, Path):
        text = text.name

    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]


def parse_delta_line(line: str) -> Dict[str, Any]:
    """Parse a single data line containing delta information.

    Args:
        line: A line from the txt file, e.g., "data: {...}"

    Returns:
        Parsed dictionary with type, index, delta info, or None if invalid.
    """
    line = line.strip()
    if not line.startswith("data: "):
        return None

    json_str = line[6:]  # Remove "data: " prefix
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError:
        return None


def consolidate_deltas(parsed_entries: List[Dict]) -> List[Dict[str, Any]]:
    """Consolidate delta entries by type and index.

    Args:
        parsed_entries: List of parsed delta entries with type, index, delta fields

    Returns:
        List of consolidated entries with type, content/delta fields
    """
    # Group by (delta_type, index)
    groups: Dict[tuple, List[Dict]] = {}

    for entry in parsed_entries:
        delta = entry.get("delta", {})
        delta_type = delta.get("type")
        index = entry.get("index", 0)

        if delta_type is None:
            continue

        key = (delta_type, index)
        if key not in groups:
            groups[key] = []
        groups[key].append(delta)

    result = []

    # Process text_delta - consolidate text content
    for (delta_type, index), deltas in sorted(groups.items(),reverse=True):
        if delta_type == "text_delta":
            content = ""
            for delta in deltas:
                content += delta.get("text", "")
            result.append({
                "type": "text",
                "content": content
            })

        elif delta_type == "thinking_delta":
            content = ""
            for delta in deltas:
                content += delta.get("thinking", "")
            result.append({
                "type": "thinking",
                "content": content
            })

        elif delta_type == "input_json_delta":
            # For input_json_delta, include the full delta structure
            for delta in deltas:
                result.append({
                    "type": "tool_use",
                    "delta": delta
                })

    return result


def process_txt_file(txt_path: Path) -> bool:
    """Process a single txt file and generate corresponding JSON.

    Args:
        txt_path: Path to the txt file

    Returns:
        True if successful, False otherwise
    """
    parsed_entries = []

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                parsed = parse_delta_line(line)
                if parsed:
                    parsed_entries.append(parsed)
    except Exception as e:
        print(f"Error reading {txt_path}: {e}")
        return False

    if not parsed_entries:
        print(f"No valid data found in {txt_path}")
        return False

    consolidated = consolidate_deltas(parsed_entries)

    # Write to JSON file with same name
    json_path = txt_path.with_suffix(".json")
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(consolidated, f, ensure_ascii=False, indent=2)
        print(f"Created: {json_path}")
        return True
    except Exception as e:
        print(f"Error writing {json_path}: {e}")
        return False


def process_directory(base_dir: Path) -> Dict[str, int]:
    """Process all txt files in subdirectories of base_dir.

    Args:
        base_dir: Base directory containing subdirectories with txt files

    Returns:
        Statistics dict with success, failure, skip counts
    """
    stats = {"success": 0, "failure": 0, "skip": 0}

    # Get all subdirectories (步骤1, 步骤2, etc.)
    subdirs = [d for d in base_dir.iterdir() if d.is_dir()]

    for subdir in subdirs:
        print(f"\nProcessing {subdir.name}/")
        txt_files = list(subdir.glob("*.txt"))

        # Sort using natural sort for proper req1, req2, ..., req10 ordering
        txt_files.sort(key=natural_sort_key)

        for txt_file in txt_files:

            if process_txt_file(txt_file):
                stats["success"] += 1
            else:
                stats["failure"] += 1

    return stats


def merge_folder_jsons(base_dir: Path, output_filename: str = "merged.json") -> bool:
    """Read all JSON files in each subfolder and merge into a single list.

    Traverses each folder under base_dir, reads all JSON files in each folder,
    combines them into a single list, and writes to a new JSON file at base_dir.

    Args:
        base_dir: Base directory containing subdirectories with JSON files
        output_filename: Name of the output JSON file (default: "merged.json")

    Returns:
        True if successful, False otherwise
    """
    merged_data = {}

    # Get all subdirectories (步骤1, 步骤2, etc.)
    subdirs = [d for d in base_dir.iterdir() if d.is_dir()]

    for subdir in sorted(subdirs, key=natural_sort_key):
        print(f"\nProcessing {subdir.name}/")
        json_files = list(subdir.glob("*.json"))
        merged_data_sub = []

        # Sort using natural sort for proper req1, req2, ..., req10 ordering
        json_files.sort(key=natural_sort_key)
        user_input = open(f"{subdir}/user.txt").read().strip() if (subdir / "user.txt").exists() else ""
        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data_sub.append(data)
                    else:
                        # If single object, wrap in list
                        merged_data_sub.append(data)
                print(f"  Read: {json_file.name} ({len(data) if isinstance(data, list) else 1} entries)")
            except Exception as e:
                print(f"  Error reading {json_file.name}: {e}")
                continue
        merged_data[user_input] = merged_data_sub

    # Write merged data to output file
    output_path = base_dir / output_filename
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print(f"\n" + "=" * 50)
        print(f"Created merged file: {output_path}")
        print(f"Total entries: {len(merged_data)}")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}")
        return False


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    base_dir = script_dir

    print("Available operations:")
    print("1. Convert txt files to JSON")
    print("2. Merge all JSON files in subfolders")
    print("=" * 50)

    choice = input("Select operation (1/2): ").strip()

    if choice == "1":
        print(f"\nProcessing txt files in: {base_dir}")
        print("=" * 50)

        stats = process_directory(base_dir)

        print("\n" + "=" * 50)
        print("Summary:")
        print(f"  Success: {stats['success']}")
        print(f"  Failure: {stats['failure']}")
        print("=" * 50)

    elif choice == "2":
        print(f"\nMerging JSON files in: {base_dir}")
        print("=" * 50)

        output_name = input("Output filename (default: merged.json): ").strip()
        if not output_name:
            output_name = "merged.json"

        if not output_name.endswith(".json"):
            output_name += ".json"

        merge_folder_jsons(base_dir, output_name)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
