from dataclasses import dataclass
from typing import Dict, Optional, Any

CQI_BANDS = [
    (95.0, "Diamond"),
    (85.0, "Platinum"),
    (70.0, "Gold"),
    (50.0, "Silver"),
    (25.0, "Bronze"),
    (0.0,  "Remediation"),
]

@dataclass
class CQIResult:
    total_score: int
    max_possible: int
    cqi: float
    band: str
    formula_trace: str
    domain_11_applicable: bool

def compute_cqi(domain_scores: Dict[int, Optional[int]], domain_11_applicable: bool, criteria: Optional[Dict[str, Any]] = None) -> CQIResult:
    scores = {k: v for k, v in domain_scores.items() if v is not None}
    total = sum(scores.values())
    max_possible = len([s for s in scores.values() if s is not None]) * 4
    cqi = round((total / max_possible) * 100, 1) if max_possible > 0 else 0.0

    cqi_config = criteria.get("cqi_bands", {}) if isinstance(criteria, dict) else {}
    if cqi_config:
        d_min = float(cqi_config.get("diamond_min", 95.0))
        p_min = float(cqi_config.get("platinum_min", 85.0))
        g_min = float(cqi_config.get("gold_min", 70.0))
        s_min = float(cqi_config.get("silver_min", 50.0))
        b_min = float(cqi_config.get("bronze_min", 25.0))
        bands = [
            (d_min, "Diamond"),
            (p_min, "Platinum"),
            (g_min, "Gold"),
            (s_min, "Silver"),
            (b_min, "Bronze"),
            (0.0, "Remediation"),
        ]
    else:
        bands = CQI_BANDS

    band = next(label for threshold, label in bands if cqi >= threshold)
    trace = f"({total} / {max_possible}) × 100 = {cqi}"
    return CQIResult(
        total_score=total,
        max_possible=max_possible,
        cqi=cqi,
        band=band,
        formula_trace=trace,
        domain_11_applicable=domain_11_applicable
    )
