> **Core Development Philosophy:** "Prioritize building a fully functional, secure, end-to-end integration skeleton (UI -> API -> Worker -> DB/S3 -> Polling) with mock scoring results first, ensuring pipeline stability and security before implementing complex calculation engines."

# Metadata Intake Form — Questionnaire Specification
# AIKosh Dataset Quality Evaluation Toolkit

---

**Document Version:** 1.0  
**Status:** Draft  
**Last Updated:** June 18, 2026  
**Prepared For:** AIKosh / IndiaAI Mission  
**References:** PRD v1.0 (Section 17.1, 18), TDD v1.0, OpenAPI Spec v1.0  
**Classification:** Internal Working Document

---

## Purpose of This Document

The Metadata Intake Form is the structured questionnaire shown to dataset custodians when they submit a health research dataset to the AIKosh Quality Toolkit. It collects information that cannot be inferred from the dataset file alone — context about how the data was collected, annotated, de-identified, governed, and documented.

**Why this form exists:** The dataset file (CSV, XLSX, etc.) tells the toolkit *what* the data contains. The form tells it *how* the data was created, who collected it, what protections were applied, and how it is managed. Without the form, Domains 1, 3, 4, 8, 9, 10, 12, 13, 14, and 15 cannot be scored at all, and Domains 2, 7, and 11 can only be partially scored.

**Important note on sourcing:** MIDAS 2.0 does not publicly release its exact questionnaire wording. Every question in this form has been reverse-engineered from the 15 MIDAS domain descriptions, MIDAS scoring criteria, and health data quality literature. Where a question maps directly to a confirmed MIDAS criterion, it is marked `[MIDAS-CONFIRMED]`. Where it is inferred, it is marked `[INFERRED]`.

---

## How to Read This Document

Each question is documented with:

- **Question text** — exactly as shown to the user
- **Field name** — the API field this maps to in `MetadataForm`
- **Type** — text / dropdown / number / date / boolean / file upload
- **Required** — whether the form blocks submission without an answer
- **Domains scored** — which MIDAS domains this answer feeds into
- **Help text** — tooltip or guidance shown alongside the question
- **Options** — for dropdown/select questions, the exact options
- **Conditional** — whether this question appears only if a prior answer triggers it
- **Validation** — rules enforced before submission
- **Source** — `[MIDAS-CONFIRMED]` or `[INFERRED]`

---

## Form Structure — Section Overview

The form is divided into 8 sections, shown as steps in a multi-step wizard:

| Section | Title | Questions | Mandatory |
|---|---|---|---|
| A | Dataset Basics | Q1–Q5 | Yes |
| B | Study & Population | Q6–Q12 | Yes |
| C | Annotation & Labelling | Q13–Q17 | Conditional |
| D | Data Standards & Interoperability | Q18–Q20 | Yes |
| E | Privacy & De-identification | Q21–Q27 | Yes |
| F | Ethics, Consent & Governance | Q28–Q36 | Yes |
| G | AI Readiness, Models & Curation | Q37–Q43 | Partial |
| H | Attachments | Q44–Q48 | Partial |

Progress bar shown at top. Custodian can save and return — form state preserved for 30 days.

---

## Section A — Dataset Basics

*These questions identify the dataset and establish its fundamental characteristics. They affect Domains 2, 3, 5, 6, and 15.*

---

### Q1 — Dataset Name

**Question text:** What is the name of this dataset?

**Field name:** `dataset_name`  
**Type:** Text (single line)  
**Required:** Yes  
**Max length:** 500 characters  
**Domains scored:** 2 (Metadata Completeness), 3 (Documentation)  
**Help text:** Use a descriptive, unique name. Avoid abbreviations that are not widely recognised. Example: *"Multi-site Pulmonary TB Cohort Study — India 2019–2023"*  
**Validation:** Non-empty. At least 5 characters.  
**Source:** [MIDAS-CONFIRMED]

---

### Q2 — Dataset Version

**Question text:** What is the version of this dataset?

**Field name:** `dataset_version`  
**Type:** Text (single line)  
**Required:** No  
**Domains scored:** 2 (Metadata Completeness), 15 (Continuous Curation & Feedback)  
**Help text:** Use semantic versioning if possible (e.g. `1.0.0`, `2.1.0`). If this is the first release, use `1.0.0`.  
**Validation:** None beyond max length (100 chars).  
**Source:** [INFERRED]

---

### Q3 — Dataset Type

**Question text:** What type of data does this dataset primarily contain?

