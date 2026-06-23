import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const ScoreHistoryTrend = ({ data }) => {
  // expects data in shape: [{ date: '2026-06-18', cqi: 67.9, prs: 22 }]
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="cqi" stroke="#0066cc" activeDot={{ r: 8 }} name="CQI Score" />
        <Line type="monotone" dataKey="prs" stroke="#cc3300" name="PRS Score" />
      </LineChart>
    </ResponsiveContainer>
  );
};
