from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Literal
from datetime import date

class MetadataForm(BaseModel):
    dataset_name: str = Field(..., min_length=5)
    dataset_version: Optional[str] = Field(None, max_length=100)
    dataset_type: Literal["tabular", "imaging", "text", "multimodal"]
    study_type: Literal["RCT", "cohort", "cross_sectional", "registry", "observational", "case_control", "other"]
    target_population: str = Field(..., min_length=20)
    geographic_coverage: Literal["village", "taluk", "district", "state", "national", "multi_country"]
    
    age_range_min: Optional[int] = Field(None, ge=0, le=120)
    age_range_max: Optional[int] = Field(None, ge=0, le=120)
    sex_distribution: Optional[Literal["male_only", "female_only", "both", "not_specified"]] = "not_specified"
    num_sites: Optional[int] = Field(None, ge=1)
    
    collection_start_date: Optional[date] = None
    collection_end_date: Optional[date] = None
    
    annotation_methodology: Optional[str] = Field(None, min_length=50)
    num_annotators: Optional[int] = Field(None, ge=1)
    irr_method: Optional[str] = None
    irr_value: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    standards_used: Optional[str] = None
    ethics_approval_ref: Optional[str] = None
    consent_type: Optional[Literal["individual", "waiver", "community", "not_applicable"]] = "not_applicable"
    deidentification_method: Optional[str] = None
    
    differential_privacy_applied: bool = False
    dp_epsilon: Optional[float] = Field(None, gt=0.0)
    
    sensitivity_class: Literal["standard", "high_stigma", "critical"]
    persistent_identifier: Optional[str] = None
    license_type: Optional[str] = None
    synthetic_data_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    
    access_control_method: Optional[str] = None
    linked_model_ids: Optional[List[str]] = Field(default_factory=list)
    data_dictionary_uploaded: bool = False
    provenance_pipeline_available: bool = False
    github_repo_url: Optional[str] = None
    changelog_provided: bool = False
    version_format: Optional[Literal["semantic", "arbitrary", "none"]] = "none"
    sustainability_info_provided: bool = False
    feedback_mechanism_exists: bool = False
    
    aikosh_dataset_id: Optional[str] = None
    webhook_url: Optional[str] = None

    @model_validator(mode="after")
    def validate_dp_parameters(self) -> 'MetadataForm':
        if self.differential_privacy_applied and self.dp_epsilon is None:
            raise ValueError("dp_epsilon is required when differential_privacy_applied is True")
        return self

    @model_validator(mode="after")
    def validate_dates(self) -> 'MetadataForm':
        if self.collection_start_date and self.collection_end_date:
            if self.collection_end_date < self.collection_start_date:
                raise ValueError("collection_end_date must be on or after collection_start_date")
        return self
