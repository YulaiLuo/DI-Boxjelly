import { create } from 'zustand'

const useMessageStore = create((set) => ({
  msgApi: null,
  setMsgApi: (msgApi) => set({ msgApi }),
}));

export default useMessageStore;