**Field name:** `dataset_type`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Tabular` — Rows and columns (CSV, Excel, structured database export)
- `Imaging` — Medical images (X-rays, MRI, CT, pathology slides, DICOM)
- `Text` — Clinical notes, discharge summaries, free-text records
- `Multimodal` — Combination of two or more types above

**Domains scored:** 5 (Data Structure & Interoperability), 6 (AI / Analytics Readiness)  
**Help text:** Select the primary data type. If your dataset has both tabular records and associated images, select *Multimodal*.  
**Source:** [INFERRED]

---

### Q4 — Persistent Identifier

**Question text:** Does this dataset have a persistent identifier (DOI, accession number, or registry ID)?

**Field name:** `persistent_identifier`  
**Type:** Text (single line)  
**Required:** No  
**Domains scored:** 2 (Metadata Completeness)  
**Help text:** A persistent identifier ensures the dataset can be permanently cited and found. Examples: DOI (`10.5281/zenodo.1234567`), CTRI registration number, ICMR registry ID, or accession number from a data archive.  
**Validation:** If provided, must match DOI format (`10.XXXX/...`) or be a non-empty string.  
**Source:** [MIDAS-CONFIRMED]

---

### Q5 — License Type

**Question text:** Under what license is this dataset being shared?

**Field name:** `license_type`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `CC BY 4.0` — Attribution required; commercial use allowed
- `CC BY-NC 4.0` — Attribution required; no commercial use
- `CC BY-NC-ND 4.0` — Attribution required; no commercial use; no derivatives
- `CC BY-SA 4.0` — Attribution required; share-alike
- `Government Open Data License (India)` — GODL-India
- `Restricted — Data Use Agreement required` — Access only via signed DUA
- `Proprietary / Custom license` — Specify in the field below
- `Not yet decided`

**Domains scored:** 8 (Security & Access Governance), 12 (Stewardship & Governance)  
**Help text:** The license governs how others may use, share, and build upon this dataset. For datasets with privacy-sensitive health data, *Restricted* with a Data Use Agreement is recommended.  
**Conditional follow-up:** If `Proprietary / Custom license` selected → show text field: *"Please describe the license terms"*  
**Source:** [INFERRED]

---

## Section B — Study & Population

*These questions document the research context and population characteristics. They primarily feed Domain 4 (Population Representativeness) and Domain 3 (Documentation).*

---

### Q6 — Study Type

**Question text:** What type of health research study generated this dataset?

**Field name:** `study_type`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Randomised Controlled Trial (RCT)`
- `Cohort study (prospective or retrospective)`
- `Cross-sectional survey`
- `Case-control study`
- `Disease registry`
- `Epidemiological surveillance`
- `Biobank / specimen collection`
- `Observational study (other)`
- `Other` — with free-text field

**Domains scored:** 1 (Annotation Reliability), 4 (Population Representativeness)  
**Help text:** The study design affects how population representativeness and annotation reliability are assessed.  
**Source:** [MIDAS-CONFIRMED]

---

### Q7 — Target Population Description

**Question text:** Describe the target population this dataset represents.

**Field name:** `target_population`  
**Type:** Text (multi-line, up to 500 characters)  
**Required:** Yes  
**Domains scored:** 4 (Population Representativeness)  
**Help text:** Describe who was intended to be studied. Include disease/condition, age group, setting, and any inclusion/exclusion criteria. Example: *"Adults aged 18–65 with confirmed pulmonary tuberculosis attending RNTCP-registered DOTS centres across 14 districts in Maharashtra and Rajasthan."*  
**Validation:** Minimum 20 characters.  
**Source:** [MIDAS-CONFIRMED]

---

### Q8 — Geographic Coverage

**Question text:** What is the geographic level of data collection?

