import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../Views/Main";
import Login from "../Views/Login.vue";
import Cookie from "js-cookie";

Vue.use(VueRouter);

const routes = [
  // 主路由
  {
    path: "/",
    name: "Main",
    component: Main,
    redirect: "/home", // 重定向
    children: [
      // 动态添加子路由
    ],
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
];

const router = new VueRouter({
  routes,
});

// 路由守卫:全局前置导航守卫
router.beforeEach((to, from, next) => {
  // 获取token
  const token = Cookie.get("token");

  if (!token && to.name !== "login") {
    next({ name: "login" });
    console.log("!token && to.name !== login")
  } else if (token && to.name === "login") {
    next({ name: "home" });
    console.log(token && to.name === "login");
  } else {
    next();
    console.log("else")
  }
});

export default router;
