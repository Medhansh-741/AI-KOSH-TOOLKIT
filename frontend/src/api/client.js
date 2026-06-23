const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const API_KEY = import.meta.env.VITE_API_KEY || 'tkt_secret_super_secure_key_12345678';

export const apiClient = {
  async submitAssessment(file, metadataJson) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadataJson));

    const response = await fetch(`${API_BASE_URL}/assess`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      },
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to submit assessment');
    return response.json();
  },

  async getAssessmentStatus(assessmentId) {
    const response = await fetch(`${API_BASE_URL}/assess/${assessmentId}`, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`
      }
    });
    if (!response.ok) throw new Error('Failed to fetch assessment status');
    return response.json();
  },

  async getHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) throw new Error('Failed to check backend health');
    return response.json();
  }
};
