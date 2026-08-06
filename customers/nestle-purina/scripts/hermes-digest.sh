#!/bin/bash
# Hermes config + cron digest for nanoclaw/ionga. Emits markdown to stdout.
# ponytail: reads live config each run, so it never goes stale.
set -euo pipefail
H="${HERMES_HOME:-$HOME/.hermes}"
CFG="$H/config.yaml"

python3 - "$CFG" "$H/.env" <<'PY'
import sys, yaml, json, os
cfg_path, env_path = sys.argv[1], sys.argv[2]
cfg = yaml.safe_load(open(cfg_path))

# Toolsets Hermes lets you toggle via agent.disabled_toolsets
MANAGED = ["browser","code_execution","computer_use","cronjob","image_gen","tts","clarify"]
disabled = set(cfg.get("agent",{}).get("disabled_toolsets") or [])
active   = [t for t in MANAGED if t not in disabled]
inactive = [t for t in MANAGED if t in disabled]

# image_gen has no local backend; flag if no cloud image key actually set
# (ignore commented lines + placeholder values like your_gemini_key)
def env_set(keys):
    found = []
    for ln in (open(env_path) if os.path.exists(env_path) else []):
        ln = ln.strip()
        if ln.startswith("#") or "=" not in ln: continue
        k, _, v = ln.partition("=")
        v = v.strip().strip('"\'')
        if k.strip() in keys and v and not v.lower().startswith("your_"):
            found.append(k.strip())
    return found
img_keys = env_set({"OPENAI_API_KEY","GEMINI_API_KEY","GOOGLE_API_KEY","XAI_API_KEY"})
notes = []
if "image_gen" in active and not img_keys:
    notes.append("image_gen: ON but NO backend key (needs OpenAI/Gemini/xAI) -> will error on use")
if "tts" in active:
    notes.append(f"tts: ON via provider '{cfg.get('tts',{}).get('provider','?')}'")
vis = cfg.get("auxiliary",{}).get("vision",{})
notes.append(f"vision: {vis.get('provider','auto')} / {vis.get('model') or '(unset)'}")

print("## Hermes toolsets")
print("**Active:** " + ", ".join(active))
print("**Inactive:** " + ", ".join(inactive))
for n in notes: print(f"- {n}")
print()

# Hermes-managed cron jobs (agent-scheduled)
jobs = json.load(open(os.path.join(os.path.dirname(cfg_path),"cron","jobs.json")))["jobs"] \
       if os.path.exists(os.path.join(os.path.dirname(cfg_path),"cron","jobs.json")) else []
print("## Hermes cron jobs (agent-scheduled)")
if not jobs:
    print("- none registered")
else:
    for j in jobs:
        print(f"- {j.get('name','?')} | {j.get('schedule','?')} | {'enabled' if j.get('enabled',True) else 'DISABLED'}")
print()
PY

# launchd recurring automation (the real scheduled jobs on this box)
echo "## launchd jobs (hermes + nanoclaw)"
launchctl list | awk 'NR>1 && ($3 ~ /hermes|nanoclaw|cruft|ionga/){
  st=($1=="-"?"idle":"pid "$1); printf "- %s | %s | last_exit %s\n", $3, st, $2 }' | sort
