<template>
  <v-app>
    <header-view />
    <default-view />

  </v-app>
</template>

<script setup>
import HeaderView from '../Header/Header.vue'
import DefaultView from './View.vue'
// const loading = ref(false)
// const name = localStorage.getItem('name')

// const features = reactive([
//   { 
//     id: 1,
//     title: 'Cắt video',
//     content: 'Cắt phần đầu và phần cuối của video để tạo clip ngắn',
//     src: "https://cdn.vuetifyjs.com/images/cards/cooking.png"
//   },
//   {
//     id: 2,
//     title: 'Nén video',
//     content: 'Giảm kích thước tệp video bằng trình nén video trực tuyến',
//     src: "https://cdn.vuetifyjs.com/images/cards/cooking.png"
//   },
//   {
//     id: 3,
//     title: 'Hình ảnh trong ảnh',
//     content: 'Chỉnh sửa video kiểu ảnh trong ảnh (PiP)  ',
//     src: "https://cdn.vuetifyjs.com/images/cards/cooking.png"
//   },
//   {
//     id: 4,
//     title: 'Trình tạo video Pexels',
//     content: 'Chỉnh sửa video bằng cách tìm kiếm thư viện video Pexels',
//     src: "https://cdn.vuetifyjs.com/images/cards/cooking.png"
//   },
// ])

// const featurePage = (id) => {
//   if (id == 1) window.location.href="/trim-video"
// }

</script>

<style>

.pointerr{
  cursor: pointer;
}

</style>