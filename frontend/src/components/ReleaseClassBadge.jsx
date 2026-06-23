import React from 'react';

export const ReleaseClassBadge = ({ classification }) => {
  const styles = {
    Open: { backgroundColor: '#d4edda', color: '#155724', border: '1px solid #c3e6cb' },
    Controlled: { backgroundColor: '#fff3cd', color: '#856404', border: '1px solid #ffeeba' },
    Restricted: { backgroundColor: '#f8d7da', color: '#721c24', border: '1px solid #f5c6cb' }
  };

  const currentStyle = styles[classification] || { backgroundColor: '#eee', color: '#333' };

  return (
    <div style={{
      padding: '10px 20px',
      borderRadius: '20px',
      display: 'inline-block',
      fontWeight: 'bold',
      fontSize: '1.2rem',
      ...currentStyle
    }}>
      Release: {classification}
    </div>
  );
};
