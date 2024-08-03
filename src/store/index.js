// src/store/index.js
import Vue from "vue";
import Vuex from "vuex";
import tab from "./tab";

Vue.use(Vuex);

const stats = {
  state: {
    statistics: {},
    selectedApps: {
      ids: [],
      names: [],
    },
  },
  mutations: {
    setStatistics(state, payload) {
      state.statistics = payload;
    },
    setSelectedApps(state, payload) {
      state.selectedApps.ids = payload.ids;
      state.selectedApps.names = payload.names;
    },
  },
  getters: {
    statistics: (state) => state.statistics,
    selectedApps: (state) => state.selectedApps,
  },
};

export default new Vuex.Store({
  modules: {
    tab,
    stats,
  },
});
