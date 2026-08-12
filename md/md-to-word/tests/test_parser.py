from pathlib import Path

from md_to_word.markdown_parser import MarkdownParser


def test_parse_basic_markdown(tmp_path: Path):
    source = """# Title

A **bold** paragraph.

```mermaid
flowchart LR
A --> B
```
"""
    path = tmp_path / "test.md"
    path.write_text(source, encoding="utf-8")

    _, nodes = MarkdownParser().parse_file(path)

    assert nodes[0].type == "heading"
    assert nodes[0].content == "Title"
    assert nodes[1].type == "paragraph"
    assert nodes[2].type == "mermaid"