**Field name:** `geographic_coverage`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Village / Panchayat level`
- `Taluk / Block level`
- `District level`
- `State level`
- `National (multiple states)`
- `Multi-country`

**Domains scored:** 4 (Population Representativeness), PRS (Privacy-Risk Score)  
**Help text:** This affects both representativeness scoring and privacy risk assessment. Village-level data combined with rare conditions can significantly increase re-identification risk.  
**Source:** [MIDAS-CONFIRMED]

---

### Q9 — Number of Collection Sites

**Question text:** How many sites or facilities contributed data to this dataset?

**Field name:** `num_sites`  
**Type:** Number (integer)  
**Required:** No  
**Minimum:** 1  
**Domains scored:** 4 (Population Representativeness)  
**Help text:** A site is any distinct facility, hospital, clinic, field station, or geographic location where data was collected. Single-site datasets typically score lower on representativeness.  
**Source:** [MIDAS-CONFIRMED]

---

### Q10 — Age Range of Study Subjects

**Question text:** What is the age range of subjects in this dataset?

**Field names:** `age_range_min`, `age_range_max`  
**Type:** Two number fields (min age, max age)  
**Required:** No  
**Domains scored:** 4 (Population Representativeness)  
**Help text:** Enter the minimum and maximum age in years. If the dataset includes newborns, enter 0. If there is no upper age limit, enter 120.  
**Validation:** `age_range_min` ≤ `age_range_max`. Both between 0 and 120.  
**Source:** [MIDAS-CONFIRMED]

---

### Q11 — Sex Distribution of Subjects

**Question text:** Which sexes are represented in the dataset?

**Field name:** `sex_distribution`  
**Type:** Dropdown (single select)  
**Required:** No  
**Options:**
- `Both male and female subjects`
- `Male subjects only`
- `Female subjects only`
- `Not specified / not recorded`

**Domains scored:** 4 (Population Representativeness)  
**Help text:** Datasets with only one sex represented will score lower on representativeness unless the research question specifically concerns that sex (e.g. cervical cancer, prostate conditions).  
**Source:** [MIDAS-CONFIRMED]

---

### Q12 — Data Collection Period

**Question text:** What was the data collection period for this dataset?

**Field names:** `collection_start_date`, `collection_end_date`  
**Type:** Two date pickers (start date, end date)  
**Required:** No  
**Format:** `DD/MM/YYYY`  
**Domains scored:** 3 (Documentation & User Guidance), 9 (Provenance & Workflow Transparency)  
**Help text:** The collection period helps users assess temporal relevance and potential distribution shift when using the dataset for AI training.  
**Validation:** End date must be on or after start date. Neither date can be in the future.  
**Source:** [INFERRED]

---

## Section C — Annotation & Labelling

*This section is shown only if the dataset contains labelled or annotated data. It feeds Domain 1 (Annotation / Labelling Reliability).*

---

### Q13 — Does This Dataset Contain Annotated or Labelled Data?

**Question text:** Does this dataset include labels, annotations, or ground-truth classifications created by human experts or trained readers?

**Field name:** *(gate question — controls visibility of Q14–Q17)*  
**Type:** Radio button (Yes / No)  
**Required:** Yes  
**Domains scored:** 1 (Annotation / Labelling Reliability)  
**Help text:** Examples of annotated data: radiologist-labelled X-rays, pathologist-graded biopsy images, clinician-coded diagnoses, expert-reviewed clinical event adjudications.  
**Conditional:** If `No` → skip to Section D. Domain 1 scored 0 unless annotation methodology described elsewhere.  
**Source:** [MIDAS-CONFIRMED]

---

### Q14 — Annotation Methodology

**Question text:** How were the annotations or labels created? Describe the annotation process.

**Field name:** `annotation_methodology`  
**Type:** Text (multi-line, up to 1000 characters)  
**Required:** Yes (if Q13 = Yes)  
**Domains scored:** 1 (Annotation / Labelling Reliability)  
**Help text:** Describe: who performed annotations (qualifications), what tool or platform was used, what guidelines annotators followed, and how disagreements were resolved. Example: *"Two radiologists with ≥5 years chest X-ray experience independently annotated each image using CAD4TB v6. Disagreements resolved by consensus with a third senior radiologist."*  
**Validation:** Minimum 50 characters if provided.  
**Source:** [MIDAS-CONFIRMED]

---

### Q15 — Annotator Qualifications

**Question text:** What were the qualifications of the annotators?

**Field name:** *(captured within `annotation_methodology` or as structured sub-field)*  
**Type:** Dropdown (single select)  
**Required:** Yes (if Q13 = Yes)  
**Options:**
- `Medical specialists (e.g. radiologists, pathologists, senior clinicians)`
- `General medical practitioners`
- `Trained research assistants with domain-specific training`
- `Lay annotators with basic training`
- `Automated tool only (no human annotators)`
- `Mixed — multiple qualification levels`

**Domains scored:** 1 (Annotation / Labelling Reliability)  
**Help text:** Annotator qualification directly affects the reliability of labels. Specialist-annotated datasets score higher on Domain 1.  
**Source:** [MIDAS-CONFIRMED]

---

### Q16 — Number of Annotators

**Question text:** How many independent annotators labelled each data item?

**Field name:** `num_annotators`  
**Type:** Number (integer)  
**Required:** Yes (if Q13 = Yes)  
**Minimum:** 1  
**Domains scored:** 1 (Annotation / Labelling Reliability)  
**Help text:** Datasets where each item was independently annotated by at least 2 annotators allow inter-rater reliability to be measured, which is required for scores of 3 or 4 on Domain 1.  
**Source:** [MIDAS-CONFIRMED]

---

### Q17 — Inter-Rater Reliability

**Question text:** Was inter-rater reliability (IRR) measured? If yes, provide the method and value.

**Field names:** `irr_method`, `irr_value`  
**Type:** Two fields — dropdown (method) + number (value)  
**Required:** No (if Q13 = Yes, strongly recommended)  
**IRR method options:**
- `Cohen's Kappa`
- `Fleiss' Kappa (for ≥3 raters)`
- `Intraclass Correlation Coefficient (ICC)`
- `Krippendorff's Alpha`
- `Percentage agreement`
- `Other` — with free-text

**IRR value:** Number between 0.00 and 1.00  
**Domains scored:** 1 (Annotation / Labelling Reliability)  
**Help text:** IRR measures how consistently different annotators produced the same labels. A Cohen's Kappa of ≥ 0.6 is considered adequate; ≥ 0.8 is considered excellent. If IRR was not measured, Domain 1 cannot score above 2.  
**Validation:** IRR value must be between 0 and 1 if provided.  
**Source:** [MIDAS-CONFIRMED — thresholds inferred from health informatics literature]

---

## Section D — Data Standards & Interoperability

*These questions assess whether the dataset follows recognised health data standards. They feed Domain 5 (Data Structure & Interoperability).*

---

### Q18 — Health Data Standards Used

**Question text:** Which health data standards or coding systems does this dataset use?

**Field name:** `standards_used`  
**Type:** Multi-select checkboxes  
**Required:** Yes  
**Options:**
- `ICD-10 / ICD-11` — International Classification of Diseases
- `SNOMED CT` — Systematised Nomenclature of Medicine
- `LOINC` — Logical Observation Identifiers Names and Codes
- `FHIR R4 / R5` — HL7 Fast Healthcare Interoperability Resources
- `HL7 v2 / v3` — Health Level 7 messaging
- `WHO-ART` — WHO Adverse Reaction Terminology
- `MedDRA` — Medical Dictionary for Regulatory Activities
- `Custom / Internal coding system`
- `No standard applied`

**Domains scored:** 5 (Data Structure & Interoperability)  
**Help text:** Using recognised standards allows interoperability with other datasets and systems, and improves AI model generalisability. If you use a custom coding system, the dataset will score lower on interoperability.  
**Source:** [MIDAS-CONFIRMED]

---

### Q19 — Data Dictionary

**Question text:** Is a data dictionary available for this dataset?

