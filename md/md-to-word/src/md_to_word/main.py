from __future__ import annotations

import argparse
from pathlib import Path

from .docx_builder import DocxBuilder
from .image_handler import ImageHandler
from .markdown_parser import MarkdownParser
from .mermaid_renderer import MermaidRenderer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Markdown to Word DOCX with images, links, tables, code, and Mermaid diagrams."
    )
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output DOCX path (default: output/<input-name>.docx)",
    )
    parser.add_argument(
        "--no-remote-images",
        action="store_true",
        help="Do not download HTTP/HTTPS images",
    )
    parser.add_argument(
        "--mermaid-command",
        default="mmdc",
        help="Mermaid CLI command/path (default: mmdc)",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        help="Directory for generated/downloaded assets",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    output_path = (
        args.output.resolve()
        if args.output
        else Path("output") / f"{input_path.stem}.docx"
    )

    assets_dir = (
        args.assets_dir.resolve()
        if args.assets_dir
        else input_path.parent / ".md-to-word-assets"
    )

    image_cache = assets_dir / "images"
    mermaid_dir = assets_dir / "mermaid"

    parser = MarkdownParser()
    _, nodes = parser.parse_file(input_path)

    image_handler = ImageHandler(
        document_dir=input_path.parent,
        cache_dir=image_cache,
        allow_remote=not args.no_remote_images,
    )
    mermaid_renderer = MermaidRenderer(
        output_dir=mermaid_dir,
        command=args.mermaid_command,
    )

    builder = DocxBuilder(
        image_handler=image_handler,
        mermaid_renderer=mermaid_renderer,
    )
    builder.build(nodes, output_path)

    print(f"Created: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
