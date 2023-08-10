<template>
  <v-navigation-drawer
    permanent
    v-model="props.drawer"
    style="background-color: #272731"
  >
    <v-row class="okokok" no-gutters style="height: 100px">
      <v-col v-for="(content, i) in contents" :key="i">
        <v-sheet
          class="mx-2 mt-3"
          style="color: white; background-color: #272731"
        >
          {{ content.title }}
        </v-sheet>
      </v-col>
      <v-col>
        <v-file-input
          density="compact"
          hide-input
          variant="filled"
          class="pa-2 mx-3"
          accept="image/* video/*"
          label="Nhập phương tiện"
          bg-color="#4F42C8"
          @change="selectImage"
        ></v-file-input>
      </v-col>
    </v-row>
    <!-- #272731 -->
    <v-card color="#272731" class="mt-3">
      <v-container fluid>
        <v-row dense>
          <v-col v-for="video in videos" :key="video.title" :cols="6">
            <v-card>
              <v-card-title
                style="
                  color: white;
                  font-size: 10px;
                  line-height: 0.5rem;
                  background-color: #272731;
                "
                v-text="video.title"
              ></v-card-title>
              <v-img
                :src="video.src"
                class="align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="75px"
                cover
                aspect-ratio="1"
                v-if="video.type === 'jpg' || video.type === 'png'"
              >
              </v-img>

              <video
                height="75"
                v-if="video.type === 'mp4'"
                loop
                autoplay
                muted
                style="display: block"
              >
                <source :src="video.src" />
              </video>

              <v-card-actions class="card-action">
                <v-btn
                  size="small"
                  color="surface-variant"
                  variant="text"
                  icon="mdi-plus"
                  @click="
                    $emit(
                      'moveSourceVideo',
                      video.src,
                      video.id,
                      video.type,
                      video.video_name
                    )
                  "
                ></v-btn>
                <v-btn
                  size="small"
                  color="surface-variant"
                  variant="text"
                  icon="mdi-minus"
                  @click="$emit('removeVideo', video.id)"
                ></v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-navigation-drawer>
</template>

<script setup>
import axios from "axios";
import { ref, reactive, watch } from "vue";
const props = defineProps({
  drawer: {
    type: Boolean,
    default: true,
  },
  videos: {
    type: Array,
    default: [],
  },
  pid: {
    type: Number,
    default: true,
  },
});

const contents = reactive([
  { title: "Tất cả" },
  { title: "Video" },
  { title: "Âm thanh" },
  { title: "Ảnh" },
]);

const addVideo = (source) => {
  console.log(666, source);
};

const selectImage = (e) => {
  const formData = new FormData();
  formData.append("pid", Number(props.pid));
  formData.append("file", e.target.files[0]);

  axios
    .post("uploads", formData)
    .then((response) => {
      let card_item = {
        title: response.data.video_name,
        src: response.data.s3_url,
        flex: 6,
        type: response.data.video_type,
        id: response.data.id,
      };
      props.videos.push(card_item);
    })
    .catch(function (error) {
      console.log(error);
    });
};
</script>

<style>
.card-action {
  min-height: 0 !important;
  justify-content: space-between;
  padding: 0 !important;
  height: 25px;
}

.file-input {
  height: 25px !important;
}
</style>
