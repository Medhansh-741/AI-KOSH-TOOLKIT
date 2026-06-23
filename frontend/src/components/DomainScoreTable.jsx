import React from 'react';

export const DomainScoreTable = ({ scores }) => {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
      <thead>
        <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
          <th style={{ padding: '10px' }}>Domain</th>
          <th style={{ padding: '10px' }}>Score</th>
          <th style={{ padding: '10px' }}>Rationale</th>
          <th style={{ padding: '10px' }}>Confidence</th>
        </tr>
      </thead>
      <tbody>
        {scores.map((s, index) => (
          <tr key={index} style={{ borderBottom: '1px solid #eee' }}>
            <td style={{ padding: '10px' }}>D{s.domain_number} - {s.domain_name}</td>
            <td style={{ padding: '10px' }}>{s.not_applicable ? 'N/A' : `${s.score}/4`}</td>
            <td style={{ padding: '10px' }}>{s.rationale}</td>
            <td style={{ padding: '10px' }}>{s.confidence}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
