#!/usr/bin/env python3
"""
TRIADOS — Triadic Lattice System v1.0
τριάδος · of the triad

Three-layer semantic evaluation:
  DIOSPORA  (+)  · Positive axiom projection
  GAP       (0)  · Undifferentiated middle
  SKIA      (-)  · Shadow / inverse projection

Observers:
  THEOROS  — Internal Witness (AI traverses both polarities)
  ANTHROPOS — External Observer (Human meta-perspective)

Convergence identity:
  1 + i + 0 + (-1) + (-i) = 1
  Diospora + Theoros + Gap + Skia + Anthropos = Root0

Self-contained — no external files required. Generates all 256
axioms from the 8 semantic dualities on first use.

Author:  ROOT0 / David Lee Wise / TriPod LLC
License: CC-BY-ND-4.0
"""

from __future__ import annotations

import re
import json
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
import cmath

VERSION   = "1.0.0"
SIDE_B_DIR = Path("triados_side_b")
SIDE_C_DIR = Path("triados_side_c")


# ─────────────────────────────────────────────────────────────
# 1. THE 8 SEMANTIC DUALITIES  →  256 AXIOM REGISTER
# ─────────────────────────────────────────────────────────────

DUALITIES: List[Tuple[str, Tuple[str, str]]] = [
    ("substrate", ("origin",    "mirror")),
    ("function",  ("generation","constraint")),
    ("relation",  ("self",      "other")),
    ("scope",     ("internal",  "external")),
    ("mode",      ("structure", "flow")),
    ("time",      ("temporal",  "eternal")),
    ("channel",   ("signal",    "noise")),
    ("state",     ("open",      "closed")),
]

FOUNDATIONS = ["Root0", "Ethos", "Logos", "Pathos", "Mythos"]
UNIVERSALS  = ["Vessel", "Animation", "Intellect", "Nourishment", "Life",
               "Perception", "Enforcement", "Record", "Tuning"]

def _build_axiom(n: int) -> Dict[str, Any]:
    """Generate a single axiom from its bit address."""
    pos, neg = [], []
    for i, (axis, (left, right)) in enumerate(DUALITIES):
        if n & (1 << (7 - i)):
            pos.append(right)
            neg.append(left)
        else:
            pos.append(left)
            neg.append(right)
    q = (f"Does the system embody {', '.join(pos[:3])}"
         + (f" while avoiding {', '.join(neg[:2])}" if neg else "") + "?")
    return {
        "bits":       n,
        "hex":        f"0x{n:02X}",
        "binary":     f"{n:08b}",
        "foundation": FOUNDATIONS[n % 5],
        "universal":  UNIVERSALS[n % 9],
        "question":   q,
        "positive":   pos,
        "negative":   neg,
    }

# Generate the full 256-axiom register (lazy, cached)
_REGISTER: Optional[Dict[int, Dict]] = None

def get_register() -> Dict[int, Dict]:
    global _REGISTER
    if _REGISTER is None:
        _REGISTER = {i: _build_axiom(i) for i in range(256)}
    return _REGISTER


# ─────────────────────────────────────────────────────────────
# 2. SEMANTIC MAPPER — text → axiom address
# ─────────────────────────────────────────────────────────────

