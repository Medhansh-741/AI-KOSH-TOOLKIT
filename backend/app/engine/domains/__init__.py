from .domain_01_annotation import AnnotationReliabilityScorer
from .domain_02_metadata import MetadataCompletenessScorer
from .domain_03_documentation import DocumentationScorer
from .domain_04_representativeness import RepresentativenessScorer
from .domain_05_interoperability import InteroperabilityScorer
from .domain_06_ai_readiness import AIReadinessScorer
from .domain_07_privacy import PrivacyScorer
from .domain_08_security import SecurityScorer
from .domain_09_provenance import ProvenanceScorer
from .domain_10_ethics import EthicsScorer
from .domain_11_synthetic import SyntheticDataScorer
from .domain_12_stewardship import StewardshipScorer
from .domain_13_model_linkage import ModelLinkageScorer
from .domain_14_sustainability import SustainabilityScorer
from .domain_15_curation import CurationScorer

DOMAIN_SCORERS = [
    AnnotationReliabilityScorer,
    MetadataCompletenessScorer,
    DocumentationScorer,
    RepresentativenessScorer,
    InteroperabilityScorer,
    AIReadinessScorer,
    PrivacyScorer,
    SecurityScorer,
    ProvenanceScorer,
    EthicsScorer,
    SyntheticDataScorer,
    StewardshipScorer,
    ModelLinkageScorer,
    SustainabilityScorer,
    CurationScorer,
]
