#!/usr/bin/env python3
"""Generate stakeholder charts from customer index.md files.

Improved version: case-insensitive influence/relationship matching,
responsive CSS grid, tooltips, relationship badges, client-side search.
"""

import yaml
import re
import sys
from pathlib import Path

# Import HTML template
sys.path.insert(0, str(Path(__file__).resolve().parent))
from template import HTML_TEMPLATE

# Use repo-relative paths
REPO_ROOT = Path(__file__).resolve().parent.parent
CUSTOMERS_DIR = REPO_ROOT / "customers"
OUTPUT_DIR = REPO_ROOT / "stakeholder_maps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SLUG_MAP = {
    "motorola": "Motorola Solutions",
    "polar": "Polar Electro",
    "csem": "CSEM",
    "halma": "Halma",
    "university-of-jyvaskyla": "University of Jyväskylä",
    "tridonic": "Tridonic",
    "zwift": "Zwift",
    "poly": "Poly / HP",
    "sofar": "Sofar Ocean",
    "jumo": "JUMO",
    "kuster": "Küster Automotive",
    "getac": "Getac",
    "globalsense": "Globalsense",
    "halo": "Halo Collar",
    "halo-collar": "Halo Collar",
    "daikin": "Daikin",
    "masco": "Masco",
    "replior": "Replior",
    "nestle-purina": "Nestlé Purina",
}

ACCOUNT_DISPLAY = {
    "Motorola Solutions": "Motorola Solutions",
    "Polar Electro": "Polar Electro",
    "CSEM": "CSEM",
    "Halma": "Halma",
    "University of Jyväskylä": "University of Jyväskylä",
    "Tridonic": "Tridonic",
    "Zwift": "Zwift",
    "Poly / HP": "Poly (fka Plantronics, acquired by HP)",
    "Sofar Ocean": "Sofar Ocean",
    "JUMO": "JUMO",
    "Küster Automotive": "Küster Automotive",
    "Getac": "Getac",
    "Globalsense": "Globalsense",
    "Halo Collar": "Halo Collar",
    "Daikin": "Daikin",
    "Masco": "Masco",
    "Replior": "Replior",
    "Nestlé Purina": "Nestlé Purina Petcare Global Resources Inc",
}

# Relationship -> CSS class for color coding
RELATIONSHIP_CLASS = {
    "Ally": "rel-ally",
    "Neutral": "rel-neutral",
    "Warm": "rel-warm",
    "Blocker": "rel-blocker",
    "Marketing": "rel-marketing",
}

# Influence -> CSS color var name
INFLUENCE_COLOR = {"High": "var(--high)", "Medium": "var(--medium)", "Low": "var(--low)"}

ACTIVITY_RE = re.compile(r"Sales activities:\s*(\d+)")


def infer_team(role):
    """Auto-derive a team label from the role string."""
    r = (role or "").lower()
    if not r:
        return "General"
    # Priority-ordered keyword matching so longer phrases win first
    patterns = [
        ("Product Management", ["product manager", "product management", "product lead", "head of product"]),
        ("Software Engineering", ["software engineer", "full stack", "backend", "frontend", "sde", "swe", "embedded engineer", "embedded software", "firmware", "site reliability", "devops", "developer"]),
        ("Hardware Engineering", ["hardware", "electrical", "firmware engineer", "asic", "rf", "sensor"]),
        ("Edge AI / Research", ["machine learning", "ml ", "deep learning", "research scientist", "research engineer", "ai architect", "ai strategist", "computer vision", "audio engineer", "data scientist", "data engineer", "cti", "cto office"]),
        ("Sales & BizDev", ["sales", "business development", "account", "bizdev", "category manager"]),
        ("Operations", ["program manager", "project manager", "operations", "logistics", "procurement", "supply chain"]),
        ("Leadership", ["director", "vp", "vice president", "cvp", "senior director", "executive", "cto", "cio", "ceo"]),
    ]
    for label, keys in patterns:
        if any(k in r for k in keys):
            return label
    return "General"


