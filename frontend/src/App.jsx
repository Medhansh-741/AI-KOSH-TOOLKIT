import React, { useState } from 'react';
import { UploadPage } from './pages/UploadPage';
import { DashboardPage } from './pages/DashboardPage';
import { ReportPage } from './pages/ReportPage';

function App() {
  const [currentView, setCurrentView] = useState('upload'); // 'upload' | 'dashboard' | 'report'
  const [assessmentId, setAssessmentId] = useState(null);

  const handleUploadSuccess = (id) => {
    setAssessmentId(id);
    setCurrentView('dashboard');
  };

  return (
    <div className="App">
      <header style={{ backgroundColor: '#1e293b', padding: '15px 30px', color: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ margin: 0 }}>AIKosh Dataset Quality Toolkit</h2>
        <nav>
          <button onClick={() => setCurrentView('upload')} style={{ marginRight: '10px', padding: '5px 10px', background: 'transparent', border: '1px solid #fff', color: '#fff', cursor: 'pointer' }}>Upload</button>
          {assessmentId && (
            <>
              <button onClick={() => setCurrentView('dashboard')} style={{ marginRight: '10px', padding: '5px 10px', background: 'transparent', border: '1px solid #fff', color: '#fff', cursor: 'pointer' }}>Dashboard</button>
              <button onClick={() => setCurrentView('report')} style={{ padding: '5px 10px', background: 'transparent', border: '1px solid #fff', color: '#fff', cursor: 'pointer' }}>Report</button>
            </>
          )}
        </nav>
      </header>

      <main>
        {currentView === 'upload' && <UploadPage onUploadSuccess={handleUploadSuccess} />}
        {currentView === 'dashboard' && <DashboardPage assessmentId={assessmentId} />}
        {currentView === 'report' && <ReportPage assessmentId={assessmentId} />}
      </main>
    </div>
  );
}

export default App;
