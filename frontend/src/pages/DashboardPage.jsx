import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { CQIGauge } from '../components/CQIGauge';
import { PRSGauge } from '../components/PRSGauge';
import { ReleaseClassBadge } from '../components/ReleaseClassBadge';
import { DomainScoreTable } from '../components/DomainScoreTable';
import { GapPanel } from '../components/GapPanel';

export const DashboardPage = ({ assessmentId }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    let interval;
    const fetchStatus = async () => {
      try {
        const result = await apiClient.getAssessmentStatus(assessmentId);
        if (result.status === 'complete') {
          setData(result);
          setLoading(false);
          clearInterval(interval);
        } else if (result.status === 'failed') {
          alert('Assessment failed: ' + (result.error_message || 'Unknown error'));
          setLoading(false);
          clearInterval(interval);
        }
      } catch (err) {
        console.error('Error fetching status:', err);
      }
    };

    fetchStatus();
    interval = setInterval(fetchStatus, 5000);

    return () => clearInterval(interval);
  }, [assessmentId]);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}><h2>Analyzing Dataset Quality (Asynchronously)...</h2><p>Usually takes less than 3 minutes.</p></div>;
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '40px auto', padding: '20px' }}>
      <h1>Dataset Quality Assessment Dashboard</h1>
      <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
        <CQIGauge value={data.cqi?.value} band={data.cqi?.band} />
        <PRSGauge value={data.prs?.value} band={data.prs?.band} />
        <div style={{ alignSelf: 'center' }}>
          <ReleaseClassBadge classification={data.release?.classification} />
          <p style={{ marginTop: '10px', color: '#666' }}>{data.release?.justification}</p>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
        <div>
          <h3>15 Domain Breakdown</h3>
          <DomainScoreTable scores={data.domain_scores || []} />
        </div>
        <div>
          <GapPanel domainScores={data.domain_scores || []} />
        </div>
      </div>
    </div>
  );
};
