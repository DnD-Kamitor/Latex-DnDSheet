"""
LaTeX document generation and compilation functions.

This module provides core functionality to generate .tex files and compile them to PDFs.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple


def generate_tex_file(
    content: str,
    output_path: Optional[Path] = None,
    template_path: Optional[Path] = None,
) -> Path:
    """
    Generate a .tex file with the given content.

    Args:
        content: LaTeX document content (full document with \\documentclass, etc.)
        output_path: Where to save the .tex file. If None, creates a temp file.
        template_path: Path to DND-5e-LaTeX-Template (for TEXINPUTS). If None, auto-detects.

    Returns:
        Path to the generated .tex file
    """
    if output_path is None:
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.tex', prefix='dndsheet_')
        os.close(fd)  # Close file descriptor, we'll write with Path
        output_path = Path(temp_path)

    # Write content to file
    output_path.write_text(content, encoding='utf-8')

    return output_path


def compile_to_pdf(
    tex_file: Path,
    output_dir: Optional[Path] = None,
    template_path: Optional[Path] = None,
    cleanup: bool = True,
) -> Tuple[bool, str, Optional[Path]]:
    """
    Compile a .tex file to PDF using LuaLaTeX.

    Args:
        tex_file: Path to the .tex file to compile
        output_dir: Directory for output PDF. If None, uses same dir as tex_file.
        template_path: Path to DND-5e-LaTeX-Template. If None, auto-detects.
        cleanup: Whether to clean up auxiliary files (.aux, .log, etc.)

    Returns:
        Tuple of (success: bool, message: str, pdf_path: Optional[Path])
    """
    if not tex_file.exists():
        return False, f"TeX file not found: {tex_file}", None

    if output_dir is None:
        output_dir = tex_file.parent

    output_dir.mkdir(parents=True, exist_ok=True)

    # Auto-detect template path if not provided
    if template_path is None:
        try:
            from .latex_env import check_dnd_template
        except ImportError:
            # Running as script, not as module
            from latex_env import check_dnd_template

        found, location = check_dnd_template()
        if found:
            template_path = Path(location)
        else:
            return False, "DND-5e-LaTeX-Template not found", None

    # Set up environment with TEXINPUTS
    env = os.environ.copy()
    texinputs = f"{template_path}//:"
    if 'TEXINPUTS' in env:
        texinputs = f"{texinputs}{env['TEXINPUTS']}"
    env['TEXINPUTS'] = texinputs

    # Compile twice for proper references (standard LaTeX practice)
    pdf_path = output_dir / f"{tex_file.stem}.pdf"

    for pass_num in [1, 2]:
        try:
            result = subprocess.run(
                [
                    "lualatex",
                    "-interaction=nonstopmode",
                    f"-output-directory={output_dir}",
                    str(tex_file),
                ],
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Check for fatal errors
            if "Fatal error" in result.stdout or result.returncode != 0:
                # Look for specific error in log
                log_file = output_dir / f"{tex_file.stem}.log"
                error_msg = f"LaTeX compilation failed (pass {pass_num})"

                if log_file.exists():
                    log_content = log_file.read_text()
                    # Try to extract useful error message
                    if "! " in log_content:
                        lines = log_content.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith('! '):
                                error_msg = line + '\n' + '\n'.join(lines[i+1:i+3])
                                break

                return False, error_msg, None

        except subprocess.TimeoutExpired:
            return False, "LaTeX compilation timed out (>60s)", None
        except Exception as e:
            return False, f"Error during compilation: {str(e)}", None

    # Check if PDF was created
    if not pdf_path.exists():
        return False, "PDF was not created (unknown error)", None

    # Cleanup auxiliary files if requested
    if cleanup:
        cleanup_aux_files(tex_file.stem, output_dir)

    return True, f"Successfully compiled to {pdf_path}", pdf_path


def cleanup_aux_files(base_name: str, directory: Path) -> None:
    """
    Remove LaTeX auxiliary files.

    Args:
        base_name: Base filename (without extension)
        directory: Directory containing the auxiliary files
    """
    aux_extensions = [
        '.aux', '.log', '.out', '.toc', '.fdb_latexmk',
        '.fls', '.synctex.gz', '.blg', '.bbl'
    ]

    for ext in aux_extensions:
        aux_file = directory / f"{base_name}{ext}"
        if aux_file.exists():
            try:
                aux_file.unlink()
            except Exception:
                pass  # Silently ignore cleanup failures


def generate_minimal_test_document() -> str:
    """
    Generate a minimal test document for validation.

    Returns:
        LaTeX source code as a string
    """
    return r"""\documentclass[letterpaper,twocolumn,openany]{dndbook}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}

\title{Test Document}
\author{dndsheet}
\date{\today}

\begin{document}

\maketitle

\chapter{Test Chapter}

This is a minimal test document to verify that LaTeX generation is working correctly.

\section{Basic Features}

\begin{DndComment}{Test Comment Box}
    This is a test comment box using the DND template styling.
\end{DndComment}

\begin{DndTable}[header=Test Table]{lX}
    \textbf{Column 1} & \textbf{Column 2} \\
    Test data & More test data \\
    Row 2 & Additional content \\
\end{DndTable}

\section{Conclusion}

If you can read this PDF, the LaTeX generation system is working!

\end{document}
"""


if __name__ == "__main__":
    """Quick test of LaTeX generation."""
    print("Testing LaTeX generation...\n")

    # Generate minimal test document
    print("1. Generating minimal test document...")
    tex_content = generate_minimal_test_document()
    tex_file = Path("test_generation.tex")
    generate_tex_file(tex_content, tex_file)
    print(f"   ✓ Created: {tex_file}")

    # Compile to PDF
    print("\n2. Compiling to PDF...")
    success, message, pdf_path = compile_to_pdf(tex_file, output_dir=Path("output"))

    if success:
        print(f"   ✓ {message}")
        print(f"\n✓ Test successful! PDF size: {pdf_path.stat().st_size} bytes")
    else:
        print(f"   ✗ {message}")
        print("\n✗ Test failed")

    # Cleanup
    if tex_file.exists():
        tex_file.unlink()
