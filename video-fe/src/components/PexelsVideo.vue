<template>
  <v-main>
    <v-container>
      <h1 class="center mt-7 headline font-weight-black mb-4">
        Chỉnh sửa video bằng cách tìm kiếm thư viện video Pexels
      </h1>

      <v-row>
        <v-col cols="6" class="bg-blue-lighten-4">
          <h2>Thông tin video</h2>
          <div class="left-column">
            <v-text-field
              v-model="search"
              label="Video về"
              placeholder="mèo, núi, người, ..."
              required
            ></v-text-field>
            <v-text-field
              v-model="title"
              label="Tên video"
              placeholder="về động vật, con người,..."
              required
            ></v-text-field>
            <v-select
              v-model="selectedValue"
              :items="items"
              @update:modelValue="updateSelectedValue"
              label="Chọn một bản nhạc"
            ></v-select>
            <v-btn @click="checkTimeout">Tạo Video</v-btn>
          </div>
        </v-col>
        <v-col cols="6">
          <div class="right-column">
            <video
              ref="videoPlayer"
              controls
              autoplay
              preload="auto"
              width="550"
              height="350"
            >
            </video>
          </div>
        </v-col>
      </v-row>
      <v-overlay
        persistent
        :model-value="overlay"
        class="align-center justify-center"
      >
        <v-progress-circular
          color="blue-grey"
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>

      <v-alert
    v-if="errorrr"
    type="error"
    title="Alert title"
    :text="errorTile"
  ></v-alert>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, watch } from "vue";
import { useField, useForm } from "vee-validate";
import axios from "axios";
import { reactive } from "vue";

const overlay = ref(false)
const selectedValue = ref(null);
const srcUrl = ref("");
const items = reactive(["Disco", "Freeflow", "Melodic"]);

const search = ref("");
const title = ref("");
let errorrr = ref(false)
let errorTile = ref('')
const checkTimeout = async () => {
      const timeout = 2 * 60 * 1000; 
      const timerPromise = new Promise((resolve, reject) => {
        setTimeout(() => {
          reject(new Error('Hàm đã chạy quá thời gian.'));
        }, timeout);
      });

      try {
        await Promise.race([timerPromise, createPexelsVideo()]);
      } catch (error) {
        errorrr.value = true
        errorTile.value = 'Không tìm thấy video'
        console.error(error);
        
      }
    }

const createPexelsVideo = () => {
  let data = {};
  data.search = search.value;
  data.title = title.value;
  data.soundtrack = selectedValue.value;
  overlay.value = true

  axios.post("/pexels", JSON.stringify(data))
    .then((response) => {
      if (response.data.status !== "success") {
        // showError(response.message);
        // $('#submit-video').prop('disabled', false);
        // console.log('errror')
        alert("Không tìm thấy video");
        overlay.value = false
      } else {
        getVideoShotStack(response.data.data.id);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
};



const getVideoShotStack = (id) => {
  axios.get(`/pexels/${id}`).then((response) => {
    let result = response.data
    // console.log(4444, result, 555, result.data)
    if (
      !(
        response.data.data.status === "done" ||
        response.data.data.status === "failed"
      )
    ) {
      setTimeout(function () {
        getVideoShotStack(id);
      }, 10 * 1000);
    } else if (response.data.data.status === "failed") {
      // console.log(1111, response.data.status);
    } else {
      // console.log(2222, response.data.data.url);
      const videoPlayer = document.querySelector("video");
      videoPlayer.src = response.data.data.url;
      overlay.value = false
      // resetForm();
    }
  });

  watch(srcUrl, (startTime, prevMessage) => {
    console.log("thay doi roi", startTime, prevMessage);
  });
};

//   const showError = (error) => {
//     {
//     updateStatus(null);

//     if (error.status === 400) {
//         var response = error.responseJSON;

//         if (response.data.isJoi) {
//             $.each(response.data.details, function(index, error) {
//                 if (error.context.key === 'search') {
//                     $('#search-group label, #search').addClass('text-danger is-invalid');
//                     $('#search-group').append('<div class="d-block invalid-feedback">Enter a subject keyword to create a video</div>').show();
//                 }

//                 if (error.context.key === 'title') {
//                     $('#title-group label, #title').addClass('text-danger is-invalid');
//                     $('#title-group').append('<div class="d-block invalid-feedback">Enter a title for your video</div>').show();
//                 }

//                 if (error.context.key === 'soundtrack') {
//                     $('#soundtrack-group label, #soundtrack').addClass('text-danger is-invalid');
//                     $('#soundtrack-group').append('<div class="d-block invalid-feedback">Please choose a soundtrack from the list</div>').show();
//                 }
//             });
//         } else if (typeof response.data === 'string') {
//             $('#errors').text(response.data).removeClass('d-hide').addClass('d-block');
//         } else {
//             $('#errors').text(unknownError).removeClass('d-hide').addClass('d-block');
//         }
//     } else {
//         $('#errors').text(unknownError).removeClass('d-hide').addClass('d-block');
//     }
// }
//   }
</script>

<style>
.center {
  text-align: center;
}

.left-column {
  align-self: flex-start;
}

.right-column {
  align-self: flex-end;
}
</style>
