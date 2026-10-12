# -*- coding: utf-8 -*-
"""
Master Builder for General Surgery University Exam Preparation Suite
Generates:
1. General_Surgery_Master_Notes.md (Cleaned Markdown with equations and tables)
2. General_Surgery_Master_Notes.html (Print-ready document with embedded diagrams)
3. General_Surgery_Master_Notes.pdf (Headless Edge compiled PDF)
4. index.html (Responsive, Interactive Study Dashboard & Topic Explorer)
"""

import os
import sys
import base64
import json
import subprocess

from content.general_surgery import CHAPTERS as c1
from content.neck_and_face import CHAPTERS as c2
from content.infections_neuro_ot import CHAPTERS as c3
from content.advanced_and_thyroid import CHAPTERS as c4
from content.cheat_sheet import CHAPTERS as c5
from content.formatter import ICONS, FAVICON_SVG, clean_latex, parse_markdown_to_html, format_inline_markdown
from content.interactive_data import CLASSIFICATION_PRESETS

ALL_CHAPTERS = c1 + c2 + c3 + c4 + c5

def load_diagrams_b64():
    b64 = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    subdirs = [
        os.path.join(base_dir, 'assets', 'diagrams'),
        os.path.join(base_dir, 'assets', 'illustrations')
    ]
    for sdir in subdirs:
        if os.path.exists(sdir):
            for f in os.listdir(sdir):
                f_lower = f.lower()
                f_path = os.path.join(sdir, f)
                if f_lower.endswith('.png'):
                    with open(f_path, 'rb') as fp:
                        b64[f] = f"data:image/png;base64,{base64.b64encode(fp.read()).decode('utf-8')}"
                elif f_lower.endswith('.jpg') or f_lower.endswith('.jpeg'):
                    with open(f_path, 'rb') as fp:
                        b64[f] = f"data:image/jpeg;base64,{base64.b64encode(fp.read()).decode('utf-8')}"
    return b64

def generate_markdown(chapters):
    md_lines = []
    md_lines.append("# Master Compendium of General Surgery: 15-Mark University Examination Monograph")
    md_lines.append("\n*Comprehensive Medical & Surgical Study Guide based on Lecture Notes & Clinical Surgical Blueprints*\n")
    md_lines.append("---\n")
    md_lines.append("## Table of Contents")
    for idx, ch in enumerate(chapters):
        md_lines.append(f"{idx+1}. [{ch['title']}](#{ch['id']}) — *Source: {ch['source']}*")
    md_lines.append("\n---\n")

    for idx, ch in enumerate(chapters):
        md_lines.append(f"\n<a id='{ch['id']}'></a>\n")
        md_lines.append(f"# Chapter {idx+1}: {ch['title']}")
        md_lines.append(f"*Source: {ch['source']}*\n")
        
        md_lines.append(f"### University 15-Mark Essay Framework Prompt")
        md_lines.append(f"> **Exam Question:** {clean_latex(ch['essay_prompt'])}\n")

        md_lines.append(f"### Layman's Explanation & Intuitive Analogy")
        md_lines.append(f"> {clean_latex(ch['layman_explanation'])}\n")

        if ch.get("diagrams"):
            md_lines.append("### Core Anatomical & Clinical Diagrams")
            for d in ch["diagrams"]:
                md_lines.append(f"- **{d['title']}** (Image file: `assets/diagrams/{d['filename']}`)")
            md_lines.append("")

        md_lines.append("### Comprehensive 15-Mark Structural Monograph")
        for sec_name, sec_content in ch["sections"].items():
            title_formatted = sec_name.replace("_", " ").title()
            md_lines.append(f"\n#### {title_formatted}\n")
            md_lines.append(clean_latex(sec_content.strip()))
            md_lines.append("")

        if ch.get("viva_pearls"):
            md_lines.append("\n### High-Yield Viva & Clinical Pearls")
            for pearl in ch["viva_pearls"]:
                md_lines.append(f"- {clean_latex(pearl)}")
            md_lines.append("")

        md_lines.append("\n---\n")

    return "\n".join(md_lines)

def generate_html(chapters, b64_images):
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">
<title>General Surgery Master Compendium - 15-Mark University Examination Monograph</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@300;400;500;600;700&display=swap');

@page {{
    size: A4;
    margin: 18mm 15mm 20mm 15mm;
    @bottom-right {{
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: #64748b;
    }}
    @bottom-left {{
        content: "General Surgery Master Compendium | 15-Mark Exam Monograph";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }}
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #1e293b;
    background-color: #ffffff;
    font-size: 10pt;
    margin: 0;
    padding: 0;
}}

.cover-page {{
    page-break-after: always;
    min-height: 85vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 40px 20px;
    border: 3px double #7c3aed;
    margin: 20px;
    background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
}}

.cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    color: #1e1b4b;
    letter-spacing: 1px;
    margin-bottom: 12px;
}}

.cover-subtitle {{
    font-size: 13pt;
    font-weight: 600;
    color: #7c3aed;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

.cover-meta {{
    font-size: 10pt;
    color: #475569;
    max-width: 650px;
    line-height: 1.6;
    margin-bottom: 40px;
}}

.cover-badges {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
}}

.badge {{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 8.5pt;
    font-weight: 600;
    background-color: #f3e8ff;
    color: #6d28d9;
    border: 1px solid #ddd6fe;
}}

.toc-page {{
    page-break-after: always;
    padding: 20px;
}}

.toc-title {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    color: #1e1b4b;
    border-bottom: 2px solid #7c3aed;
    padding-bottom: 8px;
    margin-bottom: 20px;
}}

.toc-grid {{
    column-count: 2;
    column-gap: 30px;
}}

.toc-item {{
    font-size: 9pt;
    margin-bottom: 8px;
    break-inside: avoid;
}}

.toc-item a {{
    text-decoration: none;
    color: #1e293b;
    font-weight: 500;
}}

.chapter-container {{
    page-break-before: always;
    margin-bottom: 30px;
}}

.chapter-header {{
    border-bottom: 2px solid #7c3aed;
    padding-bottom: 8px;
    margin-bottom: 16px;
}}

.chapter-number {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #7c3aed;
    font-weight: 700;
}}

.chapter-title {{
    font-family: 'Cinzel', serif;
    font-size: 17pt;
    font-weight: 700;
    color: #0f172a;
    margin: 4px 0 6px 0;
}}

.chapter-source {{
    font-size: 8pt;
    color: #64748b;
    font-style: italic;
}}

.callout {{
    border-radius: 6px;
    padding: 12px 16px;
    margin: 12px 0;
    font-size: 9pt;
    line-height: 1.5;
    break-inside: avoid;
}}

.callout-prompt {{
    background-color: #fdf2f8;
    border-left: 4px solid #db2777;
    color: #831843;
}}

.callout-layman {{
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #14532d;
}}

.callout-title {{
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 8pt;
    margin-bottom: 4px;
}}

.section-block {{
    margin: 14px 0;
    break-inside: avoid;
}}

.section-heading {{
    font-size: 11pt;
    font-weight: 700;
    color: #6d28d9;
    margin: 14px 0 6px 0;
    border-left: 3px solid #7c3aed;
    padding-left: 8px;
    text-transform: capitalize;
}}

.table-responsive {{
    overflow-x: auto;
    margin: 12px 0;
}}

table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8pt;
    break-inside: avoid;
}}

table.data-table th, table.data-table td {{
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}}

table.data-table th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
}}

table.data-table tr:nth-child(even) td {{
    background-color: #f8fafc;
}}

.diagram-card {{
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    margin: 12px 0;
    background-color: #fafafa;
    text-align: center;
    break-inside: avoid;
}}

.diagram-img {{
    max-width: 95%;
    max-height: 340px;
    object-fit: contain;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}}