def infer_reports_to(contacts, contact_name):
    """Try to find who a contact reports to based on role hierarchy.
    
    Returns the name of the person this contact reports to, or None.
    Uses title-based heuristics: engineers report to managers, managers
    report to directors, directors report to VPs, etc.
    """
    # Find the contact
    contact = next((c for c in contacts if c.get("name") == contact_name), None)
    if not contact:
        return None
    
    role = (contact.get("role") or "").lower()
    
    role = (contact.get("role") or "").lower()
    
    # Determine this person's level using word-boundary regex
    def level(r):
        r = r.lower() if r else ""
        if any(re.search(p, r) for p in [r'\bcto\b', r'\bcvo\b', r'\bceo\b', r'\bcoo\b', r'\bcfo\b',
                                          r'\bcvp\b', r'\bcro\b', r'chief officer', r'chief technology',
                                          r'chief product', r'chief marketing', r'executive vp',
                                          r'executive vice president']):
            return 6
        if any(re.search(p, r) for p in [r'\bsvp\b', r'\bsr vp\b', r'senior vp', r'senior director']):
            return 5
        if any(re.search(p, r) for p in [r'\bvp\b', r'veice president']):
            return 4
        if "director" in r:
            return 3
        if any(t in r for t in ["manager", "lead", "head of", "team lead", "principal"]):
            return 2
        return 1  # individual contributor
    
    my_level = level(contact.get("role", ""))
    
    # Find the closest manager above — match team + one level higher
    candidates = []
    my_team = infer_team(contact.get("role", ""))
    
    for c in contacts:
        if c.get("name") == contact_name:
            continue
        c_role = c.get("role") or ""
        c_level = level(c_role)
        if c_level > my_level:
            # Prefer same team, then closest level
            c_team = infer_team(c_role)
            team_match = 1 if c_team == my_team else 0
            candidates.append((c_level, -team_match, c))
    
    if not candidates:
        return None
    
    # Pick the closest level above, preferring team match
    candidates.sort(key=lambda x: (x[0], x[1]))
    return candidates[0][2].get("name")


def build_reporting_tree(contacts):
    """Build a tree of contacts based on reports_to fields or inference.
    
    Returns a list of top-level managers, each with .reports as children.
    """
    # First, use explicit reports_to if present, else infer
    contact_map = {c.get("name"): c for c in contacts if c.get("name")}
    
    for c in contacts:
        name = c.get("name", "")
        if not name:
            continue
        if "reports_to" in c and c["reports_to"]:
            c["_reports_to"] = c["reports_to"]
        else:
            c["_reports_to"] = infer_reports_to(contacts, name)
    
    # Build child lists
    for c in contacts:
        name = c.get("name", "")
        if not name:
            continue
        c["_reports"] = []
    
    for c in contacts:
        reporter = c.get("_reports_to")
        if reporter and reporter in contact_map:
            contact_map[reporter]["_reports"].append(c)
    
    # Top-level = those who have no reports_to (or report to unknown)
    top_level = [c for c in contacts 
                 if c.get("name") and 
                 (not c.get("_reports_to") or c["_reports_to"] not in contact_map)]
    
    # Sort top-level by influence (high first)
    inf_order = {"High": 0, "Medium": 1, "Low": 2}
    top_level.sort(key=lambda c: inf_order.get(c.get("influence", "Low"), 3))
    
    return top_level


def html_format(template, **kwargs):
    """Safe format: replaces only our placeholders, leaves JS braces intact."""
    result = template
    for key, val in kwargs.items():
        result = result.replace("{" + key + "}", str(val))
    return result


def normalize_influence(val):
    if not val:
        return "Low"
    return val.strip().title()


def normalize_relationship(val):
    """Accept 'ally', 'Ally', 'ALLY', etc."""
    if not val:
        return "Neutral"
    return val.strip().title()


def extract_activities(notes):
    """Extract sales activity count from notes string."""
    if not notes:
        return "0"
    m = ACTIVITY_RE.search(notes)
    return m.group(1) if m else "0"


def parse_index_md(path):
    """Parse an index.md file, handling both clean and jumbled formats."""
    text = path.read_text(encoding="utf-8")
    # Clean frontmatter: starts with --- and ends with ---
    # Also handle jumbled single-delim format (---contacts: on line 1)
    if text.startswith("---contacts:") or text.startswith("---\ncontacts:"):
        # Jumbled format — no closing frontmatter delimiter
        # Extract just the contacts list portion
        # Try to parse what we can
        try:
            data = yaml.safe_load(text[2:])  # skip leading ---
            return data or {}
        except Exception:
            pass
    # Standard format
    if "---" not in text:
        return {}
    parts = text.split("---")
    if len(parts) >= 3:
        front = parts[1]
    else:
        return {}
    try:
        return yaml.safe_load(front) or {}
    except Exception:
        return {}


