import { create } from 'zustand';

const useUserStore = create((set) => ({
  loggedIn: false,
  user: null,
  setLoggedIn: (loggedIn) => set({ loggedIn }),
  setUser: (user) => set({user}),
}));

export default useUserStore;
