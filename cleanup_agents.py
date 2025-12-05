# cleanup_agents.py
# Run: python cleanup_agents.py
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
AGENTS = (ROOT / "src" / "agents")

if not AGENTS.exists():
    print("Could not find src/agents folder. Run from project root.")
    sys.exit(1)

pattern_start = re.compile(r'^\s*powershell\s+-Command\s+["@\']', re.IGNORECASE)
pattern_end = re.compile(r"^['\"]@ \| Out-File", re.IGNORECASE)
pattern_outfile = re.compile(r"Out-File\s+-FilePath", re.IGNORECASE)

fixed_files = []
for p in AGENTS.glob("*.py"):
    text = p.read_text(encoding="utf8", errors="ignore")
    lines = text.splitlines()
    # drop leading power-shell wrapper lines
    # find first line that does NOT look like powershell wrapper / comment artifacts
    start_i = 0
    for i, L in enumerate(lines[:12]):  # only check first 12 lines
        if pattern_start.match(L) or L.strip().startswith("@'") or L.strip().startswith('@"'):
            start_i = i + 1
            continue
        # also drop echo/redirect artifacts like: echo ... >> src\agents\file.py
        if L.strip().lower().startswith('echo ') and '>>' in L:
            start_i = i + 1
            continue
        if L.strip().startswith("#") and i == 0:
            # keep initial comment lines normally
            start_i = 0
            break
        # keep first normal-looking python line
        if not L.strip().startswith('powershell') and not L.strip().startswith('echo '):
            start_i = i
            break

    # drop trailing wrapper lines (search last 12 lines)
    end_i = len(lines)
    for j, L in enumerate(lines[-12:], start=len(lines)-12):
        if pattern_end.match(L) or pattern_outfile.search(L) or "Out-File" in L:
            end_i = j
            break

    new_lines = lines[start_i:end_i]
    # Remove any stray Windows path echo lines containing ">" or ">>" that remained
    new_lines = [ln for ln in new_lines if not (ln.strip().lower().startswith('echo ') and '>>' in ln)]
    new_text = "\n".join(new_lines).strip() + "\n"
    if new_text != text:
        p.write_text(new_text, encoding="utf8")
        fixed_files.append(p.name)

print("Fixed files:", fixed_files)
print("Now check agent functions names (next steps).")
