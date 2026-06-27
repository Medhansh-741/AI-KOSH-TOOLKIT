"use client"

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAssessments } from "@/hooks/use-assessment";
import { useApiKeys, useCreateApiKey, useRevokeApiKey } from "@/hooks/use-auth";
import ScoreHistory from "@/components/score-history";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, Key, Calendar, Eye, Trash2, Clipboard, Check, Database, HelpCircle, ShieldAlert } from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const { data: assessments = [], isLoading: isLoadingAssessments } = useAssessments();
  const { data: apiKeys = [], isLoading: isLoadingKeys } = useApiKeys();
  const createApiKeyMutation = useCreateApiKey();
  const revokeApiKeyMutation = useRevokeApiKey();

  const [newKeyName, setNewKeyName] = useState("");
  const [createdKeyRaw, setCreatedKeyRaw] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleCreateKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim()) return;
    try {
      const res = await createApiKeyMutation.mutateAsync({ owner_name: newKeyName, role: "submitter" });
      setCreatedKeyRaw(res.raw_key);
      setNewKeyName("");
    } catch (err) {
      console.error(err);
    }
  };

  const handleRevokeKey = async (keyId: string) => {
    if (confirm("Are you sure you want to revoke this API key? External systems using it will be cut off immediately.")) {
      try {
        await revokeApiKeyMutation.mutateAsync(keyId);
      } catch (err) {
        console.error(err);
      }
    }
  };

  const handleCopyKey = () => {
    if (createdKeyRaw) {
      navigator.clipboard.writeText(createdKeyRaw);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Stats calculation
  const totalAssessments = assessments.length;
  const completedAssessments = assessments.filter(a => a.status === "complete").length;
  const processingAssessments = assessments.filter(a => a.status === "processing" || a.status === "queued").length;

  return (
    <div className="space-y-8">
      {/* Dashboard Top Row */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Quality & Privacy Dashboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Submit datasets for evaluation, review historical assessment runs, and manage developer keys.
          </p>
        </div>
        <Link href="/upload" passHref>
          <Button className="bg-indigo-600 hover:bg-indigo-500 text-slate-100 text-xs font-semibold py-5 shadow-lg shadow-indigo-650/15">
            <Plus className="h-4 w-4 mr-1.5" /> New Assessment
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="bg-slate-900/40 border-slate-850">
          <CardHeader className="pb-2">
            <CardDescription className="text-xs uppercase tracking-wider font-semibold text-slate-400">Total Runs</CardDescription>
            <CardTitle className="text-3xl font-black text-slate-100">{totalAssessments}</CardTitle>
          </CardHeader>
          <CardContent>
            <span className="text-[10px] text-slate-500 font-medium">All dataset evaluations submitted</span>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/40 border-slate-850">
          <CardHeader className="pb-2">
            <CardDescription className="text-xs uppercase tracking-wider font-semibold text-slate-400">Completed</CardDescription>
            <CardTitle className="text-3xl font-black text-emerald-400">{completedAssessments}</CardTitle>
          </CardHeader>
          <CardContent>
            <span className="text-[10px] text-slate-500 font-medium">Reports generated successfully</span>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/40 border-slate-850">
          <CardHeader className="pb-2">
            <CardDescription className="text-xs uppercase tracking-wider font-semibold text-slate-400">Processing</CardDescription>
            <CardTitle className="text-3xl font-black text-sky-400">{processingAssessments}</CardTitle>
          </CardHeader>
          <CardContent>
            <span className="text-[10px] text-slate-500 font-medium">Evaluating pipelines/scorers...</span>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/40 border-slate-850">
          <CardHeader className="pb-2">
            <CardDescription className="text-xs uppercase tracking-wider font-semibold text-slate-400">API Keys</CardDescription>
            <CardTitle className="text-3xl font-black text-indigo-400">{apiKeys.length}</CardTitle>
          </CardHeader>
          <CardContent>
            <span className="text-[10px] text-slate-500 font-medium">Active integration endpoints</span>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Assessment Runs Table */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center gap-2">
            <Database className="h-5 w-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-slate-100">Historical Assessments</h2>
          </div>
          
          {isLoadingAssessments ? (
            <div className="h-64 rounded-xl border border-slate-800 bg-slate-900/20 flex flex-col items-center justify-center gap-2">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
              <span className="text-xs text-slate-400 font-medium">Retrieving evaluations...</span>
            </div>
          ) : (
            <ScoreHistory
              assessments={assessments}
              onSelect={(id) => router.push(`/dashboard/${id}`)}
            />
          )}
        </div>

        {/* API Key Management */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Key className="h-5 w-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-slate-100">API Keys</h2>
          </div>

          <Card className="bg-slate-900/60 backdrop-blur-md border-slate-800 shadow-xl">
            <CardHeader className="pb-4 border-b border-slate-850">
              <CardTitle className="text-sm font-bold text-slate-200">Developer Integrations</CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Create Bearer API keys to trigger assessment evaluations programmatically.
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-4 space-y-4">
              {/* Display newly created key alert */}
              {createdKeyRaw && (
                <div className="p-3.5 rounded-lg bg-indigo-950/20 border border-indigo-500/30 text-slate-200 space-y-2.5">
                  <div className="flex items-start gap-2">
                    <ShieldAlert className="h-4 w-4 text-indigo-400 mt-0.5 shrink-0" />
                    <div className="text-[11px] font-semibold text-indigo-300">
                      Copy this key now. It will not be shown again.
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      readOnly
                      value={createdKeyRaw}
                      className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 font-mono text-[10px] text-indigo-400 select-all focus:outline-none"
                    />
                    <Button
                      size="sm"
                      onClick={handleCopyKey}
                      className="bg-indigo-600 hover:bg-indigo-500 text-xs px-2 h-7 rounded"
                    >
                      {copied ? <Check className="h-3 w-3" /> : <Clipboard className="h-3 w-3" />}
                    </Button>
                  </div>
                </div>
              )}

              {/* Generate Key Form */}
              <form onSubmit={handleCreateKey} className="flex gap-2">
                <Input
                  placeholder="Key name (e.g. AIKosh Production)"
                  value={newKeyName}
                  onChange={(e) => setNewKeyName(e.target.value)}
                  className="bg-slate-950 border-slate-800 text-xs h-9"
                />
                <Button
                  type="submit"
                  disabled={createApiKeyMutation.isPending || !newKeyName.trim()}
                  className="bg-indigo-600 hover:bg-indigo-500 text-xs h-9"
                >
                  Generate
                </Button>
              </form>

              {/* List of keys */}
              {isLoadingKeys ? (
                <div className="flex justify-center py-4">
                  <div className="h-5 w-5 animate-spin rounded-full border border-indigo-500 border-t-transparent"></div>
                </div>
              ) : apiKeys.length === 0 ? (
                <p className="text-xs text-slate-500 text-center py-4">No active API keys created.</p>
              ) : (
                <div className="space-y-2.5">
                  {apiKeys.map((key) => (
                    <div
                      key={key.key_id}
                      className="flex items-center justify-between p-3 rounded-lg border border-slate-850 bg-slate-950/40 hover:bg-slate-950/70 transition-all"
                    >
                      <div className="space-y-0.5 max-w-[70%]">
                        <span className="text-xs font-bold text-slate-350 block truncate">{key.owner_name}</span>
                        <div className="flex items-center gap-1 text-[10px] text-slate-500">
                          <span className="font-mono bg-slate-900 border border-slate-800 px-1 rounded text-indigo-400">
                            {key.key_prefix}...
                          </span>
                          <span>•</span>
                          <span>Created {new Date(key.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleRevokeKey(key.key_id)}
                        className="text-rose-500 hover:text-rose-400 hover:bg-rose-500/10 h-8 w-8 p-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
