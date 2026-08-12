from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import lxml.html
from markdown_it import MarkdownIt


@dataclass
class Node:
    type: str
    content: str = ""
    attrs: dict[str, str] = field(default_factory=dict)
    level: int = 0
    children: list["Node"] = field(default_factory=list)


class MarkdownParser:
    """Parse Markdown into a small document-oriented tree."""

    def __init__(self) -> None:
        self.md = MarkdownIt(
            "commonmark",
            {
                "html": True,
                "linkify": True,
                "typographer": True,
            },
        ).enable("table")

    def parse_file(self, path: Path) -> tuple[str, list[Node]]:
        text = path.read_text(encoding="utf-8")
        text = self._strip_front_matter(text)
        tokens = self.md.parse(text)
        return self._parse_tokens(tokens)

    @staticmethod
    def _strip_front_matter(text: str) -> str:
        if text.startswith("---"):
            match = re.match(r"^---\s*\n.*?\n---\s*\n", text, flags=re.DOTALL)
            if match:
                return text[match.end():]
        return text

    def _parse_tokens(self, tokens) -> tuple[str, list[Node]]:
        nodes: list[Node] = []
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token.type == "heading_open":
                level = int(token.tag[1:])
                inline = tokens[i + 1]
                nodes.append(
                    Node("heading", self._inline_text(inline), level=level))
                i += 3
                continue

            if token.type == "paragraph_open":
                inline = tokens[i + 1]
                nodes.append(
                    Node("paragraph", children=self._inline_nodes(inline)))
                i += 3
                continue

            if token.type == "fence":
                if token.info.strip().lower().split()[0:1] == ["mermaid"]:
                    nodes.append(Node("mermaid", token.content))
                else:
                    language = token.info.strip().split(
                    )[0] if token.info.strip() else ""
                    nodes.append(Node("code", token.content,
                                 attrs={"language": language}))
                i += 1
                continue

            if token.type == "code_block":
                nodes.append(Node("code", token.content))
                i += 1
                continue

            if token.type == "bullet_list_open":
                node, i = self._parse_list(tokens, i, ordered=False)
                nodes.append(node)
                continue

            if token.type == "ordered_list_open":
                node, i = self._parse_list(tokens, i, ordered=True)
                nodes.append(node)
                continue

            if token.type == "blockquote_open":
                child_tokens = []
                depth = 1
                j = i + 1
                while j < len(tokens):
                    if tokens[j].type == "blockquote_open":
                        depth += 1
                    elif tokens[j].type == "blockquote_close":
                        depth -= 1
                        if depth == 0:
                            break
                    child_tokens.append(tokens[j])
                    j += 1
                _, children = self._parse_tokens(child_tokens)
                nodes.append(Node("blockquote", children=children))
                i = j + 1
                continue

            if token.type == "hr":
                nodes.append(Node("hr"))
                i += 1
                continue

            if token.type == "table_open":
                node, i = self._parse_table(tokens, i)
                nodes.append(node)
                continue

            if token.type == "html_block":
                content = token.content
                # Parse HTML tables (e.g. Word/HTML-exported tables) into table nodes.
                if re.search(r"<table\b", content, re.I):
                    table = self._parse_html_table(content)
                    if table is not None:
                        nodes.append(table)
                else:
                    # Preserve simple standalone image HTML where possible.
                    img = re.search(
                        r'<img[^>]+src=["\']([^"\']+)["\']', content, re.I)
                    if img:
                        nodes.append(
                            Node("image", attrs={"src": img.group(1)}))
                i += 1
                continue

            i += 1

        return "", nodes

    def _parse_list(self, tokens, start: int, ordered: bool) -> tuple[Node, int]:
        items: list[Node] = []
        i = start + 1

        while i < len(tokens) and tokens[i].type != ("ordered_list_close" if ordered else "bullet_list_close"):
            if tokens[i].type == "list_item_open":
                i += 1
                children = []
                while i < len(tokens) and tokens[i].type != "list_item_close":
                    if tokens[i].type == "paragraph_open":
                        inline = tokens[i + 1]
                        children.append(
                            Node("paragraph", children=self._inline_nodes(inline)))
                        i += 3
                    elif tokens[i].type in {"bullet_list_open", "ordered_list_open"}:
                        nested, i = self._parse_list(
                            tokens, i, tokens[i].type == "ordered_list_open"
                        )
                        children.append(nested)
                    else:
                        i += 1
                items.append(Node("list_item", children=children))
                i += 1
            else:
                i += 1

        return Node("list", attrs={"ordered": str(ordered).lower()}, children=items), i + 1

    def _parse_table(self, tokens, start: int) -> tuple[Node, int]:
        rows: list[list[Node]] = []
        current_row: list[Node] = []
        i = start + 1

        while i < len(tokens):
            t = tokens[i]
            if t.type == "table_close":
                break
            if t.type in {"thead_open", "thead_close", "tbody_open", "tbody_close"}:
                i += 1
                continue
            if t.type == "tr_open":
                current_row = []
            elif t.type in {"th_open", "td_open"}:
                inline = tokens[i + 1]
                current_row.append(
                    Node("cell", children=self._inline_nodes(inline)))
                i += 2
                continue
            elif t.type == "tr_close":
                rows.append(current_row)
            i += 1

        return Node("table", children=[
            Node("row", children=row) for row in rows
        ]), i + 1

    def _inline_nodes(self, token):
        result: list[Node] = []

        for child in token.children or []:
            if child.type == "text":
                result.append(Node("text", child.content))
            elif child.type == "code_inline":
                result.append(Node("code_inline", child.content))
            elif child.type in {"strong_open", "em_open", "s_open"}:
                # Handled by a small recursive-ish stack below.
                result.append(Node(child.type))
            elif child.type in {"strong_close", "em_close", "s_close"}:
                result.append(Node(child.type))
            elif child.type == "softbreak":
                result.append(Node("break"))
            elif child.type == "hardbreak":
                result.append(Node("break"))
            elif child.type == "link_open":
                href = dict(child.attrs or []).get("href", "")
                result.append(Node("link_open", attrs={"href": href}))
            elif child.type == "link_close":
                result.append(Node("link_close"))
            elif child.type == "image":
                attrs = dict(child.attrs or [])
                result.append(Node("image", attrs={
                    "src": attrs.get("src", ""),
                    "alt": attrs.get("alt", ""),
                    "title": attrs.get("title", ""),
                }))
            elif child.type == "html_inline":
                # Extract inline <img> tags (common in Word/Markdown exports).
                m = re.search(
                    r'<img[^>]+src=["\']([^"\']+)["\']', child.content, re.I)
                if m:
                    result.append(
                        Node("image", attrs={"src": m.group(1), "alt": ""}))
                else:
                    result.append(
                        Node("text", re.sub(r"<[^>]+>", "", child.content)))

        return result

    @staticmethod
    def _inline_text(token) -> str:
        return "".join(
            child.content
            for child in (token.children or [])
            if child.type in {"text", "code_inline"}
        )

    def _parse_html_table(self, html: str) -> Node | None:
        """Parse an HTML <table> block into a table Node using lxml."""
        try:
            root = lxml.html.fragment_fromstring(html, create_parent="div")
        except Exception:
            return None

        rows: list[Node] = []
        for tr in root.iter("tr"):
            cells: list[Node] = []
            for cell in tr:
                if getattr(cell, "tag", None) in ("th", "td"):
                    cells.append(
                        Node("cell", children=self._html_rich_inline(cell)))
            if cells:
                rows.append(Node("row", children=cells))

        if not rows:
            return None
        return Node("table", children=rows)

    def _html_rich_inline(self, element) -> list[Node]:
        """Convert an lxml element subtree into inline Nodes (bold/italic/lists/images)."""
        nodes: list[Node] = []

        if element.text:
            nodes.append(Node("text", element.text))

        for child in element:
            tag = child.tag
            if tag is None:  # comment node
                continue
            tag = tag.lower()

            if tag == "img":
                src = child.get("src", "")
                if src:
                    nodes.append(
                        Node("image", attrs={"src": src, "alt": child.get("alt", "")}))
            elif tag in ("strong", "b"):
                nodes.append(Node("strong_open"))
                nodes.extend(self._html_rich_inline(child))
                nodes.append(Node("strong_close"))
            elif tag in ("em", "i"):
                nodes.append(Node("em_open"))
                nodes.extend(self._html_rich_inline(child))
                nodes.append(Node("em_close"))
            elif tag == "br":
                nodes.append(Node("break"))
            elif tag == "p":
                nodes.extend(self._html_rich_inline(child))
                nodes.append(Node("break"))
            elif tag == "li":
                nodes.append(Node("text", "• "))
                nodes.extend(self._html_rich_inline(child))
                nodes.append(Node("break"))
            elif tag in ("ul", "ol", "blockquote", "thead", "tbody", "tfoot",
                         "tr", "table", "colgroup", "col", "div", "span"):
                nodes.extend(self._html_rich_inline(child))
            else:
                nodes.extend(self._html_rich_inline(child))

            if child.tail:
                nodes.append(Node("text", child.tail))

        return nodes
