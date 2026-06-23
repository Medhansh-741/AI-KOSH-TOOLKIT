import React from 'react';

const API_KEY = import.meta.env.VITE_API_KEY || 'tkt_secret_super_secure_key_12345678';

export const ReportPage = ({ assessmentId }) => {
  const handleDownload = (format) => {
    window.open(`http://localhost:8000/api/v1/assess/${assessmentId}/report?format=${format}&api_key=${API_KEY}`, '_blank');
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px', border: '1px solid #ccc', textAlign: 'center' }}>
      <h1>Download Quality Assessment Report</h1>
      <p>Download the full, detailed assessment report in your preferred format.</p>
      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '30px' }}>
        <button onClick={() => handleDownload('json')} style={{ padding: '10px 20px', backgroundColor: '#333', color: '#fff', border: 'none' }}>
          JSON format
        </button>
        <button onClick={() => handleDownload('html')} style={{ padding: '10px 20px', backgroundColor: '#0066cc', color: '#fff', border: 'none' }}>
          HTML format
        </button>
        <button onClick={() => handleDownload('pdf')} style={{ padding: '10px 20px', backgroundColor: '#cc3300', color: '#fff', border: 'none' }}>
          PDF format
        </button>
      </div>
    </div>
  );
};