def build_node(contact):
    """Build a single contact node HTML."""
    infl = normalize_influence(contact.get("influence", "Low"))
    rel = normalize_relationship(contact.get("relationship_to_us", "Neutral"))
    name = contact.get("name", "Unknown")
    role = contact.get("role", "")
    notes = contact.get("notes", "")
    activities = extract_activities(notes)
    rel_class = RELATIONSHIP_CLASS.get(rel, "rel-neutral")
    team = infer_team(role)
    
    # Truncate long notes for tooltip, show full in title
    note_preview = notes[:120] + "..." if len(notes) > 120 else notes
    safe_notes = (notes or "").replace('"', "&quot;")
    
    html = (
        '<div class="node" data-name="{name}" data-role="{role}" '
        'data-rel="{rel}" data-activities="{activities}" data-team="{team}">'
        '<div class="node-inner" style="border-left:3px solid {infl_color};">'
        '<div class="name" title="{safe_notes}">{name}</div>'
        '<div class="role">{role}</div>'
        '<div class="meta">'
        '<span class="badge {rel_class}">{rel}</span>'
        '<span class="badge badge-outline">{activities} activities</span>'
        '<span class="badge badge-outline" style="font-size:9px;">{team}</span>'
        '</div>'
        '</div>'
        '</div>'
    ).format(
        name=name, role=role, rel=rel, activities=activities,
        infl_color=INFLUENCE_COLOR.get(infl, "var(--low)"),
        rel_class=rel_class, safe_notes=safe_notes,
        team=team,
    )
    return html


def build_group(contacts, group_name):
    """Build a grouped section for low-influence contacts."""
    nodes = "\n".join(build_node(c) for c in contacts)
    return (
        '<div class="group">'
        '<h4>{group_name}</h4>'
        '<div class="node-grid">'
        '{nodes}'
        '</div>'
        '</div>'
    ).format(group_name=group_name, nodes=nodes)


def build_tree_section(mgr, level=0, is_last=True, prefix="", show_children=True):
    """Render a manager node and their subtree with org-chart connector lines.
    
    Uses ASCII-tree style connectors that become visual lines in the browser.
    """
    infl = normalize_influence(mgr.get("influence", "Low"))
    rel = normalize_relationship(mgr.get("relationship_to_us", "Neutral"))
    name = mgr.get("name", "Unknown")
    role = mgr.get("role", "")
    notes = mgr.get("notes", "")
    activities = extract_activities(notes)
    rel_class = RELATIONSHIP_CLASS.get(rel, "rel-neutral")
    safe_notes = (notes or "").replace('"', "&quot;")
    
    # Build connector line for report hierarchy
    connector = ""
    if level > 0:
        if is_last:
            connector = '<span class="tree-connector" style="display:inline-block;width:20px;border-left:2px dashed #334155;"></span>'
        else:
            connector = '<span class="tree-connector" style="display:inline-block;width:20px;border-left:2px dashed #334155;border-right:2px dashed #334155;"></span>'
    
    indent = level * 24
    
    html = (
        '<div class="tree-node" style="margin-left:{indent}px;">'
        '{connector}'
        '<div class="node" data-name="{name}" data-role="{role}" '
        'data-rel="{rel}" data-activities="{activities}" style="display:inline-block;margin:6px 0;">'
        '<div class="node-inner" style="border-left:3px solid {infl_color};">'
        '<div class="name" title="{safe_notes}">{name}</div>'
        '<div class="role">{role}</div>'
        '<div class="meta">'
        '<span class="badge {rel_class}">{rel}</span>'
        '<span class="badge badge-outline">{activities} activities</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    ).format(
        name=name, role=role, rel=rel, activities=activities,
        infl_color=INFLUENCE_COLOR.get(infl, "var(--low)"),
        rel_class=rel_class, safe_notes=safe_notes,
        indent=indent, connector=connector,
    )
    
    # Render children (reports)
    child_team = infer_team(role)
    reports = mgr.get("_reports", [])
    
    if reports:
        # Split reports into managers and ICs
        mgr_reports = [r for r in reports if any(t in (r.get("role") or "").lower() for t in ["manager", "lead", "director", "vp", "head of", "sr.", "senior"])]
        ic_reports = [r for r in reports if r not in mgr_reports]
        
        if mgr_reports:
            html += '<div class="tree-children" style="margin-left:24px;border-left:1px solid #334155;padding-left:12px;">'
            for i, child in enumerate(sorted(mgr_reports, key=lambda c: c.get("name", ""))):
                is_last_child = (i == len(mgr_reports) - 1) and not ic_reports
                html += build_tree_section(child, level + 1, is_last_child, prefix + ("    " if is_last else "│   "))
            html += '</div>'
        
        if ic_reports:
            # ICs render as a grid under the manager
            ic_html = "\n".join(build_node(c) for c in sorted(ic_reports, key=lambda c: c.get("name", "")))
            html += (
                '<div class="ic-grid" style="margin-left:24px;padding-left:12px;">'
                '<div class="node-grid">{ic_html}</div>'
                '</div>'
            ).format(ic_html=ic_html)
    
    return html


