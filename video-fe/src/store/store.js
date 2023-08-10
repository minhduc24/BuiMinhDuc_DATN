import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      currentTime: 0,
      frames: []
    };
  },
  mutations: {
    setCurrentTime(state, time) {
      state.currentTime = time;
    },
    setFrames(state, frames) {
      state.frames = frames;
    }
  },
  getters: {
    currentTime: state => state.currentTime,
    frames: state => state.frames
  }
});

export default store;