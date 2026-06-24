import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../lib/api/client";
import { useAuthStore } from "../stores/auth";
import { ApiKey, User } from "../lib/types";

export function useLogin() {
  const queryClient = useQueryClient();
  const fetchUser = useAuthStore((state) => state.fetchUser);

  return useMutation({
    mutationFn: async (credentials: Record<string, string>) => {
      // API expects form-data for username/password login
      const formData = new FormData();
      formData.append("username", credentials.email);
      formData.append("password", credentials.password);
      
      return api.post<void>("/api/v1/auth/login", formData);
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
    queryFn: () => api.get<ApiKey[]>("/api/v1/auth/keys"),
  });
}

export function useCreateApiKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (name: string) => api.post<{ api_key: string }>("/api/v1/auth/keys", { name }),
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