**Field name:** `data_dictionary_uploaded`  
**Type:** Radio button (Yes / No / In progress)  
**Required:** Yes  
**Domains scored:** 3 (Documentation & User Guidance), 5 (Data Structure & Interoperability)  
**Help text:** A data dictionary defines every column/variable in the dataset — its name, data type, allowed values, units, and meaning. Without a data dictionary, Dataset users cannot reliably interpret the data.  
**Conditional:** If `Yes` → Q44 (attachment upload in Section H) prompted.  
**Source:** [MIDAS-CONFIRMED]

---

### Q20 — Automated Data Quality Checks

**Question text:** Were automated data quality checks applied to this dataset before release?

**Field name:** *(captured as structured sub-field in metadata)*  
**Type:** Multi-select checkboxes  
**Required:** No  
**Options:**
- `Completeness checks (missing value detection)`
- `Range/plausibility checks (e.g. age > 0, BMI < 100)`
- `Referential integrity checks (e.g. site IDs exist in lookup)`
- `Duplicate record detection`
- `Schema conformance validation`
- `None of the above`

**Domains scored:** 5 (Data Structure & Interoperability)  
**Help text:** Automated DQ checks improve confidence in data quality and are required for a score of 3 or above on Domain 5.  
**Source:** [MIDAS-CONFIRMED]

---

## Section E — Privacy & De-identification

*This is the most critical section for determining the Privacy-Risk Score (PRS) and whether the dataset can be released as Open, Controlled, or Restricted.*

---

### Q21 — Data Sensitivity Class

**Question text:** Does this dataset relate to any of the following sensitive categories?

**Field name:** `sensitivity_class`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Standard — General health/epidemiological data with no special sensitivity` → multiplier 1.0×
- `High Stigma / Personal Impact — Includes data on TB, HIV/AIDS, STIs, reproductive health, mental health, substance use, genomic data, caste/tribe identity, domestic violence, or disability` → multiplier 1.5×
- `Critical / Safety-Sensitive — Includes forensic data, data on detainees or prisoners, conflict-zone populations, tribal GPS coordinates, refugee or asylum-seeker data, or protest-related data` → multiplier 2.0×

**Domains scored:** PRS (Privacy-Risk Score), 7 (Privacy & Identifiability), Release Classification  
**Help text:** This classification directly affects the Privacy-Risk Score. High-stigma and critical datasets have higher re-identification risk because disclosure could cause serious harm to individuals. If unsure, select the higher category.  
**Source:** [MIDAS-CONFIRMED — from public MIDAS Lite Version Annexure I]

---

### Q22 — Direct Identifiers

**Question text:** Does this dataset contain any direct personal identifiers?

**Field name:** *(used to cross-validate profiler output)*  
**Type:** Multi-select checkboxes  
**Required:** Yes  
**Options:**
- `Full name or partial name`
- `Phone number`
- `Email address`
- `National ID (Aadhaar, PAN, Voter ID, Passport)`
- `Full date of birth (day + month + year)`
- `GPS coordinates or precise location`
- `Photograph or biometric data`
- `Hospital or patient record number`
- `None of the above — all direct identifiers have been removed`

**Domains scored:** 7 (Privacy & Identifiability), PRS  
**Help text:** Direct identifiers are data elements that can identify an individual on their own. If any of the above are present in your dataset, it cannot be released publicly and will receive the maximum baseline risk score.  
**Validation:** At least one option must be selected.  
**Source:** [MIDAS-CONFIRMED]

---

### Q23 — De-identification Method

**Question text:** What de-identification method was applied to this dataset?

**Field name:** `deidentification_method`  
**Type:** Dropdown (single select) + optional free-text description  
**Required:** Yes  
**Options:**
- `HIPAA Safe Harbor — All 18 identifiers removed per HIPAA Safe Harbor method`
- `HIPAA Expert Determination — Qualified expert certified risk < 0.05`
- `k-Anonymity — Each combination of quasi-identifiers shared by ≥ k individuals`
- `l-Diversity — k-anonymity extended to protect sensitive attribute diversity`
- `Differential Privacy — Statistical noise added with documented epsilon`
- `Pseudonymisation — Identifiers replaced with pseudonyms; mapping table retained`
- `Generalisation / Suppression — Values generalised to broader categories`
- `No de-identification applied`
- `Other` — with free-text field

**Domains scored:** 7 (Privacy & Identifiability), PRS  
**Help text:** De-identification methods vary in strength. Differential Privacy and formal k-Anonymity provide stronger guarantees than simple identifier removal. Documenting the method is required for a score of 3 on Domain 7.  
**Source:** [MIDAS-CONFIRMED]

---

### Q24 — k-Anonymity Value

**Question text:** If k-Anonymity was applied, what is the value of k?

**Field name:** *(sub-field of deidentification metadata)*  
**Type:** Number (integer)  
**Required:** No — shown only if Q23 = `k-Anonymity`  
**Minimum:** 2  
**Domains scored:** 7 (Privacy & Identifiability)  
**Help text:** k-Anonymity of 5 or more is required for Domain 7 to score 4. A value of 2 or 3 provides weaker protection.  
**Conditional:** Shown only if Q23 = `k-Anonymity` or `l-Diversity`  
**Source:** [MIDAS-CONFIRMED]

---

### Q25 — Differential Privacy Parameters

**Question text:** Was Differential Privacy applied? If yes, what is the epsilon (ε) value?

**Field names:** `differential_privacy_applied`, `dp_epsilon`  
**Type:** Radio button (Yes / No) + number field  
**Required:** No — number field shown only if `Yes`  
**Domains scored:** 7 (Privacy & Identifiability), PRS  
**Help text:** Differential Privacy adds calibrated mathematical noise to data, providing a formal privacy guarantee. The epsilon (ε) value controls the privacy-utility trade-off — lower epsilon means stronger privacy. Must be a positive number. Typical values range from 0.1 (strong) to 10.0 (weak). The toolkit uses the formula: `PRS_baseline = min(100, 20 × ε)` to compute risk.  
**Validation:** `dp_epsilon` must be > 0 if `differential_privacy_applied` is `true`.  
**Source:** [MIDAS-CONFIRMED — formula from public MIDAS PRS specification]

---

### Q26 — Quasi-Identifier Granularity

**Question text:** After de-identification, at what level of detail are the following quasi-identifiers retained?

**Field name:** *(structured sub-fields used for PRS baseline computation)*  
**Type:** Two dropdown fields (one for location, one for date/time)  
**Required:** Yes  

**Location granularity:**
- `Village / Panchayat (most specific)`
- `Taluk / Block`
- `District`
- `State`
- `National (country only) or removed`

**Temporal granularity (date of events):**
- `Exact date (day + month + year) (most specific)`
- `Month and year only`
- `Year only`
- `Date removed or replaced with age/duration`

**Domains scored:** 7 (Privacy & Identifiability), PRS  
**Help text:** Fine-grained location (village) combined with rare conditions can make individuals re-identifiable even without direct identifiers. The toolkit uses location and temporal granularity to estimate baseline re-identification risk.  
**Source:** [MIDAS-CONFIRMED — granularity levels from MIDAS PRS risk table]

---

### Q27 — Rare Condition Flag

**Question text:** Does this dataset relate to a rare disease, rare condition, or a very small patient population (fewer than 100 individuals per location)?

**Field name:** *(sub-field used for PRS baseline computation)*  
**Type:** Radio button (Yes / No / Unsure)  
**Required:** Yes  
**Domains scored:** 7 (Privacy & Identifiability), PRS  
**Help text:** If the condition is rare, even generalised location data (e.g. district-level) may be sufficient to identify individuals in the dataset. This increases the baseline privacy risk score.  
**Source:** [MIDAS-CONFIRMED — rare condition flag from MIDAS PRS Step 1 table]

---

## Section F — Ethics, Consent & Governance

*These questions cover ethics approval, consent processes, access governance, and organisational stewardship. They feed Domains 8, 10, and 12.*

---

### Q28 — Ethics Approval

**Question text:** Has this dataset received ethics approval from an Institutional Ethics Committee (IEC) or Institutional Review Board (IRB)?

**Field name:** `ethics_approval_ref`  
**Type:** Radio button (Yes / No / Pending) + text field for reference number  
**Required:** Yes  
**Domains scored:** 10 (Ethical & Social Accountability)  
**Help text:** Ethics approval is required for health research datasets. Without it, the dataset cannot score above 0 on Domain 10 and cannot be classified as Open.  
**Conditional follow-up:** If `Yes` → show text field: *"Please enter the IEC/IRB reference number (e.g. ICMR/IEC/2020/0087)"*  
**Source:** [MIDAS-CONFIRMED]

---

### Q29 — Consent Type

**Question text:** What type of consent was obtained from study participants?

**Field name:** `consent_type`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Individual written informed consent`
- `Individual verbal informed consent with documentation`
- `Waiver of consent granted by ethics committee`
- `Community consent (for community-level data)`
- `Not applicable (dataset is fully anonymised aggregate data)`