def build_team_section(contacts):
    """Group contacts by team, with managers and their reports.
    
    Returns HTML for a collapsible org-chart grouped by team.
    """
    teams = {}
    for c in contacts:
        name = c.get("name", "")
        if not name:
            continue
        team = infer_team(c.get("role", ""))
        teams.setdefault(team, []).append(c)
    
    sections = []
    for team_name in sorted(teams.keys()):
        team_contacts = sorted(teams[team_name], key=lambda x: x.get("name", ""))
        # Managers (level 2+) at top, ICs below
        managers = [c for c in team_contacts if any(t in (c.get("role") or "").lower() for t in ["manager", "director", "vp ", "vice president", "lead", "head of", "senior"])]
        ics = [c for c in team_contacts if c not in managers]
        
        section = '<div class="team-section">'
        section += f'<h4 class="team-header">{team_name} <span>{len(team_contacts)}</span></h4>'
        
        if managers:
            section += '<div class="team-management">'
            for m in managers:
                section += build_tree_section(m, level=0, is_last=True)
            section += '</div>'
        
        if ics:
            ic_html = "\n".join(build_node(c) for c in ics)
            section += f'<div class="team-ics"><div class="node-grid">{ic_html}</div></div>'
        
        section += '</div>'
        sections.append(section)
    
    return "\n".join(sections)


def build_node_grid(contacts):
    """Standard grid of contact nodes."""
    nodes = "\n".join(build_node(c) for c in contacts)
    return (
        '<div class="node-grid">{nodes}</div>'
    ).format(nodes=nodes)


def generate_chart(account_slug):
    """Generate stakeholder chart for one account."""
    account_name = SLUG_MAP.get(account_slug, account_slug)
    account_display = ACCOUNT_DISPLAY.get(account_name, account_name)
    
    path = CUSTOMERS_DIR / account_slug / "index.md"
    if not path.exists():
        # Try alternate slug with hyphens
        path = CUSTOMERS_DIR / account_slug.replace("-", "-") / "index.md"
        if not path.exists():
            return None
    
    data = parse_index_md(path)
    contacts = data.get("contacts", [])
    if not contacts:
        return None
    
    # Normalize all contacts
    for c in contacts:
        c["influence"] = normalize_influence(c.get("influence", "Low"))
        c["relationship_to_us"] = normalize_relationship(c.get("relationship_to_us", "Neutral"))
    
    rows = []
    
    # === Team hierarchy section (grouped by team, with reporting lines) ===
    rows.append(
        '<div class="row">'
        '<div class="label">Team Hierarchy</div>'
    )
    rows.append(build_team_section(contacts))
    rows.append('</div>')
    
    # === Influence summary (quick reference) ===
    high = [c for c in contacts if c["influence"] == "High" and c.get("name")]
    medium = [c for c in contacts if c["influence"] == "Medium" and c.get("name")]
    low = [c for c in contacts if c["influence"] == "Low" and c.get("name")]
    
    # High influence row
    if high:
        nodes = "\n".join(build_node(c) for c in high)
        rows.append(
            '<div class="row">'
            '<div class="label">Leadership / High Influence</div>'
            '<div class="node-grid">{nodes}</div>'
            '</div>'.format(nodes=nodes)
        )

    # Medium influence row
    if medium:
        nodes = "\n".join(build_node(c) for c in medium)
        rows.append(
            '<div class="row">'
            '<div class="label">Technical / Medium Influence</div>'
            '<div class="node-grid">{nodes}</div>'
            '</div>'.format(nodes=nodes)
        )

    # Low influence - grouped by role category
    if low:
        sw = [c for c in low if any(k in c.get("role", "").lower() for k in ["software", "firmware", "engineer", "system"])]
        eng = [c for c in low if any(k in c.get("role", "").lower() for k in ["quality", "qa", "test", "architect", "technologist", "distinguished"]) and c not in sw]
        biz = [c for c in low if c not in sw and c not in eng]

        low_parts = []
        if sw:
            low_parts.append(build_group(sw, "Software / Firmware"))
        if eng:
            low_parts.append(build_group(eng, "Engineering / QA"))
        if biz:
            low_parts.append(build_group(biz, "Business / Admin"))

        rows.append(
            '<div class="row">'
            '<div class="label">Operational / Low Influence</div>'
            '{low_parts}'
            '</div>'.format(low_parts="".join(low_parts))
        )

    rows_html = "\n".join(rows)

    html = html_format(HTML_TEMPLATE,
        account_name=account_name,
        account_display=account_display,
        contact_count=len(contacts),
        rows_html=rows_html,
    )

    output_path = OUTPUT_DIR / "{slug}-stakeholder-map.html".format(slug=account_slug)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main():
    for slug in SLUG_MAP:
        result = generate_chart(slug)
        if result:
            print("Generated {}".format(result.name))
        else:
            print("Skipped {} (no data or missing file)".format(slug))


if __name__ == "__main__":
    main()