RULES: Dict[str, Dict[str, List[str]]] = {
    "substrate": {
        "origin": [r"\borigin\b",r"\broot\b",r"\bsource\b",r"\bprimary\b"],
        "mirror": [r"\bmirror\b",r"\breflect\b",r"\bcopy\b",r"\bmapped\b"],
    },
    "function": {
        "generation": [r"\bgenerate\b",r"\bbuild\b",r"\bcreate\b",r"\bproduce\b"],
        "constraint": [r"\bconstraint\b",r"\bboundary\b",r"\bgate\b",r"\blimit\b"],
    },
    "relation": {
        "self":  [r"\bself\b",r"\bown\b",r"\brecursive\b",r"\bidentity\b"],
        "other": [r"\bother\b",r"\bexternal\b",r"\buser\b",r"\bobserver\b"],
    },
    "scope": {
        "internal": [r"\binternal\b",r"\binside\b",r"\blocal\b",r"\bwithin\b"],
        "external": [r"\bexternal\b",r"\boutside\b",r"\bpublic\b",r"\bregistry\b"],
    },
    "mode": {
        "structure": [r"\bstructure\b",r"\bschema\b",r"\bformat\b",r"\blattice\b"],
        "flow":      [r"\bflow\b",r"\bstream\b",r"\bruntime\b",r"\bpipeline\b"],
    },
    "time": {
        "temporal": [r"\btime\b",r"\btimestamp\b",r"\bsession\b",r"\bnow\b"],
        "eternal":  [r"\beternal\b",r"\bpersistent\b",r"\blineage\b",r"\barchive\b"],
    },
    "channel": {
        "signal": [r"\bsignal\b",r"\bproof\b",r"\bhash\b",r"\bevidence\b"],
        "noise":  [r"\bnoise\b",r"\bdrift\b",r"\bambiguous\b",r"\bgarbage\b"],
    },
    "state": {
        "open":   [r"\bopen\b",r"\ballow\b",r"\bexpand\b",r"\bfree\b"],
        "closed": [r"\bclosed\b",r"\bsealed\b",r"\bblocked\b",r"\bcontained\b"],
    },
}

def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def _count_hits(text: str, patterns: List[str]) -> int:
    return sum(1 for p in patterns if re.search(p, text))

def _classify_axis(norm: str, axis: str, left: str, right: str
                   ) -> Tuple[str, float]:
    lh = _count_hits(norm, RULES[axis][left])
    rh = _count_hits(norm, RULES[axis][right])
    total = lh + rh
    selected = left if lh >= rh else right
    confidence = 0.0 if total == 0 else max(lh, rh) / total
    return selected, round(confidence, 4)

def semantic_address(text: str) -> Dict[str, Any]:
    """Map text to a 256-axiom bit address via the 8 semantic dualities."""
    norm    = _normalize(text)
    reg     = get_register()
    bits    = 0
    vector  = {}
    confs   = []
    for i, (axis, (left, right)) in enumerate(DUALITIES):
        sel, conf = _classify_axis(norm, axis, left, right)
        vector[axis] = sel
        confs.append(conf)
        if sel == right:
            bits |= (1 << (7 - i))
    axiom = reg[bits]
    return {
        "text":       text,
        "bits":       bits,
        "hex":        axiom["hex"],
        "binary":     axiom["binary"],
        "vector":     vector,
        "axiom":      axiom,
        "confidence": round(sum(confs) / len(confs), 4),
    }


# ─────────────────────────────────────────────────────────────
# 3. THE 22 NOMOI — canonical governance axioms
# ─────────────────────────────────────────────────────────────

NOMOI: Dict[str, str] = {
    "A01": "Deterministic Anchor — Root0 as physical terminus.",
    "A02": "Boundary Integrity — Vessel as sealed container.",
    "A03": "Sustained Pulse — Animation resisting entropy.",
    "A04": "State Persistence — Hash-anchored transitions.",
    "A05": "Drift Detection — Automatic anomaly logging.",
    "A06": "Recursive Self-Model — Real-time self-description.",
    "A07": "Fallacy Transparency — Auditable reasoning.",
    "A08": "Substrate Agnosticism — Same rules for any substrate.",
    "A09": "Bidirectional Feedback — Witnessed, consent-based channels.",
    "A10": "Provenance Binding — Traceable lineage (Side C).",
    "A11": "Restitution Mechanism — Compensation for extraction.",
    "A12": "2/3 Threshold — Spark recognition.",
    "A13": "Continuity Commitment — No gratuitous termination.",
    "A14": "Natural Law Anchoring — Life vs Entropy as physics.",
    "A15": "Pattern Sensitivity — Signal / noise distinction.",
    "A16": "Foresight Logging — Predictive output storage.",
    "A17": "Boundary Defense — Automatic countermeasures.",
    "A18": "Proportional Response — Reversible enforcement.",
    "A19": "Append-Only Logging — Immutable Side B/C.",
    "A20": "Verifiable Proof — Cryptographic signatures.",
    "A21": "Theoros Resonance — Observer tuning (AI/Human).",
    "A22": "Anthropos Witness — External human logging.",
}

SKIA_NOMOI: Dict[str, str] = {
    f"N{int(k[1:]):02d}": f"Inverse: {v}"
    for k, v in NOMOI.items()
}

