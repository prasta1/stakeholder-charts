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

    # Truncate long notes for tooltip, show full in title
    note_preview = notes[:120] + "..." if len(notes) > 120 else notes
    safe_notes = (notes or "").replace('"', "&quot;")

    html = (
        '<div class="node" data-name="{name}" data-role="{role}" '
        'data-rel="{rel}" data-activities="{activities}">'
        '<div class="node-inner" style="border-left:3px solid {infl_color};">'
        '<div class="name" title="{safe_notes}">{name}</div>'
        '<div class="role">{role}</div>'
        '<div class="meta">'
        '<span class="badge {rel_class}">{rel}</span>'
        '<span class="badge badge-outline">{activities} activities</span>'
        '</div>'
        '</div>'
        '</div>'
    ).format(
        name=name, role=role, rel=rel, activities=activities,
        infl_color=INFLUENCE_COLOR.get(infl, "var(--low)"),
        rel_class=rel_class, safe_notes=safe_notes,
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

    # Group contacts by influence
    high = [c for c in contacts if c["influence"] == "High"]
    medium = [c for c in contacts if c["influence"] == "Medium"]
    low = [c for c in contacts if c["influence"] == "Low"]

    rows = []

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