.diagram-caption {{
    font-size: 7.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.viva-box {{
    background-color: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #d97706;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 14px 0;
    break-inside: avoid;
}}

.viva-title {{
    font-size: 8.5pt;
    font-weight: 700;
    color: #92400e;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}}

.viva-list {{
    margin: 0;
    padding-left: 18px;
    font-size: 8.5pt;
    color: #78350f;
}}

.viva-list li {{
    margin-bottom: 4px;
}}

ul.content-list, ol.content-list-ordered {{
    margin: 6px 0;
    padding-left: 20px;
}}

li {{
    margin-bottom: 3px;
}}

p.content-para {{
    margin: 5px 0;
}}
</style>
</head>
<body>

<div class="cover-page">
    <div class="cover-title">GENERAL SURGERY</div>
    <div class="cover-subtitle">15-Mark University Examination Monograph</div>
    <div class="cover-meta">
        Exhaustive, typed, and copyable clinical notes with preserved original diagrams, high-yield comparative tables, step-by-step surgical procedures, and intuitive layman explanations for MBBS & MS university examinations.
    </div>
    <div class="cover-badges">
        <span class="badge">Complete Lecture Transcripts</span>
        <span class="badge">15-Mark Master Blueprints</span>
        <span class="badge">All Original Diagrams Preserved</span>
        <span class="badge">Zero Information Omitted</span>
        <span class="badge">100% Copyable & Searchable</span>
    </div>
</div>

<div class="toc-page">
    <div class="toc-title">TABLE OF CONTENTS</div>
    <div class="toc-grid">
""")

    for idx, ch in enumerate(chapters):
        html_parts.append(f'<div class="toc-item"><strong>{idx+1}.</strong> <a href="#{ch["id"]}">{ch["title"]}</a></div>')

    html_parts.append("""
    </div>
</div>
""")

    for idx, ch in enumerate(chapters):
        html_parts.append(f"""
<div class="chapter-container" id="{ch['id']}">
    <div class="chapter-header">
        <div class="chapter-number">Chapter {idx+1}</div>
        <div class="chapter-title">{ch['title']}</div>
        <div class="chapter-source">Source Reference: {ch['source']}</div>
    </div>

    <div class="callout callout-prompt">
        <div class="callout-title">15-Mark Examination Prompt</div>
        <div>{format_inline_markdown(ch['essay_prompt'])}</div>
    </div>

    <div class="callout callout-layman">
        <div class="callout-title">Layman's Intuitive Explanation & Analogy</div>
        <div>{format_inline_markdown(ch['layman_explanation'])}</div>
    </div>
""")

        if ch.get("diagrams"):
            for d in ch["diagrams"]:
                fname = d["filename"]
                b64_data = b64_images.get(fname, "")
                if b64_data:
                    is_orig = fname.startswith('ch') or 'handwritten' in d['title'].lower() or 'notebook' in d['title'].lower()
                    badge_text = "Original Handwritten Notebook Sketch" if is_orig else "High-Resolution 300 DPI Medical Schematic"
                    html_parts.append(f"""
    <div class="diagram-card">
        <div style="font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #7c3aed; margin-bottom: 4px;">{badge_text}</div>
        <img class="diagram-img" src="{b64_data}" alt="{d['title']}">
        <div class="diagram-caption">Figure {idx+1}.{ch['diagrams'].index(d)+1}: {d['title']}</div>
    </div>
""")

        html_parts.append('<div class="sections-container">')
        for sec_name, sec_content in ch["sections"].items():
            title_formatted = sec_name.replace("_", " ").title()
            parsed_html = parse_markdown_to_html(sec_content)
            html_parts.append(f"""
    <div class="section-block">
        <div class="section-heading">{title_formatted}</div>
        <div class="section-body">{parsed_html}</div>
    </div>
""")
        html_parts.append('</div>')

        if ch.get("viva_pearls"):
            html_parts.append("""
    <div class="viva-box">
        <div class="viva-title">High-Yield Clinical & Viva Examiner Pearls</div>
        <ul class="viva-list">
""")
            for p in ch["viva_pearls"]:
                html_parts.append(f"<li>{format_inline_markdown(p)}</li>")
            html_parts.append("""
        </ul>
    </div>
""")

        html_parts.append('</div>')

    html_parts.append("""
</body>
</html>
""")
    return "\n".join(html_parts)

def generate_interactive_website(chapters, b64_images):
    # Pre-clean chapters data so no raw LaTeX or unrendered math leaks into JavaScript
    cleaned_chapters = []
    for ch in chapters:
        ch_clean = {
            "id": ch["id"],
            "title": ch["title"],
            "source": ch["source"],
            "essay_prompt": format_inline_markdown(ch["essay_prompt"]),
            "layman_explanation": format_inline_markdown(ch["layman_explanation"]),
            "diagrams": ch.get("diagrams", []),
            "viva_pearls": [format_inline_markdown(p) for p in ch.get("viva_pearls", [])],
            "sections": {}
        }
        for s_k, s_v in ch["sections"].items():
            ch_clean["sections"][s_k] = parse_markdown_to_html(s_v)
        cleaned_chapters.append(ch_clean)

    chapters_json = json.dumps(cleaned_chapters)
    images_json = json.dumps(b64_images)
    presets_json = json.dumps(CLASSIFICATION_PRESETS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">
<title>General Surgery Master Portal - University Exam Companion</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --primary: #7c3aed;
    --primary-dark: #6d28d9;
    --primary-light: #f5f3ff;
    --primary-border: #ddd6fe;
    --bg-main: #faf7fd;
    --bg-card: #ffffff;
    --text-main: #1e1b4b;
    --text-muted: #6b7280;
    --border: #e9d5ff;
    --sidebar-w: 320px;
    --accent: #f59e0b;
    --accent-purple: #8b5cf6;
    --danger: #ef4444;
    --success: #10b981;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --shadow-sm: 0 1px 3px rgba(124, 58, 237, 0.08);
    --shadow-md: 0 4px 14px rgba(124, 58, 237, 0.12);
    --shadow-lg: 0 10px 25px rgba(124, 58, 237, 0.18);
}}

body.dark {{
    --bg-main: #0c071e;
    --bg-card: #160d33;
    --text-main: #f5f3ff;
    --text-muted: #c4b5fd;
    --border: #2e1b5b;
    --primary: #8b5cf6;
    --primary-dark: #7c3aed;
    --primary-light: rgba(139, 92, 246, 0.14);
    --primary-border: rgba(139, 92, 246, 0.32);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.35);
    --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.45);
    --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.6);
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    display: flex;
    height: 100vh;
    overflow: hidden;
    font-size: 14px;
}}

/* Sidebar */
#sidebar {{
    width: var(--sidebar-w);
    background-color: var(--bg-card);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    transition: transform 0.3s ease;
    z-index: 50;
}}

.sidebar-header {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.brand-title {{
    font-family: 'Cinzel', serif;
    font-size: 14pt;
    font-weight: 700;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: 0.5px;
}}

.brand-accent {{
    color: var(--primary);
    font-weight: 800;
}}

.brand-sub {{
    font-size: 7.5pt;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: var(--text-muted);
    margin-top: 2px;
}}

.mobile-sidebar-close-btn {{
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-muted);
    padding: 6px;
    border-radius: var(--radius-sm);
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}}

.mobile-sidebar-close-btn:hover {{
    color: var(--primary);
    background-color: var(--primary-light);
}}

@media (max-width: 900px) {{
    .mobile-sidebar-close-btn {{
        display: flex;
    }}
}}

.sidebar-nav-actions {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 8px;
}}

.nav-btn {{
    flex: 1;
    padding: 8px 10px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background-color: var(--bg-main);
    color: var(--text-main);
    font-size: 8.5pt;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    transition: all 0.2s;
}}

.nav-btn:hover, .nav-btn.active {{
    background-color: var(--primary-light);
    color: var(--primary);
    border-color: var(--primary);
}}

.search-box {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    position: relative;
}}

.search-input {{
    width: 100%;
    padding: 8px 12px 8px 34px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background-color: var(--bg-main);
    color: var(--text-main);
    font-size: 9pt;
    outline: none;
    transition: border 0.2s;
}}

.search-input:focus {{
    border-color: var(--primary);
}}

.search-icon-pos {{
    position: absolute;
    left: 24px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    pointer-events: none;
}}

.topic-list {{
    flex: 1;
    overflow-y: auto;
    padding: 8px;
}}

.topic-item {{
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    font-size: 9pt;
    font-weight: 500;
    cursor: pointer;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.15s;
    color: var(--text-muted);
}}

.topic-item:hover {{
    background-color: var(--primary-light);
    color: var(--primary);
}}

.topic-item.active {{
    background-color: var(--primary);
    color: #ffffff;
    font-weight: 600;
}}

.topic-check-btn {{
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    padding: 2px;
    color: inherit;
}}

.topic-title-text {{
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

/* Main View */
#main-view {{
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
}}

.top-bar {{
    height: 56px;
    background-color: var(--bg-card);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    flex-shrink: 0;
    gap: 12px;
}}

.mobile-menu-btn {{
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-main);
    padding: 6px;
}}

.tabs-nav-wrapper {{
    display: flex;
    align-items: center;
    position: relative;
    flex: 1;
    overflow: hidden;
    gap: 4px;
}}

.tabs-arrow-btn {{
    width: 26px;
    height: 26px;
    border-radius: 50%;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    z-index: 3;
}}

.tabs-arrow-btn:hover {{
    background: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
}}

.tabs-arrow-btn.is-hidden {{
    opacity: 0.2;
    pointer-events: none;
}}

.top-tabs-scroll {{
    display: flex;
    gap: 6px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    flex: 1;
    scroll-behavior: smooth;
    padding: 4px 2px;
    scrollbar-width: thin;
    scrollbar-color: var(--primary) rgba(0, 0, 0, 0.08);
}}

.top-tabs-scroll::-webkit-scrollbar {{
    height: 3px;
    display: block;
}}
.top-tabs-scroll::-webkit-scrollbar-track {{
    background: rgba(0, 0, 0, 0.04);
    border-radius: 3px;
}}
.top-tabs-scroll::-webkit-scrollbar-thumb {{
    background: var(--primary);
    border-radius: 3px;
}}

.tabs-nav-wrapper::before,
.tabs-nav-wrapper::after {{
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    width: 16px;
    pointer-events: none;
    z-index: 2;
    opacity: 0;
    transition: opacity 0.2s;
}}

.tabs-nav-wrapper.can-scroll-left::before {{
    left: 28px;
    background: linear-gradient(to right, var(--bg-card), transparent);
    opacity: 1;
}}

.tabs-nav-wrapper.can-scroll-right::after {{
    right: 28px;
    background: linear-gradient(to left, var(--bg-card), transparent);
    opacity: 1;
}}

/* Mobile Secondary Section Nav & Quick Pills */
.mobile-section-nav {{
    display: none;
    flex-direction: column;
    background-color: var(--bg-card);
    border-bottom: 1px solid var(--border);
    padding: 8px 14px;
    gap: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}}

.mobile-section-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}}

.mobile-section-indicator-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 8pt;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.pulse-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: var(--primary);
    display: inline-block;
    box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.25);
}}

.mobile-swipe-hint-text {{
    font-size: 7pt;
    color: var(--text-muted);
    font-weight: 500;
}}

.mobile-section-quick-pills {{
    display: flex;
    gap: 5px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding: 2px 0;
    scrollbar-width: none;
}}
.mobile-section-quick-pills::-webkit-scrollbar {{
    display: none;
}}

.pill-shortcut {{
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 7.5pt;
    font-weight: 600;
    border: 1px solid var(--border);
    background: var(--bg-main);
    color: var(--text-muted);
    white-space: nowrap;
    cursor: pointer;
    transition: all 0.15s;
}}

.pill-shortcut:hover {{
    border-color: var(--primary);
    color: var(--primary);
}}

.pill-shortcut.active {{
    background-color: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
}}

.tab-btn {{
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: 8.5pt;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
    transition: all 0.2s;
}}

.tab-btn:hover {{
    color: var(--primary);
    background-color: var(--primary-light);
}}

.tab-btn.active {{
    background-color: var(--primary-light);
    color: var(--primary);
    border-color: var(--primary);
}}

.top-right-tools {{
    display: flex;
    gap: 8px;
    align-items: center;
    flex-shrink: 0;
}}

.icon-btn {{
    width: 34px;
    height: 34px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background-color: var(--bg-card);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}}

.icon-btn:hover {{
    border-color: var(--primary);
    color: var(--primary);
}}

/* Modern Unified Pill Button Architecture */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-family: inherit;
    font-weight: 600;
    font-size: 8.5pt;
    border-radius: 9999px;
    padding: 7px 18px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    text-decoration: none;
    white-space: nowrap;
    border: 1px solid transparent;
}}

.btn-primary {{
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.32);
}}

.btn-primary:hover {{
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.48);
    transform: translateY(-1px);
}}

.btn-primary:active {{
    transform: translateY(0);
}}

.btn-secondary {{
    background-color: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
}}

.btn-secondary:hover {{
    border-color: var(--primary);
    color: var(--primary);
    background-color: var(--primary-light);
}}

.btn-accent {{
    background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
    color: #ffffff;
    box-shadow: 0 2px 10px rgba(109, 40, 217, 0.35);
}}

.btn-accent:hover {{
    background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
    box-shadow: 0 4px 16px rgba(109, 40, 217, 0.5);
    transform: translateY(-1px);
}}

/* In-App PDF Viewer Modal for Tablets and Online Devices */
.pdf-modal-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(12, 7, 30, 0.85);
    backdrop-filter: blur(4px);
    z-index: 1200;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 16px;
}}

.pdf-modal-container {{
    width: 95vw;
    max-width: 1100px;
    height: 92vh;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}}

.pdf-modal-header {{
    padding: 12px 18px;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}}

.pdf-tablet-notice {{
    padding: 8px 18px;
    background: var(--primary-light);
    border-bottom: 1px solid var(--primary-border);
    font-size: 8pt;
    color: var(--primary);
}}

.pdf-iframe-view {{
    flex: 1;
    width: 100%;
    border: none;
    background: #525659;
}}

/* Viva Pearls Q&A Self-Test Blocks */
.viva-qa-block {{
    margin-bottom: 12px;
    padding: 10px 14px;
    border-radius: var(--radius-sm);
    background: var(--bg-card);
    border: 1px solid var(--border);
    transition: all 0.2s;
}}

.viva-badge-q {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 9999px;
    font-size: 7.5pt;
    font-weight: 700;
    background: var(--primary);
    color: #ffffff;
    margin-right: 6px;
}}

.viva-badge-a {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 9999px;
    font-size: 7.5pt;
    font-weight: 700;
    background: var(--success);
    color: #ffffff;
    margin-right: 6px;
}}

.viva-pearls-container.answers-hidden .viva-a-row {{
    display: none;
}}

.viva-a-row {{
    margin-top: 8px;
    padding: 10px 14px;
    background: rgba(16, 185, 129, 0.08);
    border-left: 3px solid var(--success);
    border-radius: 4px;
    font-size: 9pt;
    color: var(--text-main);
    line-height: 1.6;
}}

body.dark .viva-a-row {{
    background: rgba(16, 185, 129, 0.14);
    border-left: 3px solid #34d399;
}}

.viva-model-label {{
    color: #047857;
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

body.dark .viva-model-label {{
    color: #34d399;
}}

.quiz-badge-model {{
    background: #ecfdf5;
    color: #047857;
}}

body.dark .quiz-badge-model {{
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
}}

.content-body {{
    flex: 1;
    overflow-y: auto;
    padding: 24px 32px;
}}

/* Dashboard Landing View */
.dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}}

.stat-card {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}}

.stat-label {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-muted);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.stat-val {{
    font-size: 22pt;
    font-weight: 700;
    color: var(--primary);
}}

.progress-banner {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 24px;
}}

.progress-bar-bg {{
    width: 100%;
    height: 10px;
    background-color: var(--border);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 10px;
}}

.progress-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #0284c7 0%, #10b981 100%);
    border-radius: 999px;
    width: 0%;
    transition: width 0.4s ease;
}}

.filter-chips {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}}

.chip {{
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 8.5pt;
    font-weight: 600;
    border: 1px solid var(--border);
    background-color: var(--bg-card);
    cursor: pointer;
    color: var(--text-muted);
    transition: all 0.2s;
}}

.chip.active {{
    background-color: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
}}

.dashboard-topic-cards {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
}}

.dash-card {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s;
}}

.dash-card:hover {{
    border-color: var(--primary);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

.dash-card.completed {{
    border-left: 4px solid var(--success);
}}

.dash-card-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 10px;
    gap: 8px;
}}

.dash-card-title {{
    font-size: 10.5pt;
    font-weight: 600;
    color: var(--text-main);
}}

.dash-card-source {{
    font-size: 8pt;
    color: var(--text-muted);
    margin-bottom: 14px;
}}

.dash-card-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 10px;
    border-top: 1px solid var(--border);
}}

/* Topic View */
.topic-header-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;
}}

.topic-title-display {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    font-weight: 700;
    color: var(--text-main);
}}

.topic-actions {{
    display: flex;
    gap: 10px;
    align-items: center;
}}

.toggle-complete-btn {{
    padding: 7px 14px;
    border-radius: var(--radius-sm);
    font-size: 8.5pt;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid var(--border);
    background-color: var(--bg-card);
    color: var(--text-main);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
}}

.toggle-complete-btn.is-completed {{
    background-color: #ecfdf5;
    color: #047857;
    border-color: #a7f3d0;
}}

body.dark .toggle-complete-btn.is-completed {{
    background-color: rgba(16, 185, 129, 0.18);
    color: #6ee7b7;
    border-color: rgba(16, 185, 129, 0.45);
}}

.card {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}}

.card-title {{
    font-size: 11pt;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.prompt-box {{
    background: linear-gradient(135deg, rgba(219, 39, 119, 0.06) 0%, rgba(219, 39, 119, 0.01) 100%);
    border-left: 4px solid #db2777;
    border-radius: var(--radius-sm);
    padding: 16px 20px;
    margin-bottom: 20px;
    font-size: 9.5pt;
    color: #831843;
}}

.prompt-box-header {{
    font-weight: 700;
    text-transform: uppercase;
    font-size: 8pt;
    margin-bottom: 4px;
    color: #db2777;
}}

body.dark .prompt-box {{
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.12) 0%, rgba(236, 72, 153, 0.02) 100%);
    border-left: 4px solid #f472b6;
    color: #fdf2f8;
}}

body.dark .prompt-box-header {{
    color: #f472b6;
}}

.layman-box {{
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.01) 100%);
    border-left: 4px solid var(--success);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
    margin-bottom: 20px;
    font-size: 10pt;
    line-height: 1.6;
    color: #064e3b;
}}

.layman-box-header {{
    font-weight: 700;
    text-transform: uppercase;
    font-size: 8pt;
    margin-bottom: 4px;
    color: #059669;
}}

body.dark .layman-box {{
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.14) 0%, rgba(16, 185, 129, 0.02) 100%);
    border-left: 4px solid #34d399;
    color: #f1f5f9;
}}

body.dark .layman-box-header {{
    color: #34d399;
}}

/* Interactive Types & Subtypes Explorer */
.interactive-types-container {{
    margin: 20px 0;
    border: 1px solid var(--primary-light);
    border-radius: var(--radius-md);
    padding: 18px;
    background-color: var(--bg-card);
}}

.type-buttons-bar {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}}

.type-btn {{
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    font-size: 8.5pt;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid var(--border);
    background-color: var(--bg-main);
    color: var(--text-main);
    transition: all 0.2s;
}}

.type-btn.active {{
    background-color: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
}}

.type-detail-card {{
    background-color: var(--bg-main);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
}}

.type-detail-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
}}

.type-detail-title {{
    font-size: 11pt;
    font-weight: 700;
    color: var(--primary);
}}

.type-badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 7.5pt;
    font-weight: 700;
    background-color: var(--primary-light);
    color: var(--primary);
}}

.type-hemodynamics {{
    font-size: 9pt;
    font-weight: 600;
    color: #b45309;
    margin-bottom: 10px;
    padding: 6px 10px;
    background-color: #fffbeb;
    border-radius: var(--radius-sm);
}}

/* Personal Notes Section */
.notes-container {{
    margin-top: 16px;
}}

.notes-textarea {{
    width: 100%;
    min-height: 140px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px;
    background-color: var(--bg-main);
    color: var(--text-main);
    font-family: inherit;
    font-size: 9.5pt;
    line-height: 1.5;
    outline: none;
    resize: vertical;
    transition: border 0.2s;
}}

.notes-textarea:focus {{
    border-color: var(--primary);
}}

.notes-status {{
    font-size: 8pt;
    color: var(--text-muted);
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}}

/* Tables and Content Typography */
.table-responsive {{
    overflow-x: auto;
    margin: 12px 0;
    -webkit-overflow-scrolling: touch;
}}

table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 9pt;
}}

table.data-table th, table.data-table td {{
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
    vertical-align: top;
}}

table.data-table th {{
    background-color: var(--bg-main);
    color: var(--text-main);
    font-weight: 600;
}}

table.data-table tr:nth-child(even) td {{
    background-color: rgba(0,0,0,0.015);
}}

body.dark table.data-table tr:nth-child(even) td {{
    background-color: rgba(255,255,255,0.02);
}}

ul.content-list, ol.content-list-ordered {{
    margin: 8px 0;
    padding-left: 22px;
}}

li {{
    margin-bottom: 5px;
    line-height: 1.6;
}}

p.content-para {{
    margin: 8px 0;
    line-height: 1.6;
}}

.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: var(--primary);
    margin: 20px 0 8px 0;
    border-left: 3px solid var(--primary);
    padding-left: 8px;
    text-transform: capitalize;
}}

.sub-heading {{
    font-size: 10pt;
    font-weight: 600;
    color: var(--text-main);
    margin: 14px 0 6px 0;
}}

.viva-card {{
    background-color: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
    margin: 18px 0;
}}

body.dark .viva-card {{
    background-color: rgba(245, 158, 11, 0.12);
    border-color: rgba(245, 158, 11, 0.35);
}}

body.dark .type-hemodynamics {{
    color: #fcd34d;
    background-color: rgba(245, 158, 11, 0.15);
}}

.viva-card h4 {{
    color: #b45309;
    font-size: 9.5pt;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

body.dark .viva-card h4 {{
    color: #fcd34d !important;
}}

.diagram-gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin: 16px 0;
}}

.diagram-item {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
    text-align: center;
    display: flex;
    flex-direction: column;
}}

.diagram-header-badge {{
    padding: 10px 14px 6px 14px;
    text-align: left;
    background-color: var(--bg-card);
}}

.diagram-type-badge {{
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 9999px;
}}

.badge-original {{
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #fde68a;
}}

body.dark .badge-original {{
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border-color: rgba(245, 158, 11, 0.4);
}}

.badge-hd {{
    background: #ede9fe;
    color: #6d28d9;
    border: 1px solid #ddd6fe;
}}

body.dark .badge-hd {{
    background: rgba(139, 92, 246, 0.25);
    color: #c4b5fd;
    border-color: rgba(139, 92, 246, 0.45);
}}

.diagram-item img {{
    width: 100%;
    max-height: 320px;
    object-fit: contain;
    background-color: #ffffff;
    cursor: zoom-in;
    padding: 8px;
    flex: 1;
}}

body.dark .diagram-item img {{
    background-color: #1e153a;
}}

.diagram-item-caption {{
    padding: 10px 14px;
    font-size: 8pt;
    font-weight: 600;
    color: var(--text-muted);
    border-top: 1px solid var(--border);
    background-color: var(--bg-card);
}}

/* Dashboard Hero Card */
.dash-hero-card {{
    background: linear-gradient(135deg, #1e0b36 0%, #3b1261 50%, #4c1d95 100%);
    border-radius: var(--radius-md);
    padding: 24px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.25);
    border: 1px solid rgba(168, 85, 247, 0.3);
}}

.dash-hero-badge {{
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: rgba(168, 85, 247, 0.25);
    color: #c084fc;
    padding: 4px 10px;
    border-radius: 9999px;
    margin-bottom: 10px;
}}

.dash-hero-title {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    color: #f8fafc;
    margin: 0 0 8px 0;
    line-height: 1.25;
}}

.dash-hero-sub {{
    font-size: 9.5pt;
    color: #ddd6fe;
    margin: 0 0 16px 0;
    line-height: 1.5;
}}

.dash-hero-meta {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}}

.dash-hero-stat {{
    font-size: 8.5pt;
    background: rgba(255,255,255,0.12);
    padding: 5px 12px;
    border-radius: 9999px;
    color: #f5f3ff;
}}

.dash-hero-image-box {{
    flex-shrink: 0;
    width: 280px;
    border-radius: var(--radius-sm);
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35);
}}

/* Dashboard Rapid Revision Cheat Sheet Card */
.dash-cheat-sheet-card {{
    background: linear-gradient(135deg, #2e1065 0%, #4c1d95 50%, #6d28d9 100%);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(109, 40, 217, 0.25);
    border: 1px solid rgba(168, 85, 247, 0.4);
    flex-wrap: wrap;
}}

.cheat-sheet-badge-icon {{
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: #f5f3ff;
}}

.dash-hero-img {{
    width: 100%;
    height: auto;
    display: block;
    object-fit: cover;
}}

/* Interactive Quiz Deck Carousel */
.quiz-container {{
    max-width: 720px;
    margin: 0 auto;
}}

.quiz-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
}}

.quiz-score-badge {{
    font-size: 8.5pt;
    background: #e0f2fe;
    color: #0369a1;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 600;
}}

.quiz-progress-text {{
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 10px;
}}

.quiz-flashcard-box {{
    background-color: var(--bg-card);
    border: 2px solid var(--border);
    border-radius: var(--radius-md);
    padding: 32px 28px;
    cursor: pointer;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
}}

.quiz-flashcard-box:hover {{
    border-color: var(--primary);
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}}

.quiz-badge {{
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    background: #f1f5f9;
    color: #475569;
    padding: 3px 8px;
    border-radius: 4px;
}}

.quiz-card-a {{
    margin-top: 20px;
    padding-top: 18px;
    border-top: 1px dashed var(--border);
    animation: fadeIn 0.25s ease-in-out;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.quiz-card-action-hint {{
    margin-top: 24px;
    font-size: 8pt;
    color: var(--text-muted);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.quiz-controls-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 18px;
    flex-wrap: wrap;
    gap: 12px;
}}

/* Flashcards List */
.flashcard-wrap {{
    max-width: 650px;
    margin: 16px auto;
}}

.flashcard {{
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 24px 20px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    margin-bottom: 16px;
    transition: all 0.2s;
}}

.flashcard.mastered {{
    border-color: #86efac;
    background-color: rgba(240, 253, 244, 0.5);
}}

.flashcard:hover {{
    border-color: var(--primary);
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}}

.flashcard-q {{
    font-size: 10.5pt;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 10px;
}}

.flashcard-a {{
    font-size: 10pt;
    color: var(--text-main);
    line-height: 1.6;
    display: none;
    border-top: 1px dashed var(--border);
    padding-top: 12px;
}}

.flashcard-hint {{
    font-size: 7.5pt;
    color: var(--text-muted);
    margin-top: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Modal */
#modal {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0,0,0,0.85);
    z-index: 1000;
    justify-content: center;
    align-items: center;
    cursor: zoom-out;
}}

#modal img {{
    max-width: 92vw;
    max-height: 92vh;
    border-radius: var(--radius-sm);
    box-shadow: 0 4px 30px rgba(0,0,0,0.5);
}}

/* Mobile Drawer Overlay */
#sidebar-backdrop {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0,0,0,0.4);
    z-index: 40;
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    #sidebar {{
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        transform: translateX(-100%);
    }}
    #sidebar.open {{
        transform: translateX(0);
    }}
    #sidebar-backdrop.active {{
        display: block;
    }}
    .mobile-menu-btn {{
        display: flex;
    }}
    .content-body {{
        padding: 16px;
    }}
    .dashboard-grid {{
        grid-template-columns: 1fr 1fr;
    }}
    .topic-title-display {{
        font-size: 16pt;
    }}
    .dash-hero-card {{
        flex-direction: column-reverse;
        padding: 20px;
    }}
    .dash-hero-image-box {{
        width: 100%;
        max-width: 100%;
        max-height: 180px;
    }}
    .dash-hero-img {{
        max-height: 180px;
        object-position: center 30%;
    }}
}}

@media (max-width: 600px) {{
    .content-body {{
        padding: 12px;
    }}
    .dashboard-grid {{
        grid-template-columns: 1fr;
    }}
    .dashboard-topic-cards {{
        grid-template-columns: 1fr;
    }}
    .dash-hero-title {{
        font-size: 15pt;
    }}
    .dash-hero-meta {{
        gap: 8px;
    }}
    .quiz-controls-row {{
        flex-direction: column;
        gap: 10px;
    }}
    .quiz-controls-row button {{
        width: 100%;
    }}
    .quiz-controls-row div {{
        width: 100%;
        display: flex;
        gap: 8px;
    }}
    .quiz-controls-row div button {{
        flex: 1;
    }}
    .filter-chips {{
        overflow-x: auto;
        white-space: nowrap;
        padding-bottom: 4px;
        -webkit-overflow-scrolling: touch;
    }}
    .topic-actions {{
        width: 100%;
    }}
    .toggle-complete-btn {{
        width: 100%;
        justify-content: center;
    }}
}}
</style>
</head>
<body>

<div id="sidebar-backdrop" onclick="toggleSidebar(false)"></div>

<div id="sidebar">
    <div class="sidebar-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            {ICONS["modern_logo"]}
            <div>
                <div class="brand-title">SURGERY<span class="brand-accent">PRO</span></div>
                <div class="brand-sub">University Exam Monograph</div>
            </div>
        </div>
        <button class="mobile-sidebar-close-btn" onclick="toggleSidebar(false)" aria-label="Close Sidebar">{ICONS["close"]}</button>
    </div>

    <div class="sidebar-nav-actions">
        <button class="nav-btn active" id="btnNavDash" onclick="openDashboardView()">{ICONS["dashboard"]} Dashboard</button>
        <button class="nav-btn" onclick="openPdfModal()">{ICONS["pdf"]} Open PDF</button>
    </div>

    <div class="search-box">
        <span class="search-icon-pos">{ICONS["search"]}</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Search topics, signs, procedures...">
    </div>

    <div class="topic-list" id="topicList"></div>
</div>

<div id="main-view">
    <div class="top-bar">
        <button class="mobile-menu-btn" onclick="toggleSidebar(true)">{ICONS["menu"]}</button>
        
        <div class="tabs-nav-wrapper" id="topicTabsNav" style="display: none;">
            <button class="tabs-arrow-btn left" id="tabArrowLeft" onclick="scrollTabsNav(-150)" title="Scroll tabs left">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <div class="top-tabs-scroll" id="topicTabsBar" onscroll="updateTabScrollButtons()">
                <button class="tab-btn active" data-tab="master" onclick="switchTopicTab('master')">{ICONS["master_answer"]} 15-Mark Master Answer</button>
                <button class="tab-btn" data-tab="layman" onclick="switchTopicTab('layman')">{ICONS["layman"]} Layman's Intuition</button>
                <button class="tab-btn" data-tab="types" id="tabBtnTypes" style="display: none;" onclick="switchTopicTab('types')">{ICONS["quiz"]} Types & Subtypes</button>
                <button class="tab-btn" data-tab="diagrams" onclick="switchTopicTab('diagrams')">{ICONS["diagrams"]} Diagrams Gallery</button>
                <button class="tab-btn" data-tab="viva" onclick="switchTopicTab('viva')">{ICONS["viva"]} Viva Pearls</button>
                <button class="tab-btn" data-tab="quiz" onclick="switchTopicTab('quiz')">{ICONS["quiz"]} Flashcard Quiz</button>
                <button class="tab-btn" data-tab="notes" onclick="switchTopicTab('notes')">{ICONS["notes"]} My Notes</button>
            </div>
            <button class="tabs-arrow-btn right" id="tabArrowRight" onclick="scrollTabsNav(150)" title="Scroll tabs right">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
        </div>

        <div id="dashTitleBar" style="font-weight: 700; color: var(--primary); font-size: 11pt; display: flex; align-items: center; gap: 6px;">
            {ICONS["dashboard"]} Exam Preparation Dashboard
        </div>

        <div class="top-right-tools">
            <button class="btn btn-secondary" onclick="openPdfModal()" style="padding: 5px 12px; font-size: 8pt;">{ICONS["pdf"]} PDF Reader</button>
            <button class="icon-btn" onclick="toggleDarkMode()" title="Toggle Dark/Light Mode">{ICONS["moon"]}</button>
        </div>
    </div>

    <div class="mobile-section-nav" id="mobileSectionNav">
        <div class="mobile-section-header">
            <span class="mobile-section-indicator-badge">
                <span class="pulse-dot"></span>
                <span id="mobileActiveTabLabel">15-Mark Master Answer</span>
            </span>
            <span class="mobile-swipe-hint-text">⟷ Swipe tabs above or tap shortcuts below</span>
        </div>
        <div class="mobile-section-quick-pills">
            <button class="pill-shortcut active" data-pill="master" onclick="switchTopicTab('master')">Answer</button>
            <button class="pill-shortcut" data-pill="layman" onclick="switchTopicTab('layman')">Layman</button>
            <button class="pill-shortcut" data-pill="types" id="pillTypes" style="display: none;" onclick="switchTopicTab('types')">Types</button>
            <button class="pill-shortcut" data-pill="diagrams" onclick="switchTopicTab('diagrams')">Diagrams</button>
            <button class="pill-shortcut" data-pill="viva" onclick="switchTopicTab('viva')">Viva</button>
            <button class="pill-shortcut" data-pill="quiz" onclick="switchTopicTab('quiz')">Quiz</button>
            <button class="pill-shortcut" data-pill="notes" onclick="switchTopicTab('notes')">Notes</button>
        </div>
    </div>

    <div class="content-body" id="contentArea"></div>
</div>

<div id="modal" onclick="closeModal()">
    <img id="modalImg" src="" alt="Enlarged Diagram">
</div>

<div id="pdfModal" class="pdf-modal-overlay" style="display: none;">
    <div class="pdf-modal-container">
        <div class="pdf-modal-header">
            <div style="display: flex; align-items: center; gap: 8px;">
                {ICONS["pdf"]}
                <span style="font-weight: 700; font-size: 11pt; color: var(--text-main);">General Surgery Master Compendium Monograph</span>
            </div>
            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                <a href="General_Surgery_Master_Notes.pdf" target="_blank" class="btn btn-secondary" style="padding: 4px 12px; font-size: 8pt;">Open in New Tab</a>
                <a href="https://raw.githubusercontent.com/Krrish41/general-surgery/main/General_Surgery_Master_Notes.pdf" target="_blank" class="btn btn-primary" style="padding: 4px 12px; font-size: 8pt;">Online Mirror (For Tablets)</a>
                <a href="General_Surgery_Master_Notes.pdf" download="General_Surgery_Master_Notes.pdf" class="btn btn-secondary" style="padding: 4px 12px; font-size: 8pt;">Download PDF</a>
                <button class="icon-btn" onclick="closePdfModal()">{ICONS["close"]}</button>
            </div>
        </div>
        <div class="pdf-tablet-notice">
            <strong>Device & Tablet Access:</strong> If your iPad, tablet, or phone cannot open local files, tap <strong>"Online Mirror (For Tablets)"</strong> above to stream the compiled PDF directly from the cloud repository without downloading.
        </div>
        <iframe id="pdfIframe" src="" class="pdf-iframe-view" title="General Surgery Master PDF Reader"></iframe>
    </div>
</div>

<script>
const CHAPTERS = {chapters_json};
const DIAGRAMS = {images_json};
const PRESETS = {presets_json};
const SVG_ICONS = {{
    check: '{ICONS["check_circle"]}',
    circle: '{ICONS["circle"]}',
    notes: '{ICONS["notes"]}'
}};

let currentChapterIdx = -1; // -1 means Dashboard landing view
let currentTopicTab = 'master';
let currentDashFilter = 'all';

// State stored in localStorage
let completedTopics = JSON.parse(localStorage.getItem('surgery_completed_topics') || '{{}}');
let quizCardIdx = 0;
let quizViewMode = 'carousel';
let quizAnswerRevealed = false;
let quizMastered = JSON.parse(localStorage.getItem('surgery_quiz_mastered') || '{{}}');

function saveQuizMastery(qKey, isMastered) {{
    if (isMastered) {{
        quizMastered[qKey] = true;
    }} else {{
        delete quizMastered[qKey];
    }}
    localStorage.setItem('surgery_quiz_mastered', JSON.stringify(quizMastered));
    renderTopicView();
}}

function nextQuizCard(total) {{
    if (quizCardIdx < total - 1) {{
        quizCardIdx++;
        quizAnswerRevealed = false;
        renderTopicView();
    }}
}}

function prevQuizCard() {{
    if (quizCardIdx > 0) {{
        quizCardIdx--;
        quizAnswerRevealed = false;
        renderTopicView();
    }}
}}

function toggleQuizReveal() {{
    quizAnswerRevealed = !quizAnswerRevealed;
    renderTopicView();
}}

function toggleQuizMode() {{
    quizViewMode = quizViewMode === 'carousel' ? 'list' : 'carousel';
    quizAnswerRevealed = false;
    renderTopicView();
}}

function saveCompletion(chId, state) {{
    if (state) {{
        completedTopics[chId] = true;
    }} else {{
        delete completedTopics[chId];
    }}
    localStorage.setItem('surgery_completed_topics', JSON.stringify(completedTopics));
    renderSidebar(document.getElementById('searchInput').value);
    if (currentChapterIdx === -1) {{
        renderDashboard();
    }} else {{
        renderTopicView();
    }}
}}

function getTopicNotes(chId) {{
    return localStorage.getItem('surgery_notes_' + chId) || '';
}}

function saveTopicNotes(chId, text) {{
    localStorage.setItem('surgery_notes_' + chId, text);
    const statEl = document.getElementById('noteStatusMsg');
    if (statEl) {{
        statEl.innerText = 'Notes saved automatically';
    }}
}}

function toggleSidebar(open) {{
    const sb = document.getElementById('sidebar');
    const bd = document.getElementById('sidebar-backdrop');
    if (open) {{
        sb.classList.add('open');
        bd.classList.add('active');
    }} else {{
        sb.classList.remove('open');
        bd.classList.remove('active');
    }}
}}

function renderSidebar(filterText = '') {{
    const container = document.getElementById('topicList');
    container.innerHTML = '';
    const q = filterText.toLowerCase();

    CHAPTERS.forEach((ch, idx) => {{
        if (q && !ch.title.toLowerCase().includes(q) && !JSON.stringify(ch.sections).toLowerCase().includes(q)) {{
            return;
        }}
        const isDone = !!completedTopics[ch.id];
        const item = document.createElement('div');
        item.className = `topic-item ${{idx === currentChapterIdx ? 'active' : ''}}`;
        item.innerHTML = `
            <button class="topic-check-btn" onclick="event.stopPropagation(); saveCompletion('${{ch.id}}', ${{!isDone}})">
                ${{isDone ? SVG_ICONS.check : SVG_ICONS.circle}}
            </button>
            <span class="topic-title-text" onclick="selectChapter(${{idx}})">${{idx + 1}}. ${{ch.title}}</span>
        `;
        container.appendChild(item);
    }});
}}

function openDashboardView() {{
    currentChapterIdx = -1;
    document.getElementById('btnNavDash').classList.add('active');
    document.getElementById('topicTabsNav').style.display = 'none';
    const mobNav = document.getElementById('mobileSectionNav');
    if (mobNav) mobNav.classList.remove('active');
    document.getElementById('dashTitleBar').style.display = 'flex';
    renderSidebar(document.getElementById('searchInput').value);
    renderDashboard();
    toggleSidebar(false);
}}

function scrollTabsNav(offset) {{
    const bar = document.getElementById('topicTabsBar');
    if (bar) {{
        bar.scrollBy({{ left: offset, behavior: 'smooth' }});
        setTimeout(updateTabScrollButtons, 220);
    }}
}}

function updateTabScrollButtons() {{
    const bar = document.getElementById('topicTabsBar');
    const wrapper = document.getElementById('topicTabsNav');
    const leftBtn = document.getElementById('tabArrowLeft');
    const rightBtn = document.getElementById('tabArrowRight');
    if (!bar || !wrapper) return;

    const scrollLeft = bar.scrollLeft;
    const maxScroll = bar.scrollWidth - bar.clientWidth;

    if (leftBtn) {{
        if (scrollLeft <= 4) leftBtn.classList.add('is-hidden');
        else leftBtn.classList.remove('is-hidden');
    }}

    if (rightBtn) {{
        if (scrollLeft >= maxScroll - 4) rightBtn.classList.add('is-hidden');
        else rightBtn.classList.remove('is-hidden');
    }}

    if (scrollLeft > 4) wrapper.classList.add('can-scroll-left');
    else wrapper.classList.remove('can-scroll-left');

    if (scrollLeft < maxScroll - 4) wrapper.classList.add('can-scroll-right');
    else wrapper.classList.remove('can-scroll-right');
}}

function selectChapter(idx) {{
    currentChapterIdx = idx;
    quizCardIdx = 0;
    quizAnswerRevealed = false;
    document.getElementById('btnNavDash').classList.remove('active');
    document.getElementById('topicTabsNav').style.display = 'flex';
    const mobNav = document.getElementById('mobileSectionNav');
    if (mobNav) mobNav.classList.add('active');
    document.getElementById('dashTitleBar').style.display = 'none';
    
    // Check if preset exists for Types tab
    const hasPreset = !!PRESETS[CHAPTERS[idx].id];
    document.getElementById('tabBtnTypes').style.display = hasPreset ? 'flex' : 'none';
    const pillTypes = document.getElementById('pillTypes');
    if (pillTypes) pillTypes.style.display = hasPreset ? 'inline-block' : 'none';

    if (!hasPreset && currentTopicTab === 'types') {{
        currentTopicTab = 'master';
    }}

    renderSidebar(document.getElementById('searchInput').value);
    switchTopicTab(currentTopicTab);
    toggleSidebar(false);
    setTimeout(updateTabScrollButtons, 150);
}}

function switchTopicTab(tab) {{
    currentTopicTab = tab;

    // Highlight top bar tab & auto-scroll into view
    document.querySelectorAll('.tab-btn').forEach(btn => {{
        if (btn.getAttribute('data-tab') === tab) {{
            btn.classList.add('active');
            btn.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
        }} else {{
            btn.classList.remove('active');
        }}
    }});

    // Highlight mobile quick-pills
    document.querySelectorAll('.pill-shortcut').forEach(pill => {{
        if (pill.getAttribute('data-pill') === tab) {{
            pill.classList.add('active');
            pill.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
        }} else {{
            pill.classList.remove('active');
        }}
    }});

    const tabTitles = {{
        'master': '15-Mark Master Answer',
        'layman': "Layman's Intuition",
        'types': 'Types & Subtypes Explorer',
        'diagrams': 'Diagrams Gallery',
        'viva': 'Examiner Viva Pearls',
        'quiz': 'Active Recall Flashcard Quiz',
        'notes': 'My Clinical Notes'
    }};
    const labelEl = document.getElementById('mobileActiveTabLabel');
    if (labelEl) {{
        labelEl.innerText = tabTitles[tab] || tab;
    }}

    updateTabScrollButtons();
    renderTopicView();
}}

function renderDashboard() {{
    const total = CHAPTERS.length;
    const completedCount = Object.keys(completedTopics).length;
    const remainingCount = total - completedCount;
    const pct = Math.round((completedCount / total) * 100);

    let notesCount = 0;
    CHAPTERS.forEach(ch => {{
        if (getTopicNotes(ch.id).trim().length > 0) notesCount++;
    }});

    let html = `
        <div class="dash-hero-card">
            <div style="flex: 1;">
                <span class="dash-hero-badge">MBBS & MS GENERAL SURGERY PORTAL</span>
                <h1 class="dash-hero-title">General Surgery Master Exam Hub</h1>
                <p class="dash-hero-sub">15-Mark University Essay Blueprints • Clinical Examination Signs • Examiner Viva Pearls</p>
                <div class="dash-hero-meta">
                    <span class="dash-hero-stat"><strong>${{total}}</strong> University Topics</span>
                    <span class="dash-hero-stat"><strong style="color: #4ade80;">${{completedCount}}</strong> Completed</span>
                    <span class="dash-hero-stat"><strong style="color: #38bdf8;">${{pct}}%</strong> Syllabus Ready</span>
                </div>
            </div>
            ${{DIAGRAMS['surgery_dashboard_banner.jpg'] ? `
            <div class="dash-hero-image-box">
                <img src="${{DIAGRAMS['surgery_dashboard_banner.jpg']}}" alt="Surgical Dashboard" class="dash-hero-img">
            </div>` : ''}}
        </div>

        <div class="dash-cheat-sheet-card">
            <div style="display: flex; align-items: center; gap: 16px; flex: 1;">
                <div class="cheat-sheet-badge-icon">{ICONS["cheat_sheet"]}</div>
                <div>
                    <div style="font-size: 8pt; font-weight: 700; color: #d8b4fe; text-transform: uppercase; letter-spacing: 1px;">Exam Night Rapid Revision</div>
                    <div style="font-size: 13pt; font-weight: 700; color: #ffffff;">Chapter 24: Master Surgery Cheat Sheet</div>
                    <div style="font-size: 8.5pt; color: #e9d5ff; margin-top: 2px;">
                        Exhaustive high-yield formulas, keywords, named clinical signs, classifications & shock matrices for rapid pre-exam glance.
                    </div>
                </div>
            </div>
            <button class="btn btn-primary" onclick="selectChapter(23)" style="background: #ffffff; color: #6d28d9; font-weight: 700; padding: 10px 22px; font-size: 9pt; box-shadow: 0 4px 14px rgba(0,0,0,0.25);">
                Open Cheat Sheet →
            </button>
        </div>

        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-label">Total University Topics</div>
                <div class="stat-val">${{total}}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Topics Completed</div>
                <div class="stat-val" style="color: var(--success);">${{completedCount}}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Topics Remaining</div>
                <div class="stat-val" style="color: var(--accent);">${{remainingCount}}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Topics with Notes</div>
                <div class="stat-val">${{notesCount}}</div>
            </div>
        </div>

        <div class="progress-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 10pt;">
                <span>University Syllabus Completion</span>
                <span style="color: var(--primary);">${{pct}}%</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: ${{pct}}%;"></div>
            </div>
        </div>

        <div style="margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
            <h2 style="font-size: 12pt; font-weight: 700; color: var(--text-main);">Study Plan Topics</h2>
            <div class="filter-chips">
                <button class="chip ${{currentDashFilter === 'all' ? 'active' : ''}}" onclick="setDashFilter('all')">All Topics (${{total}})</button>
                <button class="chip ${{currentDashFilter === 'pending' ? 'active' : ''}}" onclick="setDashFilter('pending')">Pending (${{remainingCount}})</button>
                <button class="chip ${{currentDashFilter === 'completed' ? 'active' : ''}}" onclick="setDashFilter('completed')">Completed (${{completedCount}})</button>
                <button class="chip ${{currentDashFilter === 'notes' ? 'active' : ''}}" onclick="setDashFilter('notes')">Has Notes (${{notesCount}})</button>
                <button class="chip" onclick="selectChapter(23)" style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); color: #ffffff; border: none;">⚡ Cheat Sheet</button>
            </div>
        </div>

        <div class="dashboard-topic-cards">
    `;

    CHAPTERS.forEach((ch, idx) => {{
        const isDone = !!completedTopics[ch.id];
        const hasNote = getTopicNotes(ch.id).trim().length > 0;

        if (currentDashFilter === 'completed' && !isDone) return;
        if (currentDashFilter === 'pending' && isDone) return;
        if (currentDashFilter === 'notes' && !hasNote) return;

        html += `
            <div class="dash-card ${{isDone ? 'completed' : ''}}">
                <div>
                    <div class="dash-card-header">
                        <span style="font-size: 8pt; font-weight: 700; color: var(--primary); text-transform: uppercase;">Chapter ${{idx + 1}}</span>
                        ${{hasNote ? '<span style="font-size: 7.5pt; background: #f3e8ff; color: #6d28d9; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Note Saved</span>' : ''}}
                    </div>
                    <div class="dash-card-title">${{ch.title}}</div>
                    <div class="dash-card-source">${{ch.source}}</div>
                </div>
                <div class="dash-card-footer">
                    <button class="toggle-complete-btn ${{isDone ? 'is-completed' : ''}}" onclick="saveCompletion('${{ch.id}}', ${{!isDone}})">
                        ${{isDone ? SVG_ICONS.check + ' Completed' : SVG_ICONS.circle + ' Mark Done'}}
                    </button>
                    <button class="btn btn-primary" onclick="selectChapter(${{idx}})" style="padding: 6px 16px; font-size: 8.5pt;">Study →</button>
                </div>
            </div>
        `;
    }});

    html += `</div>`;
    document.getElementById('contentArea').innerHTML = html;
}}

function setDashFilter(filter) {{
    currentDashFilter = filter;
    renderDashboard();
}}

function renderTopicView() {{
    const ch = CHAPTERS[currentChapterIdx];
    const isDone = !!completedTopics[ch.id];
    const userNote = getTopicNotes(ch.id);

    let html = `
        <div class="topic-header-bar">
            <div>
                <div style="font-size: 8.5pt; text-transform: uppercase; letter-spacing: 1.5px; color: var(--primary); font-weight: 700;">Chapter ${{currentChapterIdx + 1}}</div>
                <div class="topic-title-display">${{ch.title}}</div>
                <div style="font-size: 8.5pt; color: var(--text-muted);">${{ch.source}}</div>
            </div>
            <div class="topic-actions">
                <button class="toggle-complete-btn ${{isDone ? 'is-completed' : ''}}" onclick="saveCompletion('${{ch.id}}', ${{!isDone}})">
                    ${{isDone ? SVG_ICONS.check + ' Topic Completed' : SVG_ICONS.circle + ' Mark as Completed'}}
                </button>
            </div>
        </div>
    `;

    if (currentTopicTab === 'master') {{
        html += `
            <div class="prompt-box">
                <div style="font-weight: 700; text-transform: uppercase; font-size: 8pt; margin-bottom: 4px;">University 15-Mark Examination Prompt</div>
                <div>${{ch.essay_prompt}}</div>
            </div>

            <div class="layman-box">
                <div style="font-weight: 700; text-transform: uppercase; font-size: 8pt; margin-bottom: 4px;">Layman's Intuitive Analogy</div>
                <div>${{ch.layman_explanation}}</div>
            </div>
        `;

        // Render sections with cleaned formatting
        for (const [secName, secHtml] of Object.entries(ch.sections)) {{
            const titleFormatted = secName.replace(/_/g, ' ').toUpperCase();
            html += `
                <div class="card">
                    <div class="card-title">${{titleFormatted}}</div>
                    <div style="line-height: 1.7;">${{secHtml}}</div>
                </div>
            `;
        }}

        if (ch.viva_pearls && ch.viva_pearls.length > 0) {{
            html += `
                <div class="viva-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                        <h4 style="margin: 0; display: flex; align-items: center; gap: 8px; font-size: 11pt; color: #b45309;">
                            {ICONS["viva"]} High-Yield Clinical & Viva Examiner Pearls
                        </h4>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <button class="btn btn-secondary" onclick="toggleVivaAnswers()" id="btnVivaAnswersToggle" style="padding: 4px 12px; font-size: 8pt;">
                                Hide / Show Answers
                            </button>
                            <button class="btn btn-primary" onclick="switchTopicTab('quiz')" style="padding: 4px 12px; font-size: 8pt;">
                                Practice Flashcards →
                            </button>
                        </div>
                    </div>
                    <div class="viva-pearls-container" id="vivaContainer">
            `;
            ch.viva_pearls.forEach((p, pIdx) => {{
                let qText = p;
                let aText = "";
                if (p.includes('?')) {{
                    const qEnd = p.indexOf('?') + 1;
                    qText = p.substring(0, qEnd).trim();
                    aText = p.substring(qEnd).trim();
                }}
                if (aText) {{
                    html += `
                        <div class="viva-qa-block">
                            <div style="display: flex; align-items: flex-start; gap: 8px;">
                                <span class="viva-badge-q">Q${{pIdx + 1}}</span>
                                <div style="font-weight: 600; color: var(--primary); font-size: 9.5pt; line-height: 1.5;">${{qText}}</div>
                            </div>
                            <div class="viva-a-row">
                                <strong class="viva-model-label">Model Answer: </strong>
                                <span>${{aText}}</span>
                            </div>
                        </div>
                    `;
                }} else {{
                    html += `
                        <div class="viva-qa-block" style="padding: 10px 14px; background: rgba(245, 158, 11, 0.06); border-left: 3px solid var(--accent); border-radius: 4px; font-size: 9pt; line-height: 1.6;">
                            <strong style="color: #b45309;">Clinical Pearl ${{pIdx + 1}}: </strong>
                            <span>${{p}}</span>
                        </div>
                    `;
                }}
            }});
            html += `</div></div>`;
        }}
    }} else if (currentTopicTab === 'layman') {{
        html += `
            <div class="card" style="padding: 28px;">
                <div class="card-title">Layman's Analogy & Conceptual Intuition</div>
                <p style="font-size: 11pt; line-height: 1.8; color: var(--text-main);">
                    ${{ch.layman_explanation}}
                </p>
            </div>
        `;
    }} else if (currentTopicTab === 'types') {{
        const preset = PRESETS[ch.id];
        if (preset) {{
            html += `
                <div class="interactive-types-container">
                    <h3 style="font-size: 12pt; color: var(--primary); margin-bottom: 12px;">${{preset.title}}</h3>
                    <div class="type-buttons-bar">
            `;
            preset.types.forEach((t, tIdx) => {{
                html += `<button class="type-btn ${{tIdx === 0 ? 'active' : ''}}" onclick="showTypeDetail('${{ch.id}}', ${{tIdx}})">${{t.name}}</button>`;
            }});
            html += `
                    </div>
                    <div id="typeDetailSlot" class="type-detail-card">
                        <div class="type-detail-header">
                            <span class="type-detail-title">${{preset.types[0].name}}</span>
                            <span class="type-badge">${{preset.types[0].badge}}</span>
                        </div>
                        <div class="type-hemodynamics">${{preset.types[0].hemodynamics}}</div>
                        <p class="content-para">${{preset.types[0].summary}}</p>
                    </div>
                </div>
            `;
        }} else {{
            html += `<p style="color: var(--text-muted);">No separate interactive presets for this chapter.</p>`;
        }}
    }} else if (currentTopicTab === 'diagrams') {{
        html += `<div class="card"><div class="card-title">Original Schematics & Anatomical Diagrams</div>`;
        if (ch.diagrams && ch.diagrams.length > 0) {{
            html += `<div class="diagram-gallery">`;
            ch.diagrams.forEach(d => {{
                const b64 = DIAGRAMS[d.filename] || '';
                if (b64) {{
                    const isOrig = d.filename.startsWith('ch') || d.title.toLowerCase().includes('handwritten') || d.title.toLowerCase().includes('notebook');
                    const badgeHtml = isOrig
                        ? '<span class="diagram-type-badge badge-original">Original Handwritten Note</span>'
                        : '<span class="diagram-type-badge badge-hd">High-Res 300 DPI Medical Schematic</span>';
                    html += `
                        <div class="diagram-item">
                            <div class="diagram-header-badge">${{badgeHtml}}</div>
                            <img src="${{b64}}" onclick="openModal('${{b64}}')" alt="${{d.title}}">
                            <div class="diagram-item-caption">${{d.title}}</div>
                        </div>
                    `;
                }}
            }});
            html += `</div>`;
        }} else {{
            html += `<p style="color: var(--text-muted); font-size: 9.5pt;">No diagrams available for this chapter.</p>`;
        }}
        html += `</div>`;
    }} else if (currentTopicTab === 'viva') {{
        html += `<div class="card"><div class="card-title">Examiner Viva & Practical Clinical Pearls</div><ul class="content-list">`;
        (ch.viva_pearls || []).forEach(p => {{
            html += `<li>${{p}}</li>`;
        }});
        html += `</ul></div>`;
    }} else if (currentTopicTab === 'quiz') {{
        const pearls = ch.viva_pearls || [];
        const totalCards = pearls.length;
        if (quizCardIdx >= totalCards) quizCardIdx = 0;
        if (quizCardIdx < 0) quizCardIdx = totalCards - 1;

        let masteredInTopic = 0;
        pearls.forEach((p, pIdx) => {{
            const key = ch.id + '_q_' + pIdx;
            if (quizMastered[key]) masteredInTopic++;
        }});

        html += `
            <div class="quiz-container">
                <div class="quiz-top-bar">
                    <div>
                        <h3 style="font-size: 13pt; font-weight: 700; color: var(--text-main); margin: 0 0 4px 0;">
                            Active Recall Viva Deck
                        </h3>
                        <div style="font-size: 8.5pt; color: var(--text-muted);">
                            Chapter ${{currentChapterIdx + 1}}: ${{ch.title}}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                        <span class="quiz-score-badge">
                            Mastered: <strong>${{masteredInTopic}} / ${{totalCards}}</strong>
                        </span>
                        <button class="btn btn-secondary" onclick="toggleQuizMode()" style="padding: 5px 12px; font-size: 8.5pt;">
                            ${{quizViewMode === 'carousel' ? 'Switch to All Cards List' : 'Switch to Interactive Deck'}}
                        </button>
                    </div>
                </div>
        `;

        if (totalCards === 0) {{
            html += `<p style="color: var(--text-muted); padding: 24px; text-align: center;">No flashcards available for this chapter.</p></div>`;
        }} else if (quizViewMode === 'carousel') {{
            const currPearl = pearls[quizCardIdx];
            const parts = currPearl.split('?');
            const qText = parts[0] + '?';
            const aText = parts.slice(1).join('?');
            const qKey = ch.id + '_q_' + quizCardIdx;
            const isMastered = !!quizMastered[qKey];

            html += `
                <div class="quiz-carousel-wrapper">
                    <div class="quiz-progress-text">
                        <span>Card ${{quizCardIdx + 1}} of ${{totalCards}}</span>
                        <span style="color: ${{isMastered ? 'var(--success)' : 'var(--text-muted)'}}; font-weight: 600;">
                            ${{isMastered ? SVG_ICONS.check + ' Mastered' : 'Needs Practice'}}
                        </span>
                    </div>

                    <div class="quiz-flashcard-box" onclick="toggleQuizReveal()">
                        <div class="quiz-card-q">
                            <span class="quiz-badge">Question / Viva Probe</span>
                            <div style="font-size: 12pt; font-weight: 600; color: var(--primary); margin-top: 8px; line-height: 1.5;">
                                ${{qText}}
                            </div>
                        </div>
                        
                        <div class="quiz-card-a" style="display: ${{quizAnswerRevealed ? 'block' : 'none'}};">
                            <span class="quiz-badge quiz-badge-model">Examiner Model Answer</span>
                            <div style="font-size: 11pt; color: var(--text-main); margin-top: 8px; line-height: 1.6;">
                                ${{aText}}
                            </div>
                        </div>

                        <div class="quiz-card-action-hint">
                            ${{quizAnswerRevealed ? 'Click card to hide answer' : 'Click anywhere on card to reveal answer'}}
                        </div>
                    </div>

                    <div class="quiz-controls-row">
                        <button class="btn btn-secondary" onclick="prevQuizCard()" ${{quizCardIdx === 0 ? 'disabled' : ''}} style="min-width: 105px;">
                            ← Previous
                        </button>
                        <div style="display: flex; gap: 8px;">
                            <button class="btn btn-secondary" onclick="toggleQuizReveal()">
                                ${{quizAnswerRevealed ? 'Hide Answer' : 'Show Answer'}}
                            </button>
                            <button class="btn ${{isMastered ? 'btn-secondary' : 'btn-primary'}}" onclick="saveQuizMastery('${{qKey}}', ${{!isMastered}})">
                                ${{isMastered ? '✓ Mastered' : '★ I Knew This'}}
                            </button>
                        </div>
                        <button class="btn btn-secondary" onclick="nextQuizCard(${{totalCards}})" ${{quizCardIdx === totalCards - 1 ? 'disabled' : ''}} style="min-width: 105px;">
                            Next →
                        </button>
                    </div>
                </div>
            </div>
            `;
        }} else {{
            // List view
            html += `<div class="quiz-list-wrapper">`;
            pearls.forEach((p, pIdx) => {{
                const parts = p.split('?');
                const qText = parts[0] + '?';
                const aText = parts.slice(1).join('?');
                const qKey = ch.id + '_q_' + pIdx;
                const isMastered = !!quizMastered[qKey];
                html += `
                    <div class="flashcard ${{isMastered ? 'mastered' : ''}}" onclick="toggleCard(this)">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <span style="font-size: 8pt; font-weight: 700; color: var(--primary);">Card ${{pIdx + 1}}</span>
                            <button class="toggle-complete-btn ${{isMastered ? 'is-completed' : ''}}" onclick="event.stopPropagation(); saveQuizMastery('${{qKey}}', ${{!isMastered}})" style="padding: 2px 8px; font-size: 7.5pt;">
                                ${{isMastered ? SVG_ICONS.check + ' Mastered' : SVG_ICONS.circle + ' Mark Known'}}
                            </button>
                        </div>
                        <div class="flashcard-q">Q: ${{qText}}</div>
                        <div class="flashcard-a">${{aText}}</div>
                        <div class="flashcard-hint">Click card to reveal answer</div>
                    </div>
                `;
            }});
            html += `</div></div>`;
        }}
    }} else if (currentTopicTab === 'notes') {{
        html += `
            <div class="card">
                <div class="card-title">My Personal Study & Revision Notes</div>
                <div class="notes-container">
                    <textarea class="notes-textarea" id="userTopicNotesArea" placeholder="Type your personal mnemonic, exam tips, clinical ward observations, or revision notes here...">${{userNote}}</textarea>
                    <div class="notes-status" id="noteStatusMsg">Saved automatically to your device</div>
                </div>
            </div>
        `;
    }}

    document.getElementById('contentArea').innerHTML = html;

    // Attach auto-save listener if notes tab
    if (currentTopicTab === 'notes') {{
        const area = document.getElementById('userTopicNotesArea');
        if (area) {{
            area.addEventListener('input', (e) => {{
                saveTopicNotes(ch.id, e.target.value);
            }});
        }}
    }}
}}

function showTypeDetail(chId, tIdx) {{
    const preset = PRESETS[chId];
    if (!preset) return;
    const t = preset.types[tIdx];
    const slot = document.getElementById('typeDetailSlot');
    if (!slot) return;

    document.querySelectorAll('.type-btn').forEach((btn, idx) => {{
        if (idx === tIdx) btn.classList.add('active');
        else btn.classList.remove('active');
    }});

    slot.innerHTML = `
        <div class="type-detail-header">
            <span class="type-detail-title">${{t.name}}</span>
            <span class="type-badge">${{t.badge}}</span>
        </div>
        <div class="type-hemodynamics">${{t.hemodynamics}}</div>
        <p class="content-para">${{t.summary}}</p>
    `;
}}

function toggleCard(el) {{
    const a = el.querySelector('.flashcard-a');
    const hint = el.querySelector('.flashcard-hint');
    if (a.style.display === 'block') {{
        a.style.display = 'none';
        hint.innerText = 'Click card to reveal answer';
    }} else {{
        a.style.display = 'block';
        hint.innerText = 'Click card to hide answer';
    }}
}}

function openModal(src) {{
    const m = document.getElementById('modal');
    document.getElementById('modalImg').src = src;
    m.style.display = 'flex';
}}

function closeModal() {{
    document.getElementById('modal').style.display = 'none';
}}

function openPdfModal() {{
    const modal = document.getElementById('pdfModal');
    const iframe = document.getElementById('pdfIframe');
    if (modal && iframe) {{
        if (!iframe.src || iframe.src === 'about:blank' || iframe.src === window.location.href) {{
            iframe.src = 'General_Surgery_Master_Notes.pdf';
        }}
        modal.style.display = 'flex';
    }}
}}

function closePdfModal() {{
    const modal = document.getElementById('pdfModal');
    if (modal) {{
        modal.style.display = 'none';
    }}
}}

let vivaAnswersVisible = true;
function toggleVivaAnswers() {{
    const container = document.getElementById('vivaContainer');
    const btn = document.getElementById('btnVivaAnswersToggle');
    if (container) {{
        vivaAnswersVisible = !vivaAnswersVisible;
        if (vivaAnswersVisible) {{
            container.classList.remove('answers-hidden');
            if (btn) btn.innerText = 'Hide Answers';
        }} else {{
            container.classList.add('answers-hidden');
            if (btn) btn.innerText = 'Show Answers';
        }}
    }}
}}

function toggleDarkMode() {{
    document.body.classList.toggle('dark');
}}

document.getElementById('searchInput').addEventListener('input', (e) => {{
    renderSidebar(e.target.value);
}});

// Initialize on Dashboard view
renderSidebar();
renderDashboard();
</script>
</body>
</html>
"""
    return html

def main():
    print("Loading base64 diagram assets...")
    b64_images = load_diagrams_b64()
    print(f"Loaded {len(b64_images)} diagram images.")

    print("Generating Markdown compendium...")
    md_content = generate_markdown(ALL_CHAPTERS)
    with open("General_Surgery_Master_Notes.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Saved General_Surgery_Master_Notes.md")

    print("Generating Print-Ready HTML with clean LaTeX and table parsing...")
    html_content = generate_html(ALL_CHAPTERS, b64_images)
    with open("General_Surgery_Master_Notes.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Saved General_Surgery_Master_Notes.html")

    print("Generating Interactive Study Dashboard Website...")
    site_content = generate_interactive_website(ALL_CHAPTERS, b64_images)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(site_content)
    print("Saved index.html")

    # Compiling to PDF via Headless Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_bin = None
    for p in edge_paths:
        if os.path.exists(p):
            browser_bin = p
            break

    if browser_bin:
        print(f"Compiling PDF via Headless Browser: {browser_bin}...")
        html_abs = os.path.abspath("General_Surgery_Master_Notes.html")
        pdf_abs = os.path.abspath("General_Surgery_Master_Notes.pdf")
        cmd = [
            browser_bin,
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_abs}",
            html_abs
        ]
        res = subprocess.run(cmd, capture_output=True)
        if os.path.exists(pdf_abs):
            size_mb = os.path.getsize(pdf_abs) / (1024 * 1024)
            print(f"Successfully compiled PDF: General_Surgery_Master_Notes.pdf ({size_mb:.2f} MB)")
        else:
            print("PDF generation failed:", res.stderr.decode('utf-8', 'ignore'))
    else:
        print("No headless browser found to compile PDF.")

if __name__ == "__main__":
    main()
