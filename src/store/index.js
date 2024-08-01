import Vue from "vue";
import Vuex from "vuex";
import tab from "./tab";

Vue.use(Vuex);

// 创建Vuex实例并导出
export default new Vuex.Store({
  modules: {
    tab,
  },
  state: {
    linkData: null,
    complianceData: null,
  },
  mutations: {
    setLinkData(state, data) {
      state.linkData = data;
    },
    setComplianceData(state, data) {
      state.complianceData = data;
    },
  },
  actions: {
    updateStats({ commit }, { linkData, complianceData }) {
      commit("setLinkData", linkData);
      commit("setComplianceData", complianceData);
    },
  },
});
