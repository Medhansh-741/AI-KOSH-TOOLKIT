import os

domains_code = {
    "domain_01_annotation.py": """from .base import BaseDomainScorer, DomainScoreResult

class AnnotationReliabilityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 1
    DOMAIN_NAME = "Annotation / Labelling Reliability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        data_signals = 0
        meta_signals = 4

        annotation_methodology = self.metadata.get("annotation_methodology")
        num_annotators = self.metadata.get("num_annotators")
        irr_method = self.metadata.get("irr_method")
        irr_value = self.metadata.get("irr_value")
        annotator_qualifications = self.metadata.get("annotator_qualifications")

        if not annotation_methodology:
            gaps.append("No annotation methodology documented.")
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=0,
                rationale="Annotation methodology not documented.",
                evidence_items=evidence,
                gaps=gaps,
                confidence="Low"
            )

        evidence.append("Annotation methodology documented.")
        
        # Check IRR
        if irr_value is None:
            gaps.append("No Inter-Rater Reliability (IRR) value reported.")
            score = 1
        else:
            irr_val_float = float(irr_value)
            evidence.append(f"IRR value reported: {irr_val_float} using method {irr_method or 'unknown'}")
            
            if irr_val_float < 0.6:
                gaps.append("IRR value below acceptable threshold (<0.6).")
                score = 2
            elif irr_val_float >= 0.6 and irr_val_float < 0.8:
                evidence.append("IRR value is adequate (>=0.6).")
                score = 3
            else:
                evidence.append("IRR value is exemplary (>=0.8).")
                score = 4

        if num_annotators and int(num_annotators) >= 2:
            evidence.append(f"Multi-annotator team: {num_annotators} annotators.")
        else:
            gaps.append("Dataset was annotated by a single or unknown number of annotators.")
            if score > 2:
                score = 2

        if annotator_qualifications:
            evidence.append(f"Annotator qualifications documented: {annotator_qualifications}")
        else:
            gaps.append("Annotator credentials/qualifications not reported.")
            if score == 4:
                score = 3

        confidence = self._determine_confidence(data_signals, meta_signals)
        rationale = f"Score {score}: Annotation documented, IRR is {irr_value or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence=confidence
        )
""",

    "domain_02_metadata.py": """from .base import BaseDomainScorer, DomainScoreResult

class MetadataCompletenessScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 2
    DOMAIN_NAME = "Metadata Completeness"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        # Count non-empty metadata fields
        key_fields = [
            "dataset_name", "dataset_version", "dataset_type", "study_type",
            "target_population", "geographic_coverage", "collection_start_date",
            "deidentification_method", "standards_used", "license_type"
        ]
        
        filled = 0
        for f in key_fields:
            if self.metadata.get(f):
                filled += 1
                evidence.append(f"Metadata field '{f}' is populated.")
            else:
                gaps.append(f"Metadata field '{f}' is missing.")
                
        pct = (filled / len(key_fields)) * 100
        if pct < 30:
            score = 1
        elif pct < 60:
            score = 2
        elif pct < 85:
            score = 3
        else:
            score = 4
            
        rationale = f"Score {score}: {filled} out of {len(key_fields)} key metadata fields populated ({round(pct, 1)}%)."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_03_documentation.py": """from .base import BaseDomainScorer, DomainScoreResult

class DocumentationScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 3
    DOMAIN_NAME = "Documentation & User Guidance"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        has_dict = self.metadata.get("data_dictionary_uploaded", False)
        has_ethics = bool(self.metadata.get("ethics_approval_ref"))
        has_consent = bool(self.metadata.get("consent_type"))
        has_repo = bool(self.metadata.get("github_repo_url"))
        
        items = 0
        if has_dict:
            items += 1
            evidence.append("Data dictionary uploaded.")
        else:
            gaps.append("Data dictionary missing.")
            
        if has_ethics:
            items += 1
            evidence.append(f"Ethics approval reference provided: {self.metadata.get('ethics_approval_ref')}")
        else:
            gaps.append("Ethics approval reference missing.")
            
        if has_consent:
            items += 1
            evidence.append(f"Consent type documented: {self.metadata.get('consent_type')}")
        else:
            gaps.append("Consent protocol description missing.")
            
        if has_repo:
            items += 1
            evidence.append(f"Public code repository provided: {self.metadata.get('github_repo_url')}")
        else:
            gaps.append("Code repository URL missing.")
            
        score = items
        rationale = f"Score {score}: Found {items} of 4 core documentation components."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_04_representativeness.py": """from .base import BaseDomainScorer, DomainScoreResult

class RepresentativenessScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 4
    DOMAIN_NAME = "Population Representativeness"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        geo = self.metadata.get("geographic_coverage")
        sites = self.metadata.get("num_sites")
        sex = self.metadata.get("sex_distribution")
        
        if not geo:
            gaps.append("Geographic coverage not declared.")
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=1,
                rationale="Geographic coverage not declared. Minimum representativeness score.",
                evidence_items=evidence,
                gaps=gaps,
                confidence="Low"
            )
            
        evidence.append(f"Geographic coverage declared: {geo}")
        
        sites_val = int(sites) if sites else 1
        if sites_val > 1:
            evidence.append(f"Multi-site study: {sites_val} sites.")
        else:
            gaps.append("Single site study or sites count not provided.")
            
        if sex:
            evidence.append(f"Sex distribution reported: {sex}")
        else:
            gaps.append("Sex distribution not reported.")
            
        if geo == "national" and sites_val >= 5 and sex:
            score = 4
        elif geo in ["state", "region"] and sites_val >= 3:
            score = 3
        elif geo in ["district", "taluk", "village"] or sites_val > 1:
            score = 2
        else:
            score = 1
            
        rationale = f"Score {score}: Geographic coverage is {geo} with {sites_val} sites."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_05_interoperability.py": """from .base import BaseDomainScorer, DomainScoreResult

class InteroperabilityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 5
    DOMAIN_NAME = "Data Structure & Interoperability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        data_signals = 3
        meta_signals = 1
        
        comp = self.profile.get("completeness", {})
        overall_pct = comp.get("overall_pct", 100.0)
        standards = self.profile.get("standards_detected", {})
        icd_present = standards.get("icd_codes_present", False)
        fhir_present = standards.get("fhir_structure", False)
        snomed_present = standards.get("snomed_codes_present", False)
        loinc_present = standards.get("loinc_codes_present", False)
        
        evidence.append(f"Overall cell completeness: {overall_pct}%")
        
        if overall_pct < 50.0:
            gaps.append("Extremely low data completeness (<50%).")
            score = 0
        elif overall_pct < 75.0:
            gaps.append("Low data completeness (<75%).")
            score = 1
        elif overall_pct < 90.0:
            gaps.append("Moderate data completeness (<90%).")
            score = 2
        else:
            score = 3
            if icd_present or fhir_present or snomed_present or loinc_present:
                evidence.append("Ontology standards (ICD/SNOMED/LOINC/FHIR) detected in data columns.")
                score = 4
            else:
                gaps.append("No medical coding standards detected in data.")
                
        confidence = self._determine_confidence(data_signals, meta_signals)
        rationale = f"Score {score}: Cell completeness is {overall_pct}%."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence=confidence
        )
""",

    "domain_06_ai_readiness.py": """from .base import BaseDomainScorer, DomainScoreResult

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
            evidence.append("Data dictionary and pipeline script present.")
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
""",

    "domain_07_privacy.py": """from .base import BaseDomainScorer, DomainScoreResult

class PrivacyScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 7
    DOMAIN_NAME = "Privacy & Identifiability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        data_signals = 2
        meta_signals = 3
        
        pii = self.profile.get("pii_scan", {})
        direct_ids = pii.get("direct_identifiers_detected", False)
        
        if direct_ids:
            gaps.append("Direct identifiers (name, phone, GPS or ID) detected in column headers.")
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=0,
                rationale="Direct PII identifiers found in dataset.",
                evidence_items=evidence,
                gaps=gaps,
                confidence="High"
            )
            
        evidence.append("No direct identifiers found in dataset.")
        
        deident = self.metadata.get("deidentification_method")
        dp_applied = self.metadata.get("differential_privacy_applied", False)
        k_val = self.metadata.get("k_anonymity_value")
        
        if not deident:
            gaps.append("No de-identification method declared.")
            score = 1
        elif dp_applied:
            evidence.append("Differential Privacy applied.")
            score = 4
        elif k_val and int(k_val) >= 10:
            evidence.append(f"k-anonymity verified with k={k_val}.")
            score = 4
        elif k_val and int(k_val) >= 5:
            evidence.append(f"k-anonymity verified with k={k_val}.")
            score = 3
        else:
            evidence.append(f"De-identification applied: {deident}")
            score = 2
            
        confidence = self._determine_confidence(data_signals, meta_signals)
        rationale = f"Score {score}: Direct identifiers absent. De-identification is {deident or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence=confidence
        )
