# Customer Stakeholder Management System

Complete workflow for managing customer stakeholder data from HubSpot CRM → local markdown → HTML charts → Notion databases.

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────┐
│  HubSpot CSV    │ ──▶ │  Local Markdown  │ ──▶ │  HTML Charts    │ ──▶ │   Notion     │
│  (source)       │     │  (source of      │     │  (stakeholder   │     │  (sharing &  │
│                 │     │   truth)         │     │   maps)         │     │   collaboration)│
└─────────────────┘     └──────────────────┘     └─────────────────┘     └──────────────┘
                              │                       │                       │
                              ▼                       ▼                       ▼
                        18 folders             18 HTML files            2 databases:
                        with index.md        in stakeholder maps/     - Customer Stakeholders
                                               (auto-generated)        - Customer Accounts
```

---

## Directory Structure

```
~/.hermes/projects/customer-accounts/
├── customers/                          # Source of truth (markdown per account)
│   ├── motorola/
│   │   └── index.md
│   ├── polar/
│   │   └── index.md
│   ├── csem/
│   ├── halma/
│   ├── university-of-jyvaskyla/
│   ├── tridonic/
│   ├── zwift/
│   ├── poly/
│   ├── sofar/
│   ├── jumo/
│   ├── kuester/
│   ├── getac/
│   ├── globalsense/
│   ├── halo-collar/
│   ├── daikin/
│   ├── masco/
│   ├── replior/
│   └── nestle-purina/
│       └── index.md
├── stakeholder maps/                   # Generated HTML charts
│   ├── motorola-stakeholder-map.html
│   ├── polar-stakeholder-map.html
│   ├── csem-stakeholder-map.html
│   ├── halma-stakeholder-map.html
│   ├── university-of-jyvaskyla-stakeholder-map.html
│   ├── tridonic-stakeholder-map.html
│   ├── zwift-stakeholder-map.html
│   ├── poly-stakeholder-map.html
│   ├── sofar-stakeholder-map.html
│   ├── jumo-stakeholder-map.html
│   ├── kuester-stakeholder-map.html
│   ├── getac-stakeholder-map.html
│   ├── globalsense-stakeholder-map.html
│   ├── halo-collar-stakeholder-map.html
│   ├── daikin-stakeholder-map.html
│   ├── masco-stakeholder-map.html
│   ├── replior-stakeholder-map.html
│   └── nestle-purina-stakeholder-map.html
├── scripts/
│   └── generate_stakeholder_charts.py  # Chart generator
└── README.md                           # This file
```

---

## Data Schema (index.md)

Each `index.md` has YAML frontmatter with structured contacts:

```yaml
---
name: Motorola Solutions
industry: telecommunications
tsh: Teague
customer_since: null
renewal: null
arr: unknown
health: unknown
risk_factors: []
expansion_signals: null
last_touch: null
next_touch_due: null
contacts:
  - name: Jane Doe
    role: VP Engineering
    influence: High
    relationship_to_us: Ally
    notes: "Title: VP Engineering; Last activity: 2026-01-15; Sales activities: 42"
  - name: John Smith
    role: Senior Software Engineer
    influence: Medium
    relationship_to_us: Neutral
    notes: "Title: Senior Software Engineer; Last activity: 2026-02-20; Sales activities: 18"
