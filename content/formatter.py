# -*- coding: utf-8 -*-
"""
Formatting and parsing utilities for General Surgery Study Suite.
Converts markdown, tables, and LaTeX math into semantic, responsive HTML.
Provides SVG icons to completely eliminate emojis.
"""

import re

# Clean inline SVG Icons
ICONS = {
    "dashboard": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
    "master_answer": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
    "layman": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "diagrams": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
    "viva": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "quiz": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/></svg>',
    "check_circle": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "circle": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>',
    "notes": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    "search": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "pdf": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><path d="M10 13v-2a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1z"/><path d="M10 18h4"/></svg>',
    "moon": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
    "sun": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>',
    "medical_cross": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M2 12h20"/></svg>',
    "modern_logo": '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 36 36"><defs><linearGradient id="logoG" x1="0" y1="0" x2="36" y2="36"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/></linearGradient></defs><rect width="36" height="36" rx="9" fill="url(#logoG)"/><path d="M18 8v20M8 18h20" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/><circle cx="18" cy="18" r="3.5" fill="#bae6fd"/></svg>',
    "cheat_sheet": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    "chevron_down": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
    "chevron_right": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "play": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 4 20 12 6 20 6 4"/></svg>',
    "pause": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16" rx="1.5"/><rect x="14" y="4" width="4" height="16" rx="1.5"/></svg>',
    "prev_track": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polygon points="19 20 9 12 19 4 19 20" fill="currentColor"/><line x1="5" y1="19" x2="5" y2="5"/></svg>',
    "next_track": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 4 15 12 5 20 5 4" fill="currentColor"/><line x1="19" y1="5" x2="19" y2="19"/></svg>',
    "headphones": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>',
    "volume": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>',
    "sync": '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>',
    "close_sm": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "play_sm": '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 4 20 12 6 20 6 4"/></svg>',
    "pause_sm": '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>',
    "stop_sm": '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><rect x="5" y="5" width="14" height="14" rx="2"/></svg>',
    "lock_sm": '<svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 3px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
}

# Modern Surgical Purple SVG Favicon Data URL (Caduceus cross in royal violet gradient shield)
FAVICON_SVG = """data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='32' y2='32'%3E%3Cstop offset='0%25' stop-color='%238b5cf6'/%3E%3Cstop offset='100%25' stop-color='%236d28d9'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='url(%23g)'/%3E%3Cpath d='M16 6v20M6 16h20' stroke='%23ffffff' stroke-width='3.5' stroke-linecap='round'/%3E%3Ccircle cx='16' cy='16' r='3.5' fill='%23e9d5ff'/%3E%3C/svg%3E"""

