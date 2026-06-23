import React from 'react';

export const GapPanel = ({ domainScores }) => {
  // filter domains where score <= 2
  const lowScores = domainScores.filter(s => s.score !== null && s.score <= 2);

  return (
    <div className="gap-panel" style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '5px' }}>
      <h3>🔴 Identified Gaps & Recommendations</h3>
      {lowScores.length === 0 ? (
        <p>No major quality gaps identified. Your dataset meets target quality expectations.</p>
      ) : (
        <ul>
          {lowScores.map((s, index) => (
            <li key={index} style={{ marginBottom: '15px' }}>
              <strong>D{s.domain_number} - {s.domain_name} (Score: {s.score}/4)</strong>
              <div style={{ color: '#666', fontSize: '0.95rem' }}>Gaps:</div>
              <ul style={{ margin: '5px 0' }}>
                {s.gaps.map((gap, gIdx) => <li key={gIdx}>{gap}</li>)}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