""",

    "domain_08_security.py": """from .base import BaseDomainScorer, DomainScoreResult

class SecurityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 8
    DOMAIN_NAME = "Security & Access Governance"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        control = self.metadata.get("access_control_method")
        dua = self.metadata.get("dua_required", False)
        
        if not control:
            gaps.append("No access control method documented.")
            score = 1
        elif "public" in control.lower() or "open" in control.lower():
            evidence.append("Public access control.")
            score = 2
        elif dua and ("request" in control.lower() or "approval" in control.lower()):
            evidence.append("Approval-based access with Data Use Agreement (DUA) requirement.")
            score = 3
            if "role" in control.lower() or "secure" in control.lower():
                evidence.append("Role-based access controls (RBAC) enforced.")
                score = 4
        else:
            evidence.append(f"Access control documented: {control}")
            score = 2
            
        rationale = f"Score {score}: Access control is {control or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_09_provenance.py": """from .base import BaseDomainScorer, DomainScoreResult

class ProvenanceScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 9
    DOMAIN_NAME = "Provenance & Workflow Transparency"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        pipeline = self.metadata.get("provenance_pipeline_available", False)
        changelog = self.metadata.get("changelog_provided", False)
        ver = self.metadata.get("version_format")
        
        if not pipeline and not changelog and not ver:
            gaps.append("No provenance metadata provided.")
            score = 1
        elif ver and not pipeline:
            evidence.append(f"Version format defined: {ver}")
            score = 2
        elif pipeline and not changelog:
            evidence.append("Preprocessing data lineage pipeline documented.")
            score = 3
        else:
            evidence.append("Workflow pipeline, version history, and changelog fully available.")
            score = 4
            
        rationale = f"Score {score}: Pipeline={pipeline}, Changelog={changelog}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_10_ethics.py": """from .base import BaseDomainScorer, DomainScoreResult

class EthicsScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 10
    DOMAIN_NAME = "Ethical & Social Accountability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        ethics = self.metadata.get("ethics_approval_ref")
        consent = self.metadata.get("consent_type")
        equity = self.metadata.get("equity_analysis_performed", False)
        community = self.metadata.get("community_engagement", False)
        redress = self.metadata.get("redressal_mechanism_exists", False)
        
        if not ethics and not consent:
            gaps.append("Ethics approval reference and consent protocol missing.")
            score = 0
        elif ethics and not consent:
            evidence.append(f"Ethics approval reference: {ethics}")
            gaps.append("Consent protocol not described.")
            score = 1
        elif ethics and consent:
            evidence.append(f"Ethics approval reference: {ethics}")
            evidence.append(f"Consent type: {consent}")
            score = 2
            
            if equity or community:
                evidence.append(f"Social accountability (equity={equity}, community={community}) performed.")
                score = 3
                if redress:
                    evidence.append("Grievance redressal mechanism exists.")
                    score = 4
            else:
                gaps.append("No equity analysis or community engagement reported.")
        else:
            score = 1
            
        rationale = f"Score {score}: Ethics approval={bool(ethics)}, Consent={consent}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_11_synthetic.py": """from .base import BaseDomainScorer, DomainScoreResult

class SyntheticDataScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 11
    DOMAIN_NAME = "Synthetic / Simulated Data"

    def score(self) -> DomainScoreResult:
        pct = self.metadata.get("synthetic_data_pct")
        
        if pct is None or float(pct) == 0.0:
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=None,
                rationale="Dataset contains no synthetic or simulated data. Domain excluded from CQI calculation.",
                evidence_items=[],
                gaps=[],
                confidence="Low",
                not_applicable=True
            )
            
        evidence = [f"Synthetic data ratio: {pct}%"]
        gaps = []
        
        utility = self.metadata.get("synthetic_utility_evaluated", False)
        privacy = self.metadata.get("synthetic_privacy_tested", False)
        
        if not utility and not privacy:
            gaps.append("Synthetic utility and privacy not evaluated.")
            score = 1
        elif utility and not privacy:
            evidence.append("Synthetic utility evaluated.")
            gaps.append("Synthetic privacy leakage not tested.")
            score = 2
        elif utility and privacy:
            evidence.append("Synthetic utility and privacy tested.")
            score = 3
            if float(pct) >= 50.0:
                evidence.append("Majority synthetic dataset (>50%).")
                score = 4
        else:
            score = 1
            
        rationale = f"Score {score}: Synthetic pct={pct}%, utility={utility}, privacy={privacy}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_12_stewardship.py": """from .base import BaseDomainScorer, DomainScoreResult

class StewardshipScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 12
    DOMAIN_NAME = "Stewardship & Governance"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        steward = self.metadata.get("named_steward_exists", False)
        dpdp = self.metadata.get("dpdp_compliance_status")
        
        if not steward:
            gaps.append("No named data steward or custodian designated.")
            score = 1
        else:
            evidence.append("Named data steward designated.")
            if dpdp == "compliant":
                evidence.append("DPDP compliant status verified.")
                score = 4
            elif dpdp == "under_review":
                evidence.append("DPDP compliance under review.")
                score = 3
            else:
                gaps.append("DPDP compliance status not verified or non-compliant.")
                score = 2
                
        rationale = f"Score {score}: steward={steward}, DPDP={dpdp}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_13_model_linkage.py": """from .base import BaseDomainScorer, DomainScoreResult

class ModelLinkageScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 13
    DOMAIN_NAME = "Model Linkage Integrity"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        models = self.metadata.get("linked_model_ids")
        
        if models is None:
            gaps.append("No model linkage IDs provided.")
            score = 1
        elif isinstance(models, list) and len(models) == 0:
            gaps.append("Linked models list is empty.")
            score = 2
        else:
            evidence.append(f"Linked model IDs: {models}")
            score = 3
            if isinstance(models, dict) or (isinstance(models, list) and len(models) > 1):
                evidence.append("Multiple models/configurations linked.")
                score = 4
                
        rationale = f"Score {score}: Model linkage is {models or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
""",

    "domain_14_sustainability.py": """from .base import BaseDomainScorer, DomainScoreResult

class SustainabilityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 14
    DOMAIN_NAME = "Environmental Sustainability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        fmt = self.profile.get("file", {}).get("format", "csv").lower()
        size = self.profile.get("file", {}).get("size_bytes", 0)
        
        if fmt == "parquet":
            evidence.append("Optimized binary column format (Parquet) reduces CPU cycles and storage size.")
            score = 3
        elif size < 10000000: # < 10MB
            evidence.append("Small file footprint reduces transmission and analysis carbon costs.")
            score = 3
        else:
            gaps.append("Large raw text file (CSV/XLSX) increases storage and compute footprint.")
            score = 2
            
        rationale = f"Score {score}: Sustainability assessed on size and file format."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Medium"
        )
""",

    "domain_15_curation.py": """from .base import BaseDomainScorer, DomainScoreResult

class CurationScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 15
    DOMAIN_NAME = "Continuous Curation & Feedback"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        repo = self.metadata.get("github_repo_url")
        changelog = self.metadata.get("changelog_provided", False)
        
        if not repo and not changelog:
            gaps.append("No active repository or version changelog provided.")
            score = 1
        elif repo and not changelog:
            evidence.append(f"Active code/data repository: {repo}")
            score = 2
        elif changelog and not repo:
            evidence.append("Changelog/updates documentation provided.")
            score = 3
        else:
            evidence.append("Active repository and detailed changelog provided.")
            score = 4
            
        rationale = f"Score {score}: Repo={bool(repo)}, Changelog={changelog}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
"""
}

# Create domains folder if missing
os.makedirs("backend/app/engine/domains", exist_ok=True)

# Write each file
for filename, code in domains_code.items():
    filepath = os.path.join("backend/app/engine/domains", filename)
    with open(filepath, "w") as f:
        f.write(code)
    print(f"Generated {filepath}")
