import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTriangle, Wrench } from "lucide-react";
import { DomainScore } from "../lib/types";

interface GapPanelProps {
  scores: DomainScore[];
}

export default function GapPanel({ scores }: GapPanelProps) {
  // Gaps are domains with scores <= 2 (and not N/A)
  const weakDomains = scores.filter((s) => !s.not_applicable && s.score !== null && s.score <= 2);

  if (weakDomains.length === 0) {
    return (
      <Card className="border border-emerald-500/20 bg-emerald-500/5 backdrop-blur-xl p-4 text-center">
        <p className="text-sm font-semibold text-emerald-400">
          🎉 Exemplary work! No critical quality gaps detected across all MIDAS domains.
        </p>
      </Card>
    );
  }

  return (
    <Card className="border border-white/10 bg-slate-900/60 backdrop-blur-xl transition-all duration-300">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold tracking-wider text-slate-400 uppercase flex items-center gap-1.5">
          <AlertTriangle className="h-4 w-4 text-amber-500" />
          Critical Improvement Areas ({weakDomains.length})
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 pt-2 max-h-[350px] overflow-y-auto pr-1">
        {weakDomains.map((s) => (
          <div key={s.domain_number} className="rounded-lg bg-slate-950/40 p-3 border border-white/5 space-y-2">
            <div className="flex items-center justify-between border-b border-white/5 pb-1.5">
              <span className="text-xs font-bold text-slate-400">D{s.domain_number}</span>
              <span className="text-xs font-semibold text-slate-200">{s.domain_name}</span>
              <span className="text-xs font-extrabold text-rose-400 bg-rose-500/10 border border-rose-500/20 px-1.5 rounded">
                Score {s.score}/4
              </span>
            </div>
            
            <div className="space-y-1">
              <span className="text-[10px] uppercase font-bold text-slate-500 block">Identified Gaps:</span>
              <ul className="list-disc list-inside text-xs text-rose-300 space-y-0.5 pl-1">
                {s.gaps && s.gaps.length > 0 ? (
                  s.gaps.map((gap, idx) => <li key={idx}>{gap}</li>)
                ) : (
                  <li>General quality improvement recommended.</li>
                )}
              </ul>
            </div>

            <div className="flex items-start gap-1.5 rounded-md bg-indigo-500/5 p-2 border border-indigo-500/10 mt-1">
              <Wrench className="h-3.5 w-3.5 text-indigo-400 mt-0.5 shrink-0" />
              <div className="text-[11px] text-indigo-300 leading-relaxed">
                <span className="font-bold">Recommendation: </span>
                {s.domain_number === 1 && "Document details of annotation methodology, include IRR (kappa/ICC) calculations, and credential details of medical annotators."}
                {s.domain_number === 2 && "Fill out missing metadata columns in the assessment intake form to improve discovery completeness."}
                {s.domain_number === 3 && "Provide a complete data dictionary PDF, ethics review approval numbers, and consent models."}
                {s.domain_number === 4 && "Expand multi-site sampling to state or national levels and detail demographic diversity representations."}
                {s.domain_number === 5 && "Structure variables utilizing standard ontologies (ICD-10, SNOMED, LOINC) and enforce 90%+ cell completeness."}
                {s.domain_number === 6 && "Convert tabular files to Parquet, upload data dictionaries, and link dataset generation pipelines."}
                {s.domain_number === 7 && "Apply de-identification tools, configure k-anonymity (k >= 10), or implement differential privacy controls."}
                {s.domain_number === 8 && "Implement secure role-based access mechanisms and require signed Data Use Agreements (DUA) for access."}
                {s.domain_number === 9 && "Document data pipeline lineage changes and adopt a semantic versioning pattern."}
                {s.domain_number === 10 && "Obtain institutional ethics approvals, document consent models, and conduct equity analyses."}
                {s.domain_number === 11 && "Evaluate synthetic utility and run privacy leakage assessments on synthetic attributes."}
                {s.domain_number === 12 && "Appoint a designated data steward and ensure complete DPDP compliance rules are documented."}
                {s.domain_number === 13 && "Register the precise model IDs and weight versions trained or generated using this dataset."}
                {s.domain_number === 14 && "Compress dataset footprint or migrate to binary columnar layouts (e.g. Parquet) to save compute carbon costs."}
                {s.domain_number === 15 && "Provide a public repository for updates, host active issue logs, and establish a version changelog."}
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
