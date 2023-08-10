<template>
  <v-main>
      <v-container>
        <h1 class="mt-7 headline font-weight-black mb-4">
          Welcome {{ name }}
        </h1>
        <h1 class="text-subtitle-1">
          Get started with Shotstack and start creating videos at scale.
        </h1>
        <v-alert v-if="error" type="error" dismissible>
        {{ error }}
      </v-alert>
        <v-row no-gutters class="mt-5">
          <v-col v-for="feature in features" :key="feature.id" cols="12" sm="4">
            <v-card :loading="loading" max-width="374" class="pointerr mb-5" @click="featurePage(feature.id)">
              <template v-slot:loader="{ isActive }">
                <v-progress-linear :active="isActive" color="deep-purple" height="4" indeterminate></v-progress-linear>
              </template>

              <v-img cover height="250" :src=feature.src></v-img>

              <v-card-item>
                <v-card-title class="text-blue-lighten-1">{{ feature.title }}</v-card-title>
              </v-card-item>

              <v-card-text>
                <div> {{ feature.content }} </div>
              </v-card-text>
              <!-- <v-card-actions>
                <v-text class="rounded bg-grey-darken-4 text-body-2 px-2">3min</v-text>
              </v-card-actions> -->
            </v-card>
          </v-col>
        </v-row>

      </v-container>
    </v-main>
</template>

<script setup>
import { ref } from 'vue';
import { reactive } from 'vue';

const loading = ref(false)
const name = localStorage.getItem('name')
const features = reactive([
  { 
    id: 1,
    title: 'Cắt video',
    content: 'Cắt phần đầu và phần cuối của video để tạo clip ngắn',
    src: "https://play-lh.googleusercontent.com/1wsV3nIo9R1t1m6M1s69tJjNNVs4GZSNv3aeAfNflTey-InXKI3iwiYUI0zh2eFLDg"
  },
  {
    id: 4,
    title: 'Trình tạo video Pexels',
    content: 'Chỉnh sửa video bằng cách tìm kiếm thư viện video Pexels',
    src: "https://w7.pngwing.com/pngs/748/587/png-transparent-pexels-apps-platform-apps-icon.png"
  },
    {
    id: 3,
    title: 'Lịch sử',
    content: 'Xem lại lịch sử những video đã tạo',
    src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf_j4poEeNDaR7WFq5BkXbWcafxFSVMs4Ojw&usqp=CAU"
  },
])

let error = ref(null);
const featurePage = (id) => {
  if (!localStorage.getItem("userId")) 
  {
    error.value = "Vui lòng đăng nhập để sử dụng tính năng này";
    return
  } 
  else
  {
    if (id == 1) window.location.href="/studio"
    if (id == 3) {
      let id = localStorage.getItem("userId")
      window.location.href=`/history/${id}`
    }
    if (id == 4) window.location.href="/pexels"
  }
  
}
</script>

<style>

</style>