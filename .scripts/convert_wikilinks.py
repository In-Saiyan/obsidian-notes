#!/usr/bin/env python3
"""Convert Obsidian wiki-links to standard Markdown links for Gitea compatibility.

Handles:
  ![[image.png]]                → ![](relative/path/to/image.png)
  [[#Heading]]                  → [Heading](#heading-slug)
  [[File]]                      → [File](<File.md>)  (or File.ext if not .md)
  [[File|Display]]              → [Display](<File.md>)
  [[File#Section|Display]]      → [Display](<File.md#section-slug>)
  [[File#Section]]              → [File > Section](<File.md#section-slug>)
  [[path/File|Display]]         → [Display](<path/File.md>)
"""

import os
import re
import sys
from pathlib import Path

VAULT = Path("/home/user/opt/obsidian-notes")
EXCLUDE = {".obsidian", ".git", "node_modules"}

# ---------- helpers ----------

def heading_slug(text: str) -> str:
    """GitHub / Gitea heading anchor: lowercase, strip non-alphanum/space/hyphen, spaces → hyphens."""
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)   # keep alphanumerics, underscores, whitespace, hyphens
    slug = slug.strip()
    slug = re.sub(r"\s+", "-", slug)
    return slug


def find_all_files(vault: Path) -> dict[str, Path]:
    """Build a name→path index for the entire vault (basename without extension → path)."""
    index: dict[str, Path] = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for f in files:
            p = Path(root) / f
            stem = p.stem           # e.g. "Pasted image 20250617043830"
            full = p.name           # e.g. "Pasted image 20250617043830.png"
            # Prefer first hit (closest to root) but images are unique enough
            if stem not in index:
                index[stem] = p
            if full not in index:
                index[full] = p
    return index


def relative_link(from_file: Path, to_file: Path) -> str:
    """Compute a relative path string from from_file's directory to to_file."""
    try:
        rel = os.path.relpath(to_file, from_file.parent)
    except ValueError:
        rel = str(to_file)
    # Normalise to forward slashes
    rel = rel.replace("\\", "/")
    return rel


def url_encode_path(path_str: str) -> str:
    """Percent-encode spaces (the main issue) in a path."""
    return path_str.replace(" ", "%20")


def needs_angle_brackets(path_str: str) -> bool:
    """Check if path contains spaces/special chars that need angle brackets."""
    return " " in path_str


# ---------- conversion ----------

FILE_INDEX: dict[str, Path] = {}


def resolve_target(name: str, from_file: Path) -> str | None:
    """Resolve an Obsidian link target name to a relative path string.
    
    `name` might be:
      - A bare filename:  "Basics"
      - A path:           "Special Design Patterns/Specification Design Pattern"
    """
    # If it looks like a path (has /)
    if "/" in name:
        # Try resolving relative to from_file's directory first
        candidate = from_file.parent / (name + ".md")
        if candidate.exists():
            return relative_link(from_file, candidate)
        candidate = from_file.parent / name
        if candidate.exists():
            return relative_link(from_file, candidate)

    # Try the global index
    if name in FILE_INDEX:
        return relative_link(from_file, FILE_INDEX[name])

    # Try adding .md
    if name + ".md" in FILE_INDEX:
        return relative_link(from_file, FILE_INDEX[name + ".md"])

    # Check if it's a file with extension (image, etc.)
    for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf"]:
        full = name + ext
        if full in FILE_INDEX:
            return relative_link(from_file, FILE_INDEX[full])

    return None


def convert_wikilink(match: re.Match, from_file: Path) -> str:
    """Convert a single [[...]] or ![[...]] match."""
    full = match.group(0)
    is_embed = full.startswith("!")
    inner = match.group(1)  # content between [[ and ]]

    # --- Same-file heading link: [[#Heading]] ---
    if inner.startswith("#"):
        heading_text = inner[1:]
        slug = heading_slug(heading_text)
        return f"[{heading_text}](#{slug})"

    # --- Split into target and display ---
    # Possible forms: File, File|Display, File#Section, File#Section|Display
    display = None
    section = None

    if "|" in inner:
        target_part, display = inner.split("|", 1)
    else:
        target_part = inner

    if "#" in target_part:
        file_part, section = target_part.split("#", 1)
    else:
        file_part = target_part

    # --- Image embeds: ![[image.png]] ---
    if is_embed:
        # file_part is the full image name (e.g. "Pasted image 20260301145211.png")
        rel = resolve_target(file_part, from_file)
        if rel:
            encoded = url_encode_path(rel)
            alt = display or ""
            return f"![{alt}]({encoded})"
        else:
            # Can't resolve; leave a comment-style reference
            encoded = url_encode_path(file_part)
            return f"![{display or ''}]({encoded})"

    # --- File link ---
    if file_part:
        rel = resolve_target(file_part, from_file)
        if rel is None:
            # Best effort: assume sibling .md file
            if "." not in file_part:
                rel = file_part + ".md"
            else:
                rel = file_part

        link = url_encode_path(rel)
        if section:
            link += "#" + heading_slug(section)

        if display is None:
            if section:
                display = f"{file_part} > {section}"
            else:
                display = file_part

        # Use angle brackets if path has spaces
        if needs_angle_brackets(rel):
            return f"[{display}](<{rel}{'#' + heading_slug(section) if section else ''}>)"
        else:
            return f"[{display}]({link})"

    # Edge case: [[#Section]] already handled above, but if somehow only section:
    if section:
        slug = heading_slug(section)
        return f"[{display or section}](#{slug})"

    return full  # fallback: leave unchanged


WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")


def process_file(filepath: Path) -> bool:
    """Process a single .md file. Returns True if changes were made."""
    text = filepath.read_text(encoding="utf-8")
    
    # Skip if no wikilinks
    if "[[" not in text:
        return False

    # Don't convert inside fenced code blocks
    lines = text.split("\n")
    result_lines = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result_lines.append(line)
            continue

        if in_code_block:
            result_lines.append(line)
            continue

        # Convert wikilinks in this line
        new_line = WIKILINK_RE.sub(lambda m: convert_wikilink(m, filepath), line)
        result_lines.append(new_line)

    new_text = "\n".join(result_lines)
    if new_text != text:
        filepath.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    global FILE_INDEX
    FILE_INDEX = find_all_files(VAULT)

    changed = []
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = Path(root) / f
            if process_file(filepath):
                rel = os.path.relpath(filepath, VAULT)
                changed.append(rel)

    if changed:
        print(f"Converted {len(changed)} files:")
        for f in sorted(changed):
            print(f"  {f}")
    else:
        print("No wikilinks found to convert.")


if __name__ == "__main__":
    main()
