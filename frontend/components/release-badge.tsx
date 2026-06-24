import React from "react";
import { Badge } from "@/components/ui/badge";
import { ShieldCheck, ShieldAlert, Eye } from "lucide-react";

interface ReleaseBadgeProps {
  classification: "Open" | "Controlled" | "Restricted";
  justification: string;
  policyOverrideApplied: boolean;
}

export default function ReleaseBadge({ classification, justification, policyOverrideApplied }: ReleaseBadgeProps) {
  const getBadgeStyle = (cls: string) => {
    switch (cls.toLowerCase()) {
      case "open":
        return {
          bg: "bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/30",
          text: "text-emerald-400",
          icon: <Eye className="mr-1.5 h-4 w-4 text-emerald-400" />,
        };
      case "controlled":
        return {
          bg: "bg-amber-500/10 hover:bg-amber-500/20 border-amber-500/30",
          text: "text-amber-400",
          icon: <ShieldCheck className="mr-1.5 h-4 w-4 text-amber-400" />,
        };
      case "restricted":
        return {
          bg: "bg-rose-500/10 hover:bg-rose-500/20 border-rose-500/30",
          text: "text-rose-400",
          icon: <ShieldAlert className="mr-1.5 h-4 w-4 text-rose-400" />,
        };
      default:
        return {
          bg: "bg-slate-500/10 hover:bg-slate-500/20 border-slate-500/30",
          text: "text-slate-400",
          icon: null,
        };
    }
  };

  const style = getBadgeStyle(classification);

  return (
    <div className="flex flex-col gap-2 rounded-xl border border-white/10 bg-slate-900/60 p-4 backdrop-blur-xl">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-400">Release Classification</span>
        <Badge className={`px-2.5 py-1 border text-xs font-semibold uppercase tracking-wider rounded-lg ${style.bg} ${style.text}`}>
          {style.icon}
          {classification}
        </Badge>
      </div>
      
      <p className="text-xs text-slate-300 font-medium leading-relaxed mt-1">
        {justification}
      </p>

      {policyOverrideApplied && (
        <span className="text-[10px] uppercase font-bold text-rose-400 tracking-wider">
          * Policy Override Applied
        </span>
      )}
    </div>
  );
}
