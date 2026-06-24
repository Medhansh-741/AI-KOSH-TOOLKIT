"use client"

import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useLogin } from "../../../hooks/use-auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Database, LogIn } from "lucide-react";

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email address."),
  password: z.string().min(6, "Password must be at least 6 characters."),
});

type LoginValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const { mutate: login, isPending, error } = useLogin();

  const form = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = (data: LoginValues) => {
    login(data, {
      onSuccess: () => {
        router.push("/upload");
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
            <CardTitle className="text-2xl font-bold tracking-tight text-white">Welcome back</CardTitle>
            <CardDescription className="text-slate-400">
              Sign in to assess your health research dataset quality
            </CardDescription>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="mb-4 rounded-lg border border-rose-500/20 bg-rose-500/5 p-3 text-xs font-semibold text-rose-400">
                {error.message || "Invalid credentials. Please try again."}
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
                          disabled={isPending}
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
                          disabled={isPending}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-rose-400" />
                    </FormItem>
                  )}
                />

                <Button
                  type="submit"
                  className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition"
                  disabled={isPending}
                >
                  {isPending ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></div>
                  ) : (
                    <LogIn className="h-4 w-4 mr-2" />
                  )}
                  Sign In
                </Button>
              </form>
            </Form>
          </CardContent>
          <CardFooter className="flex justify-center border-t border-white/5 pt-4">
            <span className="text-xs text-slate-400">
              Don&apos;t have an account?{" "}
              <Link href="/register" className="font-bold text-indigo-400 hover:underline">
                Create one
              </Link>
            </span>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
