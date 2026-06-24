import React, { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ChevronDown, ChevronUp, AlertCircle, CheckCircle2 } from "lucide-react";
import { DomainScore } from "../lib/types";

interface DomainScoreTableProps {
  scores: DomainScore[];
}

export default function DomainScoreTable({ scores }: DomainScoreTableProps) {
  const [expandedRows, setExpandedRows] = useState<Record<number, boolean>>({});

  const toggleRow = (domainNum: number) => {
    setExpandedRows((prev) => ({
      ...prev,
      [domainNum]: !prev[domainNum],
    }));
  };

  const getConfidenceStyle = (conf: string | null) => {
    if (!conf) return "bg-slate-500/10 text-slate-400 border-slate-500/20";
    switch (conf.toLowerCase()) {
      case "high":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
      case "medium":
        return "bg-amber-500/10 text-amber-400 border-amber-500/20";
      case "low":
        return "bg-rose-500/10 text-rose-400 border-rose-500/20";
      default:
        return "bg-slate-500/10 text-slate-400 border-slate-500/20";
    }
  };

  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/60 backdrop-blur-xl overflow-hidden">
      <Table>
        <TableHeader className="bg-slate-950/40 border-b border-white/10">
          <TableRow>
            <TableHead className="w-[80px] font-bold text-slate-300">ID</TableHead>
            <TableHead className="font-bold text-slate-300">Domain Dimension</TableHead>
            <TableHead className="w-[120px] font-bold text-slate-300">Score</TableHead>
            <TableHead className="w-[120px] font-bold text-slate-300">Confidence</TableHead>
            <TableHead className="w-[50px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {scores.map((s) => {
            const isExpanded = !!expandedRows[s.domain_number];
            const displayScore = s.score ?? 0;
            const progressPct = (displayScore / 4) * 100;

            return (
              <React.Fragment key={s.domain_number}>
                <TableRow
                  className="cursor-pointer border-b border-white/5 hover:bg-white/5 transition-all"
                  onClick={() => toggleRow(s.domain_number)}
                >
                  <TableCell className="font-mono text-xs text-slate-400">
                    D{s.domain_number}
                  </TableCell>
                  <TableCell className="font-medium text-slate-200">
                    {s.domain_name}
                  </TableCell>
                  <TableCell>
                    {s.not_applicable ? (
                      <span className="text-xs text-slate-500 italic font-semibold">N/A</span>
                    ) : (
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-slate-200 w-3">{s.score}</span>
                        <Progress value={progressPct} className="h-1.5 w-16 bg-slate-800" />
                      </div>
                    )}
                  </TableCell>
                  <TableCell>
                    <Badge className={`px-2 py-0.5 border text-[10px] uppercase font-bold rounded-md ${getConfidenceStyle(s.confidence)}`}>
                      {s.not_applicable ? "N/A" : s.confidence}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-slate-400" />
                    )}
                  </TableCell>
                </TableRow>

                {isExpanded && (
                  <TableRow className="bg-slate-950/20 border-b border-white/5 hover:bg-slate-950/20">
                    <TableCell colSpan={5} className="p-4 pl-8">
                      <div className="space-y-3">
                        <div>
                          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                            Evaluation Rationale
                          </h4>
                          <p className="text-sm text-slate-300 mt-1">{s.rationale}</p>
                        </div>

                        {s.evidence_items && s.evidence_items.length > 0 && (
                          <div>
                            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                              Observed Evidence
                            </h4>
                            <ul className="space-y-1">
                              {s.evidence_items.map((ev, idx) => (
                                <li key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                                  <span>{ev}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {s.gaps && s.gaps.length > 0 && (
                          <div>
                            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                              Identified Quality Gaps
                            </h4>
                            <ul className="space-y-1">
                              {s.gaps.map((gap, idx) => (
                                <li key={idx} className="flex items-start gap-2 text-xs text-rose-300">
                                  <AlertCircle className="h-3.5 w-3.5 text-rose-400 shrink-0 mt-0.5" />
                                  <span>{gap}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                )}
              </React.Fragment>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