def clean_latex(text: str) -> str:
    """Converts raw LaTeX math expressions and backslashes into clean readable Unicode."""
    if not text:
        return ""
    
    # Temperatures and degrees
    text = re.sub(r'([0-9\.\-\–]+)\^\\circ\\text\{C\}', r'\1°C', text)
    text = re.sub(r'([0-9\.\-\–]+)\^\\circ\s*C', r'\1°C', text)
    text = re.sub(r'([0-9\.\-\–]+)\^\\circ', r'\1°', text)
    text = text.replace(r'^\circ', '°')
    text = text.replace(r'\circ', '°')

    # Greek letters and math operators
    text = text.replace(r'\to', '→')
    text = text.replace(r'\rightarrow', '→')
    text = text.replace(r'\leftarrow', '←')
    text = text.replace(r'\uparrow', '↑')
    text = text.replace(r'\downarrow', '↓')
    text = text.replace(r'\Delta', 'Δ')
    text = text.replace(r'\delta', 'δ')
    text = text.replace(r'\ge', '≥')
    text = text.replace(r'\le', '≤')
    text = text.replace(r'\pm', '±')
    text = text.replace(r'\mu', 'µ')
    text = text.replace(r'\%', '%')
    text = text.replace(r'\_', '_')
    text = text.replace(r'\times', '×')
    text = text.replace(r'\alpha', 'α')
    text = text.replace(r'\beta', 'β')
    text = text.replace(r'\gamma', 'γ')

    # Formulas and subscripts
    text = text.replace(r'$$BP = CO \times PR$$', 'BP = CO × PR')
    text = text.replace(r'$$CO = SV \times HR$$', 'CO = SV × HR')
    text = text.replace(r'Na^+', 'Na⁺')
    text = text.replace(r'K^+', 'K⁺')
    text = text.replace(r'T_3', 'T₃')
    text = text.replace(r'T_4', 'T₄')
    text = text.replace(r'CO_2', 'CO₂')
    text = text.replace(r'H_2', 'H₂')
    text = text.replace(r'N_2O', 'N₂O')
    text = text.replace(r'FiO_2', 'FiO₂')
    text = text.replace(r'O_2', 'O₂')
    text = text.replace(r'A\beta', 'Aβ')
    text = text.replace(r'A\delta/C', 'Aδ/C')
    text = text.replace(r'TGF-\beta', 'TGF-β')
    text = text.replace(r'PAX8-PPAR\gamma', 'PAX8-PPARγ')
    text = text.replace(r'^{131}\text{I}', '¹³¹I')
    text = text.replace(r'^{131}I', '¹³¹I')

    # Arrows in LaTeX or prose
    text = re.sub(r'\\?uparrow', '↑', text)
    text = re.sub(r'\\?downarrow', '↓', text)
    text = re.sub(r'\\?rightarrow', '→', text)
    text = re.sub(r'\\?leftarrow', '←', text)
    text = text.replace('\\→', '→')
    text = text.replace('\\←', '←')
    text = text.replace('\\↑', '↑')
    text = text.replace('\\↓', '↓')

    # Clean any accidental SV...SV leaks (where dollar signs were replaced by SV)
    text = text.replace('SVSV', '')
    text = text.replace(r'SV\toSV', '→')
    text = text.replace(r'SV\to', '→')
    text = text.replace(r'\toSV', '→')
    text = text.replace('SV→SV', '→')
    text = text.replace('SV→', '→')
    text = text.replace('→SV', '→')
    text = re.sub(r'SV([^SV\n\r]+?)SV', r'\1', text)
    text = text.replace('SVSV', '')

    # Clean any \text{...} while preserving proper spacing before units
    text = re.sub(r'\\text\{\s*([^\}]+)\s*\}', r' \1', text)

    # Strip math dollar signs
    text = text.replace('$$', '')
    text = text.replace('$', '')

    # Spacing around inequality operators: < 180, > 36, ≥ 4, ≤ 5
    text = re.sub(r'(?<![a-zA-Z0-9_\<\>])([<>=≤≥])(\d)', r'\1 \2', text)

    # Spacing between numbers and clinical units: 4 weeks, 180 mg, 60 mins, 4 hours
    text = re.sub(r'(\d+)(weeks|week|days|day|hours|hour|mins|min|months|month|years|year|mg|mL|mmol|mEq|mmHg|cm|mm|kg|gm)\b', r'\1 \2', text)

    # Collapse multiple spaces (except newlines)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    return text.strip()

