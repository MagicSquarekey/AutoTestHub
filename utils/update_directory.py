# -*- coding: utf-8 -*-
# @Function: 扫描项目目录并自动生成 mu_lu_jie_gou.md

"""扫描项目目录并自动生成目录结构文档。"""

from __future__ import annotations

import io
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# 强制 UTF-8 输出
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "directory_annotations.json"
OUTPUT_PATH = PROJECT_ROOT / "mu_lu_jie_gou.md"

SKIP_DIRS = {
    ".git",
    ".idea",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "node_modules",
}

SKIP_FILES = {".DS_Store", "Thumbs.db"}


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open(encoding="utf-8") as f:
            return json.load(f)
    return {"paths": {}, "folder_defaults": {}, "file_defaults": {}}


def save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")


def infer_from_python(relative_path: Path) -> str | None:
    file_path = PROJECT_ROOT / relative_path
    if not file_path.is_file() or file_path.suffix != ".py":
        return None
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    match = re.search(r"#\s*@Function:\s*(.+)", content)
    return match.group(1).strip() if match else None


def infer_description(relative_path: Path, config: dict) -> str:
    key = relative_path.as_posix()
    paths = config.setdefault("paths", {})
    if key in paths:
        return paths[key]

    if relative_path.is_dir() or key.endswith("/"):
        clean_key = key.rstrip("/")
        top = clean_key.split("/")[0]
        desc = config.get("folder_defaults", {}).get(top, "【目录】待补充说明")
    else:
        py_desc = infer_from_python(relative_path)
        if py_desc:
            desc = py_desc
        else:
            file_defaults = config.get("file_defaults", {})
            name = relative_path.name
            suffix = relative_path.suffix
            desc = file_defaults.get(name) or file_defaults.get(suffix, "待补充说明")

    paths[key] = desc
    return desc


def should_skip(relative: Path) -> bool:
    if any(part in SKIP_DIRS for part in relative.parts):
        return True
    return relative.name in SKIP_FILES


class TreeNode:
    __slots__ = ("name", "is_dir", "children")

    def __init__(self, name: str, is_dir: bool) -> None:
        self.name = name
        self.is_dir = is_dir
        self.children: dict[str, TreeNode] = {}


def build_tree_root() -> TreeNode:
    root = TreeNode(PROJECT_ROOT.name, True)

    for path in sorted(PROJECT_ROOT.rglob("*")):
        if path == PROJECT_ROOT:
            continue
        relative = path.relative_to(PROJECT_ROOT)
        if should_skip(relative):
            continue

        node = root
        parts = list(relative.parts)
        for index, part in enumerate(parts):
            is_dir = index < len(parts) - 1 or path.is_dir()
            if part not in node.children:
                node.children[part] = TreeNode(part, is_dir)
            elif is_dir:
                node.children[part].is_dir = True
            node = node.children[part]

    return root


def render_tree(node: TreeNode, prefix: str, base: Path, config: dict, lines: list[str], is_root: bool = False) -> None:
    if is_root:
        lines.append(f"{node.name}/")

    children = sorted(
        node.children.values(),
        key=lambda item: (not item.is_dir, item.name.lower()),
    )

    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        current = base / child.name
        desc = infer_description(current, config)
        label = f"📁 {child.name}/" if child.is_dir else child.name
        lines.append(f"{prefix}{connector}{label:<28}  # {desc}")

        if child.children:
            render_tree(child, prefix + extension, current, config, lines)


def build_markdown(tree_lines: list[str]) -> str:
    body = "\n".join(tree_lines)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        "# 目录结构\n\n"
        "```\n"
        f"{body}\n"
        "```\n\n"
        "> 🔄 本文件自动生成，请勿手动编辑。\n"
        "> 运行 `python utils/update_directory.py` 更新。\n"
        "> 注释可在 `config/directory_annotations.json` 中编辑。\n"
        f"> 最后更新: {now}\n"
    )


def generate() -> bool:
    config = load_config()
    root = build_tree_root()
    lines: list[str] = []
    render_tree(root, "", Path(), config, lines, is_root=True)
    content = build_markdown(lines)

    changed = not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8") != content
    save_config(config)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    return changed


def main() -> int:
    changed = generate()
    if changed:
        print(f"已更新: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    else:
        print("目录结构无变化，跳过写入。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
