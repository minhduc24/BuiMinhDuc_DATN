import mutations from "./mutations";
import acitons from "./acitons";
import getters from "./getters";

export default {
    namespaced: true,
    state() {
        return {
            name: 'Satel laa'
        };
    },
    mutations: mutations,
    getters: getters,
    actions: acitons,
}

