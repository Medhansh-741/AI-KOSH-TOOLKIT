import React from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Calendar, AlertCircle } from "lucide-react";
import Link from "next/link";
import { Assessment } from "../lib/types";

interface ScoreHistoryProps {
  assessments: Assessment[];
  onSelect: (id: string) => void;
}

export default function ScoreHistory({ assessments, onSelect }: ScoreHistoryProps) {
  const getStatusBadge = (status: string) => {
    switch (status.toLowerCase()) {
      case "complete":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
      case "processing":
        return "bg-sky-500/10 text-sky-400 border-sky-500/20 animate-pulse";
      case "queued":
        return "bg-slate-500/10 text-slate-400 border-slate-500/20";
      default:
        return "bg-rose-500/10 text-rose-400 border-rose-500/20";
    }
  };

  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch (_) {
      return dateStr;
    }
  };

  if (assessments.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-8 rounded-xl border border-white/5 bg-slate-900/20 text-center">
        <AlertCircle className="h-8 w-8 text-slate-500 mb-2" />
        <p className="text-sm text-slate-400">No assessments found. Submit a dataset to start.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/60 backdrop-blur-xl overflow-hidden">
      <Table>
        <TableHeader className="bg-slate-950/40 border-b border-white/10">
          <TableRow>
            <TableHead className="font-bold text-slate-300">Submitted</TableHead>
            <TableHead className="font-bold text-slate-300">Format</TableHead>
            <TableHead className="font-bold text-slate-300">Status</TableHead>
            <TableHead className="w-[80px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {assessments.map((a) => (
            <TableRow key={a.assessment_id} className="border-b border-white/5 hover:bg-white/5">
              <TableCell className="text-xs text-slate-200">
                <div className="flex items-center gap-1.5 font-medium">
                  <Calendar className="h-3.5 w-3.5 text-slate-500" />
                  {formatDate(a.submitted_at)}
                </div>
              </TableCell>
              <TableCell className="font-mono text-xs uppercase text-slate-400">
                {a.file_format}
              </TableCell>
              <TableCell>
                <Badge className={`px-2 py-0.5 border text-[10px] uppercase font-bold rounded-md ${getStatusBadge(a.status)}`}>
                  {a.status}
                </Badge>
              </TableCell>
              <TableCell className="text-right">
                {a.status === "complete" ? (
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-xs text-indigo-400 hover:text-indigo-300 hover:bg-indigo-500/10 font-bold"
                    onClick={() => onSelect(a.assessment_id)}
                  >
                    View Result
                    <ArrowRight className="ml-1 h-3 w-3" />
                  </Button>
                ) : a.status === "failed" ? (
                  <span className="text-xs text-rose-500 font-semibold" title={a.error_message || "Unknown error"}>
                    Error
                  </span>
                ) : (
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-xs text-sky-400 hover:text-sky-300 hover:bg-sky-500/10 font-bold animate-pulse"
                    onClick={() => onSelect(a.assessment_id)}
                  >
                    Polling...
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
