"use client"

import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useRegister } from "../../../hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Database, UserPlus } from "lucide-react";

const registerSchema = z.object({
  email: z.string().email("Please enter a valid email address."),
  password: z.string().min(6, "Password must be at least 6 characters."),
  role: z.enum(["user", "reviewer", "admin"]),
});

type RegisterValues = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const { mutate: register, isPending, error } = useRegister();
  const [success, setSuccess] = useState(false);

  const form = useForm<RegisterValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      password: "",
      role: "user",
    },
  });

  const onSubmit = (data: RegisterValues) => {
    register(data, {
      onSuccess: () => {
        setSuccess(true);
        setTimeout(() => {
          router.push("/upload");
        }, 1500);
      },
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="relative w-full max-w-md">
        {/* Glow decoration */}
        <div className="absolute -top-16 -left-16 h-48 w-48 rounded-full bg-indigo-500/10 blur-3xl"></div>
        <div className="absolute -bottom-16 -right-16 h-48 w-48 rounded-full bg-indigo-500/10 blur-3xl"></div>

        <Card className="border border-white/10 bg-slate-900/60 backdrop-blur-xl">
          <CardHeader className="space-y-2 text-center">
            <div className="flex justify-center mb-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                <Database className="h-5 w-5" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold tracking-tight text-white">Create an account</CardTitle>
            <CardDescription className="text-slate-400">
              Register to start evaluating research dataset quality
            </CardDescription>
          </CardHeader>
          <CardContent>
            {success && (
              <div className="mb-4 rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-3 text-xs font-semibold text-emerald-400">
                Account created successfully! Redirecting to login...
              </div>
            )}

            {error && (
              <div className="mb-4 rounded-lg border border-rose-500/20 bg-rose-500/5 p-3 text-xs font-semibold text-rose-400">
                {error.message || "Registration failed. Email might already exist."}
              </div>
            )}

            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-300">Email Address</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="name@example.com"
                          className="border-white/10 bg-slate-950 text-white placeholder-slate-600 focus-visible:ring-indigo-500"
                          disabled={isPending || success}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-rose-400" />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-300">Password</FormLabel>
                      <FormControl>
                        <Input
                          type="password"
                          placeholder="••••••••"
                          className="border-white/10 bg-slate-950 text-white placeholder-slate-600 focus-visible:ring-indigo-500"
                          disabled={isPending || success}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-rose-400" />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="role"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-300">Account Role</FormLabel>
                      <FormControl>
                        <select
                          className="w-full rounded-md border border-white/10 bg-slate-950 text-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
                          disabled={isPending || success}
                          value={field.value}
                          onChange={field.onChange}
                        >
                          <option value="user">Custodian / User</option>
                          <option value="reviewer">Reviewer</option>
                          <option value="admin">Administrator</option>
                        </select>
                      </FormControl>
                      <FormMessage className="text-rose-400" />
                    </FormItem>
                  )}
                />

                <Button
                  type="submit"
                  className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition"
                  disabled={isPending || success}
                >
                  {isPending ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></div>
                  ) : (
                    <UserPlus className="h-4 w-4 mr-2" />
                  )}
                  Create Account
                </Button>
              </form>
            </Form>
          </CardContent>
          <CardFooter className="flex justify-center border-t border-white/5 pt-4">
            <span className="text-xs text-slate-400">
              Already have an account?{" "}
              <Link href="/login" className="font-bold text-indigo-400 hover:underline">
                Sign In
              </Link>
            </span>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
