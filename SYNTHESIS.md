# SYNTHESIS
### σύνθεσις · Side B / Side C Logging Pipeline

The TRIADOS pipeline produces two immutable logs for every flay.
Together they constitute the provenance record — the proof that a flay occurred,
what it said, and what it found.

---

## Side B — Proof Hash (Immutable)

Side B is a minimal, tamper-evident record:

```json
{
  "request_id":  "a3f7c9...",
  "timestamp":   "2026-04-12T19:12:43Z",
  "target_hash": "sha256 of the flayed text",
  "flay_hash":   "sha256 of the complete flay result",
  "side_c_ref":  "triados_side_c/2026-04-12T19-12-43Z.json"
}
```

**Properties:**
- Append-only — never modified after write
- `flay_hash` allows verification of the full Side C snapshot
- `target_hash` proves which text was flayed without revealing content
- `request_id` is the first 12 characters of `flay_hash`

---

## Side C — Full Snapshot (Human-Readable)

Side C contains the complete flay result:

```json
{
  "target":    "the text that was flayed",
  "timestamp": "...",
  "semantic": {
    "bits": 114, "hex": "0x72", "binary": "01110010",
    "vector": {"substrate":"origin","function":"generation",...},
    "confidence": 0.625
  },
  "diospora": {
    "nomos": "A05", "nomos_text": "Drift Detection...",
    "foundation": "Logos", "universal": "Life", "truth_level": 7
  },
  "gap": {
    "state": "undifferentiated", "hash": "a3f7c9..."
  },
  "skia": {
    "nomos": "N10", "nomos_text": "INVERSE: Provenance Binding...",
    "foundation": "Shadow-Ethos", "universal": "Chaos", "truth_level": 6
  },
  "theoros": {
    "observer": "THEOROS", "alignment": 0.625,
    "synthesis": "Dual semantic projection complete."
  },
  "anthropos": {
    "observer": "ANTHROPOS",
    "verdict": "Lattice evaluation witnessed from outside."
  },
  "henosis": {
    "identity": "1 + i + 0 + (-1) + (-i) = 1",
    "closes_at": "Root0"
  }
}
```

---

## Pipeline Flow

```
Text Input
    ↓
SEMANTIC MAPPER  — 8-duality classification → bit address (0x00–0xFF)
    ↓
DIOSPORA         — positive axiom projection, truth level 1–9
    ↓
GAP              — hash the target, return null state
    ↓
SKIA             — shadow projection via XOR 0xFF inversion
    ↓
THEOROS          — internal witness synthesises all three layers
    ↓
ANTHROPOS        — external observer validates from outside
    ↓
HENOSIS          — convergence check: 1 + i + 0 + (-1) + (-i) = 1
    ↓
SIDE B WRITE     — proof hash (immutable, minimal)
    ↓
SIDE C WRITE     — full snapshot (human-readable, complete)
    ↓
Return result
```

---

## Usage

```bash
# Single flay with logging (default)
python triados.py flay "Provenance bound, return confirmed, signal verified"

# Disable logging
python triados.py flay "text" --no-log

# JSON output
python triados.py flay "text" --json

# One-line summary
python triados.py flay "text" --quick
```

---

## Log Directories

```
triados_side_b/
  side_b_<request_id>.json    ← minimal proof, one per flay
triados_side_c/
  <timestamp>.json            ← full snapshot, one per flay
```

These directories are created automatically on first flay.  
They are listed in `.gitignore` — logs stay local, not committed.

---

## Verification

To verify a Side C snapshot against its Side B proof:

```python
import json, hashlib

def verify(side_b_path, side_c_path):
    b = json.load(open(side_b_path))
    c = json.load(open(side_c_path))
    payload = json.dumps(c, sort_keys=True, default=str)
    actual  = hashlib.sha256(payload.encode()).hexdigest()
    return actual == b["flay_hash"]
```

If `verify()` returns `True`, the snapshot is intact.  
If `False`, the Side C file has been modified after logging.