def format_inline_markdown(text: str) -> str:
    """Parses inline markdown (**bold**, *italics*, medical subscripts, unit spacing) into clean semantic HTML."""
    if not text:
        return ""
    text = clean_latex(text)
    # Parse bold: **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Parse italics: *text* (excluding newlines and empty)
    text = re.sub(r'(?<!\*)\*([^\*\n\r]+?)\*(?!\*)', r'<em>\1</em>', text)
    # Medical terms and subscripts
    text = re.sub(r'\bHbA1[cC]\b', 'HbA<sub>1c</sub>', text)
    text = re.sub(r'HbA_\{1[cC]\}', 'HbA<sub>1c</sub>', text)
    text = re.sub(r'HbA₁[cC]', 'HbA<sub>1c</sub>', text)
    text = re.sub(r'\bFiO_?2\b', 'FiO<sub>2</sub>', text)
    text = re.sub(r'\bPaO_?2\b', 'PaO<sub>2</sub>', text)
    text = re.sub(r'\bPaCO_?2\b', 'PaCO<sub>2</sub>', text)
    text = re.sub(r'\bSpO_?2\b', 'SpO<sub>2</sub>', text)
    text = re.sub(r'\bEtCO_?2\b', 'EtCO<sub>2</sub>', text)
    text = re.sub(r'\bCO_?2\b', 'CO<sub>2</sub>', text)
    text = re.sub(r'\bO_?2\b', 'O<sub>2</sub>', text)
    text = re.sub(r'\bN_?2O\b', 'N<sub>2</sub>O', text)
    text = re.sub(r'\bH_?2O\b', 'H<sub>2</sub>O', text)
    text = re.sub(r'\bH_?2\b', 'H<sub>2</sub>', text)
    text = re.sub(r'\bHCO_?3\^?-?\b', 'HCO<sub>3</sub><sup>⁻</sup>', text)
    return text

