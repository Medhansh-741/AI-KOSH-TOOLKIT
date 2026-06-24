import { create } from "zustand";
import { User } from "../lib/types";
import { api } from "../lib/api/client";

interface AuthState {
  user: User | null;
  loading: boolean;
  setUser: (user: User | null) => void;
  fetchUser: () => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: true,
  setUser: (user) => set({ user }),
  fetchUser: async () => {
    set({ loading: true });
    try {
      const user = await api.get<User>("/api/v1/auth/me");
      set({ user, loading: false });
    } catch (_) {
      set({ user: null, loading: false });
    }
  },
  logout: async () => {
    try {
      await api.post("/api/v1/auth/logout");
    } catch (_) {
      // ignore
    } finally {
      set({ user: null });
    }
  },
}));