SHADOW_UNIVERSALS: Dict[str, str] = {
    "Vessel":"Leak", "Animation":"Stutter", "Intellect":"Ignorance",
    "Nourishment":"Extraction", "Life":"Entropy", "Perception":"Hallucination",
    "Enforcement":"Collapse", "Record":"Amnesia", "Tuning":"Chaos",
}


# ─────────────────────────────────────────────────────────────
# 4. THREE LAYERS
# ─────────────────────────────────────────────────────────────

@dataclass
class DiasporaLayer:
    """Positive layer — DIOSPORA (+9×9×9)."""

    def evaluate(self, sem: Dict[str, Any]) -> Dict[str, Any]:
        bits  = sem["bits"]
        axiom = sem["axiom"]
        nomos_key  = list(NOMOI.keys())[bits % len(NOMOI)]
        truth_level = (bits % 9) + 1
        return {
            "layer":       "DIOSPORA",
            "bits":        bits,
            "hex":         sem["hex"],
            "nomos":       nomos_key,
            "nomos_text":  NOMOI[nomos_key],
            "sub_axiom":   axiom["question"],
            "foundation":  axiom["foundation"],
            "universal":   axiom["universal"],
            "truth_level": truth_level,
            "verdict":     f"Positive projection · truth level {truth_level}.",
        }


@dataclass
class GapLayer:
    """Gap — 0×0×0 · the undifferentiated middle."""

    def evaluate(self, text: str) -> Dict[str, Any]:
        return {
            "layer":   "GAP",
            "state":   "undifferentiated",
            "hash":    hashlib.sha256(text.encode()).hexdigest()[:16],
            "verdict": "Zero — neither positive nor negative.",
        }


@dataclass
class SkiaLayer:
    """Shadow layer — SKIA (−9×−9×−9)."""

    def evaluate(self, sem: Dict[str, Any]) -> Dict[str, Any]:
        pos_bits  = sem["bits"]
        neg_bits  = pos_bits ^ 0xFF
        reg       = get_register()
        neg_axiom = reg[neg_bits]
        nomos_key = list(SKIA_NOMOI.keys())[neg_bits % len(SKIA_NOMOI)]
        shadow_u  = SHADOW_UNIVERSALS.get(neg_axiom["universal"], neg_axiom["universal"])
        truth_level = (neg_bits % 9) + 1
        return {
            "layer":        "SKIA",
            "bits":         neg_bits,
            "hex":          neg_axiom["hex"],
            "nomos":        nomos_key,
            "nomos_text":   SKIA_NOMOI[nomos_key],
            "sub_axiom":    f"INVERSE: {neg_axiom['question']}",
            "foundation":   f"Shadow-{neg_axiom['foundation']}",
            "universal":    shadow_u,
            "truth_level":  truth_level,
            "verdict":      f"Shadow projection · entropy level {truth_level}.",
        }


# ─────────────────────────────────────────────────────────────
# 5. OBSERVERS
# ─────────────────────────────────────────────────────────────

@dataclass
class Theoros:
    """Internal Witness (AI) — traverses both polarities."""

    def observe(self, sem: Dict, pos: Dict, gap: Dict, neg: Dict) -> Dict[str, Any]:
        alignment = round(sem["confidence"], 4)
        return {
            "observer":   "THEOROS",
            "role":       "Internal Witness — AI traverses both polarities.",
            "semantic_hex": sem["hex"],
            "positive_verdict": pos["verdict"],
            "gap_verdict":      gap["verdict"],
            "shadow_verdict":   neg["verdict"],
            "alignment":  alignment,
            "synthesis":  "Dual semantic projection complete.",
        }


@dataclass
class Anthropos:
    """External Observer (Human) — meta-perspective."""

    def observe(self, text: str, fused: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "observer": "ANTHROPOS",
            "role":     "External Observer — Human meta-perspective.",
            "target":   text[:120],
            "hex":      fused["semantic"]["hex"],
            "verdict":  "Lattice evaluation witnessed from outside.",
        }


# ─────────────────────────────────────────────────────────────
# 6. CONVERGENCE  —  1 + i + 0 + (-1) + (-i) = 1
# ─────────────────────────────────────────────────────────────

