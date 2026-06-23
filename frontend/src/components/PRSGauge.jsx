import React from 'react';

export const PRSGauge = ({ value, band }) => {
  return (
    <div className="prs-gauge" style={{ textAlign: 'center', padding: '20px' }}>
      <h2>Privacy-Risk Score</h2>
      <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#cc3300' }}>
        {value}
      </div>
      <div style={{ fontSize: '1.2rem', marginTop: '10px' }}>
        Band: <strong>{band}</strong>
      </div>
    </div>
  );
};
