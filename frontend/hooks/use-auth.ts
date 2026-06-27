import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../lib/api/client";
import { useAuthStore } from "../stores/auth";
import { ApiKey, User } from "../lib/types";

export function useLogin() {
  const queryClient = useQueryClient();
  const fetchUser = useAuthStore((state) => state.fetchUser);

  return useMutation({
    mutationFn: async (credentials: Record<string, string>) => {
      return api.post<void>("/api/v1/auth/login", {
        email: credentials.email,
        password: credentials.password,
      });
    },
    onSuccess: async () => {
      await fetchUser();
      queryClient.invalidateQueries({ queryKey: ["user"] });
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: async (userData: Record<string, string>) => {
      return api.post<User>("/api/v1/auth/register", userData);
    },
  });
}

export function useApiKeys() {
  return useQuery<ApiKey[]>({
    queryKey: ["api-keys"],
    queryFn: async () => {
      const data = await api.get<{ keys: ApiKey[] }>("/api/v1/auth/keys");
      return data.keys;
    },
  });
}

export function useCreateApiKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ owner_name, role }: { owner_name: string; role: string }) =>
      api.post<{ raw_key: string }>("/api/v1/auth/keys", { owner_name, role }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["api-keys"] });
    },
  });
}

export function useRevokeApiKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (keyId: string) => api.delete<void>(`/api/v1/auth/keys/${keyId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["api-keys"] });
    },
  });
}
