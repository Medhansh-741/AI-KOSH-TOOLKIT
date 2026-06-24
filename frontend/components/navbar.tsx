"use client"

import React from "react";
import Link from "next/link";
import { useAuthStore } from "../stores/auth";
import { Button } from "@/components/ui/button";
import { useRouter, usePathname } from "next/navigation";
import { ShieldCheck, LogOut, Upload, LayoutDashboard, Database } from "lucide-react";

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  if (!user) return null;

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/5 bg-slate-950/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Brand */}
        <Link href="/upload" className="flex items-center gap-2 font-bold text-white transition hover:opacity-90">
          <Database className="h-5 w-5 text-indigo-500" />
          <span className="tracking-wide">AIKOSH <span className="text-indigo-400">QUALITY TOOLKIT</span></span>
        </Link>

        {/* Navigation */}
        <nav className="flex items-center gap-6">
          <Link
            href="/upload"
            className={`flex items-center gap-1.5 text-sm font-semibold transition ${
              pathname === "/upload" ? "text-indigo-400" : "text-slate-300 hover:text-white"
            }`}
          >
            <Upload className="h-4 w-4" />
            Upload
          </Link>
          
          <Link
            href="/dashboard"
            className={`flex items-center gap-1.5 text-sm font-semibold transition ${
              pathname.startsWith("/dashboard") ? "text-indigo-400" : "text-slate-300 hover:text-white"
            }`}
          >
            <LayoutDashboard className="h-4 w-4" />
            Dashboard
          </Link>

          {user.role === "admin" && (
            <Link
              href="/admin"
              className={`flex items-center gap-1.5 text-sm font-semibold transition ${
                pathname === "/admin" ? "text-indigo-400" : "text-slate-300 hover:text-white"
              }`}
            >
              <ShieldCheck className="h-4 w-4 text-rose-400" />
              Admin
            </Link>
          )}
        </nav>

        {/* User Details & Action */}
        <div className="flex items-center gap-4">
          <div className="hidden sm:flex flex-col text-right">
            <span className="text-xs font-semibold text-slate-200">{user.email}</span>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{user.role}</span>
          </div>
          
          <Button
            variant="ghost"
            size="icon"
            onClick={handleLogout}
            className="text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg h-9 w-9"
            title="Log Out"
          >
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  );
}