**Domains scored:** 7 (Privacy & Identifiability), 10 (Ethical & Social Accountability)  
**Help text:** Informed individual consent is the gold standard. Waiver of consent or community consent is acceptable with ethics committee approval but will be noted in the quality assessment.  
**Source:** [MIDAS-CONFIRMED]

---

### Q30 — Equity Analysis

**Question text:** Was a bias or equity analysis performed on this dataset to assess representation across demographic groups?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No / Planned)  
**Required:** Yes  
**Domains scored:** 10 (Ethical & Social Accountability)  
**Help text:** An equity analysis checks whether the dataset is representative across age groups, sex, socioeconomic status, geographic regions, and marginalised communities. Required for Domain 10 to score 3 or above.  
**Conditional follow-up:** If `Yes` → show text field: *"Briefly describe the findings or provide a reference to the analysis"*  
**Source:** [MIDAS-CONFIRMED]

---

### Q31 — Community / Stakeholder Engagement

**Question text:** Were the communities or populations whose data is in this dataset engaged in the research design, data collection, or governance process?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No / Not applicable)  
**Required:** Yes  
**Domains scored:** 10 (Ethical & Social Accountability)  
**Help text:** Community engagement in health research improves trust and data relevance. Evidence of engagement (e.g. community advisory boards, patient representatives, ASHA workers in design) contributes to a score of 4 on Domain 10.  
**Source:** [MIDAS-CONFIRMED]

---

### Q32 — Redressal Mechanism

**Question text:** Is there a mechanism for individuals or communities to raise concerns, request corrections, or withdraw consent related to this dataset?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No)  
**Required:** Yes  
**Domains scored:** 10 (Ethical & Social Accountability)  
**Help text:** A redressal mechanism (e.g. contact email, ombudsman, formal complaint process) demonstrates accountability and is required for the highest score on Domain 10.  
**Source:** [MIDAS-CONFIRMED]

---

### Q33 — Access Control Method

**Question text:** How is access to this dataset controlled?

