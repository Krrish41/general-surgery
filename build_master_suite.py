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
import re

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
    border: 3px double #14b8a6;
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
    color: #0d9488;
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
    background-color: #f0fdfa;
    color: #0d9488;
    border: 1px solid #ccfbf1;
}}

.toc-page {{
    page-break-after: always;
    padding: 20px;
}}

.toc-title {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    color: #1e1b4b;
    border-bottom: 2px solid #14b8a6;
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
    border-bottom: 2px solid #14b8a6;
    padding-bottom: 8px;
    margin-bottom: 16px;
}}

.chapter-number {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #0d9488;
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
    color: #0d9488;
    margin: 14px 0 6px 0;
    border-left: 3px solid #14b8a6;
    padding-left: 8px;
    text-transform: capitalize;
}}

.table-responsive {{
    overflow-x: auto;
    margin: 12px 0;
}}

.clinical-flowchart-card, .formula-card, .callout, table, tr, pre, code {{
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}}

table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8pt;
    break-inside: avoid;
    page-break-inside: avoid;
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

/* Focus Timer Pill */
.focus-timer-pill {{
    display: inline-flex;
    align-items: center;
}}
.btn-focus-timer {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    font-weight: 600;
    padding: 5px 12px;
}}
.btn-focus-timer.running {{
    border-color: var(--primary);
    color: var(--primary);
    box-shadow: 0 0 10px var(--primary-light);
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
        <div style="font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #0d9488; margin-bottom: 4px;">{badge_text}</div>
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



def generate_interactive_dashboard(chapters, b64_images):
    enriched_chapters = []
    for idx, ch in enumerate(chapters):
        ch_id = ch["id"]
        
        if idx < 6:
            category = "General Surgery & Critical Care"
        elif idx < 11:
            category = "Neck & Faciomaxillary Surgery"
        elif idx < 18:
            category = "Specialized Infections, Neuro & Operative"
        elif idx < 23:
            category = "Advanced Technologies & Endocrine"
        else:
            category = "Rapid Revision & Cheat Sheet"

        clean_title = re.sub(r'^(Chapter\s*\d+[:.]*|\d+[\.:\s]+)', '', ch["title"], flags=re.IGNORECASE).strip()
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_title).strip('-').lower()
        badge = "Rapid Revision Protocol" if idx == 23 else "University High Yield"

        # Format sections
        sections_list = []
        for sec_name, sec_content in ch["sections"].items():
            sections_list.append({
                "title": sec_name.replace('_', ' ').upper(),
                "content": sec_content
            })

        # Viva pearls & flashcards
        viva_list = ch.get("viva_pearls", [])
        first_pearl = viva_list[0] if viva_list else ""
        cards = []
        for p in viva_list:
            if '?' in p:
                parts = p.split('?', 1)
                cards.append({"q": parts[0].strip() + '?', "a": parts[1].strip()})
            else:
                cards.append({"q": f"Core Surgical Clinical Question: {clean_title}", "a": p})
        if not cards:
            cards.append({"q": f"What is the surgical hallmark of {clean_title}?", "a": first_pearl})

        # Classification types
        custom_types = CLASSIFICATION_PRESETS.get(ch_id)
        if not custom_types:
            type_list = []
            for sec in sections_list[:4]:
                clean_lines = [l.strip() for l in clean_latex(sec["content"]).split('\n') if not l.strip().startswith('|') and not l.strip().startswith('#') and l.strip()]
                clean_text = ' '.join(clean_lines)
                if len(clean_text) > 220:
                    clean_text = clean_text[:220].rsplit(' ', 1)[0] + '...'
                type_list.append({
                    "name": sec["title"],
                    "badge": "Core Surgical Section",
                    "hemodynamics": "Standard Operative Protocol",
                    "summary": clean_text
                })
            custom_types = {
                "title": f"Classification & Key Concepts: {ch['title']}",
                "types": type_list
            }

        # Analogy
        analogy = {
            "title": "Surgical Intuition & Analogy",
            "analogy": ch.get("layman_explanation", first_pearl)
        }

        # Word count & reading minutes
        word_count = sum(len(s_v.split()) for s_v in ch["sections"].values())
        word_count += len(ch.get("essay_prompt", "").split())
        word_count += len(ch.get("layman_explanation", "").split())
        read_minutes = max(5, round(word_count / 180))

        viva_q_list = [c["q"] for c in cards]

        enriched_chapters.append({
            "id": ch["id"],
            "slug": slug,
            "title": ch["title"],
            "category": category,
            "badge": badge,
            "reading_time": f"{read_minutes} min read",
            "readMinutes": read_minutes,
            "readingTime": f"{read_minutes} min read",
            "tags": [category, "surgery", slug, ch["id"]],
            "clinical_pearl": first_pearl,
            "essay_prompt": ch.get("essay_prompt", ""),
            "key_points": viva_list[:3],
            "sections": sections_list,
            "diagrams": ch.get("diagrams", []),
            "analogy": analogy,
            "flashcards": cards,
            "classification": custom_types,
            "viva_questions": viva_q_list
        })

    chapters_json = json.dumps(enriched_chapters)
    images_json = json.dumps(b64_images)
    rubric_json = json.dumps(EXAM_RUBRIC_CRITERIA)
    comparisons_json = json.dumps(COMPARISON_PAIRS)
    spotters_json = json.dumps(SPOTTER_HOTSPOTS)
    presets_json = json.dumps(CLASSIFICATION_PRESETS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/svg+xml" href="favicon.svg?v=2">
    <link rel="alternate icon" href="favicon.ico?v=2">
    <link rel="apple-touch-icon" href="apple-touch-icon.png?v=2">
    <link rel="manifest" href="manifest.json?v=2">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Surgery Pro">
    <meta name="color-scheme" content="light dark">
    <meta name="theme-color" content="#090a12" id="metaThemeColor">
    <title>Surgery Pro — University Exam Monograph | BDS Clinical Vault</title>
    <script>
    (function() {{
        try {{
            var t = localStorage.getItem('bds.theme') || localStorage.getItem('bds.surgery.theme') || localStorage.getItem('surgery_theme');
            if (t === 'light') {{
                document.documentElement.setAttribute('data-theme', 'light');
                document.documentElement.classList.remove('dark');
                document.documentElement.classList.add('light');
                document.documentElement.style.colorScheme = 'light';
            }} else {{
                document.documentElement.setAttribute('data-theme', 'dark');
                document.documentElement.classList.remove('light');
                document.documentElement.classList.add('dark');
                document.documentElement.style.colorScheme = 'dark';
            }}
        }} catch(e) {{}}
    }})();
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="portal-core/core-shell.css">
    <script src="portal-core/core-engine.js"></script>
    <style>
        :root {{
            color-scheme: dark;

            /* Per-portal Accent: General Surgery Teal */
            --accent-primary: #14b8a6;
            --accent-primary-dark: #0f766e;
            --accent-btn-bg: #0f766e;
            --accent-btn-hover: #115e59;
            --accent-btn-border: rgba(20, 184, 166, 0.55);
            --accent-light: rgba(20, 184, 166, 0.12);
            --accent-glow: rgba(20, 184, 166, 0.18);
            --border-accent: rgba(20, 184, 166, 0.28);
            --accent-text: #5eead4;
            --accent-contrast: #042f2e;
            --primary: #14b8a6;
            --primary-dark: #0f766e;
            --sidebar-w: 304px;

            /* Shared Neutral Tokens (Obsidian Dark Default) */
            --bg-base: #090a12;
            --bg-surface: #101322;
            --bg-card: #101322;
            --bg-card-hover: #171b30;
            --border-color: rgba(255, 255, 255, 0.09);
            --border-strong: rgba(255, 255, 255, 0.18);
            --border-active: #14b8a6;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --header-bg: rgba(9, 10, 18, 0.94);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.7);
        }}

        html[data-theme="light"], body.light {{
            color-scheme: light;
            --bg-base: #f8fafc;
            --bg-surface: #ffffff;
            --bg-card: #ffffff;
            --bg-card-hover: #f1f5f9;
            --border-color: #e2e8f0;
            --border-strong: #cbd5e1;
            --border-active: #14b8a6;
            --text-primary: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
            --header-bg: rgba(255, 255, 255, 0.94);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.12);
        }}

        html[data-theme="dark"], body.dark {{
            color-scheme: dark;
            --bg-base: #090a12;
            --bg-surface: #101322;
            --bg-card: #101322;
            --bg-card-hover: #171b30;
            --border-color: rgba(255, 255, 255, 0.09);
            --border-strong: rgba(255, 255, 255, 0.18);
            --border-active: #14b8a6;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --accent-primary: #14b8a6;
            --accent-primary-dark: #0f766e;
            --accent-light: rgba(20, 184, 166, 0.12);
            --accent-glow: rgba(20, 184, 166, 0.18);
            --header-bg: rgba(9, 10, 18, 0.94);
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.4);
            --shadow-md: 0 4px 14px rgba(0,0,0,0.5);
            --shadow-lg: 0 10px 30px rgba(0,0,0,0.7);
        }}

        /* Ultra-thin surgical scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(148, 163, 184, 0.35);
            border-radius: 999px;
            border: 1px solid transparent;
            background-clip: content-box;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(100, 116, 139, 0.6);
        }}
        body.dark ::-webkit-scrollbar-thumb {{
            background: rgba(148, 163, 184, 0.25);
        }}
        body.dark ::-webkit-scrollbar-thumb:hover {{
            background: rgba(148, 163, 184, 0.45);
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            scrollbar-width: thin;
            scrollbar-color: rgba(148, 163, 184, 0.35) transparent;
        }}

        /* Tactile button feedback */
        .btn:active, .nav-btn:active, .speed-pill:active, .filter-chip:active {{
            transform: scale(0.96) translateY(1px);
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-primary);
            line-height: 1.6;
            height: 100vh;
            display: flex;
            flex-direction: row;
            overflow: hidden;
            font-size: 14px;
        }}

        #sidebar-backdrop {{
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            z-index: 95;
        }}
        #sidebar-backdrop.active {{
            display: block;
        }}

        /* Sidebar - Docked 304px (Spec 2.6) */
        .sidebar {{
            width: 304px;
            min-width: 304px;
            max-width: 304px;
            flex-shrink: 0;
            border-right: 1px solid var(--border-color);
            background: var(--bg-surface);
            display: flex;
            flex-direction: column;
            height: 100vh;
            position: sticky;
            top: 0;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 100;
        }}

        /* Main View / Main Column */
        .main-column {{
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow-y: auto;
            position: relative;
            background: var(--bg-base);
        }}

        /* 64px Topbar */
        .top-bar {{
            height: 64px;
            min-height: 64px;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-color);
            background: var(--bg-surface);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            position: sticky;
            top: 0;
            z-index: 90;
            gap: 12px;
            flex-shrink: 0;
        }}

        .top-bar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 0;
        }}

        .top-right-tools {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }}

        @media (max-width: 1150px) {{
            .top-right-tools .btn-label {{
                display: none;
            }}
        }}

        .mobile-menu-btn {{
            display: none;
            background: none;
            border: none;
            cursor: pointer;
            color: var(--text-primary);
            padding: 6px;
            border-radius: var(--radius-sm);
        }}

        @media (max-width: 1024px) {{
            .mobile-menu-btn {{
                display: inline-flex;
            }}
            .sidebar {{
                position: fixed;
                left: -320px;
                top: 0;
                bottom: 0;
                width: 290px;
                min-width: 290px;
            }}
            .sidebar.open, .sidebar.active {{
                transform: translateX(320px);
            }}
        }}

        .nav-btn {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: var(--shadow-sm);
        }}

        .nav-btn:hover {{
            background: var(--accent-light);
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }}

        .nav-btn-primary {{
            background: var(--accent-btn-bg);
            color: #ffffff !important;
            border: 1px solid var(--accent-btn-border);
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
        }}
        .nav-btn-primary:hover {{
            background: var(--accent-btn-hover);
            border-color: var(--accent-primary);
            color: #ffffff !important;
            box-shadow: 0 0 14px var(--accent-glow);
        }}

        .sidebar-header {{
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
        }}

        .search-box {{
            position: relative;
            margin-bottom: 10px;
        }}

        .search-input {{
            width: 100%;
            padding: 9px 36px 9px 12px;
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 0.85rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s ease;
        }}
        .search-input:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }}

        .search-kbd-btn {{
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 0.72rem;
            display: flex;
            align-items: center;
            padding: 0;
            z-index: 2;
        }}
        .kbd-label {{
            background: var(--bg-surface, rgba(255, 255, 255, 0.08));
            border: 1px solid var(--border-color, rgba(255, 255, 255, 0.12));
            border-radius: 4px;
            padding: 2px 5px;
            font-size: 0.68rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            font-weight: 600;
            line-height: 1;
            pointer-events: none;
        }}

        .category-scroll {{
            display: flex;
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .filter-chip {{
            white-space: nowrap;
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.72rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 999px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .filter-chip:hover:not(.active) {{
            background: var(--accent-light);
            color: var(--text-primary);
            border-color: var(--border-accent);
        }}
        .filter-chip.active {{
            background: var(--accent-btn-bg);
            color: #ffffff !important;
            border-color: var(--accent-btn-border);
            box-shadow: 0 0 10px var(--accent-glow);
            font-weight: 700;
        }}
        .filter-chip.active:hover {{
            background: var(--accent-btn-hover);
            border-color: var(--accent-primary);
            color: #ffffff !important;
        }}

        .topic-list {{
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }}

        .topic-item {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
            margin-bottom: 4px;
            border: 1px solid transparent;
        }}
        .topic-item:hover {{
            background: var(--bg-card-hover);
        }}
        .topic-item.active {{
            background: var(--accent-light);
            border-color: var(--accent-primary);
        }}
        .topic-check {{
            margin-top: 2px;
            color: var(--text-muted);
            cursor: pointer;
            flex-shrink: 0;
        }}
        .topic-check.completed {{
            color: var(--accent-primary);
        }}
        .topic-info {{
            flex: 1;
            min-width: 0;
        }}
        .topic-title {{
            font-size: 0.86rem;
            font-weight: 600;
            color: var(--text-primary);
            line-height: 1.35;
            white-space: normal;
            word-break: break-word;
        }}
        .topic-meta {{
            font-size: 0.72rem;
            color: var(--text-secondary);
            font-weight: 500;
            margin-top: 2px;
        }}

        /* Content Area */
        .content-area {{
            flex: 1;
            min-width: 0;
            padding: 24px 32px 120px 32px;
            overflow-y: auto;
        }}

        /* Dashboard Hero */
        .dash-hero {{
            background: linear-gradient(135deg, rgba(147, 51, 234, 0.08), rgba(126, 34, 206, 0.03));
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .dash-badge {{
            display: inline-block;
            background: var(--accent-light);
            color: var(--accent-primary);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        .dash-title {{
            font-family: 'Newsreader', serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .dash-subtitle {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-bottom: 28px;
        }}
        .stat-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px 18px;
            box-shadow: var(--shadow-sm);
        }}
        .stat-val {{
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--accent-primary);
            line-height: 1.1;
        }}
        .stat-lbl {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 4px;
        }}

        /* Chapter View Header & Tabs */
        .chapter-header {{
            margin-bottom: 20px;
        }}
        .chapter-top-badge {{
            display: inline-block;
            background: var(--accent-light);
            color: var(--accent-primary);
            font-size: 0.75rem;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            margin-bottom: 8px;
            border: 1px solid var(--accent-primary);
        }}
        html[data-theme="light"] .chapter-top-badge,
        body.light .chapter-top-badge {{
            background: rgba(20, 184, 166, 0.12);
            color: #0f766e;
            border-color: rgba(20, 184, 166, 0.4);
        }}
        html[data-theme="dark"] .chapter-top-badge,
        body.dark .chapter-top-badge {{
            background: rgba(20, 184, 166, 0.18);
            color: #5eead4;
            border-color: rgba(20, 184, 166, 0.6);
        }}
        .chapter-title-display {{
            font-family: 'Newsreader', serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.2;
            letter-spacing: -0.5px;
        }}

        .tab-bar-container {{
            position: relative;
            background: var(--bg-base);
            z-index: 30;
            padding: 10px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }}
        .tab-bar {{
            display: flex;
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}
        .tab-btn {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.82rem;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: var(--shadow-sm);
        }}
        .tab-btn:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}
        .tab-btn.active {{
            background: var(--accent-btn-bg);
            color: #ffffff !important;
            border-color: var(--accent-btn-border);
            box-shadow: 0 4px 12px var(--accent-glow);
            font-weight: 700;
        }}

        /* 15-Mark Master Essay Reading Ergonomics */
        .master-essay-content {{
            max-width: 76ch;
            margin: 0 auto;
        }}
        .pearl-card {{
            background: var(--accent-light);
            border-left: 4px solid var(--accent-primary);
            border-radius: 0 8px 8px 0;
            padding: 14px 18px;
            margin-bottom: 24px;
            font-size: 0.92rem;
            color: var(--text-primary);
        }}
        .essay-section-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 20px;
            box-shadow: var(--shadow-sm);
        }}
        .essay-section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }}
        .essay-section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .essay-body {{
            font-size: 0.96rem;
            line-height: 1.72;
            color: var(--text-secondary);
        }}
        .essay-body h4 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 18px 0 8px 0;
        }}
        .essay-body p {{
            margin-bottom: 14px;
        }}
        .essay-body ul, .essay-body ol {{
            padding-left: 22px;
            margin-bottom: 14px;
        }}
        .essay-body li {{
            margin-bottom: 6px;
        }}
        .essay-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            font-size: 0.88rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }}
        .essay-body th, .essay-body td {{
            padding: 10px 14px;
            border: 1px solid var(--border-color);
            text-align: left;
        }}
        .essay-body th {{
            background: var(--bg-base);
            color: var(--text-primary);
            font-weight: 700;
        }}
        .essay-body tr:nth-child(even) {{
            background: var(--bg-card-hover);
        }}
        .essay-body pre {{
            background: #0f172a;
            color: #f0abfc;
            border-radius: 8px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            margin: 16px 0;
        }}

        /* Layman Intuition Card */
        .layman-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 28px;
            box-shadow: var(--shadow-sm);
        }}
        .layman-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }}
        .layman-badge {{
            background: #fdf4ff;
            color: #86198f;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 6px;
        }}
        .layman-title {{
            font-family: 'Newsreader', serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .layman-body {{
            font-size: 1.02rem;
            line-height: 1.8;
            color: var(--text-secondary);
        }}

        /* Classification / Types Explorer */
        .types-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 18px;
        }}
        .type-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }}
        .type-card:hover {{
            border-color: var(--accent-primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        .type-card-badge {{
            display: inline-block;
            background: var(--accent-light);
            color: var(--accent-primary);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 8px;
        }}
        .type-card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }}
        .type-card-stat {{
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-primary);
            margin-bottom: 10px;
        }}
        .type-card-summary {{
            font-size: 0.88rem;
            color: var(--text-secondary);
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
            transition: all 0.2s ease;
        }}
        .type-card-summary.expanded {{
            display: block;
            -webkit-line-clamp: unset;
            overflow: visible;
        }}

        /* Diagrams Gallery */
        .diagram-container {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }}
        .diagram-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 14px;
        }}
        .diagram-viewer-box {{
            cursor: zoom-in;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            background: #0f172a;
        }}

        /* Examiner Viva Voce */
        .viva-item {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 14px;
            box-shadow: var(--shadow-sm);
        }}
        .viva-q {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }}
        .viva-speaker-btn {{
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--accent-primary);
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            flex-shrink: 0;
            transition: all 0.2s ease;
        }}
        .viva-speaker-btn:hover {{
            background: var(--accent-light);
            border-color: var(--accent-primary);
        }}
        .viva-reveal-btn {{
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.8rem;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 6px;
        }}
        .viva-ans {{
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed var(--border-color);
            font-size: 0.92rem;
            color: var(--text-secondary);
            display: none;
        }}
        .viva-ans.revealed {{
            display: block;
        }}

        /* Active Recall Flashcards */
        .flashcard-wrap {{
            max-width: 620px;
            margin: 20px auto;
            perspective: 1000px;
        }}
        .flashcard {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            min-height: 280px;
            padding: 36px 32px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            cursor: pointer;
            box-shadow: var(--shadow-md);
            position: relative;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .flashcard:hover {{
            border-color: var(--accent-primary);
        }}
        .flashcard-tag {{
            position: absolute;
            top: 18px;
            left: 20px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--accent-primary);
        }}
        .flashcard-instruction {{
            position: absolute;
            bottom: 16px;
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-weight: 600;
        }}
        .flashcard-text {{
            font-size: 1.18rem;
            font-weight: 600;
            color: var(--text-primary);
            line-height: 1.6;
        }}
        .flashcard-controls {{
            display: flex;
            justify-content: center;
            gap: 14px;
            margin-top: 20px;
        }}

        /* Exam Simulator & Rubric */
        .exam-sim-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 24px;
            box-shadow: var(--shadow-sm);
        }}
        .rubric-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 12px 0;
            border-bottom: 1px solid var(--border-color);
        }}
        .rubric-info h4 {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        .rubric-info p {{
            font-size: 0.82rem;
            color: var(--text-muted);
        }}
        .rubric-slider {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        /* Clinical Notes */
        .notes-textarea {{
            width: 100%;
            height: 380px;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            font-family: inherit;
            font-size: 0.95rem;
            color: var(--text-primary);
            line-height: 1.6;
            outline: none;
            resize: vertical;
        }}
        .notes-textarea:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px var(--accent-glow);
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
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(28px) saturate(180%);
            -webkit-backdrop-filter: blur(28px) saturate(180%);
            border: 1px solid rgba(20, 184, 166, 0.35);
            border-radius: 22px;
            box-shadow: 0 16px 42px -6px rgba(15, 23, 42, 0.25), 0 4px 16px rgba(0, 0, 0, 0.05);
            padding: 12px 22px;
            display: block;
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
        }}
        body.dark .audio-dock,
        html[data-theme="dark"] .audio-dock {{
            background: rgba(16, 19, 34, 0.95);
            border: 1px solid rgba(20, 184, 166, 0.4);
            box-shadow: 0 20px 50px -8px rgba(0, 0, 0, 0.75), 0 0 24px rgba(20, 184, 166, 0.18);
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
            background: linear-gradient(135deg, #9333ea 0%, #7e22ce 100%);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);
        }}
        .audio-dock.is-playing .audio-dock-track-icon {{
            animation: pulseTrackIcon 2.4s ease-in-out infinite;
        }}
        @keyframes pulseTrackIcon {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3); }}
            50% {{ transform: scale(1.05); box-shadow: 0 6px 18px rgba(147, 51, 234, 0.45); }}
        }}
        .audio-dock-track-title {{
            font-size: 9pt;
            font-weight: 700;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .audio-dock-chapter-title {{
            font-size: 7.5pt;
            color: var(--text-secondary);
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
            min-width: 240px;
        }}
        .audio-dock-buttons {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .audio-control-btn {{
            background: transparent;
            border: none;
            color: var(--text-primary);
            cursor: pointer;
            padding: 6px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }}
        .audio-control-btn:hover {{
            background: var(--bg-card-hover);
            color: var(--accent-primary);
        }}
        .audio-btn-playpause {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--accent-btn-bg);
            border: 1px solid var(--accent-btn-border);
            color: #ffffff !important;
            box-shadow: 0 4px 14px var(--accent-glow);
        }}
        .audio-btn-playpause:hover {{
            background: var(--accent-btn-hover);
            transform: scale(1.04);
        }}
        .audio-dock-progress-wrap {{
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
            max-width: 440px;
        }}
        .audio-time-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 7.5pt;
            color: var(--text-secondary);
            min-width: 36px;
            font-weight: 600;
        }}
        .audio-scrubber {{
            flex: 1;
            -webkit-appearance: none;
            appearance: none;
            height: 4px;
            border-radius: 999px;
            background: #cbd5e1;
            outline: none;
            cursor: pointer;
        }}
        body.dark .audio-scrubber {{
            background: #334155;
        }}
        .audio-scrubber::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-primary);
            cursor: pointer;
        }}
        .audio-dock-options {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 0;
        }}
        .audio-voice-select {{
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            font-size: 7.5pt;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 8px;
            outline: none;
            cursor: pointer;
            max-width: 160px;
        }}
        .audio-speed-selector {{
            display: flex;
            align-items: center;
            gap: 4px;
            background: var(--bg-base);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 3px 6px;
        }}
        .speed-label {{
            font-size: 7.5pt;
            color: var(--text-primary);
            font-weight: 700;
            margin-right: 2px;
        }}
        .speed-pill {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 7.5pt;
            font-weight: 700;
            padding: 3px 6px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .speed-pill:hover {{
            color: var(--accent-primary);
        }}
        .speed-pill.active {{
            background: var(--accent-btn-bg);
            color: #ffffff !important;
            border: 1px solid var(--accent-btn-border);
            font-weight: 700;
        }}
        .audio-dock-close {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 6px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .audio-dock-close:hover {{
            background: var(--bg-card-hover);
            color: #ef4444;
        }}
        body.is-dashboard .content-area {{
            padding-bottom: 36px !important;
        }}

        /* Modals */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.82);
            backdrop-filter: blur(8px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
            padding: 20px;
        }}
        .modal-box {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            max-width: 960px;
            width: 100%;
            max-height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }}
        .modal-header {{
            padding: 14px 20px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .modal-body {{
            padding: 20px;
            overflow-y: auto;
            flex: 1;
        }}

        @media (max-width: 1024px) {{
            .audio-dock {{
                bottom: 74px !important;
                padding: 10px 16px;
            }}
            .sidebar {{
                position: fixed;
                left: 0;
                top: 61px;
                bottom: 0;
                transform: translateX(-100%);
            }}
            .sidebar.open {{
                transform: translateX(0);
            }}
            .content-area {{
                padding: 16px 16px calc(40px + env(safe-area-inset-bottom, 20px)) 16px;
            }}
            .dash-hero-card {{
                flex-direction: column !important;
                padding: 20px 18px !important;
                align-items: flex-start !important;
                gap: 16px !important;
            }}
            .dash-hero-image-box {{
                display: none !important;
            }}
            .dash-hero-title {{
                font-size: 1.45rem !important;
                line-height: 1.25 !important;
            }}
            .dash-hero-sub {{
                font-size: 0.85rem !important;
                line-height: 1.45 !important;
                margin-bottom: 12px !important;
            }}
            .dash-hero-badge {{
                font-size: 0.68rem !important;
                letter-spacing: 0.08em !important;
                line-height: 1.3 !important;
                border-radius: 9999px !important;
                max-width: 100% !important;
            }}
            .dash-hero-meta {{
                gap: 8px !important;
            }}
            .dash-hero-stat {{
                font-size: 0.76rem !important;
                padding: 4px 10px !important;
            }}
            .dash-cheat-sheet-card {{
                padding: 16px !important;
                flex-direction: column !important;
                align-items: stretch !important;
                gap: 14px !important;
            }}
            .dash-cheat-sheet-card .nav-btn-primary {{
                width: 100% !important;
                justify-content: center !important;
                text-align: center !important;
            }}
            .stats-grid-dashboard {{
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 10px !important;
            }}
            .stat-card-box {{
                padding: 12px 14px !important;
            }}
            .stat-card-val {{
                font-size: 1.5rem !important;
            }}
            .stat-card-label {{
                font-size: 0.68rem !important;
            }}
            .dashboard-topic-cards-grid {{
                grid-template-columns: 1fr !important;
                gap: 12px !important;
            }}
        }}

        @media (max-width: 480px) {{
            .stats-grid-dashboard {{
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 8px !important;
            }}
        }}

        @media (max-width: 640px) {{
            .navbar {{
                padding: 0.6rem 1rem;
            }}
            .chapter-title-display {{
                font-size: 1.6rem;
            }}
            .audio-dock {{
                width: calc(100% - 24px);
                padding: 8px 12px;
            }}
            .audio-voice-wrap {{
                display: none;
            }}
        }}

        /* Responsive Data Tables */
        .table-responsive {{
            width: 100%;
            overflow-x: auto;
            margin: 18px 0 24px 0;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            background: var(--bg-surface);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            line-height: 1.5;
            text-align: left;
            font-variant-numeric: tabular-nums;
        }}

        .data-table th, .data-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
        }}

        .data-table th {{
            background: var(--bg-surface);
            color: var(--accent-primary);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.74rem;
            letter-spacing: 0.06em;
            border-bottom: 2px solid var(--accent-primary);
        }}

        .data-table tbody tr:nth-child(even) {{
            background: rgba(99, 102, 241, 0.03);
        }}

        body.dark .data-table tbody tr:nth-child(even) {{
            background: rgba(255, 255, 255, 0.02);
        }}

        .data-table tbody tr:hover {{
            background: rgba(99, 102, 241, 0.08);
        }}

        /* Clinical Formula Callout Box */
        .formula-card {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.04) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-left: 4px solid var(--accent-primary);
            border-radius: 10px;
            padding: 14px 18px;
            margin: 16px 0;
        }}

        .formula-header {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--accent-primary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }}

        .formula-equation {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-primary);
            padding: 4px 0;
        }}

        /* Callout Alerts */
        .callout-alert {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 14px 18px;
            border-radius: 10px;
            margin: 16px 0;
            font-size: 0.92rem;
            line-height: 1.55;
        }}

        .callout-alert.alert-tip {{
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-left: 4px solid #10b981;
            color: var(--text-primary);
        }}

        .callout-alert.alert-note {{
            background: rgba(217, 70, 239, 0.08);
            border: 1px solid rgba(217, 70, 239, 0.25);
            border-left: 4px solid #d946ef;
            color: var(--text-primary);
        }}

        .callout-alert.alert-important {{
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-left: 4px solid #f59e0b;
            color: var(--text-primary);
        }}

        .content-list, .content-list-ordered {{
            padding-left: 24px;
            margin: 10px 0 16px 0;
        }}

        .content-list li, .content-list-ordered li {{
            margin-bottom: 6px;
            line-height: 1.55;
            color: var(--text-secondary);
        }}

        .content-para {{
            margin-bottom: 12px;
            line-height: 1.65;
            color: var(--text-secondary);
        }}

        .algorithm-block {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 14px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            margin: 16px 0;
            color: var(--text-primary);
        }}

        .inline-code {{
            background: rgba(99, 102, 241, 0.1);
            color: var(--accent-primary);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85em;
        }}

        /* Dashboard Specific Styles matching Calm Obsidian Theme */
        .dash-hero-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-primary);
            border-radius: 14px;
            padding: 26px 30px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
        }}

        .dash-hero-badge {{
            display: inline-block;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            background: var(--accent-light);
            color: var(--accent-primary);
            padding: 4px 12px;
            border-radius: 9999px;
            margin-bottom: 12px;
        }}

        .dash-hero-title {{
            font-size: 1.9rem;
            font-weight: 800;
            color: var(--text-primary);
            margin: 0 0 8px 0;
            letter-spacing: -0.02em;
            line-height: 1.25;
        }}

        .dash-hero-sub {{
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin: 0 0 16px 0;
            line-height: 1.5;
        }}

        .dash-hero-meta {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .dash-hero-stat {{
            font-size: 0.84rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            padding: 5px 14px;
            border-radius: 9999px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .dash-hero-image-box {{
            flex-shrink: 0;
            width: 260px;
            height: 140px;
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
        }}

        .dash-cheat-sheet-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-primary);
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
        }}

        .cheat-sheet-badge-icon {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: var(--accent-light);
            border: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            color: var(--accent-primary);
        }}

        .stats-grid-dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .stat-card-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: var(--shadow-sm);
        }}

        .stat-card-label {{
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-bottom: 6px;
            font-weight: 600;
        }}

        .stat-card-val {{
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--accent-primary);
            line-height: 1.2;
        }}

        .progress-banner-dash {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }}

        .progress-bar-bg-dash {{
            width: 100%;
            height: 9px;
            background-color: var(--border-color);
            border-radius: 999px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-bar-fill-dash {{
            height: 100%;
            background: linear-gradient(90deg, #0f766e 0%, #14b8a6 50%, #38bdf8 100%);
            border-radius: 999px;
            width: 0%;
            transition: width 0.4s ease;
        }}

        .dashboard-topic-cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
            gap: 16px;
        }}

        .dash-topic-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s ease;
            box-shadow: var(--shadow-sm);
        }}

        .dash-topic-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-md);
        }}

        .dash-topic-card.completed {{
            border-color: rgba(16, 185, 129, 0.4);
            background: rgba(16, 185, 129, 0.02);
        }}

        .dash-card-header-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }}

        .dash-card-chapter-tag {{
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--accent-primary);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        .dash-card-title-text {{
            font-size: 1.02rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.35;
            margin-bottom: 6px;
        }}

        .dash-card-source-text {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 16px;
        }}

        .dash-card-footer-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
        }}

        .toggle-complete-btn {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.78rem;
            padding: 6px 12px;
            border-radius: 7px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .toggle-complete-btn:hover {{
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }}

        .toggle-complete-btn.is-completed {{
            background: rgba(16, 185, 129, 0.1);
            border-color: #10b981;
            color: #10b981;
        }}

        /* Focus Timer Pill */
        .focus-timer-pill {{
            display: inline-flex;
            align-items: center;
        }}
        .btn-focus-timer {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .btn-focus-timer.running {{
            border-color: var(--accent-primary) !important;
            color: var(--accent-primary) !important;
            box-shadow: 0 0 10px var(--accent-glow) !important;
        }}

        .search-kbd-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 0.72rem;
            display: flex;
            align-items: center;
            padding: 0 6px;
        }}
    </style>
