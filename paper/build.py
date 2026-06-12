#!/usr/bin/env python3
"""
One-command, cross-platform reproduction of the manuscript.

    pip install -r requirements.txt
    python build.py

Steps: (1) regenerate all figures, (2) build the .docx, (3) try to export a PDF
(docx2pdf if Word/LibreOffice is available, else LibreOffice headless, else print a
note). Deterministic: no randomness in the build.
"""
import subprocess, sys, shutil, os

FIGS = ["make_figure", "make_pareto", "make_prisma", "make_trends", "make_graphical_abstract"]
DOCX = "KV Cache Compression_paper_revised.docx"
PDF = "KV Cache Compression_paper_revised.pdf"


def run(mod):
    print(f"  - {mod}.py", flush=True)
    subprocess.check_call([sys.executable, f"{mod}.py"])


def main():
    print("1) figures")
    for m in FIGS:
        run(m)
    print("2) manuscript ->", DOCX)
    subprocess.check_call([sys.executable, "build_manuscript.py"])
    print("3) PDF")
    # try docx2pdf (uses Word on Win/Mac), then LibreOffice headless, else skip
    try:
        from docx2pdf import convert
        convert(DOCX, PDF)
        print("   PDF written via docx2pdf ->", PDF); return
    except Exception:
        pass
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    if soffice:
        subprocess.check_call([soffice, "--headless", "--convert-to", "pdf", DOCX])
        print("   PDF written via LibreOffice ->", PDF); return
    print("   (No Word/LibreOffice found. Open the .docx and 'Save as PDF', or install "
          "LibreOffice / `pip install docx2pdf`.)")


if __name__ == "__main__":
    main()
