import { create } from 'zustand';

const useUserStore = create((set) => ({
  loggedIn: false,
  user: JSON.parse(localStorage.getItem('userDetail')) || {
    email: '',
    first_name: '',
    last_name: '',
    nickname: '',
    gender: '',
    avatar: '',
  },
  team: null,
  setLoggedIn: (loggedIn) => set({ loggedIn }),
  setUser: (user) => set({ user }),
  setTeam: (team) => set({ team }),
}));

export default useUserStore;