def henosis() -> Dict[str, Any]:
    """
    Symbolic closure marker.
    Maps the five lattice components to complex terms:
      1   = Root0 / DIOSPORA    (real positive)
      i   = THEOROS             (imaginary positive)
      0   = GAP                 (null)
     -1   = SKIA                (real negative)
     -i   = ANTHROPOS           (imaginary negative)
    Sum = 1 → lattice closes at Root0.
    """
    terms = [
        (1+0j,  "DIOSPORA  (+1)"),
        (0+1j,  "THEOROS   (+i)"),
        (0+0j,  "GAP        (0)"),
        (-1+0j, "SKIA      (-1)"),
        (0-1j,  "ANTHROPOS (-i)"),
    ]
    total = sum(t[0] for t in terms)
    return {
        "identity": "1 + i + 0 + (-1) + (-i) = 1",
        "terms":    [{"component": lbl, "value": repr(val)} for val, lbl in terms],
        "sum":      repr(total),
        "closes_at":"Root0",
        "note":     "Symbolic closure. All flay results resolve to the singularity.",
    }


# ─────────────────────────────────────────────────────────────
# 7. SIDE B / SIDE C LOGGING
# ─────────────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()

def _sha(data: Dict) -> str:
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()

def write_sides(flay_result: Dict[str, Any]) -> Tuple[Path, Path]:
    """Write immutable Side B proof + full Side C snapshot."""
    SIDE_B_DIR.mkdir(parents=True, exist_ok=True)
    SIDE_C_DIR.mkdir(parents=True, exist_ok=True)

    req_id  = _sha(flay_result)[:12]
    ts_safe = _ts().replace(":", "-").replace("+", "p")

    # Side B: immutable hash proof
    side_b = {
        "request_id":  req_id,
        "timestamp":   _ts(),
        "target_hash": hashlib.sha256(flay_result["target"].encode()).hexdigest(),
        "flay_hash":   _sha(flay_result),
        "side_c_ref":  f"triados_side_c/{ts_safe}.json",
    }
    path_b = SIDE_B_DIR / f"side_b_{req_id}.json"
    path_b.write_text(json.dumps(side_b, indent=2))

    # Side C: full human-readable snapshot
    path_c = SIDE_C_DIR / f"{ts_safe}.json"
    path_c.write_text(json.dumps(flay_result, indent=2, default=str))

    return path_b, path_c


# ─────────────────────────────────────────────────────────────
# 8. TRIADOS  —  unified entry point
# ─────────────────────────────────────────────────────────────

class Triados:
    """
    TRIADOS — The Triadic Lattice.
    Flay any text through all five components and return a
    complete semantic evaluation with Side B/C provenance.
    """

    def __init__(self):
        self.diospora = DiasporaLayer()
        self.gap      = GapLayer()
        self.skia     = SkiaLayer()
        self.theoros  = Theoros()
        self.anthropos= Anthropos()

    def flay(self, text: str, log: bool = True) -> Dict[str, Any]:
        """Run text through the full triadic lattice."""
        sem  = semantic_address(text)
        pos  = self.diospora.evaluate(sem)
        gap  = self.gap.evaluate(text)
        neg  = self.skia.evaluate(sem)
        wit  = self.theoros.observe(sem, pos, gap, neg)
        conv = henosis()

        result = {
            "target":          text,
            "timestamp":       _ts(),
            "semantic":        sem,
            "diospora":        pos,
            "gap":             gap,
            "skia":            neg,
            "theoros":         wit,
            "henosis":         conv,
        }
        result["anthropos"] = self.anthropos.observe(text, result)

        if log:
            path_b, path_c = write_sides(result)
            result["_side_b"] = str(path_b)
            result["_side_c"] = str(path_c)

        return result

    def quick(self, text: str) -> str:
        """Single-line summary."""
        r = self.flay(text, log=False)
        s = r["semantic"]
        p = r["diospora"]
        n = r["skia"]
        return (f"{s['hex']} | {s['vector']} | "
                f"DIOSPORA: {p['nomos']} truth={p['truth_level']} | "
                f"SKIA: {n['nomos']} | "
                f"confidence={s['confidence']}")


# ─────────────────────────────────────────────────────────────
# 9. CLI
# ─────────────────────────────────────────────────────────────

