import React from 'react';

export const CQIGauge = ({ value, band }) => {
  return (
    <div className="cqi-gauge" style={{ textAlign: 'center', padding: '20px' }}>
      <h2>Composite Quality Index</h2>
      <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#0066cc' }}>
        {value}%
      </div>
      <div style={{ fontSize: '1.2rem', marginTop: '10px' }}>
        Band: <strong>{band}</strong>
      </div>
    </div>
  );
};