**Field name:** `access_control_method`  
**Type:** Dropdown (single select) + optional free text  
**Required:** Yes  
**Options:**
- `Publicly downloadable — no access controls`
- `Login / registration required on a platform`
- `Formal access request process (application and approval)`
- `Data Use Agreement (DUA) required — verified user identity`
- `Controlled access via secure data enclave`
- `Restricted — available only to named collaborators`

**Domains scored:** 8 (Security & Access Governance)  
**Help text:** Stronger access controls receive higher scores on Domain 8. Datasets with high PRS bands should implement at minimum a Data Use Agreement.  
**Source:** [INFERRED]

---

### Q34 — Data Use Agreement

**Question text:** Is a formal Data Use Agreement (DUA) required to access this dataset?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No)  
**Required:** Yes  
**Domains scored:** 8 (Security & Access Governance)  
**Help text:** A DUA specifies how the data may be used, shared, and protected. It is required for Domain 8 to score 3 or above.  
**Source:** [MIDAS-CONFIRMED]

---

### Q35 — Named Data Steward

**Question text:** Is there a named individual or team responsible for the stewardship of this dataset?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No)  
**Required:** Yes  
**Domains scored:** 12 (Stewardship & Governance)  
**Help text:** A named data steward is responsible for answering queries, managing access, handling incidents, and ensuring ongoing compliance. Without a named steward, the dataset cannot score above 1 on Domain 12.  
**Conditional follow-up:** If `Yes` → show text field: *"Name and role of the data steward (e.g. Dr. Ananya Sharma, Principal Investigator, AIIMS Delhi)"*  
**Source:** [MIDAS-CONFIRMED]

---

### Q36 — DPDP Act Compliance

**Question text:** Has this dataset been assessed for compliance with India's Digital Personal Data Protection (DPDP) Act 2023?