def parse_markdown_to_html(md_text: str) -> str:
    """Parses markdown text into clean semantic HTML with responsive tables, preserved numbering, and nested lists."""
    if not md_text:
        return ""
    
    text = clean_latex(md_text.strip())

    # Pre-process and protect code blocks (``` ... ```)
    code_blocks = {}
    def save_code_block(match):
        raw_code = match.group(1).strip()
        esc = raw_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        key = f"__CODE_BLOCK_{len(code_blocks)}__"
        card = (
            '<div class="clinical-flowchart-card" style="margin: 16px 0; border: 1.5px solid #c4b5fd; '
            'border-left: 5px solid #7c3aed; border-radius: 10px; background: #fdf4ff; '
            'padding: 14px 18px; break-inside: avoid; page-break-inside: avoid;">'
            '<div class="flowchart-header" style="font-size: 8pt; font-weight: 700; text-transform: uppercase; '
            'letter-spacing: 1.2px; color: #6d28d9; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">'
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2v20M2 12h20"/></svg>'
            'CLINICAL ALGORITHM / SCHEMATIC FLOWCHART</div>'
            f'<pre class="flowchart-pre" style="margin: 0; font-family: \'JetBrains Mono\', monospace; font-size: 8pt; '
            f'line-height: 1.45; overflow-x: auto; color: #1e1b4b; white-space: pre; background: transparent; border: none; padding: 0;"><code>{esc}</code></pre>'
            '</div>'
        )
        code_blocks[key] = card
        return f"\n\n{key}\n\n"

    text = re.sub(r'```(?:[a-zA-Z0-9_\-]+)?\n?([\s\S]*?)```', save_code_block, text)

    # Pre-process formulas ($$...$$)
    formula_blocks = {}
    def save_formula(match):
        f_raw = match.group(1).strip()
        key = f"__FORMULA_BLOCK_{len(formula_blocks)}__"
        card = (
            '<div class="formula-card" style="margin: 14px 0; border: 1.5px solid #e9d5ff; '
            'border-left: 4px solid #d97706; border-radius: 8px; background: #fdf4ff; '
            'padding: 12px 16px; break-inside: avoid; page-break-inside: avoid;">'
            '<div style="font-size: 8pt; font-weight: 700; color: #d97706; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">'
            'CLINICAL FORMULA / EQUATION</div>'
            f'<div style="font-family: \'JetBrains Mono\', monospace; font-size: 10pt; font-weight: 600; color: #1e1b4b;">{clean_latex(f_raw)}</div>'
            '</div>'
        )
        formula_blocks[key] = card
        return f"\n\n{key}\n\n"

    text = re.sub(r'\$\$([\s\S]*?)\$\$', save_formula, text)

    lines = text.split("\n")
    output = []
    
    in_table = False
    table_lines = []
    in_ul = False
    in_ol = False
    in_nested_ul = False

    def close_lists():
        nonlocal in_ul, in_ol, in_nested_ul
        res = []
        if in_nested_ul:
            res.append("</ul></li>")
            in_nested_ul = False
        if in_ul:
            res.append("</ul>")
            in_ul = False
        if in_ol:
            res.append("</ol>")
            in_ol = False
        return res

    def flush_table():
        nonlocal table_lines
        if len(table_lines) < 2:
            table_lines = []
            return ""
        
        headers = [c.strip() for c in table_lines[0].split("|")[1:-1]]
        # find separator index
        start_row = 1
        if len(table_lines) > 1 and "---" in table_lines[1]:
            start_row = 2
        
        t_html = ['<div class="table-responsive"><table class="data-table"><thead><tr>']
        for h in headers:
            h_clean = format_inline_markdown(h)
            t_html.append(f'<th>{h_clean}</th>')
        t_html.append('</tr></thead><tbody>')

        for r_line in table_lines[start_row:]:
            if not r_line.strip() or "|" not in r_line:
                continue
            cols = [c.strip() for c in r_line.split("|")[1:-1]]
            t_html.append('<tr>')
            for c in cols:
                c_clean = format_inline_markdown(c)
                t_html.append(f'<td>{c_clean}</td>')
            t_html.append('</tr>')

        t_html.append('</tbody></table></div>')
        table_lines = []
        return "".join(t_html)

    for line in lines:
        s_line = line.strip()

        # Check for placeholder blocks
        if s_line.startswith("__CODE_BLOCK_") and s_line.endswith("__"):
            if in_table:
                in_table = False
                output.append(flush_table())
            output.extend(close_lists())
            output.append(code_blocks.get(s_line, ""))
            continue

        if s_line.startswith("__FORMULA_BLOCK_") and s_line.endswith("__"):
            if in_table:
                in_table = False
                output.append(flush_table())
            output.extend(close_lists())
            output.append(formula_blocks.get(s_line, ""))
            continue

        # Check for table line
        if s_line.startswith("|") and s_line.endswith("|"):
            output.extend(close_lists())
            in_table = True
            table_lines.append(s_line)
            continue
        elif in_table:
            in_table = False
            output.append(flush_table())

        if not s_line:
            # Do not close lists prematurely on empty blank lines between items
            continue

        # Check for ordered list: "1. ", "2. ", etc.
        ol_match = re.match(r'^(\d+)\.\s+(.*)$', s_line)
        if ol_match:
            num = ol_match.group(1)
            if in_nested_ul:
                output.append("</ul></li>")
                in_nested_ul = False
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if not in_ol:
                output.append(f'<ol class="content-list-ordered" start="{num}">')
                in_ol = True
            content = format_inline_markdown(ol_match.group(2).strip())
            output.append(f'<li value="{num}">{content}</li>')
            continue

        # Check for unordered list: "- ", "* "
        if s_line.startswith("- ") or s_line.startswith("* "):
            content = format_inline_markdown(s_line[2:].strip())
            if in_ol:
                if not in_nested_ul:
                    output.append('<li class="nested-list-container" style="list-style-type: none;"><ul class="content-list nested-list" style="margin-top: 4px; margin-bottom: 8px; padding-left: 20px;">')
                    in_nested_ul = True
                output.append(f'<li>{content}</li>')
                continue
            else:
                if not in_ul:
                    output.append('<ul class="content-list">')
                    in_ul = True
                output.append(f'<li>{content}</li>')
                continue

        # Check for headings or other elements
        output.extend(close_lists())

        if s_line.startswith("### "):
            h_text = format_inline_markdown(s_line[4:].strip())
            output.append(f'<h4 class="sub-heading">{h_text}</h4>')
            continue
        elif s_line.startswith("## "):
            h_text = format_inline_markdown(s_line[3:].strip())
            output.append(f'<h3 class="section-title">{h_text}</h3>')
            continue

        # Normal paragraph
        p_text = format_inline_markdown(s_line)
        output.append(f'<p class="content-para">{p_text}</p>')

    if in_table:
        output.append(flush_table())
    output.extend(close_lists())
    output.extend(close_lists())

    return "\n".join(output)
