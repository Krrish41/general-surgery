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
from content.interactive_data import CLASSIFICATION_PRESETS, SPOTTER_HOTSPOTS, COMPARISON_PAIRS, EXAM_RUBRIC_CRITERIA

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
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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
    border: 3px double #0369a1;
    margin: 20px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
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
    color: #0369a1;
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
    background-color: #f0f9ff;
    color: #0369a1;
    border: 1px solid #bae6fd;
}}

.toc-page {{
    page-break-after: always;
    padding: 20px;
}}

.toc-title {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    color: #1e1b4b;
    border-bottom: 2px solid #0369a1;
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
    border-bottom: 2px solid #0369a1;
    padding-bottom: 8px;
    margin-bottom: 16px;
}}

.chapter-number {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #0369a1;
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
    color: #0369a1;
    margin: 14px 0 6px 0;
    border-left: 3px solid #0369a1;
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
        <div style="font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #0369a1; margin-bottom: 4px;">{badge_text}</div>
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
    spotters_json = json.dumps(SPOTTER_HOTSPOTS)
    pairs_json = json.dumps(COMPARISON_PAIRS)
    rubric_json = json.dumps(EXAM_RUBRIC_CRITERIA)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">
<link rel="manifest" href="manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Surgery Pro">
<meta name="theme-color" content="#0369a1">
<link rel="apple-touch-icon" href="{FAVICON_SVG}">
<title>General Surgery Master Portal - University Exam Companion</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
    --primary: #0369a1;
    --primary-dark: #075985;
    --primary-light: rgba(3, 105, 161, 0.08);
    --primary-border: rgba(3, 105, 161, 0.22);
    --bg-main: #fbfbfa;
    --bg-card: #ffffff;
    --bg-surface: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #475569;
    --border: #e2e8f0;
    --border-strong: #cbd5e1;
    --sidebar-w: 320px;
    --accent: #d97706;
    --accent-light: rgba(217, 119, 6, 0.1);
    --accent-crimson: #be123c;
    --danger: #ef4444;
    --success: #059669;
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06);
    --shadow-md: 0 4px 14px rgba(15, 23, 42, 0.08);
    --shadow-lg: 0 10px 25px rgba(15, 23, 42, 0.12);
}}

body.dark {{
    --bg-main: #090d16;
    --bg-card: #0f172a;
    --bg-surface: #1e293b;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border: #1e293b;
    --border-strong: #334155;
    --primary: #38bdf8;
    --primary-dark: #0284c7;
    --primary-light: rgba(56, 189, 248, 0.12);
    --primary-border: rgba(56, 189, 248, 0.32);
    --accent: #f59e0b;
    --accent-light: rgba(245, 158, 11, 0.15);
    --accent-crimson: #fb7185;
    --danger: #f87171;
    --success: #10b981;
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.55);
    --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.7);
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    display: flex;
    height: 100vh;
    overflow: hidden;
    font-size: 14px;
}}


/* Accessibility Focus Rings & Keyboard Navigation */
:focus-visible {{
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}}
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {{
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}}

@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }}
}}

/* Editorial Medical Heading Typography */
h1, h2, h3, .brand-title, .dash-hero-title, .topic-title-display, .card-title {{
    font-family: 'Newsreader', Georgia, 'Times New Roman', serif;
    letter-spacing: -0.015em;
    font-weight: 700;
}}

/* Tabular Mono for Classifications, Scores & Dosages */
code, pre, .stat-val, .table-cell-numeric, .audio-time-label, .score-badge, .formula-box, table.data-table td, table.data-table th, .exam-clock {{
    font-variant-numeric: tabular-nums;
}}

/* Reading Ergonomics (<80 Characters Line Length) */
.master-essay-content {{
    flex: 1;
    min-width: 0;
    max-width: 76ch;
}}

/* Keyboard hint badge next to search */
.search-kbd-hint {{
    position: absolute;
    right: 22px;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
}}
.search-kbd-hint kbd {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 7.5pt;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    font-weight: 600;
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
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3);
}}

.btn-primary:hover {{
    background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.42);
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
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: #ffffff;
    box-shadow: 0 2px 10px rgba(2, 132, 199, 0.3);
}}

.btn-accent:hover {{
    background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);
    transform: translateY(-1px);
}}

/* In-App PDF Viewer Modal for Tablets and Online Devices */
.pdf-modal-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(9, 13, 22, 0.85);
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

.viva-qa-block {{
    cursor: pointer;
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    margin-bottom: 8px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}}

.viva-qa-block:hover {{
    border-color: rgba(2, 132, 199, 0.2);
    background: rgba(2, 132, 199, 0.04);
}}

body.dark .viva-qa-block:hover {{
    border-color: rgba(56, 189, 248, 0.3);
    background: rgba(56, 189, 248, 0.06);
}}

.viva-pearls-container.answers-hidden .viva-qa-block:not(.revealed) .viva-a-row {{
    display: none;
}}

.viva-pearls-container.answers-hidden .viva-qa-block.revealed .viva-a-row {{
    display: block !important;
    animation: fadeIn 0.2s ease;
}}

.viva-pearls-container.answers-hidden .viva-click-hint {{
    display: inline-block;
}}

.viva-click-hint {{
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
    color: #0369a1;
    border: 1px solid #bae6fd;
}}

body.dark .badge-hd {{
    background: rgba(2, 132, 199, 0.25);
    color: #38bdf8;
    border-color: rgba(56, 189, 248, 0.35);
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
    background: linear-gradient(135deg, #090d16 0%, #0f172a 60%, #1e293b 100%);
    border-radius: var(--radius-md);
    padding: 24px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.25);
    border: 1px solid rgba(56, 189, 248, 0.25);
}}

.dash-hero-badge {{
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: rgba(56, 189, 248, 0.2);
    color: #7dd3fc;
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
    color: #bae6fd;
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
    color: #f8fafc;
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
    background: linear-gradient(135deg, #042f2e 0%, #0f172a 100%);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(4, 47, 46, 0.25);
    border: 1px solid rgba(20, 184, 166, 0.35);
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
    color: #f8fafc;
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

/* Enhanced Diagram Lightbox Modal */
#modal {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(9, 13, 22, 0.92);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: 1200;
    justify-content: center;
    align-items: center;
    padding: 12px;
    box-sizing: border-box;
}}

.modal-dialog-box {{
    width: 96vw;
    max-width: 1320px;
    height: 94vh;
    background: #0f0d1b;
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: var(--radius-md);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75);
}}

.modal-dialog-header {{
    padding: 10px 16px;
    background: #17132a;
    border-bottom: 1px solid rgba(2, 132, 199, 0.25);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
}}

.modal-dialog-title {{
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}}

.modal-diagram-badge {{
    background: var(--primary);
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 3px 8px;
    border-radius: 4px;
    white-space: nowrap;
}}

#modalTitleText {{
    font-size: 9.5pt;
    font-weight: 600;
    color: #f3f4f6;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.modal-dialog-actions {{
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
}}

.modal-tool-btn {{
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 8pt;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.modal-tool-btn:hover {{
    background: var(--primary);
    color: #ffffff;
    border-color: #0369a1;
}}

.modal-tool-btn.modal-close-btn {{
    background: rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    border-color: rgba(239, 68, 68, 0.4);
    padding: 5px 12px;
}}

.modal-tool-btn.modal-close-btn:hover {{
    background: #dc2626;
    color: #ffffff;
    border-color: #dc2626;
}}

.modal-image-viewport {{
    flex: 1;
    width: 100%;
    min-height: 0;
    overflow: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 16px;
    background: #090d16;
    -webkit-overflow-scrolling: touch;
    box-sizing: border-box;
}}

#modalImg {{
    border-radius: var(--radius-sm);
    box-shadow: 0 4px 25px rgba(0,0,0,0.5);
    transition: transform 0.15s ease-out;
    display: block;
}}

#modalImg.modal-fit-mode {{
    max-width: 100%;
    max-height: calc(94vh - 130px);
    width: auto;
    height: auto;
    object-fit: contain;
}}

#modalImg.modal-actual-mode {{
    max-width: none;
    max-height: none;
    object-fit: initial;
}}

