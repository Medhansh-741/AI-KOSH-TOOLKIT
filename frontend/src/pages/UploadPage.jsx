import React, { useState } from 'react';
import { apiClient } from '../api/client';

export const UploadPage = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [datasetName, setDatasetName] = useState('');
  const [datasetType, setDatasetType] = useState('tabular');
  const [studyType, setStudyType] = useState('cohort');
  const [targetPopulation, setTargetPopulation] = useState('');
  const [geographicCoverage, setGeographicCoverage] = useState('district');
  const [sensitivityClass, setSensitivityClass] = useState('standard');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert('Please select a file');

    setSubmitting(true);
    const metadata = {
      dataset_name: datasetName,
      dataset_type: datasetType,
      study_type: studyType,
      target_population: targetPopulation,
      geographic_coverage: geographicCoverage,
      sensitivity_class: sensitivityClass
    };

    try {
      const result = await apiClient.submitAssessment(file, metadata);
      onUploadSuccess(result.assessment_id);
    } catch (err) {
      alert('Error submitting dataset: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px', border: '1px solid #ccc' }}>
      <h1>Upload Health Research Dataset</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Dataset File (.csv, .xlsx, .json, .parquet, .zip):</label>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Dataset Name:</label>
          <input type="text" value={datasetName} onChange={(e) => setDatasetName(e.target.value)} required minLength={5} style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Target Population:</label>
          <textarea value={targetPopulation} onChange={(e) => setTargetPopulation(e.target.value)} required minLength={20} style={{ width: '100%', height: '80px' }} />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Sensitivity Class:</label>
          <select value={sensitivityClass} onChange={(e) => setSensitivityClass(e.target.value)} style={{ width: '100%' }}>
            <option value="standard">Standard</option>
            <option value="high_stigma">High Stigma (TB, HIV, Reproductive)</option>
            <option value="critical">Critical (Detainee, Forensic)</option>
          </select>
        </div>
        <button type="submit" disabled={submitting} style={{ padding: '10px 20px', backgroundColor: '#0066cc', color: '#fff', border: 'none' }}>
          {submitting ? 'Uploading & Queuing...' : 'Submit Assessment'}
        </button>
      </form>
    </div>
  );
};