**Field name:** *(boolean sub-field)*  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Yes — fully assessed and compliant`
- `Yes — assessed; minor gaps being addressed`
- `In progress`
- `No — not yet assessed`
- `Not applicable (dataset contains no personal data)`

**Domains scored:** 12 (Stewardship & Governance)  
**Help text:** The DPDP Act 2023 governs the processing of personal digital data in India. Health research datasets containing individual-level data must comply with its provisions regarding consent, data minimisation, and security.  
**Source:** [INFERRED — derived from MIDAS Domain 12 governance requirement + DPDP Act 2023]

---

## Section G — AI Readiness, Models & Curation

*These questions cover AI/ML readiness, linked models, environmental sustainability, and versioning. They feed Domains 6, 11, 13, 14, and 15.*

---

### Q37 — Synthetic Data

**Question text:** Does this dataset contain any synthetic or simulated data?

**Field name:** `synthetic_data_pct`  
**Type:** Radio button (Yes / No) + number field (percentage)  
**Required:** Yes  
**Options (radio):** `Yes` / `No`  
**If Yes:** Show number field: *"What percentage of the dataset is synthetic? (0–100)"*  
**Domains scored:** 11 (Synthetic / Simulated Data)  
**Help text:** Synthetic data is artificially generated to mimic real data — for example, generated using GANs or statistical simulation. If your dataset contains any synthetic records, Domain 11 will be scored. If none, Domain 11 is excluded from the quality calculation.  
**Validation:** Percentage must be between 0.01 and 100 if `Yes` selected.  
**Source:** [MIDAS-CONFIRMED]

---

### Q38 — Synthetic Data Utility Evaluation

**Question text:** If synthetic data is present, was its utility formally evaluated against the real data?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No / Not applicable)  
**Required:** Yes (if Q37 = Yes)  
**Domains scored:** 11 (Synthetic / Simulated Data)  
**Help text:** Utility evaluation measures how well the synthetic data preserves the statistical properties of the real data (e.g. correlation structure, marginal distributions). Required for Domain 11 to score above 1.  
**Conditional:** Shown only if Q37 = `Yes`  
**Source:** [MIDAS-CONFIRMED]

---

### Q39 — Privacy Testing of Synthetic Data

**Question text:** If synthetic data is present, was its privacy formally tested (e.g. membership inference, attribute inference)?

**Field name:** *(boolean sub-field)*  
**Type:** Radio button (Yes / No / Not applicable)  
**Required:** Yes (if Q37 = Yes)  
**Domains scored:** 11 (Synthetic / Simulated Data)  
**Help text:** Synthetic data can still leak private information about the individuals in the training data. Formal privacy tests such as membership inference attacks assess this risk. Required for Domain 11 to score 3 or above.  
**Conditional:** Shown only if Q37 = `Yes`  
**Source:** [MIDAS-CONFIRMED]

---

### Q40 — Linked AI Models

**Question text:** Are there any AI or machine learning models that were trained on this dataset and released publicly?

**Field name:** `linked_model_ids`  
**Type:** Radio button (Yes / No) + repeating text field for model IDs  
**Required:** Yes  
**Domains scored:** 13 (Model Linkage Integrity)  
**Help text:** If models trained on this dataset have been released (on AIKosh, HuggingFace, or elsewhere), link them here. This enables users to trace the dataset–model relationship. If no models have been released, Domain 13 will receive a neutral score.  
**Conditional follow-up:** If `Yes` → show repeating field: *"Enter model ID or URL (e.g. AIKosh model ID, HuggingFace model path)"* — up to 10 entries  
**Source:** [MIDAS-CONFIRMED]

---

### Q41 — Environmental Sustainability Information

**Question text:** Has the energy or carbon footprint of storing and processing this dataset been estimated or measured?

**Field name:** `sustainability_info_provided`  
**Type:** Dropdown (single select)  
**Required:** Yes  
**Options:**
- `Yes — carbon footprint formally estimated or measured`
- `Yes — energy usage estimated`
- `Storage optimisation applied (compression, deduplication)`
- `Hosted on certified green infrastructure`
- `No — not yet assessed`

**Domains scored:** 14 (Environmental Sustainability)  
**Help text:** Environmental sustainability is an emerging consideration in responsible data sharing. Datasets stored on green infrastructure or with documented carbon footprints score higher on Domain 14. This does not affect the privacy or quality scores.  
**Source:** [INFERRED — derived from MIDAS Domain 14 description]

---

### Q42 — Versioning and Changelog

**Question text:** Does this dataset follow a versioning scheme, and is a changelog maintained?

**Field names:** `version_format`, `changelog_provided`  
**Type:** Two fields — dropdown (version scheme) + radio button (changelog)  

**Version scheme options:**
- `Semantic versioning (e.g. 1.0.0, 2.1.3)`
- `Date-based versioning (e.g. 2024-01)`
- `Arbitrary version numbers`
- `No versioning`

**Changelog:**
- `Yes — changelog available`
- `No`

**Required:** Yes  
**Domains scored:** 15 (Continuous Curation & Feedback)  
**Help text:** A changelog documents what changed between versions — new records added, corrections made, columns renamed. Semantic versioning + changelog is required for Domain 15 to score 3 or above.  
**Source:** [MIDAS-CONFIRMED]

---

### Q43 — User Feedback Mechanism

**Question text:** Is there a mechanism for dataset users to submit feedback, report errors, or request updates?

**Field name:** `feedback_mechanism_exists`  
**Type:** Radio button (Yes / No)  
**Required:** Yes  
**Domains scored:** 15 (Continuous Curation & Feedback)  
**Help text:** A feedback mechanism can be as simple as a public email address, a GitHub issue tracker, or a form on the dataset page. Datasets that incorporate user feedback into new versions score highest on Domain 15.  
**Conditional follow-up:** If `Yes` → show text field: *"Describe or link to the feedback mechanism"*  
**Source:** [MIDAS-CONFIRMED]

---

## Section H — Attachments

*Supporting documents that significantly improve scoring accuracy across multiple domains. None are mandatory, but all are strongly recommended.*

---

### Q44 — Data Dictionary Upload

**Question text:** Please upload the data dictionary for this dataset.

**Field name:** `data_dictionary_uploaded`  
**Type:** File upload  
**Required:** No (strongly recommended)  
**Accepted formats:** PDF, CSV, XLSX, JSON  
**Max size:** 50MB  
**Domains scored:** 3 (Documentation & User Guidance), 5 (Data Structure & Interoperability)  
**Help text:** A data dictionary should define every variable/column in the dataset: name, data type, allowed values or ranges, units, coding system, and plain-language description. Without it, Domain 3 cannot score above 2.  
**Source:** [MIDAS-CONFIRMED]

---

### Q45 — Provenance Pipeline Script

**Question text:** Please upload the data processing pipeline used to produce this dataset from raw source data.

**Field name:** `provenance_pipeline_available`  
**Type:** File upload  
**Required:** No  
**Accepted formats:** `.py`, `.R`, `.sh`, `Makefile`, `Dockerfile`, `.ipynb`, `.zip` (containing scripts)  
**Max size:** 100MB  
**Domains scored:** 9 (Provenance & Workflow Transparency)  
**Help text:** An executable pipeline (Python script, R script, shell script, or Dockerfile) that reproduces the processed dataset from raw inputs is the gold standard for provenance. Without it, Domain 9 cannot score above 2.  
**Conditional follow-up:** If no upload but GitHub URL known → show text field in Q12 area: *"Alternatively, provide a GitHub / GitLab repository URL for the pipeline"*  
**Source:** [MIDAS-CONFIRMED]

---

### Q46 — GitHub / GitLab Repository URL

**Question text:** If the processing pipeline is in a version-controlled repository, provide the URL.

**Field name:** `github_repo_url`  
**Type:** Text (URL)  
**Required:** No  
**Domains scored:** 9 (Provenance & Workflow Transparency)  
**Help text:** A public or shared repository URL pointing to the data pipeline. Example: `https://github.com/icmr-lab/tb-cohort-pipeline`  
**Validation:** Must be a valid URL starting with `https://`  
**Source:** [INFERRED]

---

### Q47 — Standard Operating Procedure (SOP)

**Question text:** Please upload the Standard Operating Procedure (SOP) for data collection, if available.

**Field name:** *(attachment stored as `sop`)*  
**Type:** File upload  
**Required:** No  
**Accepted formats:** PDF, DOCX  
**Max size:** 50MB  
**Domains scored:** 1 (Annotation / Labelling Reliability), 9 (Provenance & Workflow Transparency)  
**Help text:** SOPs describe the exact procedures followed during data collection and annotation. They provide evidence that the data was collected consistently and can be verified.  
**Source:** [MIDAS-CONFIRMED]

---

### Q48 — Consent Documentation

**Question text:** Please upload evidence of ethics approval and consent documentation.

