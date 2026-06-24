import pandas as pd
import numpy as np
import re
import os
from typing import Dict, Any, List
from app.config import settings

class DatasetProfiler:
    def __init__(self, df: pd.DataFrame):
        self.raw_len = len(df)
        self.sampled = False
        self.sample_rows = None
        
        sample_rows_limit = getattr(settings, "PROFILING_SAMPLE_ROWS", 100000)
        if self.raw_len > sample_rows_limit:
            self.df = df.sample(n=sample_rows_limit, random_state=42)
            self.sampled = True
            self.sample_rows = sample_rows_limit
        else:
            self.df = df

    def profile_dataset(self) -> Dict[str, Any]:
        """Orchestrates completeness, identifier scan, standards checks, and returns a profile dict."""
        columns_profile = []
        
        pii_scan = {
            "direct_identifiers_detected": False,
            "name_columns": [],
            "phone_columns": [],
            "id_columns": [],
            "gps_columns": [],
            "dob_columns": []
        }
        
        standards_detected = {
            "icd_codes_present": False,
            "icd_columns": [],
            "snomed_codes_present": False,
            "loinc_codes_present": False,
            "fhir_structure": False
        }
        
        total_cells = len(self.df) * len(self.df.columns) if not self.df.empty else 0
        total_missing = 0
        
        columns_below_90pct = []
        columns_below_50pct = []
        
        icd10_pattern = re.compile(r'^[A-Z][0-9][0-9AB](?:\.[0-9A-Z]{1,4})?$', re.IGNORECASE)
        loinc_pattern = re.compile(r'^\d{3,5}-\d$')
        
        for col_name in self.df.columns:
            series = self.df[col_name]
            col_len = len(series)
            missing_count = int(series.isnull().sum())
            total_missing += missing_count
            
            completeness_pct = round(((col_len - missing_count) / col_len) * 100, 2) if col_len > 0 else 100.0
            
            if completeness_pct < 90.0:
                columns_below_90pct.append(col_name)
            if completeness_pct < 50.0:
                columns_below_50pct.append(col_name)
                
            non_null_series = series.dropna()
            
            dtype = "string"
            is_numeric = False
            
            if pd.api.types.is_numeric_dtype(series):
                if non_null_series.nunique() <= 2:
                    dtype = "categorical"
                else:
                    dtype = "numeric"
                    is_numeric = True
            elif pd.api.types.is_datetime64_any_dtype(series):
                dtype = "datetime"
            else:
                try:
                    pd.to_datetime(non_null_series.head(100), errors='raise')
                    dtype = "datetime"
                except (ValueError, TypeError):
                    unique_count = non_null_series.nunique()
                    if unique_count <= 20 or (col_len > 0 and unique_count / col_len < 0.05):
                        dtype = "categorical"
                    else:
                        dtype = "string"

            col_info = {
                "name": col_name,
                "dtype": dtype,
                "completeness_pct": completeness_pct,
                "missing_count": missing_count
            }
            
            if is_numeric and not non_null_series.empty:
                col_info["min"] = float(non_null_series.min())
                col_info["max"] = float(non_null_series.max())
                col_info["mean"] = float(non_null_series.mean())
                col_info["median"] = float(non_null_series.median())
                col_info["std"] = float(non_null_series.std()) if len(non_null_series) > 1 else 0.0
                
                try:
                    q75, q25 = np.percentile(non_null_series, [75, 25])
                    iqr = q75 - q25
                    lower_bound = q25 - (1.5 * iqr)
                    upper_bound = q75 + (1.5 * iqr)
                    outliers = non_null_series[(non_null_series < lower_bound) | (non_null_series > upper_bound)]
                    col_info["outlier_pct"] = round((len(outliers) / len(non_null_series)) * 100, 2)
                except:
                    col_info["outlier_pct"] = 0.0
                    
                col_info["range_violation"] = bool((non_null_series < 0).any())
            elif dtype == "datetime" and not non_null_series.empty:
                try:
                    dt_series = pd.to_datetime(non_null_series)
                    col_info["min"] = str(dt_series.min())
                    col_info["max"] = str(dt_series.max())
                except:
                    pass
            elif dtype == "categorical":
                col_info["unique_values"] = int(non_null_series.nunique())
                col_info["value_counts"] = {str(k): int(v) for k, v in non_null_series.value_counts().head(10).items()}
            elif dtype == "string":
                col_info["unique_values"] = int(non_null_series.nunique())

            col_name_lower = col_name.lower().replace("_", "").replace("-", "")
            pii_flag = None
            pii_confidence = "Low"
            
            if any(p in col_name_lower for p in ["name", "firstname", "lastname", "fullname", "patientname"]):
                pii_scan["name_columns"].append(col_name)
                pii_flag = "name_pattern"
                pii_confidence = "High"
            elif any(p in col_name_lower for p in ["phone", "mobile", "tel", "contact", "telephone"]):
                pii_scan["phone_columns"].append(col_name)
                pii_flag = "phone_pattern"
                pii_confidence = "High"
            elif any(p in col_name_lower for p in ["nationalid", "ssn", "aadhaar", "uid", "passport", "govtid"]):
                pii_scan["id_columns"].append(col_name)
                pii_flag = "id_pattern"
                pii_confidence = "High"
            elif col_name_lower in ["id", "uuid"]:
                pii_scan["id_columns"].append(col_name)
                pii_flag = "id_pattern"
                pii_confidence = "Medium"
            elif any(p in col_name_lower for p in ["gps", "latitude", "longitude", "lat", "lon", "coordinates"]):
                pii_scan["gps_columns"].append(col_name)
                pii_flag = "gps_pattern"
                pii_confidence = "High"
            elif any(p in col_name_lower for p in ["dob", "birthdate", "dateofbirth"]):
                pii_scan["dob_columns"].append(col_name)
                pii_flag = "dob_pattern"
                pii_confidence = "High"
                
            if pii_flag:
                col_info["pii_flag"] = pii_flag
                col_info["pii_confidence"] = pii_confidence
                pii_scan["direct_identifiers_detected"] = True

            is_icd_col = False
            if "icd" in col_name_lower:
                is_icd_col = True
            elif dtype == "string" and not non_null_series.empty:
                sample_vals = non_null_series.head(100).astype(str)
                matches = sample_vals.apply(lambda x: bool(icd10_pattern.match(x)))
                if len(sample_vals) > 0 and (matches.sum() / len(sample_vals) > 0.3):
                    is_icd_col = True
            
            if is_icd_col:
                standards_detected["icd_codes_present"] = True
                standards_detected["icd_columns"].append(col_name)

            is_loinc = False
            if "loinc" in col_name_lower:
                is_loinc = True
            elif dtype == "string" and not non_null_series.empty:
                sample_vals = non_null_series.head(100).astype(str)
                matches = sample_vals.apply(lambda x: bool(loinc_pattern.match(x)))
                if len(sample_vals) > 0 and (matches.sum() / len(sample_vals) > 0.3):
                    is_loinc = True
                    
            if is_loinc:
                standards_detected["loinc_codes_present"] = True

            if "snomed" in col_name_lower:
                standards_detected["snomed_codes_present"] = True

            columns_profile.append(col_info)

        overall_pct = round(((total_cells - total_missing) / total_cells) * 100, 2) if total_cells > 0 else 100.0
        
        completeness = {
            "overall_pct": overall_pct,
            "columns_below_90pct": columns_below_90pct,
            "columns_below_50pct": columns_below_50pct
        }

        if any('.' in col for col in self.df.columns) or "resourcetype" in [c.lower() for c in self.df.columns]:
            standards_detected["fhir_structure"] = True

        return {
            "file": {
                "format": "csv",
                "size_bytes": 0,
                "encoding": "UTF-8"
            },
            "shape": {
                "rows": self.raw_len,
                "columns": len(self.df.columns) if not self.df.empty else 0
            },
            "columns": columns_profile,
            "pii_scan": pii_scan,
            "completeness": completeness,
            "standards_detected": standards_detected,
            "sampled": self.sampled,
            "sample_rows": self.sample_rows
        }