notes_links: []
---
```

**Contact fields:**
| Field | Type | Values |
|-------|------|--------|
| `name` | string | Full name |
| `role` | string | Job title |
| `influence` | select | `High`, `Medium`, `Low` |
| `relationship_to_us` | select | `Ally`, `Neutral`, `Warm`, `Blocker`, `Marketing` |
| `notes` | string | Free text with activity metadata |

---

## Workflow Commands

### 1. Update Contacts from HubSpot CSV

```bash
# After downloading new HubSpot export to Downloads/
python3 ~/.hermes/scripts/sync_hubspot_to_markdown.py
```
*(Script not yet created — currently manual CSV → markdown via execute_code)*

### 2. Regenerate All Stakeholder Charts

```bash
python3 ~/.hermes/scripts/generate_stakeholder_charts.py
```

Output: 18 HTML files in `stakeholder maps/`

### 3. Push Contacts to Notion

```bash
# Run the upload script (requires NOTION_API_KEY env var)
export NOTION_API_KEY="ntn_..."
python3 ~/.hermes/scripts/upload_to_notion.py
```

### 4. Update Notion Account Chart URLs

```bash
# After regenerating charts, update URLs in Notion
python3 ~/.hermes/scripts/update_notion_chart_urls.py
```

### 5. Serve Charts Locally (for stakeholder sharing)

```bash
cd ~/.hermes/projects/customer-accounts/stakeholder\ maps/
python3 -m http.server 8080
# Access at http://localhost:8080/motorola-stakeholder-map.html
```

### 6. Publish Charts for External Access

Deploy the `stakeholder maps/` folder to:
- **GitHub Pages** (free, custom domain supported)
- **Netlify** (drag-drop deploy, HTTPS automatic)
- **Vercel** (git-connected, preview deployments)

Then update Notion `Chart URL` property to the public HTTPS URLs.

---

## Notion Databases

### Customer Stakeholders
- **ID:** `3a70efce-9aed-80fc-8a7d-d68e4f03de78`
- **Data Source:** `3a70efce-9aed-8024-966c-000b8ad90e4a`
- **Properties:** Name, Account (select), Role, Influence, Relationship, Last Activity, Sales Activities, Notes
- **Rows:** ~639 contacts across 18 accounts

### Customer Accounts
- **ID:** `3a70efce-9aed-80a1-b089-000b1fb5128f`
- **Properties:** Name, Account (select), Chart URL, Chart File, Contact Count, TSH, Contacts (relation → Customer Stakeholders)
- **Rows:** 18 (one per account)

**Key feature:** The `Contacts` relation on Customer Accounts links to all contacts for that account in Customer Stakeholders. Open an account row → see all its stakeholders.

---

## Adding/Editing Contacts

### Option A: Edit Local Markdown (Recommended)
1. Open `~/.hermes/projects/customer-accounts/customers/<account>/index.md`
2. Add/edit contacts in the `contacts:` array
3. Run chart generator: `python3 ~/.hermes/scripts/generate_stakeholder_charts.py`
4. (Optional) Re-upload to Notion: `python3 ~/.hermes/scripts/upload_to_notion.py`

### Option B: Edit in Notion
1. Open Customer Stakeholders database
2. Add/edit rows directly
3. **Caution:** Notion changes won't sync back to local markdown automatically

---

## Influence & Relationship Definitions

### Influence
| Level | Criteria |
|-------|----------|
| **High** | C-suite, VP, Director, Head of, GM, CTO, CEO |
| **Medium** | Senior, Lead, Architect, Principal, Manager, Distinguished, Expert |
| **Low** | Individual contributors, Junior, Intern, Student (unless activity ≥30 → Medium) |

### Relationship
| Level | Criteria |
|-------|----------|
| **Ally** | Customer/In Progress/Nurture lifecycle; or >15 sales activities |
| **Warm** | 5-15 sales activities |
| **Neutral** | New, Educational Community, or <5 activities |
| **Blocker** | Disqualified, Do Not Contact |
| **Marketing** | Marketing contact status |

---

## Environment Setup

```bash
# ~/.hermes/.env or shell profile
export NOTION_API_KEY="ntn_N40232947012yYBIk1hW21rD0UQTRNvXYUVTYiruBkagiI"
```

Integration must have access to both Notion databases (share each database with "Hermes Desktop - Mac Studio" integration).

---

## Key Scripts Reference

### `generate_stakeholder_charts.py`
Reads all `customers/*/index.md`, outputs `stakeholder maps/*.html`

### Chart Generator Features
- Groups by influence (High → Medium → Low)
- Low influence grouped by role category (Software/Firmware, Engineering/QA, Business/Admin)
- Color-coded influence bars (amber/green/blue)
- Activity badges for low-influence contacts
- Responsive grid layout
- Dark theme optimized for presentation

### Notion Sync Scripts
| Script | Purpose |
|--------|---------|
| `upload_to_notion.py` | Pushes all contacts from markdown → Notion Customer Stakeholders |
| `update_notion_chart_urls.py` | Updates Customer Accounts Chart URL property |

*(These are embedded in execute_code calls in chat history — extract to files for persistence)*

---

## Troubleshooting

### Notion API Errors
| Error | Fix |
|-------|-----|
| `400: relation.length ≤ 100` | Motorola has 307 contacts; only first 100 linked. Acceptable limit. |
| `404: page not found` | Share the database/page with the integration in Notion UI |
| `400: validation_error` | Check property IDs match (run query to get current IDs) |

### Chart Generation Issues
| Issue | Fix |
|-------|-----|
| Missing contacts in chart | Verify `index.md` has valid YAML and `contacts:` array |
| Duplicate contacts | Deduplication runs on `(account, name)` key |
| Encoding errors | Ensure files are UTF-8; special chars (ä, é, etc.) handled by yaml |

### CSV → Markdown Sync
Currently manual via `execute_code`. To automate:
1. Create `sync_hubspot_to_markdown.py` that:
   - Reads latest CSV from `~/Downloads/`
   - Applies "No Longer Here" filter
   - Maps HubSpot company names to account slugs
   - Writes/updates each `index.md`

---

## Maintenance Checklist

**Weekly:**
- [ ] Download fresh HubSpot export
- [ ] Run sync to update local markdown
- [ ] Regenerate charts
- [ ] Push to Notion

**Monthly:**
- [ ] Review influence/relationship assignments
- [ ] Archive stale contacts (no activity > 180 days)
- [ ] Verify Notion relations intact

**Quarterly:**
- [ ] Re-host charts if URLs changed
- [ ] Audit Notion database permissions
- [ ] Backup local markdown to git

---

## Git Backup (Optional)

```bash
cd ~/.hermes/projects/customer-accounts/
git init
git add customers/ scripts/ README.md
git commit -m "Initial stakeholder system"
# Add remote and push for version history
```

---

## Contact

System maintained by Patrick Ruster. For questions about the data flow or Notion integration, see chat history with Hermes (Wren) from July 2026.