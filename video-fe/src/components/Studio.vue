<template>
  <v-main>
    <v-container>
      <h1 class="mt-7 headline font-weight-black mb-5">Cắt video</h1>
      <h1 class="text-subtitle-1 font-weight-black">
        Một số mẫu bạn có thể thích !!!
      </h1>
      <v-row>
        <v-col v-for="(video, index) in videos" :key="index" cols="2">
          <v-img
            :src="video.thumbnail"
            @click="openPopup(video)"
            :width="300"
            height="125"
            aspect-ratio="16/9"
            cover
          ></v-img>
          <v-card-title class="text-h6">
              {{ video.name }}
            </v-card-title>
        </v-col>
      </v-row>

      <v-dialog
        v-model="showPopup"
        max-width="800"
        hide-overlay
        transition="dialog-bottom-transition"
      >
        <v-card>
          <v-card-text>
            <video controls :src="currentVideo.url" width="640" height="360">
              Your browser does not support HTML5 video.
            </video>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" text @click="closePopup">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <div class="d-flex flex-wrap justify-space-between mt-5">
        <h1 class="text-subtitle-1 font-weight-black">MẪU CỦA TÔI</h1>
        <v-btn class="bg-teal-accent-2" @click="trimVideoPage">
          Tạo Teamplate
        </v-btn>
      </div>
      <v-alert v-if="error" type="error" dismissible>
        {{ error }}
      </v-alert>
      <v-row class="mt-3" dense>
        <v-col cols="12" v-for="project in state.projects">
          <v-card color="#4D4D4F" theme="dark">
            <v-card-title class="text-h5"> {{ project.name }} </v-card-title>
            <v-card-actions>
              <!-- <v-btn class="ms-2" variant="outlined" size="small"> Thêm </v-btn> -->
              <v-btn
                class="ms-2"
                variant="outlined"
                size="small"
                @click="editVideoPage(project)"
              >
                Chỉnh sửa
              </v-btn>
              <v-btn
                class="ms-2"
                variant="outlined"
                size="small"
                @click="deleteProject(project.id)"
              >
                Xóa
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref } from "vue";
import { reactive } from "vue";
import axios from "axios";
import router from "@/router";
const videos = reactive([
  {
    thumbnail: "https://videoaws.s3.ap-southeast-1.amazonaws.com/catt.jpg",
    url: "https://videoaws.s3.ap-southeast-1.amazonaws.com/cat_template.mp4",
    name: 'Loài Mèo'
  },
  {
    thumbnail: "https://videoaws.s3.ap-southeast-1.amazonaws.com/thiennga.jpg",
    url: "https://videoaws.s3.ap-southeast-1.amazonaws.com/thien_nga.mp4",
    name: 'Thiên Nga'
  },
  {
    thumbnail: "https://videoaws.s3.ap-southeast-1.amazonaws.com/dog.jpg",
    url: "https://videoaws.s3.ap-southeast-1.amazonaws.com/dogs.mp4",
    name: 'Loài chó'
  },
  {
    thumbnail: "https://videoaws.s3.ap-southeast-1.amazonaws.com/red_bear.jpg",
    url: "https://videoaws.s3.ap-southeast-1.amazonaws.com/bearr.mp4",
    name: "Gấu đỏ"
  },
  {
    thumbnail: "https://videoaws.s3.ap-southeast-1.amazonaws.com/panda.jpg",
    url: "https://videoaws.s3.ap-southeast-1.amazonaws.com/panda.mp4",
    name: "Gấu trúc"
  },
  {
    thumbnail: "https://videoaws.s3.ap-southeast-1.amazonaws.com/birdd.jpg",
    url: "https://videoaws.s3.ap-southeast-1.amazonaws.com/bird.mp4",
    name: 'Loài chim'
  },
  // Thêm các video khác vào đây
]);

const showPopup = ref(false);
const currentVideo = ref(null);

const openPopup = (video) => {
  currentVideo.value = video;
  showPopup.value = true;
};
const closePopup = () => {
  showPopup.value = false;
};

let state = reactive({
  projects: [],
  project_infor: {},
});

let error = ref(null);

const userId = localStorage.getItem("userId");
axios
  .get(`projects?user_id=${userId}`)
  .then((response) => {
    let projects = response.data ? response.data : [];
    state.projects = projects.map((project, index) => {
      return (state.project_infor = {
        id: project.id,
        name: project.project_name,
        pinfor: project.project_information,
        ps3_url: project.s3_url,
      });
    });
  })
  .catch(function (error) {
    console.log(error);
  });

const trimVideoPage = () => {
  if (!localStorage.getItem("userId")) {
    error.value = "Vui lòng đăng nhập để sử dụng tính năng này";
    return;
  }

  let data = {
    project_name: "Untitled",
    user_id: localStorage.getItem("userId"),
    project_information: "{}",
    s3_url: "",
  };

  axios
    .post("projects", data)
    .then((response) => {
      let id = response.data.id;
      router.push({ path: `/trim-video/${id}` });
    })
    .catch(function (error) {
      console.log(error);
    });
};

const editVideoPage = (project) => {
  router.push({ path: `/trim-video/${project.id}` });
};

const deleteProject = (projectId) => {
  axios
    .patch(`projects/${projectId}`)
    .then((response) => {
      location.reload();
    })
    .catch(function (error) {
      console.log(error);
    });
};
</script>
