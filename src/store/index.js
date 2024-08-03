// src/store/index.js
import Vue from "vue";
import Vuex from "vuex";
import tab from "./tab";

Vue.use(Vuex);

const stats = {
  state: {
    statistics: {},
  },
  mutations: {
    setStatistics(state, payload) {
      state.statistics = payload;
    },
  },
  getters: {
    statistics: (state) => state.statistics,
  },
};

export default new Vuex.Store({
  modules: {
    tab,
    stats,
  },
});
