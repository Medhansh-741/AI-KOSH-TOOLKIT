import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import { DomainScore } from "../lib/types";

interface DomainRadarChartProps {
  scores: DomainScore[];
}

export default function DomainRadarChart({ scores }: DomainRadarChartProps) {
  // Format data for Recharts
  const data = scores.map((s) => ({
    subject: `D${s.domain_number}`,
    fullDomainName: s.domain_name,
    score: s.score === null ? 0 : s.score,
    fullMark: 4,
  }));

  return (
    <Card className="overflow-hidden border border-white/10 bg-slate-900/60 backdrop-blur-xl transition-all duration-300 hover:border-white/20 col-span-1 md:col-span-2">
      <CardHeader className="pb-0">
        <CardTitle className="text-sm font-semibold tracking-wider text-slate-400 uppercase">
          15-Domain Radar Profile
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[280px] flex items-center justify-center p-2">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid stroke="#334155" />
            <PolarAngleAxis
              dataKey="subject"
              tick={{ fill: "#94a3b8", fontSize: 11, fontWeight: 600 }}
            />
            <PolarRadiusAxis
              angle={30}
              domain={[0, 4]}
              tickCount={5}
              tick={{ fill: "#64748b", fontSize: 10 }}
            />
            <Radar
              name="Dataset Quality"
              dataKey="score"
              stroke="#6366f1"
              fill="#6366f1"
              fillOpacity={0.25}
            />
          </RadarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