</head>
<body class="dark is-dashboard">
    <!-- Docked Sidebar Render Target -->
    <aside class="portal-sidebar" id="sidebar" data-testid="sidebar"></aside>

    <!-- Main View Column -->
    <div class="main-column" id="mainView">
        <header class="portal-topbar" id="portalTopBar" data-testid="topbar"></header>

        <!-- Main Content Viewer -->
        <main class="content-area" id="mainContent">
            <!-- Dynamically rendered (Dashboard or Chapter View) -->
        </main>
    </div>

    <!-- Floating Island Audio Dock -->
    <div id="masterAudioDock" class="audio-dock hidden">
        <div class="audio-dock-inner">
            <div class="audio-dock-meta">
                <div class="audio-dock-track-icon">{ICONS["headphones"]}</div>
                <div class="audio-dock-text">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="audio-dock-track-title" id="audioDockTrackTitle">15-Mark Answer</div>
                        <button class="audio-switch-pill" onclick="openAudioSectionModal()" title="Switch Audio Section">Switch ▾</button>
                    </div>
                    <div class="audio-dock-chapter-title" id="audioDockChapterTitle">General Surgery Monograph</div>
                </div>
            </div>

            <div class="audio-dock-controls-wrap">
                <div class="audio-dock-buttons">
                    <button class="audio-control-btn" onclick="prevAudioTrack()" title="Previous Section">{ICONS["prev_track"]}</button>
                    <button class="audio-control-btn audio-btn-playpause" onclick="togglePlayPauseAudio()" id="audioDockPlayPauseBtn" title="Play / Pause">{ICONS["play"]}</button>
                    <button class="audio-control-btn" onclick="nextAudioTrack()" title="Next Section">{ICONS["next_track"]}</button>
                </div>
                <div class="audio-dock-progress-wrap">
                    <span class="audio-time-label" id="audioCurrentTime">0:00</span>
                    <input type="range" class="audio-scrubber" id="audioProgressScrubber" min="0" max="100" value="0" oninput="onAudioScrub(this.value)" aria-label="Audio playback progress scrubber">
                    <span class="audio-time-label" id="audioDuration">0:00</span>
                </div>
            </div>

            <div class="audio-dock-options">
                <div class="audio-voice-wrap" title="Narration Voice Engine">
                    <span class="speed-label">Voice:</span>
                    <select id="audioVoiceSelect" class="audio-voice-select" onchange="onVoiceSelected(this.value)" aria-label="Select Narration Voice">
                        <option value="auto">Natural / System Default</option>
                    </select>
                </div>
                <div class="audio-speed-selector">
                    <span class="speed-label">Speed:</span>
                    <button class="speed-pill active" onclick="setAudioPlaybackRate(1.0)" data-speed="1.0">1x</button>
                    <button class="speed-pill" onclick="setAudioPlaybackRate(1.25)" data-speed="1.25">1.25x</button>
                    <button class="speed-pill" onclick="setAudioPlaybackRate(1.5)" data-speed="1.5">1.5x</button>
                    <button class="speed-pill" onclick="setAudioPlaybackRate(2.0)" data-speed="2.0">2x</button>
                </div>
                <button class="audio-dock-close" onclick="closeAudioDock()" title="Stop and Close Player">{ICONS["close"]}</button>
            </div>
        </div>
    </div>

    <!-- Audio Section Selection Modal -->
    <div class="modal-overlay" id="audioSectionModal" onclick="closeAudioSectionModal(event)">
        <div class="audio-section-modal-box" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div>
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-primary);">Audio Walk • Narration Mode</div>
                    <h3 id="audioModalTopicTitle" style="font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin-top: 2px;">Select Narration Section</h3>
                </div>
                <button class="audio-dock-close" onclick="closeAudioSectionModal()">{ICONS["close"]}</button>
            </div>
            <div class="audio-section-modal-body">
                <p style="font-size: 0.82rem; color: var(--text-secondary); margin: 0 0 4px 0;">Choose which clinical section to listen to in this topic:</p>
                <div class="audio-section-options-grid">
                    <div class="audio-section-card" onclick="selectAndPlaySection('master')">
                        <div class="audio-section-card-header">
                            <span class="audio-section-badge">Standard Essay</span>
                            <span style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">~12-15 min</span>
                        </div>
                        <div class="audio-section-card-title">15-Mark Master Answer</div>
                        <div class="audio-section-card-desc">Comprehensive surgical essay covering definition, classification, surgical anatomy, clinical signs, differential diagnosis, and step-by-step operative management.</div>
                        <button class="audio-card-btn" onclick="event.stopPropagation(); selectAndPlaySection('master');">
                            {ICONS["play"]} Play 15-Mark Answer
                        </button>
                    </div>

                    <div class="audio-section-card" onclick="selectAndPlaySection('viva')">
                        <div class="audio-section-card-header">
                            <span class="audio-section-badge viva">High-Yield Viva</span>
                            <span style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">~4-6 min</span>
                        </div>
                        <div class="audio-section-card-title">Examiner Viva Pearls</div>
                        <div class="audio-section-card-desc">High-frequency viva questions, chairside pearls, eponyms, examiner traps, and quick-fire clinical points.</div>
                        <button class="audio-card-btn" style="background: #d946ef; color: #fff;" onclick="event.stopPropagation(); selectAndPlaySection('viva');">
                            {ICONS["play"]} Play Viva Pearls
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Master PDF Modal -->
    <div class="modal-overlay" id="pdfModal" onclick="closePdfModal(event)">
        <div class="modal-box" style="height: 85vh;" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 style="font-size: 1.1rem; font-weight: 700;">General Surgery Master Compendium (PDF)</h3>
                <div style="display: flex; gap: 8px;">
                    <a href="General_Surgery_Master_Notes.pdf" download class="nav-btn nav-btn-primary" style="padding: 4px 10px; font-size: 0.78rem;">Download</a>
                    <button class="audio-dock-close" onclick="closePdfModal()">{ICONS["close"]}</button>
                </div>
            </div>
            <div class="modal-body" style="padding: 0;">
                <iframe src="General_Surgery_Master_Notes.pdf" style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
        </div>
    </div>

    <!-- Spotter / Diagram Zoom Modal -->
    <div class="modal-overlay" id="modal" onclick="closeDiagramModal(event)">
        <div class="modal-box" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 id="modalDiagramTitle" style="font-size: 1.1rem; font-weight: 700;">Microscopic Spotter Schematic</h3>
                <button class="audio-dock-close" onclick="closeDiagramModal()">{ICONS["close"]}</button>
            </div>
            <div class="modal-body" id="modalDiagramBody" style="display:flex; justify-content:center; align-items:center; background:#0f172a;">
                <!-- Injected SVG / Image -->
            </div>
        </div>
    </div>

    <!-- Application Script Bundle -->
    <script>
        const CHAPTERS = {chapters_json};
        const DIAGRAMS = {images_json};
        const PRESETS = {presets_json};
        const SPOTTERS = {spotters_json};
        const COMPARISONS = {comparisons_json};
        const RUBRIC = {rubric_json};

        let currentChapterIdx = -1;
        let currentDashFilter = 'all';
        let activeTab = 'master';
        let currentCategory = 'All';
        let completedTopics = JSON.parse(localStorage.getItem('bds.surgery.progress') || localStorage.getItem('surgery_completed_topics') || '{{}}');
        let currentFlashcardIdx = 0;
        let isFlashcardFlipped = false;

        // --- Sentence-Chunked Smooth Audio & Narration Engine ---
        let availableVoices = [];
        let selectedVoice = null;
        let isAudioPlaying = false;
        let audioPlaybackSpeed = 1.0;
        let activeAudioSectionType = 'master'; // 'master' or 'viva'
        let currentSentences = [];
        let currentSentenceIdx = 0;
        let estTotalDurationSec = 0;
        let speechTickerTimer = null;
        let audioElapsedSec = 0;

        function initVoiceList() {{
            if (!('speechSynthesis' in window)) return;
            const updateVoices = () => {{
                const all = window.speechSynthesis.getVoices();
                if (!all || all.length === 0) return;

                const pickVoice = (langPrefix) => {{
                    const regional = all.filter(v => v.lang && v.lang.toLowerCase().replace('_', '-').startsWith(langPrefix.toLowerCase()));
                    if (regional.length === 0) return null;
                    return regional.find(v => /natural|neural|online|google|samantha|karen|daniel|rishi|veena/i.test(v.name)) || regional[0];
                }};

                const curated = [
                    {{ key: 'auto', label: 'Natural / System Default', voice: null }},
                    {{ key: 'us', label: 'English (United States)', voice: pickVoice('en-US') }},
                    {{ key: 'gb', label: 'English (United Kingdom)', voice: pickVoice('en-GB') }},
                    {{ key: 'in', label: 'English (India)', voice: pickVoice('en-IN') }},
                    {{ key: 'au', label: 'English (Australia)', voice: pickVoice('en-AU') }}
                ].filter(item => item.key === 'auto' || item.voice !== null);

                availableVoices = curated;
                const select = document.getElementById('audioVoiceSelect');
                if (!select) return;

                const savedKey = localStorage.getItem('bds_curated_voice_key') || 'auto';
                select.innerHTML = '';

                curated.forEach(item => {{
                    const opt = document.createElement('option');
                    opt.value = item.key;
                    opt.textContent = item.label;
                    if (item.key === savedKey) {{
                        opt.selected = true;
                        selectedVoice = item.voice;
                    }}
                    select.appendChild(opt);
                }});
            }};

            updateVoices();
            if (window.speechSynthesis.onvoiceschanged !== undefined) {{
                window.speechSynthesis.onvoiceschanged = updateVoices;
            }}
        }}

        function onVoiceSelected(key) {{
            localStorage.setItem('bds_curated_voice_key', key);
            const found = availableVoices.find(v => v.key === key);
            selectedVoice = (found && found.voice) ? found.voice : null;
            if (isAudioPlaying) {{
                window.speechSynthesis.cancel();
                speakCurrentSentence();
            }}
        }}

        function cleanMedicalTextForSpeech(text) {{
            if (!text) return '';
            let s = text.replace(/<[^>]+>/g, ' ');
            s = s.replace(/\|/g, ' ');
            s = s.replace(/\*\*/g, '');
            s = s.replace(/```[\s\S]*?```/g, ' ');
            s = s.replace(/`([^`]+)`/g, '$1');

            const expansions = [
                [/\\bFNAC\\b/g, 'Fine Needle Aspiration Cytology'],
                [/\\bRLN\\b/g, 'Recurrent Laryngeal Nerve'],
                [/\\bEBSLN\\b/g, 'External Branch of Superior Laryngeal Nerve'],
                [/\\bMEN\\b/g, 'Multiple Endocrine Neoplasia'],
                [/\\bMTC\\b/g, 'Medullary Thyroid Carcinoma'],
                [/\\bPTC\\b/g, 'Papillary Thyroid Carcinoma'],
                [/\\bFTC\\b/g, 'Follicular Thyroid Carcinoma'],
                [/\\bCVP\\b/g, 'Central Venous Pressure'],
                [/\\bDVT\\b/g, 'Deep Vein Thrombosis'],
                [/\\bPE\\b/g, 'Pulmonary Embolism'],
                [/\\bIV\\b/g, 'Intravenous'],
                [/\\bIM\\b/g, 'Intramuscular'],
                [/\\bCBC\\b/g, 'Complete Blood Count'],
                [/\\bLFT\\b/g, 'Liver Function Tests'],
                [/\\bRFT\\b/g, 'Renal Function Tests'],
                [/\\bUSG\\b/g, 'Ultrasonography'],
                [/\\bCT\\b/g, 'Computed Tomography'],
                [/\\bMRI\\b/g, 'Magnetic Resonance Imaging'],
                [/\\bRSN\\b/g, 'R S N'],
                [/\\bNSN\\b/g, 'N S N'],
                [/\\bTGN\\b/g, 'T G N'],
                [/\\bCSE\\b/g, 'C S E']
            ];

            expansions.forEach(([rx, replacement]) => {{
                s = s.replace(rx, replacement);
            }});
            return s.trim();
        }}

        function openAudioSectionModal() {{
            if (currentChapterIdx < 0) selectChapter(0);
            const ch = CHAPTERS[currentChapterIdx];
            const titleEl = document.getElementById('audioModalTopicTitle');
            if (titleEl && ch) {{
                titleEl.textContent = `${{currentChapterIdx + 1}}. ${{ch.title}}`;
            }}
            const modal = document.getElementById('audioSectionModal');
            if (modal) {{
                modal.classList.add('open');
                modal.style.display = 'flex';
            }}
        }}

        function closeAudioSectionModal(e) {{
            if (e && e.target && e.target !== e.currentTarget && !e.target.closest('.audio-dock-close')) return;
            const modal = document.getElementById('audioSectionModal');
            if (modal) {{
                modal.classList.remove('open');
                modal.style.display = 'none';
            }}
        }}

        function selectAndPlaySection(sectionType) {{
            activeAudioSectionType = sectionType;
            closeAudioSectionModal();
            playAudioSection(sectionType);
        }}

        function splitIntoSentences(text) {{
            if (!text) return [];
            const raw = text.match(/[^.!?\\n]+[.!?\\n]+(?:\\s+|$)|[^.!?\\n]+$/g) || [text];
            return raw.map(s => s.trim()).filter(s => s.length > 0);
        }}

        function buildSectionText(ch, sectionType) {{
            if (sectionType === 'viva') {{
                const parts = [];
                if (ch.clinical_pearl) {{
                    parts.push(`Clinical Viva Pearl. ${{ch.clinical_pearl}}`);
                }}
                if (Array.isArray(ch.flashcards)) {{
                    ch.flashcards.forEach((fc, idx) => {{
                        parts.push(`Viva Question ${{idx + 1}}. ${{fc.q}}. Answer: ${{fc.a}}`);
                    }});
                }}
                if (parts.length === 0 && Array.isArray(ch.key_points)) {{
                    parts.push(ch.key_points.join('. '));
                }}
                return parts.join(' ');
            }} else {{
                const parts = [`${{ch.title}}. Category: ${{ch.category}}.`];
                if (ch.clinical_pearl) {{
                    parts.push(`Clinical Pearl: ${{ch.clinical_pearl}}`);
                }}
                if (Array.isArray(ch.sections)) {{
                    ch.sections.forEach(sec => {{
                        parts.push(`${{sec.title}}. ${{sec.content}}`);
                    }});
                }}
                return parts.join(' ');
            }}
        }}

        function playAudioSection(sectionType) {{
            if (!('speechSynthesis' in window)) {{
                if (window.CoreEngine && CoreEngine.showToast) {{
                    CoreEngine.showToast('Speech synthesis is not supported in this browser.', 'error');
                }}
                return;
            }}

            if (currentChapterIdx < 0) selectChapter(0);
            const ch = CHAPTERS[currentChapterIdx];
            if (!ch) return;

            activeAudioSectionType = sectionType || activeAudioSectionType || 'master';

            const dock = document.getElementById('masterAudioDock');
            if (dock) dock.classList.remove('hidden');

            const sectionName = activeAudioSectionType === 'viva' ? 'Viva Pearls' : '15-Mark Answer';
            const titleEl = document.getElementById('audioDockTrackTitle');
            const chTitleEl = document.getElementById('audioDockChapterTitle');
            if (titleEl) titleEl.innerText = sectionName;
            if (chTitleEl) chTitleEl.innerText = `${{currentChapterIdx + 1}}. ${{ch.title}}`;

            window.speechSynthesis.cancel();
            clearInterval(speechTickerTimer);

            const rawText = buildSectionText(ch, activeAudioSectionType);
            const cleaned = cleanMedicalTextForSpeech(rawText);
            currentSentences = splitIntoSentences(cleaned);
            currentSentenceIdx = 0;
            audioElapsedSec = 0;

            const totalWords = cleaned.split(/\\s+/).length;
            estTotalDurationSec = Math.max(10, (totalWords / (145 * (audioPlaybackSpeed || 1.0))) * 60);

            const durEl = document.getElementById('audioDuration');
            if (durEl) durEl.innerText = formatTime(estTotalDurationSec);

            isAudioPlaying = true;
            updateAudioUI();
            speakCurrentSentence();

            speechTickerTimer = setInterval(() => {{
                if (isAudioPlaying) {{
                    audioElapsedSec += 0.5;
                    const curTimeEl = document.getElementById('audioCurrentTime');
                    if (curTimeEl) curTimeEl.innerText = formatTime(audioElapsedSec);
                    const scrubber = document.getElementById('audioProgressScrubber');
                    if (scrubber && estTotalDurationSec > 0) {{
                        scrubber.value = Math.min(100, (audioElapsedSec / estTotalDurationSec) * 100);
                    }}
                }}
            }}, 500);
        }}

        function speakCurrentSentence() {{
            if (!isAudioPlaying || currentSentenceIdx >= currentSentences.length) {{
                if (currentSentenceIdx >= currentSentences.length && currentSentences.length > 0) {{
                    isAudioPlaying = false;
                    clearInterval(speechTickerTimer);
                    updateAudioUI();
                    if (window.CoreEngine && CoreEngine.showToast) {{
                        CoreEngine.showToast('Section narration completed.', 'info');
                    }}
                }}
                return;
            }}

            const sentenceText = currentSentences[currentSentenceIdx];
            const utterance = new SpeechSynthesisUtterance(sentenceText);
            utterance.rate = audioPlaybackSpeed || 1.0;
            if (selectedVoice) {{
                utterance.voice = selectedVoice;
            }}

            utterance.onend = () => {{
                if (isAudioPlaying) {{
                    currentSentenceIdx++;
                    speakCurrentSentence();
                }}
            }};

            utterance.onerror = (e) => {{
                console.warn('Speech error on sentence:', e);
                if (isAudioPlaying) {{
                    currentSentenceIdx++;
                    speakCurrentSentence();
                }}
            }};

            window.speechSynthesis.speak(utterance);
        }}

        function togglePlayPauseAudio() {{
            if (!('speechSynthesis' in window)) return;

            if (currentSentences.length === 0) {{
                openAudioSectionModal();
                return;
            }}

            if (isAudioPlaying) {{
                // Instant 0ms pause with cancel()
                isAudioPlaying = false;
                window.speechSynthesis.cancel();
                updateAudioUI();
            }} else {{
                // Instant 0ms resume from currentSentenceIdx
                isAudioPlaying = true;
                updateAudioUI();
                speakCurrentSentence();
            }}
        }}

        function setAudioPlaybackRate(rate) {{
            audioPlaybackSpeed = rate;
            document.querySelectorAll('.speed-pill').forEach(pill => {{
                const pSpeed = parseFloat(pill.getAttribute('data-speed'));
                if (Math.abs(pSpeed - rate) < 0.01) {{
                    pill.classList.add('active');
                }} else {{
                    pill.classList.remove('active');
                }}
            }});
            if (isAudioPlaying) {{
                window.speechSynthesis.cancel();
                speakCurrentSentence();
            }}
        }}

        function onAudioScrub(val) {{
            if (!currentSentences || currentSentences.length === 0) return;
            const pct = parseFloat(val) / 100;
            currentSentenceIdx = Math.min(currentSentences.length - 1, Math.floor(pct * currentSentences.length));
            audioElapsedSec = pct * estTotalDurationSec;
            const curTimeEl = document.getElementById('audioCurrentTime');
            if (curTimeEl) curTimeEl.innerText = formatTime(audioElapsedSec);
            if (isAudioPlaying) {{
                window.speechSynthesis.cancel();
                speakCurrentSentence();
            }}
        }}

        function prevAudioTrack() {{
            if (currentChapterIdx > 0) {{
                currentChapterIdx--;
                selectChapter(currentChapterIdx);
                if (isAudioPlaying) {{
                    playAudioSection(activeAudioSectionType);
                }}
            }}
        }}

        function nextAudioTrack() {{
            if (currentChapterIdx + 1 < CHAPTERS.length) {{
                currentChapterIdx++;
                selectChapter(currentChapterIdx);
                if (isAudioPlaying) {{
                    playAudioSection(activeAudioSectionType);
                }}
            }}
        }}

        function closeAudioDock() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
            }}
            clearInterval(speechTickerTimer);
            isAudioPlaying = false;
            currentSentences = [];
            currentSentenceIdx = 0;
            const dock = document.getElementById('masterAudioDock');
            if (dock) dock.classList.add('hidden');
            updateAudioUI();
        }}

        function updateAudioUI() {{
            const btn = document.getElementById('audioDockPlayPauseBtn');
            const dock = document.getElementById('masterAudioDock');
            if (btn) {{
                btn.innerHTML = isAudioPlaying ? '{ICONS["pause"]}' : '{ICONS["play"]}';
            }}
            if (dock) {{
                if (isAudioPlaying) dock.classList.add('is-playing');
                else dock.classList.remove('is-playing');
            }}
            if (window.CoreEngine && CoreEngine.setAudioPlayingState) {{
                CoreEngine.setAudioPlayingState(isAudioPlaying);
            }}
        }}

        function speakVivaPearl(btn, text) {{
            if (!('speechSynthesis' in window)) return;
            window.speechSynthesis.cancel();
            const cleanText = cleanMedicalTextForSpeech(text);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = audioPlaybackSpeed || 1.0;
            if (selectedVoice) utterance.voice = selectedVoice;

            btn.style.color = 'var(--accent-primary, #14b8a6)';
            utterance.onend = () => {{ btn.style.color = ''; }};
            utterance.onerror = () => {{ btn.style.color = ''; }};
            window.speechSynthesis.speak(utterance);
        }}

        function formatTime(sec) {{
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
        }}

        // --- View & Navigation Logic ---
        function renderSidebar() {{
            const query = (document.getElementById('searchInput').value || '').toLowerCase();
            const listEl = document.getElementById('sidebarTopicList');
            listEl.innerHTML = '';

            const filtered = CHAPTERS.filter(ch => {{
                const matchesCat = (currentCategory === 'All') || ch.category.toLowerCase().includes(currentCategory.toLowerCase());
                const matchesQuery = !query || ch.title.toLowerCase().includes(query) || ch.sections.some(s => s.content.toLowerCase().includes(query));
                return matchesCat && matchesQuery;
            }});

            if (filtered.length === 0) {{
                listEl.innerHTML = '<div style="padding:20px; color:var(--text-muted); text-align:center;">No matching pathological lesions found.</div>';
                return;
            }}

            filtered.forEach((ch, idx) => {{
                const originalIdx = CHAPTERS.findIndex(c => c.id === ch.id);
                const isCompleted = !!completedTopics[ch.id];
                const item = document.createElement('div');
                item.className = 'topic-item' + (originalIdx === currentChapterIdx ? ' active' : '');
                item.onclick = () => selectChapter(originalIdx);
                item.innerHTML = `
                    <div class="topic-check ${{isCompleted ? 'completed' : ''}}" onclick="event.stopPropagation(); toggleTopicComplete('${{ch.id}}')">
                        ${{isCompleted ? '{ICONS["check_circle"]}' : '{ICONS["circle"]}'}}
                    </div>
                    <div class="topic-info">
                        <div class="topic-title">${{originalIdx + 1}}. ${{ch.title}}</div>
                        <div class="topic-meta">${{ch.category}} • ${{ch.reading_time}}</div>
                    </div>
                `;
                listEl.appendChild(item);
            }});
        }}

        function getSlugForChapter(idx) {{
            if (idx < 0 || idx >= CHAPTERS.length) return '';
            const ch = CHAPTERS[idx];
            const cleanTitle = (ch.title || '').replace(/^(chapter\s*\d+[:.]*|\d+[\.:\s]+)/i, '').trim();
            return cleanTitle.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        }}

        function handleHashRoute() {{
            const hash = window.location.hash || '';
            if (!hash || hash === '#' || hash === '#/') {{
                if (currentChapterIdx !== -1) showDashboard(false);
                return;
            }}
            if (hash.startsWith('#/topic/')) {{
                const targetSlug = hash.replace('#/topic/', '').toLowerCase();
                const foundIdx = CHAPTERS.findIndex((ch, i) => {{
                    const s = getSlugForChapter(i);
                    return s === targetSlug || (ch.id && ch.id.toLowerCase() === targetSlug) || ('chap' + (i + 1) === targetSlug) || (String(i + 1) === targetSlug);
                }});
                if (foundIdx !== -1) {{
                    if (currentChapterIdx !== foundIdx) {{
                        selectChapter(foundIdx, false);
                    }}
                }} else {{
                    console.warn('Unknown topic slug:', targetSlug);
                    showDashboard(false);
                }}
            }} else if (hash === '#/simulator') {{
                launchExamSimFromDashboard();
            }} else if (hash === '#/spotters') {{
                openDiagramSpotterFromDashboard();
            }}
        }}

        function selectChapter(idx, updateHash = true) {{
            document.body.classList.remove('is-dashboard');
            currentChapterIdx = idx;
            if (updateHash) {{
                const slug = getSlugForChapter(idx);
                if (slug && window.location.hash !== `#/topic/${{slug}}`) {{
                    history.pushState(null, '', `#/topic/${{slug}}`);
                }}
            }}
            if (window.CoreEngine) {{
                CoreEngine.currentTopicIndex = idx;
                CoreEngine.updateViewHeading(CHAPTERS[idx].title, CHAPTERS[idx].category, idx + 1);
                const activeRow = document.querySelector(`.topic-row[data-topic-id="${{CHAPTERS[idx].id}}"]`);
                if (activeRow) {{
                    document.querySelectorAll('.topic-row').forEach(r => r.classList.remove('active'));
                    activeRow.classList.add('active');
                }}
            }}
            renderChapterView();
            toggleMobileSidebar(false);
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function showDashboard(updateHash = true) {{
            document.body.classList.add('is-dashboard');
            currentChapterIdx = -1;
            if (updateHash && window.location.hash && window.location.hash !== '#/' && window.location.hash !== '#') {{
                history.pushState(null, '', '#/');
            }}
            if (window.CoreEngine) {{
                CoreEngine.currentTopicIndex = -1;
                CoreEngine.updateViewHeading('Dashboard');
                CoreEngine.toggleSidebar(false);
            }}
            renderDashboard();
            toggleMobileSidebar(false);
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function setDashFilter(filter) {{
            currentDashFilter = filter;
            renderDashboard();
        }}

        function renderDashboard() {{
            document.body.classList.add('is-dashboard');
            currentChapterIdx = -1;
            const main = document.getElementById('mainContent');
            const total = CHAPTERS.length;
            const completed = Object.keys(completedTopics).length;
            const remaining = total - completed;
            const pct = Math.round((completed / total) * 100);

            let notesCount = 0;
            CHAPTERS.forEach(ch => {{
                if ((localStorage.getItem('surgery_notes_' + ch.id) || '').trim().length > 0) notesCount++;
            }});

            const dashBtn = document.getElementById('sidebarDashBtn');
            if (dashBtn) dashBtn.classList.add('nav-btn-primary');
            document.querySelectorAll('.topic-item').forEach(el => el.classList.remove('active'));

            let html = `
                <div class="dash-hero-card">
                    <div style="flex: 1;">
                        <span class="dash-hero-badge">BDS 3RD YEAR &amp; MBBS GENERAL SURGERY PORTAL</span>
                        <h1 class="dash-hero-title">General Surgery Master Exam Hub</h1>
                        <p class="dash-hero-sub">15-Mark University Essay Blueprints • Emergency Protocols • Bedside Clinical Pearls</p>
                        <div class="dash-hero-meta">
                            <span class="dash-hero-stat"><strong>${{total}}</strong> University Topics</span>
                            <span class="dash-hero-stat"><strong style="color: #4ade80;">${{completed}}</strong> Completed</span>
                            <span class="dash-hero-stat"><strong style="color: var(--accent-primary);">${{pct}}%</strong> Syllabus Ready</span>
                        </div>
                    </div>
                    <div class="dash-hero-image-box">
                        <svg viewBox="0 0 260 140" width="260" height="140" xmlns="http://www.w3.org/2000/svg">
                            <rect width="260" height="140" fill="#042f2e" rx="8"/>
                            <path d="M30 100 L110 30 L130 50 L50 120 Z" fill="#14b8a6" fill-opacity="0.3" stroke="#5eead4" stroke-width="2"/>
                            <line x1="110" y1="30" x2="220" y2="30" stroke="#14b8a6" stroke-width="2" stroke-dasharray="4 4"/>
                            <circle cx="110" cy="30" r="4" fill="#5eead4"/>
                            <path d="M70 65 L190 65" stroke="#2dd4bf" stroke-width="1.5"/>
                            <circle cx="190" cy="65" r="4" fill="#14b8a6"/>
                            <text x="130" y="125" fill="#5eead4" font-size="10" font-family="'Plus Jakarta Sans',sans-serif" font-weight="700" text-anchor="middle">OPERATIVE SURGERY &amp; ANATOMY</text>
                        </svg>
                    </div>
                </div>

                <div class="dash-cheat-sheet-card">
                    <div style="display: flex; align-items: center; gap: 16px; flex: 1;">
                        <div class="cheat-sheet-badge-icon">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
                            </svg>
                        </div>
                        <div>
                            <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.08em;">Exam Night Rapid Revision</div>
                            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary);">Chapter 24: Rapid Revision Master Cheat Sheet</div>
                            <div style="font-size: 0.84rem; color: var(--text-secondary); margin-top: 2px;">
                                Exhaustive high-yield formulas, keywords, named clinical signs, classifications &amp; shock matrices for rapid pre-exam glance.
                            </div>
                        </div>
                    </div>
                    <button class="nav-btn nav-btn-primary" onclick="selectChapter(23)" style="padding: 10px 20px; font-size: 0.88rem;">
                        Launch Master Cheat Sheet →
                    </button>
                </div>

                <div class="stats-grid-dashboard">
                    <div class="stat-card-box">
                        <div class="stat-card-label">Total University Topics</div>
                        <div class="stat-card-val">${{total}}</div>
                    </div>
                    <div class="stat-card-box">
                        <div class="stat-card-label">Topics Completed</div>
                        <div class="stat-card-val" style="color: #10b981;">${{completed}}</div>
                    </div>
                    <div class="stat-card-box">
                        <div class="stat-card-label">Topics Remaining</div>
                        <div class="stat-card-val" style="color: #f59e0b;">${{remaining}}</div>
                    </div>
                    <div class="stat-card-box">
                        <div class="stat-card-label">Topics with Notes</div>
                        <div class="stat-card-val" style="color: var(--accent-primary);">${{notesCount}}</div>
                    </div>
                </div>

                <div class="progress-banner-dash">
                    <div style="display: flex; justify-content: space-between; align-items: center; font-weight: 700; font-size: 0.92rem;">
                        <span>University Syllabus Completion</span>
                        <span style="color: var(--accent-primary);">${{pct}}%</span>
                    </div>
                    <div class="progress-bar-bg-dash" data-testid="progress">
                        <div class="progress-bar-fill-dash" style="width: ${{pct}}%;"></div>
                    </div>
                </div>

                <div style="margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <h2 style="font-size: 1.1rem; font-weight: 800; color: var(--text-primary);">Study Plan Topics</h2>
                    <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                        <div class="category-scroll">
                            <button class="filter-chip ${{currentDashFilter === 'all' ? 'active' : ''}}" onclick="setDashFilter('all')">All Topics (${{total}})</button>
                            <button class="filter-chip ${{currentDashFilter === 'pending' ? 'active' : ''}}" onclick="setDashFilter('pending')">Pending (${{remaining}})</button>
                            <button class="filter-chip ${{currentDashFilter === 'completed' ? 'active' : ''}}" onclick="setDashFilter('completed')">Completed (${{completed}})</button>
                            <button class="filter-chip ${{currentDashFilter === 'notes' ? 'active' : ''}}" onclick="setDashFilter('notes')">Has Notes (${{notesCount}})</button>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;" data-testid="modules">
                            <button class="filter-chip" data-testid="voice-walk" onclick="togglePlayPauseAudio()" style="cursor: pointer;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;" aria-hidden="true"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>Voice Walk</button>
                            <button class="filter-chip" data-testid="exam-simulator" onclick="launchExamSimFromDashboard()" style="cursor: pointer;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>Exam Simulator</button>
                            <button class="filter-chip" data-testid="spotters" onclick="openDiagramSpotterFromDashboard()" style="cursor: pointer;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/></svg>Spotters</button>
                            <button class="filter-chip" data-testid="flashcards" onclick="openFlashcardsFromDashboard()" style="cursor: pointer;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;" aria-hidden="true"><rect width="18" height="14" x="3" y="5" rx="2"/><line x1="7" y1="15" x2="7.01" y2="15"/></svg>Flashcards</button>
                            <button class="filter-chip" data-testid="schematics" onclick="openDiagramSpotterFromDashboard()" style="cursor: pointer;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Schematics</button>
                            <button class="filter-chip" data-testid="cheat-sheet" onclick="selectChapter(23)" style="cursor: pointer;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>Cheat Sheet</button>
                        </div>
                    </div>
                </div>

                <div class="dashboard-topic-cards-grid">
            `;

            CHAPTERS.forEach((ch, idx) => {{
                const isDone = !!completedTopics[ch.id];
                const hasNote = ((localStorage.getItem('surgery_notes_' + ch.id) || '').trim().length > 0);

                if (currentDashFilter === 'completed' && !isDone) return;
                if (currentDashFilter === 'pending' && isDone) return;
                if (currentDashFilter === 'notes' && !hasNote) return;

                html += `
                    <div class="dash-topic-card ${{isDone ? 'completed' : ''}}">
                        <div>
                            <div class="dash-card-header-row">
                                <span class="dash-card-chapter-tag">Chapter ${{idx + 1}}</span>
                                ${{hasNote ? '<span style="font-size: 0.72rem; background: rgba(192, 86, 211, 0.15); color: #f5d0fe; padding: 2px 7px; border-radius: 4px; font-weight: 600;">Note Saved</span>' : ''}}
                            </div>
                            <div class="dash-card-title-text">${{ch.title}}</div>
                            <div class="dash-card-source-text">${{ch.category}} • ${{ch.reading_time}}</div>
                        </div>
                        <div class="dash-card-footer-row">
                            <button class="toggle-complete-btn ${{isDone ? 'is-completed' : ''}}" onclick="toggleTopicComplete('${{ch.id}}')">
                                ${{isDone ? 'Completed' : 'Mark Done'}}
                            </button>
                            <button class="nav-btn nav-btn-primary" onclick="selectChapter(${{idx}})" style="padding: 6px 14px; font-size: 0.8rem;">
                                Study →
                            </button>
                        </div>
                    </div>
                `;
            }});

            html += `</div>`;
            main.innerHTML = html;
        }}

        function renderChapterView() {{
            if (currentChapterIdx < 0 || currentChapterIdx >= CHAPTERS.length) {{
                renderDashboard();
                return;
            }}
            document.body.classList.remove('is-dashboard');

            const ch = CHAPTERS[currentChapterIdx];
            const main = document.getElementById('mainContent');

            main.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                    <button class="nav-btn" onclick="showDashboard()">
                        ← Back to Dashboard
                    </button>
                    <div style="font-size: 0.82rem; color: var(--text-muted); font-weight: 600;">
                        Chapter ${{currentChapterIdx + 1}} of ${{CHAPTERS.length}}
                    </div>
                </div>

                <div class="chapter-header">
                    <span class="chapter-top-badge">${{ch.category}} • ${{ch.badge}}</span>
                    <h2 class="chapter-title-display">${{ch.title}}</h2>
                </div>

                <div class="tab-bar-container">
                    <div class="tab-bar" role="tablist" aria-label="Curriculum Topic Sections">
                        <button class="tab-btn ${{activeTab === 'master' ? 'active' : ''}}" data-tab="master" role="tab" aria-selected="${{activeTab === 'master' ? 'true' : 'false'}}" tabindex="${{activeTab === 'master' ? '0' : '-1'}}" onclick="switchTab('master')">
                            {ICONS["master_answer"]} 15-Mark Master Answer
                        </button>
                        <button class="tab-btn ${{activeTab === 'layman' ? 'active' : ''}}" data-tab="layman" role="tab" aria-selected="${{activeTab === 'layman' ? 'true' : 'false'}}" tabindex="${{activeTab === 'layman' ? '0' : '-1'}}" onclick="switchTab('layman')">
                            {ICONS["layman"]} Layman's Intuition
                        </button>
                        <button class="tab-btn ${{activeTab === 'types' ? 'active' : ''}}" data-tab="types" role="tab" aria-selected="${{activeTab === 'types' ? 'true' : 'false'}}" tabindex="${{activeTab === 'types' ? '0' : '-1'}}" onclick="switchTab('types')">
                            {ICONS["dashboard"]} Surgical Explorer
                        </button>
                        <button class="tab-btn ${{activeTab === 'diagrams' ? 'active' : ''}}" data-tab="diagrams" role="tab" aria-selected="${{activeTab === 'diagrams' ? 'true' : 'false'}}" tabindex="${{activeTab === 'diagrams' ? '0' : '-1'}}" data-testid="schematics" onclick="switchTab('diagrams')">
                            {ICONS["diagrams"]} Clinical Spotters &amp; Schematics
                        </button>
                        <button class="tab-btn ${{activeTab === 'viva' ? 'active' : ''}}" data-tab="viva" role="tab" aria-selected="${{activeTab === 'viva' ? 'true' : 'false'}}" tabindex="${{activeTab === 'viva' ? '0' : '-1'}}" onclick="switchTab('viva')">
                            {ICONS["viva"]} Examiner Viva Pearls
                        </button>
                        <button class="tab-btn ${{activeTab === 'quiz' ? 'active' : ''}}" data-tab="quiz" role="tab" aria-selected="${{activeTab === 'quiz' ? 'true' : 'false'}}" tabindex="${{activeTab === 'quiz' ? '0' : '-1'}}" data-testid="flashcards" onclick="switchTab('quiz')">
                            {ICONS["quiz"]} Active Recall Flashcards
                        </button>
                        <button class="tab-btn ${{activeTab === 'exam' ? 'active' : ''}}" data-tab="exam" role="tab" aria-selected="${{activeTab === 'exam' ? 'true' : 'false'}}" tabindex="${{activeTab === 'exam' ? '0' : '-1'}}" data-testid="exam-simulator" onclick="switchTab('exam')">
                            {ICONS["cheat_sheet"]} Exam Rubric Simulator
                        </button>
                        <button class="tab-btn ${{activeTab === 'notes' ? 'active' : ''}}" data-tab="notes" role="tab" aria-selected="${{activeTab === 'notes' ? 'true' : 'false'}}" tabindex="${{activeTab === 'notes' ? '0' : '-1'}}" onclick="switchTab('notes')">
                            {ICONS["notes"]} My Surgical Notes
                        </button>
                    </div>
                </div>

                <div id="tabContentContainer">
                    ${{getTabHTML(ch, activeTab)}}
                </div>
            `;
        }}

        function switchTab(tab) {{
            activeTab = tab;
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                const bTab = btn.getAttribute('data-tab');
                const isMatch = bTab === tab;
                btn.classList.toggle('active', isMatch);
                btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
                btn.setAttribute('tabindex', isMatch ? '0' : '-1');
                if (isMatch) {{
                    btn.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
                }}
            }});

            // Sync URL query (?tab=...)
            try {{
                const url = new URL(window.location.href);
                if (url.hash.includes('?')) {{
                    const parts = url.hash.split('?');
                    const params = new URLSearchParams(parts[1]);
                    params.set('tab', tab);
                    url.hash = parts[0] + '?' + params.toString();
                }} else {{
                    url.hash = url.hash + '?tab=' + tab;
                }}
                history.replaceState(null, '', url.toString());
            }} catch(e) {{}}

            const ch = CHAPTERS[currentChapterIdx];
            const container = document.getElementById('tabContentContainer');
            if (container && ch) {{
                container.innerHTML = getTabHTML(ch, tab);
                container.scrollTop = 0;
            }}

            if (tab === 'exam' && ch && window.BdsSimulator) {{
                setTimeout(() => window.BdsSimulator.renderHistoryList('pathology', ch.id), 20);
            }}
        }}

        function getTabHTML(ch, tab) {{
            if (tab === 'master') {{
                return `
                    <div class="master-essay-content">
                        <div class="pearl-card">
                            <strong style="color: var(--accent-primary);">Surgical Clinical Pearl:</strong> ${{ch.clinical_pearl}}
                        </div>
                        ${{ch.sections.map(sec => `
                            <div class="essay-section-card">
                                <div class="essay-section-header">
                                    <h3 class="essay-section-title">${{sec.title}}</h3>
                                </div>
                                <div class="essay-body">${{parseMarkdown(sec.content)}}</div>
                            </div>
                        `).join('')}}
                    </div>
                `;
            }} else if (tab === 'layman') {{
                const layman = ch.analogy || {{ title: 'Pathological Intuition', analogy: ch.clinical_pearl }};
                return `
                    <div class="master-essay-content">
                        <div class="layman-card">
                            <div class="layman-header">
                                <span class="layman-badge">INTUITIVE SURGICAL ANALOGY</span>
                                <h3 class="layman-title">${{layman.title}}</h3>
                            </div>
                            <div class="layman-body">${{layman.analogy}}</div>
                        </div>
                    </div>
                `;
            }} else if (tab === 'types') {{
                const cls = ch.classification;
                return `
                    <div>
                        <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 14px;">${{cls.title}}</h3>
                        <div class="types-grid">
                            ${{cls.types.map((t, tIdx) => `
                                <div class="type-card" id="typeCard_${{tIdx}}">
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                        <span class="type-card-badge">${{t.badge || 'Histopathologic Criteria'}}</span>
                                        ${{t.hemodynamics && t.hemodynamics !== 'Pathognomonic Microscopic Sign' ? `<span class="type-card-stat">${{t.hemodynamics}}</span>` : ''}}
                                    </div>
                                    <div class="type-card-title">${{t.name}}</div>
                                    <div class="type-card-summary" id="typeSummary_${{tIdx}}">${{parseMarkdown(t.summary)}}</div>
                                    <button type="button" class="type-card-expand-btn" onclick="toggleTypeCardExpand(${{tIdx}})" aria-expanded="false" style="margin-top:8px; background:none; border:none; color:var(--accent-primary, #14b8a6); font-size:0.75rem; font-weight:700; cursor:pointer; padding:0; display:inline-flex; align-items:center; gap:4px;">
                                        Read full criteria ▾
                                    </button>
                                </div>
                            `).join('')}}
                        </div>
                    </div>
                `;
            }} else if (tab === 'diagrams') {{
                const diagList = ch.diagrams || [];
                if (diagList.length > 0) {{
                    return `
                        <div>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                                ${{diagList.map((d, dIdx) => {{
                                    const b64 = DIAGRAMS[d.filename] || '';
                                    const safeTitle = (d.title || '').replace(/'/g, "\\'");
                                    return `
                                        <div class="diagram-container" style="margin-bottom: 0;">
                                            <div class="diagram-title">${{d.title}}</div>
                                            <div class="diagram-viewer-box" style="display:flex; justify-content:center; align-items:center; min-height: 240px; background: #0f172a; cursor: pointer;" onclick="openDiagramModal('${{d.filename}}', '${{safeTitle}}')">
                                                ${{b64 ? `<img src="${{b64}}" alt="${{d.title}}" style="max-height: 380px; width: auto; max-width: 100%; border-radius: 8px;">` : `<div style="color:var(--text-muted);">Diagram: ${{d.title}}</div>`}}
                                            </div>
                                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                                                <span>${{d.description || ''}}</span>
                                                <span style="color: var(--accent-primary); font-weight: 600;">Tap to expand ⤢</span>
                                            </div>
                                        </div>
                                    `;
                                }}).join('')}}
                            </div>
                        </div>
                    `;
                }} else {{
                    return `
                        <div>
                            <div class="diagram-container">
                                <div class="diagram-title">${{ch.title}}: Surgical Schematic</div>
                                <div class="diagram-viewer-box" style="display:flex; justify-content:center; align-items:center; min-height: 240px; color: var(--text-muted);">
                                    High-resolution anatomical schematics available in print monograph.
                                </div>
                            </div>
                        </div>
                    `;
                }}
            }} else if (tab === 'viva') {{
                return `
                    <div class="master-essay-content">
                        <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 16px;">Examiner Viva Voce High-Yield Pearls</h3>
                        ${{ch.viva_questions.map((q, idx) => `
                            <div class="viva-item">
                                <div class="viva-q">
                                    <span>Q${{idx + 1}}: ${{q}}</span>
                                    <button class="viva-speaker-btn" onclick="speakVivaPearl(this, '${{q.replace(/'/g, "\\'")}}')">
                                        {ICONS["volume"]}
                                    </button>
                                </div>
                                <button class="viva-reveal-btn" onclick="toggleVivaAnswer(this)">Tap to Reveal Answer</button>
                                <div class="viva-ans">
                                    <strong>Model Answer:</strong> ${{ch.flashcards[idx] ? ch.flashcards[idx].a : ch.clinical_pearl}}
                                </div>
                            </div>
                        `).join('')}}
                    </div>
                `;
            }} else if (tab === 'quiz') {{
                currentFlashcardIdx = 0;
                isFlashcardFlipped = false;
                const card = ch.flashcards[0] || {{ q: 'No flashcard available.', a: '' }};
                return `
                    <div class="flashcard-wrap">
                        <div class="flashcard" id="activeFlashcard" onclick="flipFlashcard()">
                            <span class="flashcard-tag" id="flashcardTag">QUESTION (CARD 1 OF ${{ch.flashcards.length}})</span>
                            <div class="flashcard-text" id="flashcardText">${{card.q}}</div>
                            <span class="flashcard-instruction">Click anywhere to flip</span>
                        </div>
                        <div class="flashcard-controls">
                            <button class="nav-btn" onclick="prevFlashcard()">← Previous</button>
                            <button class="nav-btn nav-btn-primary" onclick="nextFlashcard()">Next Card →</button>
                        </div>
                    </div>
                `;
            }} else if (tab === 'exam') {{
                return `
                    <div class="master-essay-content">
                        <div class="exam-sim-card">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                                <div>
                                    <h3 style="font-size: 1.25rem; font-weight: 700; margin: 0 0 4px 0;">25-Minute Timed University Exam Simulator</h3>
                                    <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0;">Evaluate your structured 15-mark essay against the university examiner 10-point scoring matrix.</p>
                                </div>
                                <div id="simSaveStatus" style="font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; color: var(--text-muted);"></div>
                            </div>
                            <div class="rubric-row">
                                <div class="rubric-info">
                                    <h4>1. Definition, Origin &amp; WHO Classification (2 Marks)</h4>
                                    <p>Exact cell of origin, embryonic tissue remnants, and standard WHO classification table.</p>
                                </div>
                                <div class="rubric-slider"><input type="range" id="rubric_range_1" min="0" max="10" value="8" oninput="updateRubricScore()"></div>
                            </div>
                            <div class="rubric-row">
                                <div class="rubric-info">
                                    <h4>2. Pathogenesis &amp; Molecular Genetics (3 Marks)</h4>
                                    <p>Mutations (BRAF, PTCH1, GNAS, TP53), signaling pathways, and Layman's explanation.</p>
                                </div>
                                <div class="rubric-slider"><input type="range" id="rubric_range_2" min="0" max="10" value="8" oninput="updateRubricScore()"></div>
                            </div>
                            <div class="rubric-row">
                                <div class="rubric-info">
                                    <h4>3. Clinical &amp; Radiographic Hallmarks (3 Marks)</h4>
                                    <p>Age, sex, site predilection, expansion pattern (BL vs AP), and radiographic multilocularity.</p>
                                </div>
                                <div class="rubric-slider"><input type="range" id="rubric_range_3" min="0" max="10" value="8" oninput="updateRubricScore()"></div>
                            </div>
                            <div class="rubric-row">
                                <div class="rubric-info">
                                    <h4>4. Pathognomonic Histopathology (4 Marks)</h4>
                                    <p>Detailed architectural pattern, cell morphology, special stains, and DIF findings.</p>
                                </div>
                                <div class="rubric-slider"><input type="range" id="rubric_range_4" min="0" max="10" value="9" oninput="updateRubricScore()"></div>
                            </div>
                            <div class="rubric-row">
                                <div class="rubric-info">
                                    <h4>5. Management &amp; Recurrence Risk (3 Marks)</h4>
                                    <p>Enucleation vs resection margins, Carnoy's solution, and long-term surveillance protocol.</p>
                                </div>
                                <div class="rubric-slider"><input type="range" id="rubric_range_5" min="0" max="10" value="8" oninput="updateRubricScore()"></div>
                            </div>
                            <div style="margin-top: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; padding-top: 16px; border-top: 1px solid var(--border-color);">
                                <div style="font-size: 1.1rem; font-weight: 700;">Simulated Exam Score: <span id="examScoreTotal" style="color: var(--accent-primary);">12.5 / 15 Marks (Honors)</span></div>
                                <button class="nav-btn nav-btn-primary btn-save-evaluation" id="btnSaveEvaluation" onclick="saveSurgeryEvaluation('${{ch.id}}')" style="min-height: 44px; padding: 0 18px; font-weight: 700;">Save Evaluation</button>
                            </div>
                            <div class="sim-history-pane" style="margin-top: 20px; padding: 14px; background: rgba(0,0,0,0.18); border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
                                <details>
                                    <summary style="font-size: 0.82rem; font-weight: 700; color: var(--text-secondary); cursor: pointer;">
                                        Past Evaluation Attempts &amp; Score Logs
                                    </summary>
                                    <div id="simHistoryList" style="margin-top: 10px;"></div>
                                </details>
                            </div>
                        </div>
                    </div>
                `;
            }} else if (tab === 'notes') {{
                const savedNotes = localStorage.getItem('surgery_notes_' + ch.id) || '';
                return `
                    <div class="master-essay-content">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <h3 style="font-size: 1.2rem; font-weight: 700;">My Surgical Notes</h3>
                            <span id="notesStatus" style="font-size: 0.78rem; color: var(--accent-primary);">Auto-saved locally</span>
                        </div>
                        <textarea class="notes-textarea" id="notesTextarea" placeholder="Type chairside microscopic notes, mnemonics, or revision reminders for this lesion..." oninput="saveTopicNotes('${{ch.id}}', this.value)">${{savedNotes}}</textarea>
                    </div>
                `;
            }}
            return '';
        }}

        function parseMarkdown(md) {{
            if (!md) return '';

            // Clean LaTeX and medical notations
            let text = md
                .replace(/\\\\times(?![a-zA-Z])/g, '×')
                .replace(/\\\\pm(?![a-zA-Z])/g, '±')
                .replace(/\\\\ge(?![a-zA-Z])/g, '≥')
                .replace(/\\\\le(?![a-zA-Z])/g, '≤')
                .replace(/\\\\to(?![a-zA-Z])/g, '→')
                .replace(/\\\\rightarrow(?![a-zA-Z])/g, '→')
                .replace(/\\\\leftarrow(?![a-zA-Z])/g, '←')
                .replace(/\\\\uparrow(?![a-zA-Z])/g, '↑')
                .replace(/\\\\downarrow(?![a-zA-Z])/g, '↓')
                .replace(/\\\\Delta(?![a-zA-Z])/g, 'Δ')
                .replace(/\\\\circ(?![a-zA-Z])/g, '°')
                .replace(/\\\\mu(?![a-zA-Z])/g, 'µ')
                .replace(/\\\\alpha(?![a-zA-Z])/g, 'α')
                .replace(/\\\\beta(?![a-zA-Z])/g, 'β')
                .replace(/\\\\gamma(?![a-zA-Z])/g, 'γ')
                .replace(/\\\\text\\{{([^\\}}]+)\\}}/g, ' $1')
                .replace(/\\bHbA1[cC]\\b/g, 'HbA<sub>1c</sub>')
                .replace(/\\bFiO_?2\\b/g, 'FiO<sub>2</sub>')
                .replace(/\\bPaO_?2\\b/g, 'PaO<sub>2</sub>')
                .replace(/\\bPaCO_?2\\b/g, 'PaCO<sub>2</sub>')
                .replace(/\\bSpO_?2\\b/g, 'SpO<sub>2</sub>')
                .replace(/\\bCO_?2\\b/g, 'CO<sub>2</sub>')
                .replace(/\\bO_?2\\b/g, 'O<sub>2</sub>')
                .replace(/\\bH_?2O\\b/g, 'H<sub>2</sub>O')
                .replace(/\\bNa\\^\\+/g, 'Na⁺')
                .replace(/\\bK\\^\\+/g, 'K⁺')
                .replace(/\\bCa\\^2\\+/g, 'Ca²⁺');

            // Format formula blocks ($$...$$)
            text = text.replace(/\$\$([\s\S]*?)\$\$/g, (m, formula) => {{
                return `<div class="formula-card"><div class="formula-header"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/></svg> CLINICAL FORMULA</div><div class="formula-equation">${{formula.trim()}}</div></div>`;
            }});

            // Preserve code blocks
            const codeBlocks = [];
            text = text.replace(/```([\s\S]*?)```/g, (m, code) => {{
                const id = `__CODE_BLOCK_${{codeBlocks.length}}__`;
                codeBlocks.push(`<pre class="algorithm-block"><code>${{code.trim()}}</code></pre>`);
                return id;
            }});

            const lines = text.split('\\n');
            const result = [];
            let inTable = false;
            let tableLines = [];
            let inUl = false;
            let inOl = false;

            function closeLists() {{
                if (inUl) {{ result.push('</ul>'); inUl = false; }}
                if (inOl) {{ result.push('</ol>'); inOl = false; }}
            }}

            function formatInline(str) {{
                let s = str;
                const count = (s.match(/\*\*/g) || []).length;
                if (count % 2 !== 0) {{
                    const lastIdx = s.lastIndexOf('**');
                    s = s.substring(0, lastIdx) + s.substring(lastIdx + 2);
                }}
                return s
                    .replace(/\*\*(.*?)\*\*/g, '<strong style="color:var(--text-primary); font-weight:700;">$1</strong>')
                    .replace(/(?<!\*)\*([^*]+?)\*(?!\*)/g, '<em>$1</em>')
                    .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
                    .replace(/\$([^$]+)\$/g, '<span class="inline-math">$1</span>');
            }}

            function flushTable() {{
                if (tableLines.length < 2) {{
                    tableLines = [];
                    return;
                }}
                const headers = tableLines[0].split('|').slice(1, -1).map(h => h.trim());
                let startRow = 1;
                if (tableLines.length > 1 && tableLines[1].includes('---')) {{
                    startRow = 2;
                }}

                let html = '<div class="table-responsive"><table class="data-table"><thead><tr>';
                headers.forEach(h => {{
                    html += `<th>${{formatInline(h)}}</th>`;
                }});
                html += '</tr></thead><tbody>';

                for (let i = startRow; i < tableLines.length; i++) {{
                    const line = tableLines[i].trim();
                    if (!line || !line.includes('|')) continue;
                    const cols = line.split('|').slice(1, -1).map(c => c.trim());
                    html += '<tr>';
                    cols.forEach(c => {{
                        html += `<td>${{formatInline(c)}}</td>`;
                    }});
                    html += '</tr>';
                }}
                html += '</tbody></table></div>';
                result.push(html);
                tableLines = [];
            }}

            for (let i = 0; i < lines.length; i++) {{
                const line = lines[i];
                const trimmed = line.trim();

                if (trimmed.startsWith('|') && trimmed.endsWith('|')) {{
                    closeLists();
                    inTable = true;
                    tableLines.push(trimmed);
                    continue;
                }} else if (inTable) {{
                    inTable = false;
                    flushTable();
                }}

                if (!trimmed) {{
                    closeLists();
                    continue;
                }}

                if (trimmed.startsWith('#### ')) {{
                    closeLists();
                    result.push(`<h5 class="essay-subheading" style="font-size:1.02rem; font-weight:700; margin:14px 0 6px 0; color:var(--text-primary);">${{formatInline(trimmed.substring(5))}}</h5>`);
                    continue;
                }}
                if (trimmed.startsWith('### ')) {{
                    closeLists();
                    result.push(`<h4 class="essay-section-title" style="font-size:1.1rem; font-weight:700; margin:18px 0 8px 0; color:var(--accent-primary);">${{formatInline(trimmed.substring(4))}}</h4>`);
                    continue;
                }}
                if (trimmed.startsWith('## ')) {{
                    closeLists();
                    result.push(`<h3 class="essay-major-title" style="font-size:1.22rem; font-weight:800; margin:22px 0 10px 0; color:var(--text-primary);">${{formatInline(trimmed.substring(3))}}</h3>`);
                    continue;
                }}

                if (trimmed.startsWith('> [!TIP]')) {{
                    closeLists();
                    const tipText = formatInline(trimmed.replace('> [!TIP]', '').replace('**Histopathological Pearl:**', '').replace('**Clinical Pearl:**', '').trim());
                    result.push(`<div class="callout-alert alert-tip"><div class="alert-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div><div><strong>Pathology Pearl:</strong> ${{tipText}}</div></div>`);
                    continue;
                }}
                if (trimmed.startsWith('> [!NOTE]')) {{
                    closeLists();
                    const noteText = formatInline(trimmed.replace('> [!NOTE]', '').trim());
                    result.push(`<div class="callout-alert alert-note"><div class="alert-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg></div><div>${{noteText}}</div></div>`);
                    continue;
                }}
                if (trimmed.startsWith('> [!IMPORTANT]')) {{
                    closeLists();
                    const impText = formatInline(trimmed.replace('> [!IMPORTANT]', '').trim());
                    result.push(`<div class="callout-alert alert-important"><div class="alert-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div><div>${{impText}}</div></div>`);
                    continue;
                }}
                if (trimmed.startsWith('> ')) {{
                    closeLists();
                    result.push(`<blockquote class="clinical-quote" style="border-left: 3px solid var(--accent-primary); padding-left: 14px; margin: 12px 0; color: var(--text-secondary); font-style: italic;">${{formatInline(trimmed.substring(2))}}</blockquote>`);
                    continue;
                }}

                const olMatch = trimmed.match(/^(\\d+)\\.\\s+(.*)$/);
                if (olMatch) {{
                    if (inUl) {{ result.push('</ul>'); inUl = false; }}
                    if (!inOl) {{
                        result.push(`<ol class="content-list-ordered" start="${{olMatch[1]}}">`);
                        inOl = true;
                    }}
                    result.push(`<li>${{formatInline(olMatch[2])}}</li>`);
                    continue;
                }}

                if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {{
                    if (inOl) {{ result.push('</ol>'); inOl = false; }}
                    if (!inUl) {{
                        result.push('<ul class="content-list">');
                        inUl = true;
                    }}
                    result.push(`<li>${{formatInline(trimmed.substring(2))}}</li>`);
                    continue;
                }}

                closeLists();
                result.push(`<p class="content-para">${{formatInline(trimmed)}}</p>`);
            }}

            if (inTable) flushTable();
            closeLists();

            let finalHtml = result.join('\\n');
            codeBlocks.forEach((code, idx) => {{
                finalHtml = finalHtml.replace(`__CODE_BLOCK_${{idx}}__`, code);
            }});

            return finalHtml;
        }}

        function toggleTopicComplete(chId, state) {{
            const willBeDone = (state !== undefined) ? !!state : !completedTopics[chId];
            if (willBeDone) completedTopics[chId] = true;
            else delete completedTopics[chId];
            try {{
                localStorage.setItem('bds.surgery.progress', JSON.stringify(completedTopics));
                localStorage.setItem('surgery_completed_topics', JSON.stringify(completedTopics));
            }} catch(e) {{}}
            if (window.CoreEngine && CoreEngine.updateProgressDisplays) {{
                CoreEngine.updateProgressDisplays();
            }}
            if (currentChapterIdx === -1) {{
                renderDashboard();
            }} else {{
                renderChapterView();
            }}
        }}

        function onSearchInput() {{
            renderSidebar();
        }}

        function setCategoryFilter(cat) {{
            currentCategory = cat;
            document.querySelectorAll('#categoryPillBar .filter-chip').forEach(btn => {{
                if (btn.innerText.toLowerCase().includes(cat.toLowerCase()) || (cat === 'All' && btn.innerText.includes('All'))) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            renderSidebar();
        }}

        function toggleSidebar(open) {{
            const sb = document.getElementById('sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (!sb) return;
            const willOpen = (open !== undefined) ? open : !sb.classList.contains('open');
            if (willOpen) {{
                sb.classList.add('open');
                if (backdrop) backdrop.classList.add('active');
            }} else {{
                sb.classList.remove('open');
                if (backdrop) backdrop.classList.remove('active');
            }}
        }}

        function toggleMobileSidebar(open) {{
            toggleSidebar(open);
        }}

        function toggleVivaAnswer(btn) {{
            const ans = btn.nextElementSibling;
            if (ans) {{
                ans.classList.toggle('revealed');
                btn.innerText = ans.classList.contains('revealed') ? 'Hide Answer' : 'Tap to Reveal Answer';
            }}
        }}

        function flipFlashcard() {{
            const ch = CHAPTERS[currentChapterIdx];
            if (!ch || !ch.flashcards || ch.flashcards.length === 0) return;
            const card = ch.flashcards[currentFlashcardIdx];
            isFlashcardFlipped = !isFlashcardFlipped;

            const textEl = document.getElementById('flashcardText');
            const tagEl = document.getElementById('flashcardTag');
            if (isFlashcardFlipped) {{
                textEl.innerText = card.a;
                tagEl.innerText = `ANSWER (CARD ${{currentFlashcardIdx + 1}} OF ${{ch.flashcards.length}})`;
                tagEl.style.color = 'var(--accent-primary, #14b8a6)';
            }} else {{
                textEl.innerText = card.q;
                tagEl.innerText = `QUESTION (CARD ${{currentFlashcardIdx + 1}} OF ${{ch.flashcards.length}})`;
                tagEl.style.color = '';
            }}
        }}

        function prevFlashcard() {{
            const ch = CHAPTERS[currentChapterIdx];
            if (!ch || !ch.flashcards) return;
            if (currentFlashcardIdx > 0) {{
                currentFlashcardIdx--;
                isFlashcardFlipped = false;
                const card = ch.flashcards[currentFlashcardIdx];
                document.getElementById('flashcardText').innerText = card.q;
                document.getElementById('flashcardTag').innerText = `QUESTION (CARD ${{currentFlashcardIdx + 1}} OF ${{ch.flashcards.length}})`;
                document.getElementById('flashcardTag').style.color = '';
            }}
        }}

        function nextFlashcard() {{
            const ch = CHAPTERS[currentChapterIdx];
            if (!ch || !ch.flashcards) return;
            if (currentFlashcardIdx + 1 < ch.flashcards.length) {{
                currentFlashcardIdx++;
                isFlashcardFlipped = false;
                const card = ch.flashcards[currentFlashcardIdx];
                document.getElementById('flashcardText').innerText = card.q;
                document.getElementById('flashcardTag').innerText = `QUESTION (CARD ${{currentFlashcardIdx + 1}} OF ${{ch.flashcards.length}})`;
                document.getElementById('flashcardTag').style.color = '';
            }}
        }}

        function saveTopicNotes(chId, val) {{
            localStorage.setItem('surgery_notes_' + chId, val);
            const status = document.getElementById('notesStatus');
            if (status) status.innerText = 'Saved ' + new Date().toLocaleTimeString();
        }}

        function updateRubricScore() {{
            const sliders = document.querySelectorAll('.rubric-slider input');
            let total = 0;
            sliders.forEach(s => total += parseInt(s.value));
            const scaled = ((total / (sliders.length * 10)) * 15).toFixed(1);
            document.getElementById('examScoreTotal').innerText = `${{scaled}} / 15 Marks (${{scaled >= 11 ? 'Honors' : 'Pass'}})`;
        }}

        function toggleTypeCardExpand(idx) {{
            const sumEl = document.getElementById('typeSummary_' + idx);
            const cardEl = document.getElementById('typeCard_' + idx);
            if (!sumEl || !cardEl) return;
            const btn = cardEl.querySelector('.type-card-expand-btn');
            const isExpanded = sumEl.classList.contains('expanded');
            if (isExpanded) {{
                sumEl.classList.remove('expanded');
                if (btn) btn.innerHTML = 'Read full criteria ▾';
            }} else {{
                sumEl.classList.add('expanded');
                if (btn) btn.innerHTML = 'Collapse criteria ▴';
            }}
        }}

        function saveSurgeryEvaluation(topicId) {{
            const totalEl = document.getElementById('examScoreTotal');
            const totalText = totalEl ? totalEl.textContent : '12.5';
            const match = totalText.match(/([0-9.]+)\s*\/\s*15/);
            const scoreVal = match ? parseFloat(match[1]) : 12.5;

            let gradeLabel = 'Pass';
            if (scoreVal >= 12.0) gradeLabel = 'Honors / Distinction';
            else if (scoreVal >= 10.0) gradeLabel = 'First Class';
            else if (scoreVal < 7.5) gradeLabel = 'Needs Revision';

            const scores = {{}};
            for (let i = 1; i <= 5; i++) {{
                const slider = document.getElementById('rubric_range_' + i);
                if (slider) scores['criteria_' + i] = parseFloat(slider.value) || 0;
            }}

            if (window.BdsSimulator) {{
                window.BdsSimulator.saveEvaluation('surgery', topicId, {{
                    total: scoreVal,
                    outOf: 15,
                    gradeLabel: gradeLabel,
                    scores: scores
                }});
            }}
        }}

        window.applyLoadedEvaluationScores = function(scores) {{
            if (!scores) return;
            for (let i = 1; i <= 5; i++) {{
                const slider = document.getElementById('rubric_range_' + i);
                if (slider && scores['criteria_' + i] !== undefined) {{
                    slider.value = scores['criteria_' + i];
                }}
            }}
            updateRubricScore();
        }};

        function openPdfModal() {{
            document.getElementById('pdfModal').style.display = 'flex';
        }}
        function closePdfModal() {{
            document.getElementById('pdfModal').style.display = 'none';
        }}

        function openDiagramModal(filename, title) {{
            const b64 = DIAGRAMS[filename] || '';
            const modalEl = document.getElementById('modal');
            const titleEl = document.getElementById('modalDiagramTitle');
            const bodyEl = document.getElementById('modalDiagramBody');
            if (titleEl) titleEl.innerText = title || 'Surgical Schematic';
            if (bodyEl) {{
                if (b64) {{
                    bodyEl.innerHTML = `<img src="${{b64}}" alt="${{title || ''}}" style="max-height:80vh; max-width:95vw; object-fit:contain; border-radius:8px;">`;
                }} else {{
                    bodyEl.innerHTML = `<div style="padding:40px; color:var(--text-muted); text-align:center;">Diagram image: ${{filename}}</div>`;
                }}
            }}
            if (modalEl) modalEl.style.display = 'flex';
        }}
        function closeDiagramModal() {{
            document.getElementById('modal').style.display = 'none';
        }}

        function toggleStudyFocusTimer() {{
            if (window.BdsTimer) {{
                window.BdsTimer.toggle();
            }}
        }}

        function launchExamSimFromDashboard() {{
            selectChapter(0);
            setTimeout(() => {{
                switchTab('exam');
            }}, 120);
        }}

        function openDiagramSpotterFromDashboard() {{
            selectChapter(0);
            setTimeout(() => {{
                switchTab('diagrams');
            }}, 120);
        }}

        function openFlashcardsFromDashboard() {{
            selectChapter(0);
            setTimeout(() => {{
                switchTab('quiz');
            }}, 120);
        }}

        function toggleTheme() {{
            if (window.CoreEngine && typeof window.CoreEngine.toggleTheme === 'function') {{
                window.CoreEngine.toggleTheme();
            }} else {{
                const isLight = document.documentElement.getAttribute('data-theme') === 'light' || document.body.classList.contains('light');
                const next = isLight ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', next);
                document.documentElement.classList.remove('dark', 'light');
                document.documentElement.classList.add(next);
                document.documentElement.style.colorScheme = next;
                if (document.body) {{
                    document.body.classList.remove('dark', 'light');
                    document.body.classList.add(next);
                }}
                const metaTheme = document.getElementById('metaThemeColor') || document.querySelector('meta[name="theme-color"]');
                if (metaTheme) metaTheme.setAttribute('content', next === 'light' ? '#f8fafc' : '#090a12');
                try {{
                    localStorage.setItem('surgery_theme', next);
                    localStorage.setItem('bds.surgery.theme', next);
                    localStorage.setItem('bds.theme', next);
                }} catch(e) {{}}
            }}
            const isDark = document.documentElement.getAttribute('data-theme') !== 'light' && !document.body.classList.contains('light');
            const btn = document.getElementById('themeToggleBtn');
            if (btn) btn.innerHTML = isDark ? '{ICONS["sun"]}' : '{ICONS["moon"]}';
        }}

        // Scalpel Logo SVG for Surgery Pro
        const SURGERY_LOGO_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs><linearGradient id="surgBgCard" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0f766e"/><stop offset="100%" stop-color="#042f2e"/></linearGradient></defs><rect width="512" height="512" rx="112" fill="url(#surgBgCard)" stroke="rgba(255,255,255,0.20)" stroke-width="16"/><g fill="none" stroke="#f8fafc" stroke-linecap="round" stroke-linejoin="round"><path d="M128 384 L244 268" stroke-width="28"/><line x1="148" y1="336" x2="164" y2="352" stroke="#5eead4" stroke-width="10"/><line x1="172" y1="312" x2="188" y2="328" stroke="#5eead4" stroke-width="10"/><line x1="196" y1="288" x2="212" y2="304" stroke="#5eead4" stroke-width="10"/><path d="M236 276 L252 260" stroke="#f8fafc" stroke-width="34"/><path d="M244 268 L384 128 C416 148 400 200 364 236 C324 276 276 280 244 268 Z" fill="#5eead4" fill-opacity="0.25" stroke="#ffffff" stroke-width="24"/><line x1="272" y1="240" x2="324" y2="188" stroke="#5eead4" stroke-width="12"/></g></svg>`;

        // Keyboard Shortcuts (Esc to close modals)
        window.addEventListener('keydown', e => {{
            if (e.key === 'Escape') {{
                closePdfModal();
                closeDiagramModal();
                toggleMobileSidebar(false);
            }}
        }});

        // Initialize Shared Core Engine
        if (window.CoreEngine) {{
            CoreEngine.init({{
                portalKey: 'surgery',
                name: 'SURGERY PRO',
                subtitle: 'Paper I · General Surgery',
                logoSvg: SURGERY_LOGO_SVG,
                hubUrl: 'https://krrish41.github.io/bds-vault/#surgery',
                pdfUrl: 'General_Surgery_Master_Notes.pdf',
                searchPlaceholder: 'Search surgical procedures, signs, instruments...',
                topics: CHAPTERS,
                currentTopicIndex: currentChapterIdx,
                onToggleAudioWalk: () => {{
                    togglePlayPauseAudio();
                }},
                onOpenDashboard: () => {{
                    showDashboard(true);
                }},
                onSelectTopic: (idx) => {{
                    selectChapter(idx, true);
                }},
                onOpenSimulator: () => {{
                    selectChapter(currentChapterIdx >= 0 ? currentChapterIdx : 0);
                    setTimeout(() => switchTab('exam'), 120);
                }},
                onOpenSpotters: () => {{
                    selectChapter(currentChapterIdx >= 0 ? currentChapterIdx : 0);
                    setTimeout(() => switchTab('diagrams'), 120);
                }},
                onOpenFlashcards: () => {{
                    selectChapter(currentChapterIdx >= 0 ? currentChapterIdx : 0);
                    setTimeout(() => switchTab('quiz'), 120);
                }},
                onOpenCheatSheet: () => {{
                    selectChapter(23);
                }},
                onToggleComplete: (id, isDone) => {{
                    toggleTopicComplete(id, isDone);
                }},
                onResetStatusFilter: () => {{
                    setCategoryFilter('All');
                }}
            }});
        }}

        initVoiceList();
        window.addEventListener('hashchange', handleHashRoute);
        if (window.location.hash && window.location.hash.startsWith('#/topic/')) {{
            handleHashRoute();
        }} else {{
            renderDashboard();
        }}
    </script>
</body>
</html>
"""
    return html




def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("Loading base64 diagram assets...")
    b64_images = load_diagrams_b64()
    print(f"Loaded {len(b64_images)} diagram images.")

    print("Generating Markdown compendium...")
    md_content = generate_markdown(ALL_CHAPTERS)
    with open(os.path.join(base_dir, "General_Surgery_Master_Notes.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Saved General_Surgery_Master_Notes.md")

    print("Generating Print-Ready HTML with clean LaTeX and table parsing...")
    html_content = generate_html(ALL_CHAPTERS, b64_images)
    with open(os.path.join(base_dir, "General_Surgery_Master_Notes.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Saved General_Surgery_Master_Notes.html")

    print("Generating Interactive Study Dashboard Website...")
    site_content = generate_interactive_dashboard(ALL_CHAPTERS, b64_images)
    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(site_content)
    print("Saved index.html")

    # Emit topics.json registry
    topics_registry = []
    for idx, ch in enumerate(ALL_CHAPTERS):
        title = ch["title"]
        clean_title = re.sub(r'^(Chapter\s*\d+[:.]*|\d+[\.:\s]+)', '', title, flags=re.IGNORECASE).strip()
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_title).strip('-').lower()
        is_cheat_sheet = "cheat sheet" in title.lower() or "rapid revision" in title.lower() or idx >= 23

        if idx < 6:
            category = "General Surgery & Critical Care"
        elif idx < 11:
            category = "Neck & Faciomaxillary Surgery"
        elif idx < 18:
            category = "Specialized Infections, Neuro & Operative"
        elif idx < 23:
            category = "Advanced Technologies & Endocrine"
        else:
            category = "Rapid Revision & Cheat Sheet"

        word_count = sum(len(s_v.split()) for s_v in ch["sections"].values())
        word_count += len(ch.get("essay_prompt", "").split())
        word_count += len(ch.get("layman_explanation", "").split())
        read_minutes = max(5, round(word_count / 180))

        topics_registry.append({
            "id": slug,
            "title": title,
            "category": category,
            "readMinutes": read_minutes,
            "readingTime": f"{read_minutes} min read",
            "portal": "surgery",
            "portalName": "General Surgery Pro",
            "paper": "Paper I · Surgery",
            "chapter": idx + 1,
            "type": "cheat-sheet" if is_cheat_sheet else "essay",
            "url": f"https://krrish41.github.io/general-surgery/#/topic/{slug}",
            "order": idx + 1,
            "tags": [category, "surgery", slug]
        })
    with open(os.path.join(base_dir, "topics.json"), "w", encoding="utf-8") as f:
        json.dump(topics_registry, f, indent=2)
    print(f"Emitted topics.json ({len(topics_registry)} topics).")

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
        html_abs = os.path.join(base_dir, "General_Surgery_Master_Notes.html")
        pdf_abs = os.path.join(base_dir, "General_Surgery_Master_Notes.pdf")
        cmd = [
            browser_bin,
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_abs}",
            f"file:///{html_abs.replace(os.sep, '/')}"
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            if os.path.exists(pdf_abs):
                size_mb = os.path.getsize(pdf_abs) / (1024 * 1024)
                print(f"Successfully compiled PDF: General_Surgery_Master_Notes.pdf ({size_mb:.2f} MB)")
            else:
                print("PDF generation failed:", res.stderr.decode('utf-8', 'ignore'))
        except Exception as e:
            print("PDF generation failed with exception:", e)
    else:
        print("No headless browser found to compile PDF.")

if __name__ == "__main__":
    main()
