import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

export const RadarScoreChart = ({ data }) => {
  // expects data in shape: [{ domain: 'Domain Name', score: 3 }]
  return (
    <ResponsiveContainer width="100%" height={400}>
      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="domain" />
        <PolarRadiusAxis angle={30} domain={[0, 4]} />
        <Radar name="Quality Score" dataKey="score" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
      </RadarChart>
    </ResponsiveContainer>
  );
};
