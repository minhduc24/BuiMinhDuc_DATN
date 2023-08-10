<template>
  <v-navigation-drawer
    permanent
    theme="blue"
    class="ml"
    v-model="props.drawer"
    location="right"
  >
    <v-card class="mx-auto" max-width="344" variant="outlined" title="Video">
      <v-card-item>
        <div>
          <!-- <v-text-field label="trim start"></v-text-field> -->
          <v-text-field
            readonly
            type="number"
            min="0"
            v-model="props.startTimeVid"
            label="bắt đầu"
          ></v-text-field>
          <v-text-field
            readonly
            type="number"
            min="0"
            v-model="props.endTimeVid"
            label="kết thúc"
          ></v-text-field>
        </div>
      </v-card-item>
    </v-card>

    <v-card
      class="mx-auto"
      max-width="344"
      variant="outlined"
      title="Image"
      v-show="videoCheck"
    >
      <v-card-item>
        <div class="d-flex justify-center">
          <v-row align="center" class="w-100">
            <v-col cols="6">
              <v-text-field
                type="number"
                v-model="positionImg.start"
                min="0"
                step="0.1"
                label="bắt đầu"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                type="number"
                v-model="positionImg.end"
                min="0"
                step="0.1"  
                label="kết thúc"
              ></v-text-field>
            </v-col>
          </v-row>
        </div>
        <div class="d-flex justify-center">
          <v-row align="center" class="w-100">
            <v-col cols="6">
              <v-text-field
                type="number"
                v-model="positionImg.horizontal"
                label="lệch ngang"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                type="number"
                v-model="positionImg.vertical"
                label="lệch dọc"
              ></v-text-field>
            </v-col>
          </v-row>
        </div>
        <v-col cols="6">
          <v-text-field
            v-model="positionImg.scale"
            type="number"
            label="Scale"
            min="0"
            step="0.01"
          ></v-text-field>
        </v-col>

        <!-- <div class="d-flex">
          <v-row align="center" class="w-100">
            <v-col cols="6">
              <v-text-field
                v-model="positionImg.width"
                type="number"
                label="độ dài"
                min="0"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="positionImg.height"
                type="number"
                label="chiều cao"
                min="0"
              ></v-text-field>
            </v-col>
          </v-row>
        </div> -->
      </v-card-item>
    </v-card>

    <v-btn variant="outlined" @click="exportVideo"> Xuất Video </v-btn>
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
  </v-navigation-drawer>
</template>

<script setup>
import axios from "axios";
import { watch, watchEffect } from "vue";
import { ref, reactive } from "vue";
const overlay = ref(false);
const props = defineProps({
  drawer: {
    type: Boolean,
    default: true,
  },
  sources: {
    type: Array,
    default: [],
  },
  vid: {
    type: Number,
    default: 0,
  },
  startTimeVid: {
    type: Number,
    default: 0,
  },
  endTimeVid: {
    type: Number,
    default: 0,
  },
  positionImageeeee: {
    type: Object,
    default: {},
  },
  imageHandle: {
    type: Object,
    default: {},
  },
  paramVideo: {
    type: Object,
    default: {},
  },
});

const options = reactive(["Crop", "Cover", "Contain", "None"]);

const positionImg = reactive({
  start: 0,
  end: 0,
  horizontal: 160,
  vertical: 90,
  fit: "Crop",
  scale: 0.5,
  width: 320,
  height: 180,
});

const exportVideo = () => {
  overlay.value = true;
  let sources = props.sources.filter((src) => src.id == props.vid);
  console.log(2222, sources, props.sources)
  let params = {
    videos: {
      start_time: props.startTimeVid,
      end_time: props.endTimeVid,
      s3_url: props.paramVideo.src,
      video_name: props.paramVideo.name,
      video_type: "mp4",
      pId: sources[0].pId,
      user_id: localStorage.getItem("userId"),
      pName: sources[0].pName,
    },
    images: props.positionImageeeee,
  };

  axios
    .post("http://127.0.0.1:8000/projects/edit", params)
    .then(function (response) {
      overlay.value = false;
      // console.log(223232, response.data)
      window.location.assign(response.data.s3_url);
    })
    .catch(function (error) {
      console.log(error);
    });
};

const emit = defineEmits(["position-image"]);
watch(
  () => positionImg,
  (newValue) => {
    emit("position-image", newValue);
    // console.log(newValue)
  },
  { deep: true }
);

const videoCheck = ref(false);
watch(
  () => props.positionImageeeee,
  (newValue) => {
    // Xử lý khi props.myObject thay đổi
    videoCheck.value = true;
  }
);
</script>

<style></style>
