import { create } from 'zustand';

const useUserStore = create((set) => ({
  loggedIn: false,
  user: null,
  team: null,
  setLoggedIn: (loggedIn) => set({ loggedIn }),
  setUser: (user) => set({ user }),
  setTeam: (team) => set({ team }),
}));

export default useUserStore;
