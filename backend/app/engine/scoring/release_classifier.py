from typing import Dict, Any, Literal
from pydantic import BaseModel

class ReleaseClassificationResult(BaseModel):
    classification: Literal["Open", "Controlled", "Restricted"]
    justification: str
    policy_override_applied: bool

class ReleaseClassificationEngine:
    @staticmethod
    def classify_release(
        cqi: float,
        prs: int,
        prs_band: str,
        sensitivity_class: str,
        differential_privacy_verified: bool = False
    ) -> ReleaseClassificationResult:
        """Applies the CQI x PRS matrix to classify the dataset release."""
        # Policy override: high-stigma / critical data
        if sensitivity_class in ("high_stigma", "critical"):
            if prs_band in ("High", "Very High"):
                return ReleaseClassificationResult(
                    classification="Restricted",
                    justification=f"High-stigma data with {prs_band} PRS. Restricted per MIDAS policy.",
                    policy_override_applied=True
                )
            if not differential_privacy_verified:
                return ReleaseClassificationResult(
                    classification="Controlled",
                    justification=f"High-stigma data defaults to Controlled unless Differential Privacy is independently verified.",
                    policy_override_applied=True
                )

        # Standard CQI × PRS matrix
        if cqi >= 70.0 and prs_band == "Low":
            return ReleaseClassificationResult(
                classification="Open",
                justification=f"CQI={cqi} (>=70) and PRS={prs} (Low). Open access permitted.",
                policy_override_applied=False
            )
        if cqi >= 70.0 and prs_band == "Moderate":
            return ReleaseClassificationResult(
                classification="Controlled",
                justification=f"CQI={cqi} (>=70) but PRS={prs} (Moderate). Controlled access required.",
                policy_override_applied=False
            )
        if prs_band in ("High", "Very High"):
            return ReleaseClassificationResult(
                classification="Restricted",
                justification=f"PRS={prs} ({prs_band}). Restricted regardless of CQI.",
                policy_override_applied=False
            )
        if cqi < 50.0:
            if prs_band == "Low":
                return ReleaseClassificationResult(
                    classification="Controlled",
                    justification=f"CQI={cqi} (<50). Controlled until quality improved.",
                    policy_override_applied=False
                )
            return ReleaseClassificationResult(
                classification="Restricted",
                justification=f"CQI={cqi} (<50) and PRS={prs} ({prs_band}). Restricted.",
                policy_override_applied=False
            )

        # Default (CQI 50–69, PRS Low/Moderate)
        return ReleaseClassificationResult(
            classification="Controlled",
            justification=f"CQI={cqi} (Silver/Gold band). Controlled access.",
            policy_override_applied=False
        )

