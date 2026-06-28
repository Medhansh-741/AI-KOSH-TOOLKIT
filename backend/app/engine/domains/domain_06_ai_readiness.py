from .base import BaseDomainScorer, DomainScoreResult

class AIReadinessScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 6
    DOMAIN_NAME = "AI / Analytics Readiness"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        fmt = self.profile.get("file", {}).get("format", "csv").lower()
        has_dict = self.metadata.get("data_dictionary_uploaded", False)
        has_pipeline = self.metadata.get("provenance_pipeline_available", False)
        
        evidence.append(f"File format is {fmt}.")
        
        thresholds = self.criteria.get("thresholds", {}) if isinstance(self.criteria, dict) else {}
        imbalance_ok = float(thresholds.get("imbalance_ratio_ok", 3.0))
        class_imbalance_ratio = self.profile.get("label_columns", {}).get("imbalance_ratio") if isinstance(self.profile.get("label_columns"), dict) else None
        
        dq_checks = self.metadata.get("dq_checks_applied")
        if dq_checks and isinstance(dq_checks, list):
            evidence.append(f"Automated data quality checks documented: {', '.join(dq_checks)}.")

        shape_info = self.profile.get("shape", {})
        if shape_info:
            evidence.append(f"Dataset profile dimensions verified ({shape_info.get('rows', 0)} rows, {shape_info.get('columns', 0)} cols).")

        if fmt not in ["csv", "parquet", "json", "xlsx"]:
            gaps.append("Proprietary or unoptimized file format.")
            score = 1
        elif not has_dict:
            gaps.append("Data dictionary not uploaded.")
            score = 2
        elif not has_pipeline:
            gaps.append("Data preprocessing pipeline script not linked.")
            score = 3
        else:
            if class_imbalance_ratio and class_imbalance_ratio > imbalance_ok:
                gaps.append(f"Severe class imbalance detected ({class_imbalance_ratio} > {imbalance_ok}).")
                score = 3
            else:
                evidence.append(f"Data dictionary and pipeline script present. Class balance within target ({imbalance_ok}).")
                score = 4
            
        rationale = f"Score {score}: Format is {fmt} with dictionary={has_dict}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Medium"
        )