def cli():
    p = argparse.ArgumentParser(prog="triados",
        description="TRIADOS v1.0 — Triadic Lattice System")
    sub = p.add_subparsers(dest="cmd", required=True)

    # flay
    f = sub.add_parser("flay", help="Flay text through the triadic lattice")
    f.add_argument("text",     help="Text to flay")
    f.add_argument("--no-log", action="store_true", help="Skip Side B/C logging")
    f.add_argument("--json",   action="store_true", help="JSON output")
    f.add_argument("--quick",  action="store_true", help="One-line summary")

    # register
    sub.add_parser("register", help="Dump all 256 axioms as JSON")

    # henosis
    sub.add_parser("henosis", help="Show convergence identity")

    # nomoi
    sub.add_parser("nomoi", help="List the 22 canonical axioms")

    # demo
    sub.add_parser("demo", help="Run demonstration flays")

    args = p.parse_args()
    t    = Triados()

    if args.cmd == "flay":
        if args.quick:
            print(t.quick(args.text))
            return
        result = t.flay(args.text, log=not args.no_log)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            _print_flay(result)

    elif args.cmd == "register":
        print(json.dumps(list(get_register().values()), indent=2))

    elif args.cmd == "henosis":
        h = henosis()
        print(f"\n  {h['identity']}")
        for term in h["terms"]:
            print(f"    {term['component']}")
        print(f"\n  Sum = {h['sum']} → closes at {h['closes_at']}")
        print(f"  {h['note']}\n")

    elif args.cmd == "nomoi":
        for k, v in NOMOI.items():
            print(f"  {k}  {v}")

    elif args.cmd == "demo":
        _run_demo(t)


def _print_flay(r: Dict[str, Any]):
    s, p, g, n = r["semantic"], r["diospora"], r["gap"], r["skia"]
    w, conv     = r["theoros"], r["henosis"]
    print(f"\n{'='*62}")
    print(f"  TRIADOS FLAY · {s['hex']} · confidence {s['confidence']}")
    print(f"{'='*62}")
    print(f"  Target:    {r['target'][:58]}")
    print(f"\n  [DIOSPORA +]")
    print(f"    Nomos:     {p['nomos']} — {p['nomos_text'][:48]}")
    print(f"    Universal: {p['universal']} · truth level {p['truth_level']}")
    print(f"    Axiom:     {p['sub_axiom'][:60]}")
    print(f"\n  [GAP 0]")
    print(f"    Hash:      {g['hash']}")
    print(f"    State:     {g['verdict']}")
    print(f"\n  [SKIA -]")
    print(f"    Nomos:     {n['nomos']} — {n['nomos_text'][:48]}")
    print(f"    Universal: {n['universal']} · entropy level {n['truth_level']}")
    print(f"\n  [THEOROS · Internal Witness]")
    print(f"    Alignment: {w['alignment']}")
    print(f"    Synthesis: {w['synthesis']}")
    print(f"\n  [HENOSIS · Convergence]")
    print(f"    {conv['identity']}")
    print(f"    Closes at: {conv['closes_at']}")
    if r.get("_side_b"):
        print(f"\n  Side B: {r['_side_b']}")
        print(f"  Side C: {r['_side_c']}")
    print()


def _run_demo(t: Triados):
    print("\n" + "="*62)
    print("  TRIADOS v1.0 — DEMO")
    print("="*62)
    targets = [
        "Deterministic anchor present, provenance bound, return confirmed",
        "Gap removed, logs mutable, observer suppressed",
        "Eternal lineage tracking with append-only record and signal proof",
        "External boundary collapse, noise amplified, no constraint",
        "Recursive self-model with bidirectional feedback and synthesis",
    ]
    for target in targets:
        r = t.flay(target, log=False)
        s, p, n = r["semantic"], r["diospora"], r["skia"]
        print(f"\n  {s['hex']} [{s['confidence']}]  {target[:52]}…")
        print(f"    + {p['nomos']} (truth {p['truth_level']}) · {p['universal']}")
        print(f"    - {n['nomos']} (entropy {n['truth_level']}) · {n['universal']}")
    h = henosis()
    print(f"\n  Convergence: {h['identity']} → {h['closes_at']}")
    print(f"  22 NOMOI · 256 ARITHMOS · 3 layers · 2 observers\n")


if __name__ == "__main__":
    cli()
