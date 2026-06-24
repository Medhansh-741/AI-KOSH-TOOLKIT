"use client"

import React from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api/client";
import { User } from "@/lib/types";
import { useAuthStore } from "@/stores/auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { ShieldCheck, ShieldAlert, ArrowLeft, Users, Calendar, Power, AlertOctagon } from "lucide-react";

export default function AdminPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user: currentUser } = useAuthStore();

  // Role Guard
  const isAdmin = currentUser?.role === "admin";

  const { data: users = [], isLoading, error } = useQuery<User[]>({
    queryKey: ["admin-users"],
    queryFn: () => api.get<User[]>("/api/v1/admin/users"),
    enabled: isAdmin, // Only fetch if user is admin
  });

  const toggleActiveMutation = useMutation({
    mutationFn: (userId: string) => api.post<User>(`/api/v1/admin/users/${userId}/toggle-active`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-users"] });
    },
  });

  const handleToggleActive = async (userId: string) => {
    try {
      await toggleActiveMutation.mutateAsync(userId);
    } catch (err: any) {
      alert(err.message || "Failed to update user status.");
    }
  };

  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch (_) {
      return dateStr;
    }
  };

  if (!isAdmin) {
    return (
      <div className="max-w-md mx-auto pt-16">
        <Card className="border-red-500/20 bg-red-950/10 p-6 text-center space-y-4">
          <AlertOctagon className="h-12 w-12 text-rose-500 mx-auto" />
          <CardTitle className="text-lg text-slate-200">Access Denied</CardTitle>
          <CardDescription className="text-sm text-slate-400">
            This administrator console is restricted to users with the administrator role only.
          </CardDescription>
          <Link href="/dashboard" passHref className="block mt-4">
            <Button variant="outline" className="border-slate-800 hover:bg-slate-900 text-xs">
              <ArrowLeft className="h-4 w-4 mr-1.5" /> Return to Dashboard
            </Button>
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-slate-850 pb-4">
        <Users className="h-7 w-7 text-indigo-400" />
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100">Administrator Console</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Manage user accounts, toggle active states, and monitor system enrollment.
          </p>
        </div>
      </div>

      {/* Users Card List */}
      <Card className="bg-slate-900/60 backdrop-blur-md border-slate-800 shadow-xl">
        <CardHeader className="pb-4">
          <CardTitle className="text-sm font-bold text-slate-200">Registered Users</CardTitle>
          <CardDescription className="text-xs text-slate-400">
            Administrators cannot read datasets or quality reports due to strict security guidelines.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex h-36 flex-col items-center justify-center gap-2">
              <div className="h-6 w-6 animate-spin rounded-full border border-indigo-500 border-t-transparent"></div>
              <span className="text-xs text-slate-400">Loading user catalog...</span>
            </div>
          ) : error ? (
            <p className="text-xs text-rose-400 text-center py-4">Failed to fetch users: {error.message}</p>
          ) : users.length === 0 ? (
            <p className="text-xs text-slate-500 text-center py-4">No users enrolled in system.</p>
          ) : (
            <div className="rounded-lg border border-slate-850 overflow-hidden bg-slate-950/20">
              <Table>
                <TableHeader className="bg-slate-950/50">
                  <TableRow className="border-b border-slate-850">
                    <TableHead className="font-bold text-slate-350 text-xs">Email Address</TableHead>
                    <TableHead className="font-bold text-slate-350 text-xs">Role</TableHead>
                    <TableHead className="font-bold text-slate-350 text-xs">Joined</TableHead>
                    <TableHead className="font-bold text-slate-350 text-xs">Status</TableHead>
                    <TableHead className="w-[100px]"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {users.map((u) => {
                    const isSelf = u.id === currentUser?.id;
                    return (
                      <TableRow key={u.id} className="border-b border-slate-850 hover:bg-slate-900/30">
                        <TableCell className="font-semibold text-slate-200 text-xs">{u.email}</TableCell>
                        <TableCell>
                          <Badge className={`text-[9px] font-bold rounded uppercase ${
                            u.role === "admin" 
                              ? "bg-purple-500/10 text-purple-400 border border-purple-500/20"
                              : u.role === "reviewer"
                              ? "bg-sky-500/10 text-sky-400 border border-sky-500/20"
                              : "bg-slate-500/10 text-slate-450 border border-slate-500/20"
                          }`}>
                            {u.role}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-xs text-slate-400 font-medium">
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3.5 w-3.5 text-slate-500" />
                            {formatDate(u.created_at)}
                          </span>
                        </TableCell>
                        <TableCell>
                          <Badge className={`text-[9px] font-bold rounded uppercase ${
                            u.is_active
                              ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                              : "bg-rose-500/10 text-rose-450 border border-rose-500/20"
                          }`}>
                            {u.is_active ? "Active" : "Suspended"}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">
                          {!isSelf && (
                            <Button
                              size="sm"
                              variant={u.is_active ? "destructive" : "default"}
                              onClick={() => handleToggleActive(u.id)}
                              disabled={toggleActiveMutation.isPending}
                              className={`text-[10px] font-bold h-7 px-2.5 ${
                                u.is_active
                                  ? "bg-rose-950/30 text-rose-400 hover:bg-rose-950/60 border border-rose-500/20"
                                  : "bg-emerald-950/30 text-emerald-400 hover:bg-emerald-950/60 border border-emerald-500/20"
                              }`}
                            >
                              <Power className="mr-1 h-3.5 w-3.5" />
                              {u.is_active ? "Suspend" : "Activate"}
                            </Button>
                          )}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
