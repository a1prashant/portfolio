from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class MermaidRenderer:
    """Render Mermaid source blocks using Mermaid CLI (mmdc)."""

    def __init__(self, output_dir: Path, command: str = "mmdc") -> None:
        self.output_dir = Path(output_dir)
        self.command = command

    def is_available(self) -> bool:
        return shutil.which(self.command) is not None

    def render(self, source: str, name: str) -> Path:
        if not self.is_available():
            raise RuntimeError(
                "Mermaid CLI 'mmdc' was not found. Install it with: "
                "npm install -g @mermaid-js/mermaid-cli"
            )

        self.output_dir.mkdir(parents=True, exist_ok=True)
        source_file = self.output_dir / f"{name}.mmd"
        output_file = self.output_dir / f"{name}.png"

        source_file.write_text(source.strip() + "\n", encoding="utf-8")

        command = [
            self.command,
            "-i", str(source_file),
            "-o", str(output_file),
            "-b", "transparent",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Mermaid rendering failed for {name}:\n"
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        if not output_file.exists():
            raise RuntimeError(f"Mermaid CLI did not create {output_file}")

        return output_file
