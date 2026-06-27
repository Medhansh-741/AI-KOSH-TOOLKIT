import pandas as pd
from app.engine.profiler.profiler import DatasetProfiler

def test_profiler_completeness_and_shape():
    # Construct a simple dataframe
    data = {
        "col_numeric": [1.0, 2.0, 3.0, 4.0, None],  # 80% complete
        "col_string": ["A", "B", None, "D", "E"],   # 80% complete
    }
    df = pd.DataFrame(data)
    profiler = DatasetProfiler(df)
    profile = profiler.profile_dataset()
    
    assert profile["shape"]["rows"] == 5
    assert profile["shape"]["columns"] == 2
    
    completeness = profile["completeness"]
    assert completeness["overall_pct"] == 80.0
    assert "col_numeric" in completeness["columns_below_90pct"]
    assert "col_string" in completeness["columns_below_90pct"]
    assert len(completeness["columns_below_50pct"]) == 0

def test_profiler_pii_detection():
    data = {
        "patient_name": ["Alice", "Bob"],
        "normal_column": [1, 2],
        "dob": ["1990-01-01", "1995-05-05"],
        "lat": [12.97, 13.08]
    }
    df = pd.DataFrame(data)
    profiler = DatasetProfiler(df)
    profile = profiler.profile_dataset()
    
    pii = profile["pii_scan"]
    assert pii["direct_identifiers_detected"] is True
    assert "patient_name" in pii["name_columns"]
    assert "dob" in pii["dob_columns"]
    assert "lat" in pii["gps_columns"]
    assert len(pii["phone_columns"]) == 0

def test_profiler_standards_detection():
    data = {
        "icd_col": ["U07.1", "A09.9", "B97.29"],
        "loinc_col": ["29463-7", "883-9", "4544-3"],
        "snomed_col": ["22298006", "386661006", "44054006"]
    }

    df = pd.DataFrame(data)
    profiler = DatasetProfiler(df)
    profile = profiler.profile_dataset()
    
    standards = profile["standards_detected"]
    assert standards["icd_codes_present"] is True
    assert "icd_col" in standards["icd_columns"]
    assert standards["loinc_codes_present"] is True
    assert standards["snomed_codes_present"] is True
