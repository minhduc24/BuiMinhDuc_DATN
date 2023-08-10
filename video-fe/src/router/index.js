// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/components/Home.vue'),
      },
      {
        path: 'studio',
        name: 'Studio',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/components/Studio.vue'),
      },
      {
        path: 'pexels',
        name: 'Pexels',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/components/PexelsVideo.vue'),
      },
      { 
        name: 'history',
        path: 'history/:id',
        component: () => import('@/components/History.vue')
      },
      { 
        name: 'profile',
        path: 'profile',
        component: () => import('@/components/Profile.vue')
      },
    ],
  },
  {
    path: '/login',
    component: () => import('@/components/Login.vue')
  },
  {
    path: '/register',
    component: () => import('@/components/Register.vue')
  },
  {
    path: '/trim-video/:id',
    component: () => import('@/components/TrimVideo.vue')
  },
  {
    path: '/test',
    component: () => import('@/layouts/Canvas/VideoCanvas.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