.modal-dialog-footer {{
    padding: 6px 16px;
    background: #120e22;
    border-top: 1px solid rgba(56, 189, 248, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7.5pt;
    color: #94a3b8;
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

    /* ========================================================== */
    /* Sticky Section Table of Contents (Mini-Map) on Desktop     */
    /* ========================================================== */
    .master-answer-wrapper {{
        display: flex;
        gap: 24px;
        align-items: flex-start;
        position: relative;
    }}
    .master-essay-content {{
        flex: 1;
        min-width: 0;
    }}
    .sticky-minimap-rail {{
        width: 200px;
        position: sticky;
        top: 20px;
        flex-shrink: 0;
        display: block;
        max-height: calc(100vh - 120px);
        overflow-y: auto;
    }}
    @media (max-width: 960px) {{
        .sticky-minimap-rail {{
            display: none;
        }}
    }}
    .sticky-minimap-card {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 12px;
        box-shadow: var(--shadow-sm);
    }}
    .minimap-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid var(--border);
    }}
    .minimap-title {{
        font-size: 8pt;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--primary);
    }}
    .minimap-badge {{
        font-size: 6.5pt;
        background: var(--primary-light);
        color: var(--primary);
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }}
    .minimap-nav {{
        display: flex;
        flex-direction: column;
        gap: 3px;
    }}
    .minimap-link {{
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 5px 8px;
        border-radius: 6px;
        font-size: 7.8pt;
        color: var(--text-muted);
        text-decoration: none;
        transition: all 0.2s ease;
        cursor: pointer;
        border-left: 2px solid transparent;
        line-height: 1.3;
    }}
    .minimap-link:hover {{
        color: var(--primary);
        background: var(--primary-light);
    }}
    .minimap-link.active {{
        color: var(--primary);
        font-weight: 600;
        background: var(--primary-light);
        border-left: 3px solid var(--primary);
    }}
    .minimap-dot {{
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: currentColor;
        opacity: 0.6;
        flex-shrink: 0;
    }}

    /* ========================================================== */
    /* 15-Mark Timed Exam Simulator & Marking Rubric              */
    /* ========================================================== */
    .exam-simulator-banner {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 12px 18px;
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.08) 0%, rgba(239, 68, 68, 0.08) 100%);
        border: 1.5px dashed var(--primary-border);
        border-radius: var(--radius-md);
        margin-bottom: 20px;
    }}
    .exam-simulator-view {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin-bottom: 24px;
    }}
    .exam-sim-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 14px 18px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }}
    .exam-status-badge {{
        font-size: 7.5pt;
        font-weight: 800;
        letter-spacing: 1px;
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        padding: 3px 8px;
        border-radius: 4px;
    }}
    .exam-clock {{
        font-family: 'Cinzel', monospace, serif;
        font-size: 20pt;
        font-weight: 700;
        color: #ef4444;
        letter-spacing: 2px;
        padding: 0 10px;
    }}
    .exam-clock.warning {{
        color: #f59e0b;
    }}
    .exam-clock.urgent {{
        color: #ef4444;
        animation: pulseClock 1s infinite;
    }}
    @keyframes pulseClock {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.35; }}
        100% {{ opacity: 1; }}
    }}
    .exam-clock-controls {{
        display: flex;
        gap: 6px;
    }}
    .exam-clock-controls button {{
        padding: 4px 10px;
        font-size: 8pt;
    }}
    .exam-workspace-split {{
        display: grid;
        grid-template-columns: 1.25fr 1fr;
        gap: 20px;
    }}
    @media (max-width: 992px) {{
        .exam-workspace-split {{
            grid-template-columns: 1fr;
        }}
    }}
    .exam-editor-pane {{
        display: flex;
        flex-direction: column;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 18px;
        box-shadow: var(--shadow-sm);
    }}
    .exam-draft-textarea {{
        width: 100%;
        min-height: 480px;
        background: var(--bg-main);
        color: var(--text-main);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 14px;
        font-family: 'Inter', monospace, sans-serif;
        font-size: 9.5pt;
        line-height: 1.7;
        resize: vertical;
        outline: none;
        transition: border 0.2s ease;
    }}
    .exam-draft-textarea:focus {{
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }}
    .exam-rubric-pane {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 18px;
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
    }}
    .rubric-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        margin-bottom: 12px;
        border-bottom: 1px solid var(--border);
    }}
    .rubric-total-badge {{
        font-size: 13pt;
        font-weight: 800;
        color: var(--primary);
        background: var(--primary-light);
        padding: 4px 12px;
        border-radius: 8px;
    }}
    .rubric-items-list {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-height: 520px;
        overflow-y: auto;
        padding-right: 4px;
    }}
    .rubric-item {{
        background: var(--bg-main);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 10px 12px;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }}
    .rubric-item input[type="checkbox"] {{
        margin-top: 3px;
        accent-color: var(--primary);
        cursor: pointer;
        width: 16px;
        height: 16px;
    }}
    .rubric-item-content {{
        flex: 1;
    }}
    .rubric-item-title {{
        font-size: 8.5pt;
        font-weight: 700;
        color: var(--text-main);
        display: flex;
        justify-content: space-between;
    }}
    .rubric-item-desc {{
        font-size: 7.5pt;
        color: var(--text-muted);
        margin-top: 3px;
        line-height: 1.4;
    }}
    .rubric-item-score-select {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 6px;
    }}
    .rubric-item-score-select input[type="range"] {{
        flex: 1;
        accent-color: var(--primary);
    }}
    .rubric-item-score-select span {{
        font-size: 8pt;
        font-weight: 700;
        color: var(--primary);
        min-width: 36px;
        text-align: right;
    }}

    /* ========================================================== */
    /* Side-by-Side Comparison Slider                             */
    /* ========================================================== */
    .split-comparison-card {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 16px;
        margin-bottom: 24px;
        box-shadow: var(--shadow-sm);
    }}
    .split-comparison-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 14px;
    }}
    .split-pair-buttons {{
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }}
    .split-pair-btn {{
        padding: 4px 10px;
        font-size: 7.5pt;
        font-weight: 600;
        border-radius: 6px;
        border: 1px solid var(--border);
        background: var(--bg-main);
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .split-pair-btn.active {{
        background: var(--primary);
        color: #ffffff;
        border-color: var(--primary);
    }}
    .before-after-container {{
        position: relative;
        width: 100%;
        height: 460px;
        max-height: 65vh;
        overflow: hidden;
        border-radius: var(--radius-md);
        background: #0a0618;
        user-select: none;
        -webkit-user-select: none;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
    }}
    .before-after-layer {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-sizing: border-box;
    }}
    .before-after-layer img {{
        width: 100%;
        height: 100%;
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        pointer-events: none;
        padding: 10px;
        box-sizing: border-box;
    }}
    .before-after-layer.after-layer {{
        background: #110c28;
        z-index: 1;
    }}
    .before-after-layer.before-layer {{
        background: #070412;
        z-index: 2;
        clip-path: polygon(0 0, 50% 0, 50% 100%, 0 100%);
    }}
    .before-after-badge {{
        position: absolute;
        top: 12px;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 7.5pt;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        z-index: 4;
        backdrop-filter: blur(6px);
    }}
    .before-after-badge.badge-left {{
        left: 12px;
        background: rgba(245, 158, 11, 0.9);
        color: #ffffff;
    }}
    .before-after-badge.badge-right {{
        right: 12px;
        background: rgba(2, 132, 199, 0.9);
        color: #ffffff;
    }}
    .before-after-divider {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 3px;
        background: var(--primary);
        z-index: 5;
        transform: translateX(-50%);
        pointer-events: none;
        box-shadow: 0 0 12px rgba(2, 132, 199, 0.6);
    }}
    .before-after-handle {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 38px;
        height: 38px;
        background: #ffffff;
        color: var(--primary-dark);
        border: 3px solid var(--primary);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 8.5pt;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }}
    .before-after-range {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: ew-resize;
        z-index: 10;
        margin: 0;
    }}

    /* ========================================================== */
    /* Spotter / Image Occlusion Mode ("Anki Mode")               */
    /* ========================================================== */
    .diagram-mode-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        padding: 10px 14px;
        background: var(--primary-light);
        border: 1px solid var(--primary-border);
        border-radius: var(--radius-sm);
        margin-bottom: 16px;
    }}
    .spotter-interactive-container {{
        position: relative;
        display: block;
        width: 100%;
        overflow: hidden;
        border-radius: 8px;
        line-height: 0;
    }}
    .spotter-interactive-container img {{
        display: block;
        width: 100% !important;
        height: auto !important;
        max-height: none !important;
        object-fit: initial !important;
        cursor: zoom-in;
    }}
    .spotter-box {{
        position: absolute;
        cursor: pointer;
        border-radius: 6px;
        z-index: 10;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
        transform-style: preserve-3d;
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        overflow: hidden;
    }}
    .spotter-box .spotter-front,
    .spotter-box .spotter-back {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 3px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        border-radius: 6px;
    }}
    .spotter-box .spotter-front {{
        background: rgba(2, 132, 199, 0.94);
        border: 1.5px solid #bae6fd;
        color: #ffffff;
    }}
    .spotter-box .spotter-front .spotter-num {{
        font-size: 7.5pt;
        font-weight: 800;
        letter-spacing: 0.5px;
    }}
    .spotter-box .spotter-front .spotter-hint-text {{
        font-size: 6.5pt;
        opacity: 0.9;
        margin-top: 1px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 90%;
    }}
    .spotter-box .spotter-back {{
        background: rgba(16, 185, 129, 0.96);
        border: 1.5px solid #a7f3d0;
        color: #ffffff;
        transform: rotateY(180deg);
    }}
    .spotter-box .spotter-back .spotter-label-text {{
        font-size: 7.5pt;
        font-weight: 700;
        line-height: 1.2;
    }}
    .spotter-box.revealed {{
        transform: rotateY(180deg);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.45);
    }}

    /* Modal Spotter Overlay */
    .modal-diagram-stage {{
        position: relative;
        display: inline-block;
        max-width: 100%;
        max-height: 100%;
        line-height: 0;
    }}
    .modal-spotter-overlay {{
        position: absolute;
        inset: 0;
        pointer-events: auto;
        z-index: 15;
    }}

    /* ========================================================== */
    /* Speech Synthesis Viva Buttons                              */
    /* ========================================================== */
    .viva-audio-speak-btn {{
        background: var(--primary-light);
        border: 1px solid var(--primary-border);
        color: var(--primary);
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 9pt;
        cursor: pointer;
        transition: all 0.2s ease;
        flex-shrink: 0;
    }}
    .viva-audio-speak-btn:hover {{
        background: var(--primary);
        color: #ffffff;
        transform: scale(1.1);
    }}
    .viva-audio-speak-btn.speaking {{
        background: #ef4444;
        color: #ffffff;
        border-color: #ef4444;
        animation: speakPulse 1s infinite alternate;
    }}
    @keyframes speakPulse {{
        from {{ transform: scale(1); box-shadow: 0 0 4px rgba(239, 68, 68, 0.4); }}
        to {{ transform: scale(1.15); box-shadow: 0 0 12px rgba(239, 68, 68, 0.8); }}
    }}

    /* ========================================================== */
    /* Mobile Floating Bottom Bar                                 */
    /* ========================================================== */
    .mobile-floating-bottom-bar {{
        display: none;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: rgba(15, 23, 42, 0.94);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-top: 1px solid rgba(2, 132, 199, 0.25);
        z-index: 950;
        justify-content: space-around;
        align-items: center;
        padding: 0 8px;
        padding-bottom: env(safe-area-inset-bottom, 0px);
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.35);
    }}
    body:not(.dark) .mobile-floating-bottom-bar {{
        background: rgba(255, 255, 255, 0.94);
        border-top: 1px solid var(--border);
        box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.08);
    }}
    @media (max-width: 768px) {{
        .mobile-floating-bottom-bar.in-chapter {{
            display: flex !important;
        }}
        .content-body.with-bottom-bar {{
            padding-bottom: 78px !important;
        }}
    }}
    .mobile-bottom-tab {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 3px;
        background: transparent;
        border: none;
        color: var(--text-muted);
        cursor: pointer;
        padding: 6px 4px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }}
    .mobile-bottom-tab .bottom-tab-icon {{
        font-size: 13pt;
        line-height: 1;
    }}
    .mobile-bottom-tab .bottom-tab-text {{
        font-size: 7.5pt;
        font-weight: 600;
    }}
    .mobile-bottom-tab.active {{
        color: var(--primary);
        background: var(--primary-light);
    }}
    /* Hands-Free Walking Audio Mode Banner */
    /* Hands-Free Walking Audio Mode Banner */
    .hands-free-audio-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.06) 0%, rgba(56, 189, 248, 0.12) 100%);
        border: 1px solid var(--primary-border);
        border-radius: var(--radius-md);
        padding: 14px 20px;
        margin-bottom: 18px;
        box-shadow: var(--shadow-sm);
        flex-wrap: wrap;
    }}
    .audio-banner-left {{
        display: flex;
        align-items: center;
        gap: 14px;
        flex: 1;
        min-width: 260px;
    }}
    .audio-banner-pulse-icon {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
    }}
    .audio-banner-title {{
        font-size: 10pt;
        font-weight: 700;
        color: var(--text-main);
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}
    .audio-badge-lock {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(16, 185, 129, 0.12);
        color: #059669;
        border: 1px solid rgba(16, 185, 129, 0.28);
        font-size: 7pt;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .audio-banner-sub {{
        font-size: 8pt;
        color: var(--text-muted);
        margin-top: 2px;
        line-height: 1.4;
    }}
    .btn-audio-play-all {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        border: none;
        padding: 9px 20px;
        border-radius: 9999px;
        font-size: 8.5pt;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        white-space: nowrap;
    }}
    .btn-audio-play-all:hover {{
        transform: translateY(-1.5px);
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
    }}
    .btn-audio-play-all:active {{
        transform: translateY(0);
    }}
    .btn-audio-play-all.is-playing {{
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
    }}

    /* Animated 3-Bar Equalizer inside Section Buttons */
    .modern-eq-bars {{
        display: inline-flex;
        align-items: flex-end;
        gap: 2.5px;
        height: 12px;
        width: 12px;
    }}
    .modern-eq-bars span {{
        display: block;
        width: 2.5px;
        background: currentColor;
        border-radius: 1px;
        animation: eqBounce 1.2s ease-in-out infinite alternate;
    }}
    .modern-eq-bars span:nth-child(1) {{
        height: 40%;
        animation-delay: 0.1s;
    }}
    .modern-eq-bars span:nth-child(2) {{
        height: 95%;
        animation-delay: 0.35s;
    }}
    .modern-eq-bars span:nth-child(3) {{
        height: 60%;
        animation-delay: 0.2s;
    }}
    @keyframes eqBounce {{
        0% {{ height: 25%; }}
        50% {{ height: 100%; }}
        100% {{ height: 35%; }}
    }}

    /* Modern Section Audio Pill Button */
    .section-audio-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--bg-card);
        border: 1px solid var(--primary-border);
        color: var(--primary);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 7.5pt;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 1px 3px rgba(2, 132, 199, 0.08);
    }}
    .section-audio-pill:hover {{
        background: var(--primary-light);
        border-color: var(--primary);
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(2, 132, 199, 0.15);
    }}
    .section-audio-pill:active {{
        transform: translateY(0);
    }}
    .section-audio-pill.speaking {{
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        border-color: transparent;
        box-shadow: 0 3px 12px rgba(2, 132, 199, 0.35);
        animation: pulseAudioGlow 2.5s infinite;
    }}
    @keyframes pulseAudioGlow {{
        0%, 100% {{ box-shadow: 0 3px 12px rgba(2, 132, 199, 0.35); }}
        50% {{ box-shadow: 0 6px 20px rgba(2, 132, 199, 0.55); }}
    }}

    .essay-section-card.audio-active-section {{
        border: 2px solid var(--primary) !important;
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.25) !important;
        position: relative;
    }}
    .essay-section-card.audio-active-section::before {{
        content: 'PLAYING NOW';
        position: absolute;
        top: -9px;
        right: 18px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #fff;
        font-size: 6.5pt;
        font-weight: 800;
        letter-spacing: 0.8px;
        padding: 2px 8px;
        border-radius: 9999px;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
    }}

    /* Modern Floating Island Audio Player Dock */
    .audio-dock {{
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 48px);
        max-width: 1040px;
        z-index: 1050;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(28px) saturate(180%);
        -webkit-backdrop-filter: blur(28px) saturate(180%);
        border: 1px solid rgba(2, 132, 199, 0.25);
        border-radius: 22px;
        box-shadow: 0 16px 42px -6px rgba(15, 23, 42, 0.25), 0 4px 16px rgba(0, 0, 0, 0.05);
        padding: 12px 22px;
        display: block;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
    }}
    body.dark .audio-dock {{
        background: rgba(15, 23, 42, 0.94);
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 20px 50px -8px rgba(0, 0, 0, 0.75), 0 0 24px rgba(2, 132, 199, 0.18);
    }}
    .audio-dock.hidden {{
        transform: translate(-50%, 150%);
        opacity: 0;
        pointer-events: none;
    }}
    .audio-dock-inner {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        flex-wrap: wrap;
    }}
    .audio-dock-meta {{
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 200px;
        max-width: 300px;
        flex-shrink: 0;
    }}
    .audio-dock-track-icon {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        transition: transform 0.2s ease;
    }}
    .audio-dock.is-playing .audio-dock-track-icon {{
        animation: pulseTrackIcon 2.4s ease-in-out infinite;
    }}
    @keyframes pulseTrackIcon {{
        0%, 100% {{ transform: scale(1); box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3); }}
        50% {{ transform: scale(1.05); box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45); }}
    }}
    .audio-dock-text {{
        overflow: hidden;
    }}
    .audio-dock-track-title {{
        font-size: 9pt;
        font-weight: 700;
        color: var(--text-main);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        letter-spacing: -0.2px;
    }}
    .audio-dock-chapter-title {{
        font-size: 7.5pt;
        color: var(--text-muted);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: 2px;
    }}
    .audio-dock-controls-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        flex: 1;
        min-width: 260px;
    }}
    .audio-dock-buttons {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .audio-control-btn {{
        background: transparent;
        border: none;
        color: var(--text-main);
        cursor: pointer;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
    }}
    .audio-control-btn:hover {{
        background: var(--primary-light);
        color: var(--primary);
        transform: scale(1.1);
    }}
    .audio-control-btn:active {{
        transform: scale(0.92);
    }}
    .audio-btn-playpause {{
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .audio-btn-playpause:hover {{
        transform: scale(1.08);
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
    }}
    .audio-btn-playpause:active {{
        transform: scale(0.94);
    }}
    .audio-mode-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(2, 132, 199, 0.08);
        border: 1px solid rgba(2, 132, 199, 0.2);
        color: var(--primary);
        font-size: 7.5pt;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        cursor: pointer;
        transition: all 0.2s ease;
        letter-spacing: 0.2px;
    }}
    .audio-mode-indicator:hover {{
        background: rgba(2, 132, 199, 0.15);
        border-color: var(--primary);
    }}
    .mode-pulse-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 6px #10b981;
        animation: radarPulse 1.8s infinite;
    }}
    @keyframes radarPulse {{
        0% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.85); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    .audio-dock-progress-wrap {{
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        max-width: 500px;
    }}
    .audio-time-label {{
        font-size: 7.5pt;
        font-weight: 600;
        color: var(--text-muted);
        min-width: 34px;
        font-variant-numeric: tabular-nums;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .audio-scrubber {{
        -webkit-appearance: none;
        appearance: none;
        flex: 1;
        height: 4px;
        border-radius: 9999px;
        background: linear-gradient(to right, #0284c7 var(--scrub-percent, 0%), rgba(2, 132, 199, 0.16) var(--scrub-percent, 0%));
        cursor: pointer;
        outline: none;
        transition: height 0.15s ease;
    }}
    .audio-scrubber:hover {{
        height: 6px;
    }}
    .audio-scrubber::-webkit-slider-thumb {{
        -webkit-appearance: none;
        appearance: none;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #ffffff;
        border: 2px solid #0284c7;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.35);
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .audio-scrubber:hover::-webkit-slider-thumb {{
        transform: scale(1.25);
        box-shadow: 0 3px 10px rgba(2, 132, 199, 0.5);
    }}
    .audio-dock-options {{
        display: flex;
        align-items: center;
        gap: 12px;
        flex-shrink: 0;
    }}
    /* Modern Segmented Control for Speed */
    .audio-speed-selector {{
        display: inline-flex;
        align-items: center;
        gap: 2px;
        background: rgba(2, 132, 199, 0.08);
        padding: 3px;
        border-radius: 9999px;
        border: 1px solid rgba(2, 132, 199, 0.18);
    }}
    body.dark .audio-speed-selector {{
        background: rgba(2, 132, 199, 0.12);
        border: 1px solid rgba(2, 132, 199, 0.25);
    }}
    .speed-pill {{
        background: transparent;
        border: none;
        color: var(--text-muted);
        font-size: 7.5pt;
        font-weight: 600;
        padding: 4px 9px;
        border-radius: 9999px;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        line-height: 1;
    }}
    .speed-pill:hover {{
        color: var(--primary);
    }}
    .speed-pill.active {{
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
    }}
    .audio-dock-close {{
        background: transparent;
        border: none;
        color: var(--text-muted);
        cursor: pointer;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        padding: 0;
    }}
    .audio-dock-close:hover {{
        color: var(--danger);
        background: rgba(239, 68, 68, 0.12);
        transform: rotate(90deg);
    }}

    @media (max-width: 768px) {{
        .audio-dock {{
            padding: 10px 14px;
            bottom: 74px; /* Dock gracefully above mobile bottom bar */
            width: calc(100% - 20px);
            border-radius: 20px;
        }}
        .audio-dock-meta {{
            min-width: 100%;
            max-width: 100%;
            justify-content: space-between;
        }}
        .audio-dock-controls-wrap {{
            width: 100%;
        }}
        .audio-dock-options {{
            width: 100%;
            justify-content: space-between;
            margin-top: 4px;
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
        <input type="text" id="searchInput" class="search-input" placeholder="Search topics, signs, procedures..." aria-label="Search surgical topics and procedures">
        <span class="search-kbd-hint"><kbd>/</kbd></span>
    </div>

    <div class="topic-list" id="topicList"></div>
</div>

<div id="main-view">
    <div class="top-bar">
        <button class="mobile-menu-btn" onclick="toggleSidebar(true)" aria-label="Open Topics Menu">{ICONS["menu"]}</button>
        
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
            <button class="icon-btn" onclick="toggleDarkMode()" title="Toggle Dark/Light Mode" aria-label="Toggle between dark and light mode">{ICONS["moon"]}</button>
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

    <nav class="mobile-floating-bottom-bar" id="mobileFloatingBottomBar">
    <button class="mobile-bottom-tab active" data-tab="master" onclick="switchTopicTab('master')">
        <span class="bottom-tab-icon">📝</span>
        <span class="bottom-tab-text">Answer</span>
    </button>
    <button class="mobile-bottom-tab" data-tab="diagrams" onclick="switchTopicTab('diagrams')">
        <span class="bottom-tab-icon">🖼️</span>
        <span class="bottom-tab-text">Diagrams</span>
    </button>
    <button class="mobile-bottom-tab" data-tab="viva" onclick="switchTopicTab('viva')">
        <span class="bottom-tab-icon">💡</span>
        <span class="bottom-tab-text">Viva</span>
    </button>
    <button class="mobile-bottom-tab" data-tab="quiz" onclick="switchTopicTab('quiz')">
        <span class="bottom-tab-icon">🗂️</span>
        <span class="bottom-tab-text">Quiz</span>
    </button>
    <button class="mobile-bottom-tab" data-tab="notes" onclick="switchTopicTab('notes')">
        <span class="bottom-tab-icon">📓</span>
        <span class="bottom-tab-text">Notes</span>
    </button>
    </nav>
</div>

<div id="modal" onclick="onModalBackdropClick(event)">
    <div class="modal-dialog-box" onclick="event.stopPropagation()">
        <div class="modal-dialog-header">
            <div class="modal-dialog-title">
                <span class="modal-diagram-badge">HD Diagram</span>
                <span id="modalTitleText">Medical Diagram Viewer</span>
            </div>
            <div class="modal-dialog-actions">
                <button class="modal-tool-btn" onclick="toggleModalSpotter()" id="btnModalSpotter" title="Spotter Testing Mode">🎯 Spotter Mode</button>
                <button class="modal-tool-btn" onclick="zoomModalImg(1.25)" title="Zoom In">Zoom In ＋</button>
                <button class="modal-tool-btn" onclick="zoomModalImg(0.8)" title="Zoom Out">Zoom Out －</button>
                <button class="modal-tool-btn" onclick="toggleModalFit()" id="btnModalFit" title="Toggle 100% / Fit to Viewport">100% Size</button>
                <button class="modal-tool-btn" onclick="openModalImgTab()" title="Open Original Diagram in New Tab">⤢ New Tab</button>
                <button class="modal-tool-btn modal-close-btn" onclick="closeModal()" title="Close Viewer">✕ Close</button>
            </div>
        </div>
        <div class="modal-image-viewport" id="modalViewport">
            <div class="modal-diagram-stage" id="modalDiagramStage">
                <img id="modalImg" class="modal-fit-mode" src="" alt="Enlarged Diagram">
                <div id="modalSpotterOverlay" class="modal-spotter-overlay" style="display: none;"></div>
            </div>
        </div>
        <div class="modal-dialog-footer">
            <span>💡 <strong>Zero Cutoff Guarantee:</strong> Use 100% Size or Zoom buttons to inspect intricate details and wide matrices. Scroll horizontally or vertically freely.</span>
            <span style="font-size: 7pt; color: var(--text-muted);">Press Esc to Exit</span>
        </div>
    </div>
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
                <button class="icon-btn" onclick="closePdfModal()" aria-label="Close PDF Viewer" title="Close PDF Viewer">{ICONS["close"]}</button>
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
const SPOTTERS = {spotters_json};
const COMPARISON_PAIRS = {pairs_json};
const RUBRIC_CRITERIA = {rubric_json};
const SVG_ICONS = {{
    check: '{ICONS["check_circle"]}',
    circle: '{ICONS["circle"]}',
    notes: '{ICONS["notes"]}',
    play: '{ICONS["play"]}',
    pause: '{ICONS["pause"]}',
    play_sm: '{ICONS["play_sm"]}',
    pause_sm: '{ICONS["pause_sm"]}',
    prev_track: '{ICONS["prev_track"]}',
    next_track: '{ICONS["next_track"]}',
    headphones: '{ICONS["headphones"]}',
    volume: '{ICONS["volume"]}',
    sync: '{ICONS["sync"]}',
    close_sm: '{ICONS["close_sm"]}',
    stop_sm: '{ICONS["stop_sm"]}',
    lock_sm: '{ICONS["lock_sm"]}'
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

// Exam Simulator State
let isExamSimActive = false;
let examTimerSeconds = 25 * 60;
let examTimerInterval = null;
let examIsRunning = false;
let rubricScores = {{}};
let examSubmitted = false;

// Spotter & Comparison State
let spotterModeActive = false;
let revealedSpotters = {{}};
let activeComparePairIdx = 0;
let modalCurrentFilename = '';
let modalSpotterActive = false;

// --- Continuous Studio Audio & Lock-Screen Playback Engine ---
let masterAudio = new Audio();
let audioTrack = null; // (chId, secKey, title, chapterTitle)
let audioPlaybackSpeed = parseFloat(localStorage.getItem('surgery_audio_speed') || '1.0');
let isAudioPlaying = false;
let isChapterAutoAdvance = false;
let chapterAudioQueue = [];
let chapterQueueIdx = 0;
let currentSpeakingBtn = null;
let currentUtterance = null;
let playlistRunning = false;
let playlistIdx = 0;


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
            <button class="topic-check-btn" aria-label="Toggle completion for ${{ch.title}}" title="Toggle completion" onclick="event.stopPropagation(); saveCompletion('${{ch.id}}', ${{!isDone}})">
                ${{isDone ? SVG_ICONS.check : SVG_ICONS.circle}}
            </button>
            <span class="topic-title-text" onclick="selectChapter(${{idx}})">${{idx + 1}}. ${{ch.title}}</span>
        `;
        container.appendChild(item);
    }});
}}

function openDashboardView() {{
    currentChapterIdx = -1;
    stopCurrentSpeech();
    document.getElementById('btnNavDash').classList.add('active');
    document.getElementById('topicTabsNav').style.display = 'none';
    const mobNav = document.getElementById('mobileSectionNav');
    if (mobNav) mobNav.classList.remove('active');
    const bottomBar = document.getElementById('mobileFloatingBottomBar');
    if (bottomBar) bottomBar.classList.remove('in-chapter');
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
    isExamSimActive = false;
    stopCurrentSpeech();
    quizCardIdx = 0;
    quizAnswerRevealed = false;
    vivaAnswersVisible = false;
    document.getElementById('btnNavDash').classList.remove('active');
    document.getElementById('topicTabsNav').style.display = 'flex';
    const mobNav = document.getElementById('mobileSectionNav');
    if (mobNav) mobNav.classList.add('active');
    const bottomBar = document.getElementById('mobileFloatingBottomBar');
    if (bottomBar) bottomBar.classList.add('in-chapter');
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
    if ('speechSynthesis' in window && window.speechSynthesis.speaking) {{
        window.speechSynthesis.cancel();
    }}

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

    // Highlight mobile floating bottom bar
    document.querySelectorAll('.mobile-bottom-tab').forEach(btab => {{
        if (btab.getAttribute('data-tab') === tab) {{
            btab.classList.add('active');
        }} else {{
            btab.classList.remove('active');
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
                    <div style="font-size: 8pt; font-weight: 700; color: #bae6fd; text-transform: uppercase; letter-spacing: 1px;">Exam Night Rapid Revision</div>
                    <div style="font-size: 13pt; font-weight: 700; color: #ffffff;">Chapter 24: Master Surgery Cheat Sheet</div>
                    <div style="font-size: 8.5pt; color: #e0f2fe; margin-top: 2px;">
                        Exhaustive high-yield formulas, keywords, named clinical signs, classifications & shock matrices for rapid pre-exam glance.
                    </div>
                </div>
            </div>
            <button class="btn btn-primary" onclick="selectChapter(23)" style="background: #ffffff; color: #0369a1; font-weight: 700; padding: 10px 22px; font-size: 9pt; box-shadow: 0 4px 14px rgba(0,0,0,0.25);">
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
                <button class="chip" onclick="selectChapter(23)" style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: #ffffff; border: none;">⚡ Cheat Sheet</button>
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
                        ${{hasNote ? '<span style="font-size: 7.5pt; background: #f0f9ff; color: #0369a1; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Note Saved</span>' : ''}}
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

// --- Continuous Background Audio Engine (Lock-Screen & Mobile/Tablet Pocket Playback) ---
function initMasterAudio() {{
    masterAudio.preload = 'auto';
    masterAudio.playbackRate = audioPlaybackSpeed;

    masterAudio.addEventListener('play', () => {{
        isAudioPlaying = true;
        updateAudioDockUI();
        updateSectionButtonsUI();
    }});

    masterAudio.addEventListener('pause', () => {{
        isAudioPlaying = false;
        updateAudioDockUI();
        updateSectionButtonsUI();
    }});

    masterAudio.addEventListener('loadedmetadata', () => {{
        updateAudioScrubberUI();
    }});

    masterAudio.addEventListener('timeupdate', () => {{
        updateAudioScrubberUI();
    }});

    masterAudio.addEventListener('ended', () => {{
        handleAudioEnded();
    }});

    masterAudio.addEventListener('error', (e) => {{
        console.warn('Audio stream error, falling back if needed:', e);
        if (isChapterAutoAdvance) {{
            handleAudioEnded();
        }}
    }});

    // Native MediaSession for Samsung One UI Lock-Screen, Tablet Pocket Playback, & Earbuds
    if ('mediaSession' in navigator) {{
        try {{
            navigator.mediaSession.setActionHandler('play', () => {{
                masterAudio.play();
            }});
            navigator.mediaSession.setActionHandler('pause', () => {{
                masterAudio.pause();
            }});
            navigator.mediaSession.setActionHandler('previoustrack', () => {{
                prevAudioTrack();
            }});
            navigator.mediaSession.setActionHandler('nexttrack', () => {{
                nextAudioTrack();
            }});
            navigator.mediaSession.setActionHandler('seekto', (details) => {{
                if (details.seekTime && masterAudio.duration) {{
                    masterAudio.currentTime = details.seekTime;
                }}
            }});
            navigator.mediaSession.setActionHandler('seekbackward', (details) => {{
                const skip = details.seekOffset || 15;
                masterAudio.currentTime = Math.max(0, masterAudio.currentTime - skip);
            }});
            navigator.mediaSession.setActionHandler('seekforward', (details) => {{
                const skip = details.seekOffset || 15;
                masterAudio.currentTime = Math.min(masterAudio.duration || 0, masterAudio.currentTime + skip);
            }});
        }} catch (err) {{
            console.warn('MediaSession handler registration error:', err);
        }}
    }}
}}

function updateMediaSessionMetadata(trackTitle, chapterTitle) {{
    if ('mediaSession' in navigator) {{
        try {{
            navigator.mediaSession.metadata = new MediaMetadata({{
                title: trackTitle,
                artist: 'General Surgery Pro • Sanjay Marwah Monograph',
                album: chapterTitle,
                artwork: [
                    {{ src: 'favicon.svg', sizes: '96x96', type: 'image/svg+xml' }}
                ]
            }});
            navigator.mediaSession.playbackState = isAudioPlaying ? 'playing' : 'paused';
        }} catch (e) {{}}
    }}
}}

function playSectionAudio(chId, secKey, secTitle, autoAdvance = false) {{
    const ch = CHAPTERS.find(c => c.id === chId) || CHAPTERS[currentChapterIdx];
    const chTitle = ch ? ch.title : 'Chapter ' + (currentChapterIdx + 1);
    const audioSrc = 'assets/audio/' + chId + '_' + secKey + '.mp3';

    audioTrack = {{
        chId: chId,
        secKey: secKey,
        title: secTitle,
        chapterTitle: chTitle
    }};
    isChapterAutoAdvance = autoAdvance;

    const dock = document.getElementById('masterAudioDock');
    if (dock) dock.classList.remove('hidden');

    if (!masterAudio.src.endsWith(audioSrc)) {{
        masterAudio.src = audioSrc;
    }}
    masterAudio.playbackRate = audioPlaybackSpeed;

    masterAudio.play().then(() => {{
        isAudioPlaying = true;
        updateAudioDockUI();
        updateSectionButtonsUI();
        highlightActiveAudioSection(secKey);
        updateMediaSessionMetadata(secTitle, chTitle);
    }}).catch(err => {{
        console.warn('Playback request error:', err);
    }});
}}

function toggleSectionAudio(chId, secKey, secTitle) {{
    if (audioTrack && audioTrack.chId === chId && audioTrack.secKey === secKey) {{
        if (isAudioPlaying) {{
            masterAudio.pause();
        }} else {{
            masterAudio.play();
        }}
    }} else {{
        const ch = CHAPTERS.find(c => c.id === chId) || CHAPTERS[currentChapterIdx];
        if (ch && ch.sections) {{
            const keys = Object.keys(ch.sections);
            chapterAudioQueue = keys.map(k => ({{
                chId: ch.id,
                secKey: k,
                title: k.replace(/_/g, ' ').toUpperCase()
            }}));
            chapterQueueIdx = keys.indexOf(secKey);
            if (chapterQueueIdx === -1) chapterQueueIdx = 0;
        }}
        playSectionAudio(chId, secKey, secTitle, false);
    }}
}}

function playContinuousChapterAudio() {{
    const ch = CHAPTERS[currentChapterIdx];
    if (!ch || !ch.sections) return;

    if (isAudioPlaying && isChapterAutoAdvance && audioTrack && audioTrack.chId === ch.id) {{
        masterAudio.pause();
        return;
    }}

    const keys = Object.keys(ch.sections);
    if (keys.length === 0) return;

    chapterAudioQueue = keys.map(k => ({{
        chId: ch.id,
        secKey: k,
        title: k.replace(/_/g, ' ').toUpperCase()
    }}));
    chapterQueueIdx = 0;
    isChapterAutoAdvance = true;

    const first = chapterAudioQueue[0];
    playSectionAudio(first.chId, first.secKey, first.title, true);
}}

function handleAudioEnded() {{
    if (isChapterAutoAdvance && chapterAudioQueue.length > 0 && chapterQueueIdx + 1 < chapterAudioQueue.length) {{
        chapterQueueIdx++;
        const nextTrack = chapterAudioQueue[chapterQueueIdx];
        playSectionAudio(nextTrack.chId, nextTrack.secKey, nextTrack.title, true);
    }} else {{
        isChapterAutoAdvance = false;
        isAudioPlaying = false;
        updateAudioDockUI();
        updateSectionButtonsUI();
        clearActiveAudioSectionHighlight();
    }}
}}

function togglePlayPauseAudio() {{
    if (masterAudio.src) {{
        if (masterAudio.paused) {{
            masterAudio.play();
        }} else {{
            masterAudio.pause();
        }}
    }} else if (currentChapterIdx >= 0) {{
        playContinuousChapterAudio();
    }}
}}

function prevAudioTrack() {{
    if (chapterAudioQueue.length > 0 && chapterQueueIdx > 0) {{
        chapterQueueIdx--;
        const prevTrack = chapterAudioQueue[chapterQueueIdx];
        playSectionAudio(prevTrack.chId, prevTrack.secKey, prevTrack.title, isChapterAutoAdvance);
    }} else if (masterAudio.currentTime > 3) {{
        masterAudio.currentTime = 0;
    }}
}}

function nextAudioTrack() {{
    if (chapterAudioQueue.length > 0 && chapterQueueIdx + 1 < chapterAudioQueue.length) {{
        chapterQueueIdx++;
        const nextTrack = chapterAudioQueue[chapterQueueIdx];
        playSectionAudio(nextTrack.chId, nextTrack.secKey, nextTrack.title, isChapterAutoAdvance);
    }}
}}

function setAudioPlaybackRate(rate) {{
    audioPlaybackSpeed = rate;
    masterAudio.playbackRate = rate;
    localStorage.setItem('surgery_audio_speed', rate.toString());

    document.querySelectorAll('.speed-pill').forEach(pill => {{
        const pSpeed = parseFloat(pill.getAttribute('data-speed'));
        if (pSpeed === rate) {{
            pill.classList.add('active');
        }} else {{
            pill.classList.remove('active');
        }}
    }});
}}

function onAudioScrub(val) {{
    if (masterAudio.duration) {{
        masterAudio.currentTime = (val / 100) * masterAudio.duration;
    }}
    const scrubber = document.getElementById('audioProgressScrubber');
    if (scrubber) {{
        scrubber.style.setProperty('--scrub-percent', val + '%');
    }}
}}

function updateAudioScrubberUI() {{
    const curTimeEl = document.getElementById('audioCurrentTime');
    const durEl = document.getElementById('audioDuration');
    const scrubber = document.getElementById('audioProgressScrubber');

    if (masterAudio.duration && !isNaN(masterAudio.duration)) {{
        const pct = (masterAudio.currentTime / masterAudio.duration) * 100;
        if (scrubber) {{
            scrubber.value = pct;
            scrubber.style.setProperty('--scrub-percent', pct + '%');
        }}
        if (curTimeEl) curTimeEl.innerText = formatAudioTime(masterAudio.currentTime);
        if (durEl) durEl.innerText = formatAudioTime(masterAudio.duration);
    }} else {{
        if (curTimeEl) curTimeEl.innerText = formatAudioTime(masterAudio.currentTime || 0);
        if (scrubber) {{
            scrubber.value = 0;
            scrubber.style.setProperty('--scrub-percent', '0%');
        }}
    }}
}}

function formatAudioTime(secs) {{
    if (isNaN(secs) || !isFinite(secs) || secs < 0) return '00:00';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
}}

function updateAudioDockUI() {{
    const playPauseBtn = document.getElementById('audioDockPlayPauseBtn');
    const trackTitleEl = document.getElementById('audioDockTrackTitle');
    const chTitleEl = document.getElementById('audioDockChapterTitle');
    const modeBadgeText = document.getElementById('audioModeBadgeText');
    const playAllBtn = document.getElementById('btnPlayAllChapter');
    const dock = document.getElementById('masterAudioDock');

    if (dock) {{
        if (isAudioPlaying) {{
            dock.classList.add('is-playing');
        }} else {{
            dock.classList.remove('is-playing');
        }}
    }}

    if (playPauseBtn) {{
        playPauseBtn.innerHTML = isAudioPlaying ? SVG_ICONS.pause : SVG_ICONS.play;
    }}
    if (playAllBtn) {{
        if (isAudioPlaying && isChapterAutoAdvance) {{
            playAllBtn.innerHTML = SVG_ICONS.pause_sm + ' <span>Pause Chapter Audio Walk</span>';
            playAllBtn.classList.add('is-playing');
        }} else {{
            playAllBtn.innerHTML = SVG_ICONS.play_sm + ' <span>Play Full Chapter (All Sections)</span>';
            playAllBtn.classList.remove('is-playing');
        }}
    }}
    if (trackTitleEl && audioTrack) {{
        trackTitleEl.innerText = audioTrack.title;
    }}
    if (chTitleEl && audioTrack) {{
        chTitleEl.innerText = audioTrack.chapterTitle;
    }}
    if (modeBadgeText) {{
        if (isChapterAutoAdvance) {{
            modeBadgeText.innerText = 'Auto Walk (' + (chapterQueueIdx + 1) + '/' + chapterAudioQueue.length + ')';
        }} else {{
            modeBadgeText.innerText = 'Single Section';
        }}
    }}

    document.querySelectorAll('.speed-pill').forEach(pill => {{
        const pSpeed = parseFloat(pill.getAttribute('data-speed'));
        if (pSpeed === audioPlaybackSpeed) {{
            pill.classList.add('active');
        }} else {{
            pill.classList.remove('active');
        }}
    }});
}}

function updateSectionButtonsUI() {{
    document.querySelectorAll('.section-audio-pill').forEach(btn => {{
        const secId = btn.id.replace('btn_sec_audio_', '');
        const isThis = audioTrack && audioTrack.secKey === secId && isAudioPlaying;
        const iconSpan = btn.querySelector('.sec-audio-icon');
        const labelSpan = btn.querySelector('.sec-audio-label');

        if (isThis) {{
            btn.classList.add('speaking');
            if (iconSpan) iconSpan.innerHTML = '<span class="modern-eq-bars"><span></span><span></span><span></span></span>';
            if (labelSpan) labelSpan.innerText = 'Pause Audio';
        }} else {{
            btn.classList.remove('speaking');
            if (iconSpan) iconSpan.innerHTML = SVG_ICONS.volume;
            if (labelSpan) labelSpan.innerText = 'Listen Section';
        }}
    }});
}}

function highlightActiveAudioSection(secKey) {{
    document.querySelectorAll('.essay-section-card').forEach(c => {{
        c.classList.remove('audio-active-section');
    }});
    const target = document.getElementById('sec_' + secKey.toLowerCase());
    if (target) {{
        target.classList.add('audio-active-section');
        try {{
            target.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }} catch (e) {{}}
    }}
}}

function clearActiveAudioSectionHighlight() {{
    document.querySelectorAll('.essay-section-card').forEach(c => {{
        c.classList.remove('audio-active-section');
    }});
}}

function closeAudioDock() {{
    masterAudio.pause();
    isAudioPlaying = false;
    isChapterAutoAdvance = false;
    const dock = document.getElementById('masterAudioDock');
    if (dock) dock.classList.add('hidden');
    clearActiveAudioSectionHighlight();
    updateSectionButtonsUI();
    updateAudioDockUI();
}}

function stopCurrentSpeech() {{
    if (masterAudio && !masterAudio.paused) {{
        masterAudio.pause();
        isAudioPlaying = false;
    }}
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
    }}
    if (currentSpeakingBtn) {{
        currentSpeakingBtn.innerHTML = SVG_ICONS.volume;
        currentSpeakingBtn.classList.remove('speaking');
        currentSpeakingBtn = null;
    }}
    currentUtterance = null;
    updateAudioDockUI();
    updateSectionButtonsUI();
}}

function speakVivaPearl(btn, pearlIdx) {{
    if (masterAudio && !masterAudio.paused) {{
        masterAudio.pause();
    }}
    if (!('speechSynthesis' in window)) {{
        alert('Web Speech API is not supported on this browser.');
        return;
    }}

    if (window.speechSynthesis.speaking && currentSpeakingBtn === btn) {{
        stopCurrentSpeech();
        return;
    }}

    stopCurrentSpeech();

    const ch = CHAPTERS[currentChapterIdx];
    if (!ch || !ch.viva_pearls || !ch.viva_pearls[pearlIdx]) return;
    const pearl = ch.viva_pearls[pearlIdx];

    let textToSpeak = "";
    if (pearl.includes('?')) {{
        const qEnd = pearl.indexOf('?') + 1;
        const q = pearl.substring(0, qEnd).trim();
        const a = pearl.substring(qEnd).trim();
        textToSpeak = `Question: ${{q}}. Examiner Model Answer: ${{a}}`;
    }} else {{
        textToSpeak = `Clinical Pearl: ${{pearl}}`;
    }}

    btn.innerHTML = '<span class="modern-eq-bars"><span></span><span></span><span></span></span>';
    btn.classList.add('speaking');
    currentSpeakingBtn = btn;

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = audioPlaybackSpeed || 1.0;
    utterance.pitch = 1.0;
    utterance.onend = () => {{
        btn.innerHTML = SVG_ICONS.volume;
        btn.classList.remove('speaking');
        currentSpeakingBtn = null;
        currentUtterance = null;
        if (playlistRunning) {{
            playNextInPlaylist();
        }}
    }};
    utterance.onerror = () => {{
        btn.innerHTML = SVG_ICONS.volume;
        btn.classList.remove('speaking');
        currentSpeakingBtn = null;
        currentUtterance = null;
    }};

    currentUtterance = utterance;
    window.speechSynthesis.speak(utterance);
}}

function toggleAudioPlaylist() {{
    const plBtn = document.getElementById('btnAudioPlaylist');
    if (playlistRunning) {{
        playlistRunning = false;
        stopCurrentSpeech();
        if (plBtn) plBtn.innerHTML = SVG_ICONS.headphones + ' <span>Audio Walk Mode (Play All)</span>';
    }} else {{
        playlistRunning = true;
        playlistIdx = 0;
        if (plBtn) plBtn.innerHTML = SVG_ICONS.stop_sm + ' <span>Stop Audio Walk</span>';
        playNextInPlaylist();
    }}
}}

function playNextInPlaylist() {{
    if (!playlistRunning) return;
    const ch = CHAPTERS[currentChapterIdx];
    if (!ch || !ch.viva_pearls || playlistIdx >= ch.viva_pearls.length) {{
        playlistRunning = false;
        const plBtn = document.getElementById('btnAudioPlaylist');
        if (plBtn) plBtn.innerHTML = SVG_ICONS.headphones + ' <span>Audio Walk Mode (Play All)</span>';
        return;
    }}
    const targetIdx = playlistIdx;
    playlistIdx++;
    const btns = document.querySelectorAll('.viva-audio-speak-btn');
    const targetBtn = btns[targetIdx] || null;
    speakVivaPearl(targetBtn, targetIdx);
}}

// --- 15-Mark Timed Exam Simulator ---
function toggleExamSimulator(active) {{
    isExamSimActive = active;
    if (active) {{
        resetExamTimer();
    }} else {{
        pauseExamTimer();
    }}
    renderTopicView();
}}

function startExamTimer() {{
    if (examIsRunning) return;
    examIsRunning = true;
    const btnStart = document.getElementById('btnExamStart');
    const btnPause = document.getElementById('btnExamPause');
    if (btnStart) btnStart.classList.add('active');
    if (btnPause) btnPause.classList.remove('active');

    examTimerInterval = setInterval(() => {{
        if (examTimerSeconds > 0) {{
            examTimerSeconds--;
            updateExamClockDisplay();
        }} else {{
            pauseExamTimer();
            alert('⏱️ Time Up! 25 minutes allocated for this 15-Mark University Essay have concluded. Submit your draft to self-grade against the university rubric.');
        }}
    }}, 1000);
}}

function pauseExamTimer() {{
    examIsRunning = false;
    if (examTimerInterval) {{
        clearInterval(examTimerInterval);
        examTimerInterval = null;
    }}
    const btnStart = document.getElementById('btnExamStart');
    const btnPause = document.getElementById('btnExamPause');
    if (btnStart) btnStart.classList.remove('active');
    if (btnPause) btnPause.classList.add('active');
}}

function resetExamTimer() {{
    pauseExamTimer();
    examTimerSeconds = 25 * 60;
    updateExamClockDisplay();
}}

function updateExamClockDisplay() {{
    const clock = document.getElementById('examCountdownClock');
    if (!clock) return;
    const mins = Math.floor(examTimerSeconds / 60);
    const secs = examTimerSeconds % 60;
    clock.innerText = `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;

    if (examTimerSeconds < 120) {{
        clock.className = 'exam-clock urgent';
    }} else if (examTimerSeconds < 300) {{
        clock.className = 'exam-clock warning';
    }} else {{
        clock.className = 'exam-clock';
    }}
}}

function onExamDraftInput(chId, textarea) {{
    const val = textarea.value;
    localStorage.setItem('surgery_exam_draft_' + chId, val);
    updateExamWordCount(val);
}}

function updateExamWordCount(text) {{
    const counter = document.getElementById('examWordCount');
    if (!counter) return;
    const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
    const chars = text.length;
    counter.innerText = `${{words}} words | ${{chars}} characters`;
}}

function insertRubricTemplate() {{
    const area = document.getElementById('examDraftArea');
    if (!area) return;
    const template = `1. DEFINITION, CLASSIFICATION & EPIDEMIOLOGY:
- Formal Definition:
- Classification / Subtypes:
- Incidence & Demographics:

2. SURGICAL ANATOMY & RELATIONS:
- Key Fascial Planes:
- Vital Neurovascular Relations:
- Embryological Landmarks:

3. ETIOPATHOGENESIS & PATHOPHYSIOLOGY:
- Pathogen / Molecular Driver:
- Cellular Mechanism / Microcirculation:
- Progression Cascade:

4. CLINICAL PRESENTATION & NAMED SIGNS:
- Cardinal Symptoms:
- Physical Examination (Inspection & Palpation):
- Pathognomonic Named Clinical Signs:

5. DIFFERENTIAL DIAGNOSIS:
- Comparative Distinction Table:

6. DIAGNOSTIC WORKUP:
- Laboratory / Biochemical:
- Radiologic Imaging (USG / Contrast CT):
- Cytopathology / Histology / Staging:

7. PREOPERATIVE RESUSCITATION & OPTIMIZATION:
- Hemodynamic Stabilization:
- Antibiotic & Fluid Protocol:
- Risk Stratification:

8. STEP-BY-STEP SURGICAL TECHNIQUE:
- Position & Incision:
- Landmark Exposure:
- Neurovascular Preservation & Dissection:
- Hemostasis & Closure:

9. POSTOPERATIVE CARE & COMPLICATIONS:
- Immediate & Early Complications:
- Late Sequelae & Strictures:
- Definitive Salvage Protocol:

10. VIVA PEARLS & SCHEMATICS:
- Examiner Traps & High-Yield Values:
- Labeled Diagram Outline:
`;
    if (!area.value.trim()) {{
        area.value = template;
    }} else {{
        area.value += `\n\n` + template;
    }}
    const ch = CHAPTERS[currentChapterIdx];
    if (ch) onExamDraftInput(ch.id, area);
}}

function updateRubricScore(num, val, isChecked) {{
    const ch = CHAPTERS[currentChapterIdx];
    if (!ch) return;
    if (!rubricScores[ch.id]) rubricScores[ch.id] = {{}};

    if (isChecked !== undefined) {{
        const crit = RUBRIC_CRITERIA.find(c => c.num === num);
        const slider = document.getElementById('rubric_range_' + num);
        const valDisp = document.getElementById('rubric_val_' + num);
        if (isChecked) {{
            const score = crit ? crit.marks : 1.0;
            rubricScores[ch.id][num] = score;
            if (slider) slider.value = score;
            if (valDisp) valDisp.innerText = score.toFixed(1);
        }} else {{
            rubricScores[ch.id][num] = 0;
            if (slider) slider.value = 0;
            if (valDisp) valDisp.innerText = '0.0';
        }}
    }} else {{
        const score = parseFloat(val) || 0;
        rubricScores[ch.id][num] = score;
        const chk = document.getElementById('rubric_chk_' + num);
        const valDisp = document.getElementById('rubric_val_' + num);
        if (chk) chk.checked = score > 0;
        if (valDisp) valDisp.innerText = score.toFixed(1);
    }}

    calculateTotalRubricScore();
}}

function calculateTotalRubricScore() {{
    const ch = CHAPTERS[currentChapterIdx];
    if (!ch) return 0;
    const scores = rubricScores[ch.id] || {{}};
    let total = 0;
    for (const [k, v] of Object.entries(scores)) {{
        total += parseFloat(v) || 0;
    }}
    const disp = document.getElementById('rubricScoreDisplay');
    if (disp) {{
        let grade = '';
        if (total >= 12.0) grade = ' (Distinction)';
        else if (total >= 10.0) grade = ' (First Class)';
        else if (total >= 7.5) grade = ' (Pass)';
        else grade = ' (Needs Revision)';
        disp.innerText = `${{total.toFixed(1)}} / 15.0${{grade}}`;
    }}
    return total;
}}

function submitExamForReview() {{
    pauseExamTimer();
    examSubmitted = true;
    const reviewSlot = document.getElementById('examModelEssaySlot');
    if (reviewSlot) {{
        reviewSlot.style.display = 'block';
        reviewSlot.scrollIntoView({{ behavior: 'smooth' }});
    }}
}}

// --- Spotter Mode & Label Occlusion ---
function toggleSpotterMode() {{
    spotterModeActive = !spotterModeActive;
    renderTopicView();
}}

function toggleSpotterHotspot(filename, hIdx) {{
    const key = filename + '_' + hIdx;
    revealedSpotters[key] = !revealedSpotters[key];
    renderTopicView();
}}

function revealAllSpotters() {{
    const ch = CHAPTERS[currentChapterIdx];
    if (!ch || !ch.diagrams) return;
    ch.diagrams.forEach(d => {{
        const spots = SPOTTERS[d.filename] || [];
        spots.forEach((h, hIdx) => {{
            revealedSpotters[d.filename + '_' + hIdx] = true;
        }});
    }});
    renderTopicView();
}}

function resetAllSpotters() {{
    revealedSpotters = {{}};
    renderTopicView();
}}

function toggleModalSpotter() {{
    modalSpotterActive = !modalSpotterActive;
    const btn = document.getElementById('btnModalSpotter');
    const overlay = document.getElementById('modalSpotterOverlay');
    if (btn) {{
        btn.innerText = modalSpotterActive ? '🎯 Spotter Mode: ON' : '🎯 Spotter Mode';
        btn.style.background = modalSpotterActive ? 'var(--primary)' : '';
        btn.style.color = modalSpotterActive ? '#fff' : '';
    }}
    if (overlay) {{
        overlay.style.display = modalSpotterActive ? 'block' : 'none';
        renderModalSpotters();
    }}
}}

function renderModalSpotters() {{
    const overlay = document.getElementById('modalSpotterOverlay');
    if (!overlay || !modalCurrentFilename) return;
    const spots = SPOTTERS[modalCurrentFilename] || [];
    if (!spots.length) {{
        overlay.innerHTML = '<div style="position: absolute; top: 12px; left: 12px; background: rgba(2,132,199,0.9); color: #fff; padding: 6px 14px; border-radius: 6px; font-size: 8pt; font-weight: 600;">🎯 No labeled landmarks registered for this diagram.</div>';
        return;
    }}
    let html = '';
    spots.forEach((h, hIdx) => {{
        const isRev = !!revealedSpotters[modalCurrentFilename + '_' + hIdx];
        html += `
            <div class="spotter-box ${{isRev ? 'revealed' : ''}}" style="top: ${{h.top}}%; left: ${{h.left}}%; width: ${{h.width}}%; height: ${{h.height}}%;" onclick="toggleModalSpotterHotspot('${{modalCurrentFilename}}', ${{hIdx}})" title="Tap to flip">
                <div class="spotter-front">
                    <span class="spotter-num">? ${{hIdx + 1}}</span>
                    <span class="spotter-hint-text">${{h.hint || 'Tap to reveal'}}</span>
                </div>
                <div class="spotter-back">
                    <span class="spotter-label-text">${{h.label}}</span>
                </div>
            </div>
        `;
    }});
    overlay.innerHTML = html;
}}

function toggleModalSpotterHotspot(filename, hIdx) {{
    const key = filename + '_' + hIdx;
    revealedSpotters[key] = !revealedSpotters[key];
    renderModalSpotters();
}}

// --- Side-by-Side Comparison Slider ---
function switchComparePair(idx) {{
    activeComparePairIdx = idx;
    renderTopicView();
}}

function updateSplitSlider(val) {{
    const beforeWrap = document.getElementById('splitBeforeWrap');
    const divider = document.getElementById('splitDivider');
    if (beforeWrap) beforeWrap.style.clipPath = `polygon(0 0, ${{val}}% 0, ${{val}}% 100%, 0 100%)`;
    if (divider) divider.style.left = val + '%';
}}

// --- Sticky Table of Contents Mini-Map & Scrollspy ---
function scrollToSection(secId) {{
    const el = document.getElementById(secId);
    if (el) {{
        el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
}}

function initScrollspy() {{
    const container = document.getElementById('contentArea');
    if (!container) return;

    const onScroll = () => {{
        const sections = document.querySelectorAll('.essay-section-card');
        const links = document.querySelectorAll('.minimap-link');
        if (!sections.length || !links.length) return;

        let activeId = '';
        const offset = 140;
        sections.forEach(sec => {{
            const rect = sec.getBoundingClientRect();
            if (rect.top <= offset) {{
                activeId = sec.id;
            }}
        }});

        if (!activeId && sections.length > 0) {{
            activeId = sections[0].id;
        }}

        links.forEach(l => {{
            if (l.getAttribute('href') === '#' + activeId) {{
                l.classList.add('active');
            }} else {{
                l.classList.remove('active');
            }}
        }});
    }};

    container.removeEventListener('scroll', onScroll);
    container.addEventListener('scroll', onScroll, {{ passive: true }});
    window.removeEventListener('scroll', onScroll);
    window.addEventListener('scroll', onScroll, {{ passive: true }});
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
        // Banner for 15-Mark University Essay Exam Simulator
        html += `
            <div class="exam-simulator-banner">
                <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="font-size: 18pt;">⏱️</span>
                    <div>
                        <div style="font-weight: 700; font-size: 10pt; color: var(--text-main);">15-Mark University Essay Exam Simulator</div>
                        <div style="font-size: 8pt; color: var(--text-muted);">Timed 25-minute mock test environment with standard 10-point university marking rubric</div>
                    </div>
                </div>
                <button class="btn btn-primary" onclick="toggleExamSimulator(${{!isExamSimActive}})" style="padding: 6px 16px; font-size: 8.5pt; font-weight: 600;">
                    ${{isExamSimActive ? '✕ Exit Timed Simulator' : 'Launch 25-Min Timed Exam'}}
                </button>
            </div>
        `;

        if (isExamSimActive) {{
            // Render University Exam Simulator Workspace
            const draftText = localStorage.getItem('surgery_exam_draft_' + ch.id) || '';
            const wordsCount = draftText.trim() ? draftText.trim().split(/\\s+/).length : 0;
            const currentScores = rubricScores[ch.id] || {{}};
            let scoreSum = 0;
            for (const v of Object.values(currentScores)) scoreSum += parseFloat(v) || 0;

            html += `
                <div class="exam-simulator-view">
                    <div class="exam-sim-header">
                        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                            <span class="exam-status-badge">🔴 LIVE UNIVERSITY EXAM SIMULATOR</span>
                            <div class="exam-clock" id="examCountdownClock">25:00</div>
                            <div class="exam-clock-controls">
                                <button class="btn btn-secondary" onclick="startExamTimer()" id="btnExamStart">{ICONS["play_sm"]} Start</button>
                                <button class="btn btn-secondary" onclick="pauseExamTimer()" id="btnExamPause">{ICONS["pause_sm"]} Pause</button>
                                <button class="btn btn-secondary" onclick="resetExamTimer()">{ICONS["sync"]} Reset 25m</button>
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span class="exam-word-count" id="examWordCount">${{wordsCount}} words | ${{draftText.length}} characters</span>
                            <button class="btn btn-secondary" onclick="toggleExamSimulator(false)" style="padding: 5px 12px; font-size: 8pt;">{ICONS["close_sm"]} Exit</button>
                        </div>
                    </div>

                    <div class="prompt-box" style="border-left-color: #ef4444; background: rgba(239, 68, 68, 0.05); margin-bottom: 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">
                            <span style="font-weight: 800; text-transform: uppercase; font-size: 8pt; color: #dc2626; letter-spacing: 1px;">
                                University 15-Mark Examination Paper
                            </span>
                            <span style="font-size: 8pt; font-weight: 700; color: #dc2626;">Time Allowed: 25 Minutes | Maximum Marks: 15</span>
                        </div>
                        <div style="font-size: 11pt; font-weight: 600; color: var(--text-main); line-height: 1.6;">${{ch.essay_prompt}}</div>
                    </div>

                    <div class="exam-workspace-split">
                        <div class="exam-editor-pane">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                                <label style="font-size: 8.5pt; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
                                    Student Essay Draft Area
                                </label>
                                <button class="btn btn-secondary" onclick="insertRubricTemplate()" style="padding: 3px 10px; font-size: 7.5pt;">
                                    Insert 10-Heading Outline
                                </button>
                            </div>
                            <textarea class="exam-draft-textarea" id="examDraftArea" oninput="onExamDraftInput('${{ch.id}}', this)" placeholder="Begin drafting your university answer here... Follow the standard 10 university subheadings (Definition, Anatomy, Pathophysiology, Clinical Signs, Differential, Workup, Pre-op, Surgical Technique, Complications, Viva Pearls)...">${{draftText}}</textarea>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; flex-wrap: wrap; gap: 8px;">
                                <span style="font-size: 7.5pt; color: var(--text-muted);">💾 Draft saved locally to your device</span>
                                <button class="btn btn-primary" onclick="submitExamForReview()" style="padding: 7px 18px; font-size: 8.5pt; font-weight: 600;">
                                    Submit Draft & Self-Grade against Rubric
                                </button>
                            </div>
                        </div>

                        <div class="exam-rubric-pane">
                            <div class="rubric-header">
                                <div>
                                    <div style="font-weight: 700; font-size: 9.5pt; color: var(--text-main);">University Marking Rubric (15 Marks)</div>
                                    <div style="font-size: 7.5pt; color: var(--text-muted);">Self-grade each section against gold-standard university criteria</div>
                                </div>
                                <div class="rubric-total-badge" id="rubricScoreDisplay">${{scoreSum.toFixed(1)}} / 15.0</div>
                            </div>
                            <div class="rubric-items-list" id="rubricItemsList">
            `;

            RUBRIC_CRITERIA.forEach(crit => {{
                const assigned = currentScores[crit.num] !== undefined ? currentScores[crit.num] : 0;
                const isChecked = assigned > 0;
                html += `
                    <div class="rubric-item">
                        <input type="checkbox" id="rubric_chk_${{crit.num}}" ${{isChecked ? 'checked' : ''}} onchange="updateRubricScore(${{crit.num}}, null, this.checked)">
                        <div class="rubric-item-content">
                            <div class="rubric-item-title">
                                <span>${{crit.num}}. ${{crit.title}}</span>
                                <span style="color: var(--primary); font-weight: 800;">${{crit.marks}} Marks</span>
                            </div>
                            <div class="rubric-item-desc">${{crit.desc}}</div>
                            <div class="rubric-item-score-select">
                                <input type="range" id="rubric_range_${{crit.num}}" min="0" max="${{crit.marks}}" step="0.5" value="${{assigned}}" oninput="updateRubricScore(${{crit.num}}, this.value)">
                                <span id="rubric_val_${{crit.num}}">${{assigned.toFixed(1)}}</span>
                            </div>
                        </div>
                    </div>
                `;
            }});

            html += `
                            </div>
                        </div>
                    </div>

                    <div id="examModelEssaySlot" style="display: ${{examSubmitted ? 'block' : 'none'}}; margin-top: 24px;">
                        <div style="background: var(--bg-card); border: 2px solid var(--primary); border-radius: var(--radius-md); padding: 18px; margin-bottom: 20px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <h3 style="font-size: 12pt; color: var(--primary); margin: 0; font-weight: 700;">
                                    Benchmark Your Draft Against the Master Monograph
                                </h3>
                                <button class="btn btn-secondary" onclick="document.getElementById('examModelEssaySlot').style.display='none'" style="padding: 4px 10px; font-size: 8pt;">Hide Model Answer</button>
                            </div>
                            <p style="font-size: 8.5pt; color: var(--text-muted); margin: 0;">Compare your essay response against the 10 university gold-standard sections below to refine your knowledge and precision.</p>
                        </div>
            `;

            // Append the master essay below for direct comparison
            for (const [secName, secHtml] of Object.entries(ch.sections)) {{
                const titleFormatted = secName.replace(/_/g, ' ').toUpperCase();
                html += `
                    <div class="card">
                        <div class="card-title">${{titleFormatted}}</div>
                        <div style="line-height: 1.7;">${{secHtml}}</div>
                    </div>
                `;
            }}

            html += `</div></div>`;
        }} else {{
            // Render standard essay with Sticky Section Table of Contents Mini-Map
            html += `
                <div class="master-answer-wrapper">
                    <div class="master-essay-content">
                        <div class="hands-free-audio-bar">
                            <div class="audio-banner-left">
                                <div class="audio-banner-pulse-icon">{ICONS["headphones"]}</div>
                                <div>
                                    <div class="audio-banner-title">
                                        Hands-Free Walking Audio Mode (15-Mark Master Essay)
                                        <span class="audio-badge-lock">{ICONS["lock_sm"]} Pocket & Lock-Screen Ready</span>
                                    </div>
                                    <div class="audio-banner-sub">
                                        Lock your Samsung tablet, put it in your pocket, and listen to all sections sequentially with human studio AI narration.
                                    </div>
                                </div>
                            </div>
                            <div class="hands-free-audio-actions">
                                <button class="btn-audio-play-all" onclick="playContinuousChapterAudio()" id="btnPlayAllChapter">
                                    {ICONS["play_sm"]} <span>Play Full Chapter (All Sections)</span>
                                </button>
                            </div>
                        </div>

                        <div class="prompt-box">
                            <div style="font-weight: 700; text-transform: uppercase; font-size: 8pt; margin-bottom: 4px;">University 15-Mark Examination Prompt</div>
                            <div>${{ch.essay_prompt}}</div>
                        </div>

                        <div class="layman-box">
                            <div style="font-weight: 700; text-transform: uppercase; font-size: 8pt; margin-bottom: 4px;">Layman's Intuitive Analogy</div>
                            <div>${{ch.layman_explanation}}</div>
                        </div>
            `;

            // Render sections with cleaned formatting, individual audio buttons, and section IDs for mini-map scrollspy
            for (const [secName, secHtml] of Object.entries(ch.sections)) {{
                const titleFormatted = secName.replace(/_/g, ' ').toUpperCase();
                const secId = 'sec_' + secName.toLowerCase();
                const isPlayingThis = (audioTrack && audioTrack.chId === ch.id && audioTrack.secKey === secName && isAudioPlaying);
                html += `
                    <div class="card essay-section-card ${{isPlayingThis ? 'audio-active-section' : ''}}" id="${{secId}}" data-sec="${{secName}}">
                        <div class="card-title" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                            <span>${{titleFormatted}}</span>
                            <button class="section-audio-pill ${{isPlayingThis ? 'speaking' : ''}}" onclick="toggleSectionAudio('${{ch.id}}', '${{secName}}', '${{titleFormatted.replace(/'/g, "\\'")}}')" id="btn_sec_audio_${{secName}}" title="Listen to this section">
                                <span class="sec-audio-icon">${{isPlayingThis ? '<span class="modern-eq-bars"><span></span><span></span><span></span></span>' : SVG_ICONS.volume}}</span>
                                <span class="sec-audio-label">${{isPlayingThis ? 'Pause Audio' : 'Listen Section'}}</span>
                            </button>
                        </div>
                        <div style="line-height: 1.7;">${{secHtml}}</div>
                    </div>
                `;
            }}

            if (ch.viva_pearls && ch.viva_pearls.length > 0) {{
                html += `
                    <div class="viva-card essay-section-card" id="sec_viva_pearls">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                            <h4 style="margin: 0; display: flex; align-items: center; gap: 8px; font-size: 11pt; color: #b45309;">
                                {ICONS["viva"]} High-Yield Clinical & Viva Examiner Pearls
                            </h4>
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <button class="btn btn-secondary" onclick="toggleVivaAnswers()" id="btnVivaAnswersToggle" style="padding: 4px 14px; font-size: 8pt; font-weight: 600; min-width: 65px;">
                                    ${{vivaAnswersVisible ? 'Hide' : 'Show'}}
                                </button>
                                <button class="btn btn-primary" onclick="switchTopicTab('quiz')" style="padding: 4px 12px; font-size: 8pt;">
                                    Practice Flashcards →
                                </button>
                            </div>
                        </div>
                        <div class="viva-pearls-container ${{vivaAnswersVisible ? '' : 'answers-hidden'}}" id="vivaContainer">
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
                            <div class="viva-qa-block" onclick="toggleSingleVivaAnswer(this)">
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <span class="viva-badge-q">Q${{pIdx + 1}}</span>
                                    <div style="flex: 1;">
                                        <div style="font-weight: 600; color: var(--primary); font-size: 9.5pt; line-height: 1.5;">${{qText}}</div>
                                        <div class="viva-click-hint" style="font-size: 7.5pt; color: var(--text-muted); margin-top: 3px;">
                                            💡 Tap question to reveal model answer
                                        </div>
                                    </div>
                                    <button class="viva-audio-speak-btn" onclick="event.stopPropagation(); speakVivaPearl(this, ${{pIdx}})" title="Listen to question & answer hands-free">
                                        ${{SVG_ICONS.volume}}
                                    </button>
                                </div>
                                <div class="viva-a-row">
                                    <strong class="viva-model-label">Model Answer: </strong>
                                    <span>${{aText}}</span>
                                </div>
                            </div>
                        `;
                    }} else {{
                        html += `
                            <div class="viva-qa-block" style="padding: 10px 14px; background: rgba(245, 158, 11, 0.06); border-left: 3px solid var(--accent); border-radius: 4px; font-size: 9pt; line-height: 1.6; display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: #b45309;">Clinical Pearl ${{pIdx + 1}}: </strong>
                                    <span>${{p}}</span>
                                </div>
                                <button class="viva-audio-speak-btn" onclick="event.stopPropagation(); speakVivaPearl(this, ${{pIdx}})" title="Listen to pearl hands-free">
                                    ${{SVG_ICONS.volume}}
                                </button>
                            </div>
                        `;
                    }}
                }});
                html += `</div></div>`;
            }}

            html += `
                    </div>
                    <aside class="sticky-minimap-rail" id="stickyMinimapRail">
                        <div class="sticky-minimap-card">
                            <div class="minimap-header">
                                <span class="minimap-title">15-Mark Essay Map</span>
                                <span class="minimap-badge">10 Sections</span>
                            </div>
                            <nav class="minimap-nav">
            `;

            for (const secName of Object.keys(ch.sections)) {{
                const titleFormatted = secName.replace(/_/g, ' ');
                const secId = 'sec_' + secName.toLowerCase();
                html += `
                    <a class="minimap-link" href="#${{secId}}" onclick="event.preventDefault(); scrollToSection('${{secId}}')">
                        <span class="minimap-dot"></span>
                        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{titleFormatted}}</span>
                    </a>
                `;
            }}

            if (ch.viva_pearls && ch.viva_pearls.length > 0) {{
                html += `
                    <a class="minimap-link" href="#sec_viva_pearls" onclick="event.preventDefault(); scrollToSection('sec_viva_pearls')">
                        <span class="minimap-dot"></span>
                        <span>Viva Examiner Pearls</span>
                    </a>
                `;
            }}

            html += `
                            </nav>
                        </div>
                    </aside>
                </div>
            `;
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
        const pairs = COMPARISON_PAIRS[ch.id] || [];
        if (pairs.length > 0) {{
            const pIdx = activeComparePairIdx < pairs.length ? activeComparePairIdx : 0;
            const pair = pairs[pIdx];
            const b64_hd = DIAGRAMS[pair.hd_file] || '';
            const b64_orig = DIAGRAMS[pair.orig_file] || '';

            let pairBtnsHtml = '';
            if (pairs.length > 1) {{
                pairBtnsHtml += '<div class="split-pair-buttons">';
                pairs.forEach((p, idx) => {{
                    pairBtnsHtml += `<button class="split-pair-btn ${{idx === pIdx ? 'active' : ''}}" onclick="switchComparePair(${{idx}})">${{p.title}}</button>`;
                }});
                pairBtnsHtml += '</div>';
            }}

            html += `
                <div class="split-comparison-card">
                    <div class="split-comparison-header">
                        <div>
                            <div style="font-weight: 700; font-size: 10.5pt; color: var(--primary); display: flex; align-items: center; gap: 8px;">
                                <span>🔄</span> Side-by-Side Split Comparison Slider
                            </div>
                            <div style="font-size: 8pt; color: var(--text-muted); margin-top: 2px;">
                                Drag the divider handle to see how lecture notes translate into clean 300 DPI schematics: <strong>${{pair.title}}</strong>
                            </div>
                        </div>
                        ${{pairBtnsHtml}}
                    </div>

                    <div class="before-after-container" id="splitCompareBox">
                        <div class="before-after-layer after-layer">
                            <img src="${{b64_hd}}" alt="${{pair.hd_label}}">
                            <span class="before-after-badge badge-right">${{pair.hd_label}}</span>
                        </div>
                        <div class="before-after-layer before-layer" id="splitBeforeWrap">
                            <img src="${{b64_orig}}" alt="${{pair.orig_label}}">
                            <span class="before-after-badge badge-left">${{pair.orig_label}}</span>
                        </div>
                        <div class="before-after-divider" id="splitDivider" style="left: 50%;">
                            <div class="before-after-handle">⮜ ⮞</div>
                        </div>
                        <input type="range" min="0" max="100" value="50" class="before-after-range" id="splitRangeInput" oninput="updateSplitSlider(this.value)">
                    </div>
                </div>
            `;
        }}

        html += `
            <div class="card">
                <div class="card-title">Original Schematics & Anatomical Diagrams</div>
                <div class="diagram-mode-bar">
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <span style="font-size: 9.5pt; font-weight: 700; color: var(--text-main);">Interactive Spotter Test:</span>
                        <button class="btn ${{spotterModeActive ? 'btn-primary' : 'btn-secondary'}}" onclick="toggleSpotterMode()" style="padding: 5px 14px; font-size: 8.5pt; font-weight: 600;">
                            ${{spotterModeActive ? '🎯 Spotter Mode: ON' : '🎯 Spotter / Test Me Mode: OFF'}}
                        </button>
                        ${{spotterModeActive ? `
                            <button class="btn btn-secondary" onclick="revealAllSpotters()" style="padding: 4px 10px; font-size: 8pt;">👁️ Reveal All</button>
                            <button class="btn btn-secondary" onclick="resetAllSpotters()" style="padding: 4px 10px; font-size: 8pt;">🔄 Hide All</button>
                        ` : ''}}
                    </div>
                    <div style="font-size: 8pt; color: var(--text-muted);">
                        ${{spotterModeActive ? '💡 Tap purple masks to flip and reveal anatomical structure names' : 'Active Viva Spotter Mode available — tap button to hide labels and test recall'}}
                    </div>
                </div>
        `;

        if (ch.diagrams && ch.diagrams.length > 0) {{
            html += `<div class="diagram-gallery">`;
            ch.diagrams.forEach((d, dIdx) => {{
                const b64 = DIAGRAMS[d.filename] || '';
                if (b64) {{
                    const isOrig = d.filename.startsWith('ch') || d.title.toLowerCase().includes('handwritten') || d.title.toLowerCase().includes('notebook');
                    const badgeHtml = isOrig
                        ? '<span class="diagram-type-badge badge-original">Original Handwritten Note</span>'
                        : '<span class="diagram-type-badge badge-hd">High-Res 300 DPI Medical Schematic</span>';
                    const safeTitle = (d.title || '').replace(/'/g, "\\'");
                    const spots = SPOTTERS[d.filename] || [];

                    let spotterOverlaysHtml = '';
                    if (spotterModeActive && spots.length > 0) {{
                        spots.forEach((h, hIdx) => {{
                            const isRev = !!revealedSpotters[d.filename + '_' + hIdx];
                            spotterOverlaysHtml += `
                                <div class="spotter-box ${{isRev ? 'revealed' : ''}}" style="top: ${{h.top}}%; left: ${{h.left}}%; width: ${{h.width}}%; height: ${{h.height}}%;" onclick="event.stopPropagation(); toggleSpotterHotspot('${{d.filename}}', ${{hIdx}})" title="Tap to flip">
                                    <div class="spotter-front">
                                        <span class="spotter-num">? ${{hIdx + 1}}</span>
                                        <span class="spotter-hint-text">${{h.hint || 'Tap to reveal'}}</span>
                                    </div>
                                    <div class="spotter-back">
                                        <span class="spotter-label-text">${{h.label}}</span>
                                    </div>
                                </div>
                            `;
                        }});
                    }}

                    html += `
                        <div class="diagram-item">
                            <div class="diagram-header-badge">${{badgeHtml}}</div>
                            <div class="spotter-interactive-container">
                                <img src="${{b64}}" onclick="openModal('${{b64}}', '${{safeTitle}}', '${{d.filename}}')" alt="${{d.title}}">
                                ${{spotterOverlaysHtml}}
                            </div>
                            <div class="diagram-item-caption">
                                ${{spotterModeActive && spots.length === 0 ? `
                                    <div style="background: rgba(2, 132, 199, 0.08); border: 1px dashed var(--primary); padding: 6px; border-radius: 6px; margin-bottom: 4px; font-size: 7.5pt; color: var(--primary); cursor: pointer;" onclick="this.nextElementSibling.style.display='block'; this.style.display='none';">
                                        🎯 Spotter Challenge: Test yourself! Tap to reveal schematic caption.
                                    </div>
                                    <div style="display: none;">${{d.title}}</div>
                                ` : d.title}}
                            </div>
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
        const pearls = ch.viva_pearls || [];
        html += `
            <div class="viva-card" style="padding: 22px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h3 style="margin: 0; display: flex; align-items: center; gap: 8px; font-size: 12pt; color: #b45309; font-weight: 700;">
                            {ICONS["viva"]} High-Yield Clinical & Viva Examiner Pearls
                        </h3>
                        <div style="font-size: 8.5pt; color: var(--text-muted); margin-top: 3px;">
                            Active Test-Yourself Mode — Answers hidden by default. Tap question or use speaker to listen hands-free.
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                        <button class="btn btn-secondary" onclick="toggleAudioPlaylist()" id="btnAudioPlaylist" style="padding: 5px 14px; font-size: 8.5pt; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                            ${{playlistRunning ? SVG_ICONS.stop_sm + ' <span>Stop Audio Walk</span>' : SVG_ICONS.headphones + ' <span>Audio Walk Mode (Play All)</span>'}}
                        </button>
                        <button class="btn btn-secondary" onclick="toggleVivaAnswers()" id="btnVivaAnswersToggle" style="padding: 5px 16px; font-size: 8.5pt; font-weight: 600; min-width: 65px;">
                            ${{vivaAnswersVisible ? 'Hide' : 'Show'}}
                        </button>
                        <button class="btn btn-primary" onclick="switchTopicTab('quiz')" style="padding: 5px 14px; font-size: 8.5pt;">
                            Practice Flashcards →
                        </button>
                    </div>
                </div>
                <div class="viva-pearls-container ${{vivaAnswersVisible ? '' : 'answers-hidden'}}" id="vivaContainer">
        `;
        pearls.forEach((p, pIdx) => {{
            let qText = p;
            let aText = "";
            if (p.includes('?')) {{
                const qEnd = p.indexOf('?') + 1;
                qText = p.substring(0, qEnd).trim();
                aText = p.substring(qEnd).trim();
            }}
            if (aText) {{
                html += `
                    <div class="viva-qa-block" onclick="toggleSingleVivaAnswer(this)">
                        <div style="display: flex; align-items: flex-start; gap: 8px;">
                            <span class="viva-badge-q">Q${{pIdx + 1}}</span>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; color: var(--primary); font-size: 9.5pt; line-height: 1.5;">${{qText}}</div>
                                <div class="viva-click-hint" style="font-size: 7.5pt; color: var(--text-muted); margin-top: 3px;">
                                    💡 Tap question to reveal model answer
                                </div>
                            </div>
                            <button class="viva-audio-speak-btn" onclick="event.stopPropagation(); speakVivaPearl(this, ${{pIdx}})" title="Listen to question & model answer hands-free">
                                ${{SVG_ICONS.volume}}
                            </button>
                        </div>
                        <div class="viva-a-row">
                            <strong class="viva-model-label">Model Answer: </strong>
                            <span>${{aText}}</span>
                        </div>
                    </div>
                `;
            }} else {{
                html += `
                    <div class="viva-qa-block" style="padding: 10px 14px; background: rgba(245, 158, 11, 0.06); border-left: 3px solid var(--accent); border-radius: 4px; font-size: 9pt; line-height: 1.6; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #b45309;">Clinical Pearl ${{pIdx + 1}}: </strong>
                            <span>${{p}}</span>
                        </div>
                        <button class="viva-audio-speak-btn" onclick="event.stopPropagation(); speakVivaPearl(this, ${{pIdx}})" title="Listen to pearl hands-free">
                            ${{SVG_ICONS.volume}}
                        </button>
                    </div>
                `;
            }}
        }});
        html += `</div></div>`;
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
                            <button class="btn btn-secondary" onclick="toggleQuizReveal()" style="min-width: 80px; font-weight: 600;">
                                ${{quizAnswerRevealed ? 'Hide' : 'Show'}}
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

    if (currentTopicTab === 'master' && !isExamSimActive) {{
        setTimeout(initScrollspy, 100);
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

let modalCurrentScale = 1.0;
let modalIsFitMode = true;

function openModal(src, title, filename) {{
    const m = document.getElementById('modal');
    const img = document.getElementById('modalImg');
    const titleEl = document.getElementById('modalTitleText');
    const fitBtn = document.getElementById('btnModalFit');
    const spotBtn = document.getElementById('btnModalSpotter');
    const spotOverlay = document.getElementById('modalSpotterOverlay');
    
    modalCurrentFilename = filename || '';
    img.src = src;
    modalCurrentScale = 1.0;
    modalIsFitMode = true;
    img.className = 'modal-fit-mode';
    img.style.transform = 'scale(1)';
    if (fitBtn) fitBtn.innerText = '100% Size';
    if (titleEl) titleEl.innerText = title || 'Medical Diagram Viewer';
    
    modalSpotterActive = false;
    if (spotOverlay) {{
        spotOverlay.style.display = 'none';
        spotOverlay.innerHTML = '';
    }}
    if (spotBtn) {{
        const hasSpots = !!(SPOTTERS[modalCurrentFilename] && SPOTTERS[modalCurrentFilename].length);
        spotBtn.style.display = hasSpots ? 'inline-block' : 'none';
        spotBtn.innerText = '🎯 Spotter Mode';
        spotBtn.style.background = '';
        spotBtn.style.color = '';
    }}
    
    m.style.display = 'flex';
}}

function closeModal() {{
    const m = document.getElementById('modal');
    if (m) m.style.display = 'none';
}}

function onModalBackdropClick(event) {{
    if (event.target.id === 'modal') {{
        closeModal();
    }}
}}

function zoomModalImg(factor) {{
    const img = document.getElementById('modalImg');
    if (!img) return;
    if (modalIsFitMode) {{
        modalIsFitMode = false;
        img.className = 'modal-actual-mode';
        const fitBtn = document.getElementById('btnModalFit');
        if (fitBtn) fitBtn.innerText = 'Fit View';
    }}
    modalCurrentScale = Math.max(0.4, Math.min(3.5, modalCurrentScale * factor));
    img.style.transform = `scale(${{modalCurrentScale}})`;
}}

function toggleModalFit() {{
    const img = document.getElementById('modalImg');
    const fitBtn = document.getElementById('btnModalFit');
    if (!img) return;
    
    if (modalIsFitMode) {{
        modalIsFitMode = false;
        modalCurrentScale = 1.0;
        img.className = 'modal-actual-mode';
        img.style.transform = 'scale(1)';
        if (fitBtn) fitBtn.innerText = 'Fit View';
    }} else {{
        modalIsFitMode = true;
        modalCurrentScale = 1.0;
        img.className = 'modal-fit-mode';
        img.style.transform = 'scale(1)';
        if (fitBtn) fitBtn.innerText = '100% Size';
    }}
}}

function openModalImgTab() {{
    const img = document.getElementById('modalImg');
    if (img && img.src) {{
        const win = window.open();
        win.document.write('<body style="margin:0; background:#090d16; display:flex; justify-content:center; align-items:center; min-height:100vh;"><img src="' + img.src + '" alt="Full Resolution Surgical Diagram" style="max-width:100%; height:auto;"></body>');
    }}
}}

window.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') {{
        closeModal();
        closePdfModal();
        const searchInput = document.getElementById('searchInput');
        if (document.activeElement === searchInput) {{
            searchInput.blur();
        }}
    }} else if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {{
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {{
            searchInput.focus();
            searchInput.select();
        }}
    }} else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {{
            searchInput.focus();
            searchInput.select();
        }}
    }}
}});

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

let vivaAnswersVisible = false; // Always hidden by default!

function toggleVivaAnswers() {{
    const container = document.getElementById('vivaContainer');
    const btn = document.getElementById('btnVivaAnswersToggle');
    if (container) {{
        vivaAnswersVisible = !vivaAnswersVisible;
        if (vivaAnswersVisible) {{
            container.classList.remove('answers-hidden');
            if (btn) btn.innerText = 'Hide';
        }} else {{
            container.classList.add('answers-hidden');
            container.querySelectorAll('.viva-qa-block.revealed').forEach(el => el.classList.remove('revealed'));
            if (btn) btn.innerText = 'Show';
        }}
    }}
}}

function toggleSingleVivaAnswer(el) {{
    const container = document.getElementById('vivaContainer');
    if (!container) return;
    if (container.classList.contains('answers-hidden')) {{
        el.classList.toggle('revealed');
    }} else {{
        const row = el.querySelector('.viva-a-row');
        if (row) {{
            row.style.display = row.style.display === 'none' ? 'block' : 'none';
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
initMasterAudio();

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {{
    window.addEventListener('load', () => {{
        navigator.serviceWorker.register('./sw.js').catch(() => {{}});
    }});
}}
</script>

<!-- Floating Background Audio Dock -->
<div id="masterAudioDock" class="audio-dock hidden">
    <div class="audio-dock-inner">
        <!-- Track & Chapter Info -->
        <div class="audio-dock-meta">
            <div class="audio-dock-track-icon">{ICONS["headphones"]}</div>
            <div class="audio-dock-text">
                <div class="audio-dock-track-title" id="audioDockTrackTitle">Section Audio</div>
                <div class="audio-dock-chapter-title" id="audioDockChapterTitle">General Surgery Monograph</div>
            </div>
        </div>

        <!-- Central Player Controls -->
        <div class="audio-dock-controls-wrap">
            <div class="audio-dock-buttons">
                <button class="audio-control-btn" onclick="prevAudioTrack()" title="Previous Section">{ICONS["prev_track"]}</button>
                <button class="audio-control-btn audio-btn-playpause" onclick="togglePlayPauseAudio()" id="audioDockPlayPauseBtn" title="Play / Pause">{ICONS["play"]}</button>
                <button class="audio-control-btn" onclick="nextAudioTrack()" title="Next Section">{ICONS["next_track"]}</button>
                <button class="audio-mode-indicator" id="audioModeBadge" title="Playback Mode">
                    <span class="mode-pulse-dot"></span>
                    <span id="audioModeBadgeText">Auto Walk</span>
                </button>
            </div>
            <div class="audio-dock-progress-wrap">
                <span class="audio-time-label" id="audioCurrentTime">00:00</span>
                <input type="range" class="audio-scrubber" id="audioProgressScrubber" min="0" max="100" value="0" oninput="onAudioScrub(this.value)" aria-label="Audio playback scrub progress">
                <span class="audio-time-label" id="audioDuration">00:00</span>
            </div>
        </div>

        <!-- Right Side: Speed Selector (1x, 1.25x, 1.5x, 2x) & Dismiss -->
        <div class="audio-dock-options">
            <div class="audio-speed-selector">
                <span class="speed-label">Speed:</span>
                <button class="speed-pill active" onclick="setAudioPlaybackRate(1.0)" data-speed="1.0">1x</button>
                <button class="speed-pill" onclick="setAudioPlaybackRate(1.25)" data-speed="1.25">1.25x</button>
                <button class="speed-pill" onclick="setAudioPlaybackRate(1.5)" data-speed="1.5">1.5x</button>
                <button class="speed-pill" onclick="setAudioPlaybackRate(2.0)" data-speed="2.0">2x</button>
            </div>
            <button class="audio-dock-close" onclick="closeAudioDock()" title="Stop and Close Player">{ICONS["close_sm"]}</button>
        </div>
    </div>
</div>
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
