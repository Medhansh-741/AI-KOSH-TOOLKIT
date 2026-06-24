import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface PRSGaugeProps {
  value: number;
  band: string;
  baseline: number;
  multiplier: number;
  sensitivity: string;
  trace: string;
}

export default function PRSGauge({ value, band, baseline, multiplier, sensitivity, trace }: PRSGaugeProps) {
  // Get color based on risk band
  const getRiskColorClass = (b: string) => {
    switch (b.toLowerCase()) {
      case "low":
        return "text-emerald-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.4)]";
      case "moderate":
        return "text-amber-400 drop-shadow-[0_0_12px_rgba(251,191,36,0.4)]";
      case "high":
        return "text-rose-400 drop-shadow-[0_0_12px_rgba(251,113,133,0.4)]";
      case "very high":
        return "text-purple-400 drop-shadow-[0_0_12px_rgba(192,132,252,0.4)]";
      default:
        return "text-slate-400";
    }
  };

  const circumference = 2 * Math.PI * 50;
  const strokeDashoffset = circumference - (value / 100) * circumference;

  return (
    <Card className="overflow-hidden border border-white/10 bg-slate-900/60 backdrop-blur-xl transition-all duration-300 hover:border-white/20">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold tracking-wider text-slate-400 uppercase">
          Patient Risk Score (PRS)
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center pt-2">
        <div className="relative flex h-36 w-36 items-center justify-center">
          {/* Background circle */}
          <svg className="absolute top-0 left-0 h-full w-full -rotate-90">
            <circle
              cx="72"
              cy="72"
              r="50"
              className="fill-none stroke-slate-800"
              strokeWidth="10"
            />
            {/* Foreground circle with gradient */}
            <circle
              cx="72"
              cy="72"
              r="50"
              className="fill-none transition-all duration-1000 ease-out"
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              stroke="url(#prsGradient)"
            />
            <defs>
              <linearGradient id="prsGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" className="stop-color-prs-start" />
                <stop offset="100%" className="stop-color-prs-end" />
              </linearGradient>
            </defs>
            <style>{`
              .stop-color-prs-start { stop-color: ${band.toLowerCase() === "low" ? "#34d399" : band.toLowerCase() === "moderate" ? "#fbbf24" : band.toLowerCase() === "high" ? "#fb7185" : "#c084fc"}; }
              .stop-color-prs-end { stop-color: ${band.toLowerCase() === "low" ? "#059669" : band.toLowerCase() === "moderate" ? "#d97706" : band.toLowerCase() === "high" ? "#e11d48" : "#7c3aed"}; }
            `}</style>
          </svg>

          {/* Score display */}
          <div className="text-center z-10">
            <span className="text-3xl font-extrabold tracking-tight text-white">
              {value}
            </span>
            <div className={`mt-0.5 text-xs font-bold uppercase tracking-wider ${getRiskColorClass(band)}`}>
              {band}
            </div>
          </div>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-slate-400">
            Baseline: <span className="font-semibold text-slate-200">{baseline}</span> | Mult: <span className="font-semibold text-slate-200">{multiplier}x</span> ({sensitivity})
          </p>
          <p className="mt-1 font-mono text-[10px] text-slate-500 max-w-[200px] truncate" title={trace}>
            {trace}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