**Field name:** *(attachment stored as `consent_doc`)*  
**Type:** File upload  
**Required:** No (strongly recommended)  
**Accepted formats:** PDF  
**Max size:** 50MB  
**Domains scored:** 10 (Ethical & Social Accountability)  
**Help text:** This may include the ethics approval letter from the IEC/IRB, a sample of the informed consent form provided to participants, or a waiver of consent approval. Uploading this document enables verification of the ethics approval reference number entered in Q28.  
**Source:** [MIDAS-CONFIRMED]

---

## Conditional Logic Summary

The table below documents all conditional question display rules.

| Trigger Question | Trigger Condition | Questions Shown / Hidden |
|---|---|---|
| Q13 (Has annotated data?) | `Yes` | Show Q14, Q15, Q16, Q17 |
| Q13 (Has annotated data?) | `No` | Skip Q14–Q17 (Domain 1 scores 0) |
| Q17 (IRR method?) | Any method selected | Show IRR value number field |
| Q23 (De-identification method?) | `k-Anonymity` or `l-Diversity` | Show Q24 (k value) |
| Q25 (Differential Privacy?) | `Yes` | Show DP epsilon field |
| Q28 (Ethics approval?) | `Yes` | Show ethics reference number field |
| Q30 (Equity analysis?) | `Yes` | Show equity analysis description field |
| Q31 (Community engagement?) | `Yes` | Show description field |
| Q33 (Access control?) | Any option | Show Q34 (DUA) |
| Q35 (Named steward?) | `Yes` | Show steward name/role field |
| Q37 (Synthetic data?) | `Yes` | Show synthetic data % field, Q38, Q39 |
| Q40 (Linked models?) | `Yes` | Show model ID entry fields |
| Q43 (Feedback mechanism?) | `Yes` | Show feedback mechanism description |
| Q5 (License?) | `Proprietary / Custom` | Show custom license description field |

---

## Domain Coverage Map

Which questions feed which MIDAS domains.

| Domain | Domain Name | Questions |
|---|---|---|
| 1 | Annotation / Labelling Reliability | Q6, Q13, Q14, Q15, Q16, Q17, Q47 |
| 2 | Metadata Completeness | Q1, Q2, Q4, Q5 |
| 3 | Documentation & User Guidance | Q1, Q2, Q12, Q19, Q44 |
| 4 | Population Representativeness | Q7, Q8, Q9, Q10, Q11 |
| 5 | Data Structure & Interoperability | Q3, Q18, Q19, Q20, Q44 |
| 6 | AI / Analytics Readiness | Q3 (+ profiler auto-detection) |
| 7 | Privacy & Identifiability | Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29 |
| 8 | Security & Access Governance | Q5, Q33, Q34 |
| 9 | Provenance & Workflow Transparency | Q12, Q45, Q46, Q47 |
| 10 | Ethical & Social Accountability | Q28, Q29, Q30, Q31, Q32, Q48 |
| 11 | Synthetic / Simulated Data | Q37, Q38, Q39 |
| 12 | Stewardship & Governance | Q5, Q35, Q36 |
| 13 | Model Linkage Integrity | Q40 |
| 14 | Environmental Sustainability | Q41 |
| 15 | Continuous Curation & Feedback | Q2, Q42, Q43 |
| PRS | Privacy-Risk Score | Q21, Q22, Q25, Q26, Q27 |

---

## Scoring Impact Reference

Questions that have the **highest impact on scores** — if these are not answered or answered poorly, scores drop significantly:

| Question | Domain | Impact |
|---|---|---|
| Q17 (IRR value) | 1 | Score cannot exceed 2 without IRR ≥ 0.6 |
| Q4 (Persistent identifier) | 2 | Score cannot exceed 2 without DOI/accession |
| Q19 + Q44 (Data dictionary) | 3 | Score cannot exceed 2 without data dictionary |
| Q8 + Q9 (Geography + sites) | 4 | Single site = capped at Score 1 |
| Q18 (Standards) | 5 | No standard = Score 0 |
| Q21 (Sensitivity class) | PRS | Determines multiplier: 1.0×/1.5×/2.0× |
| Q22 (Direct identifiers) | 7, PRS | Any identifier present = Domain 7 Score 0, PRS baseline = 50 |
| Q25 (Differential Privacy) | 7 | Only path to Score 4 on Domain 7 alongside k-anonymity |
| Q28 (Ethics approval) | 10 | Score 0 without ethics approval |
| Q45/Q46 (Pipeline) | 9 | Score cannot exceed 2 without executable pipeline |

---

## Assumptions & Inferences Log

| Question | Assumption | Status |
|---|---|---|
| Q17 IRR thresholds (0.6/0.8) | Derived from health informatics literature (Cohen's Kappa) | [INFERRED] |
| Q21 Sensitivity multipliers (1.0/1.5/2.0) | From public MIDAS Lite Version Annexure I snippets | [MIDAS-CONFIRMED] |
| Q24 k-Anonymity threshold (k ≥ 5 for Score 4) | Standard privacy literature | [INFERRED] |
| Q36 DPDP Act compliance | Not in original MIDAS domains; added as India-specific governance requirement | [INFERRED] |
| Q41 Sustainability options | Derived from MIDAS Domain 14 description; no specific scoring rubric publicly available | [INFERRED] |
| Section C conditionality | If no annotation, Domain 1 scores 0 — inferred from MIDAS "if applicable" language | [INFERRED] |

---

*End of Document*

---

**Document History**

| Version | Date | Author | Notes |
|---|---|---|---|
| 1.0 | June 18, 2026 | — | Initial questionnaire specification reverse-engineered from MIDAS 2.0 public domain descriptions |
