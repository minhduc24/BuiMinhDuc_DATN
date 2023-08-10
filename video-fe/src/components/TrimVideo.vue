<template>
  <v-app>
    <v-layout class="bg-blue">
      <v-app-bar :elevation="0" height="40">
        <v-btn
          density="compact"
          icon="mdi-keyboard-backspace"
          @click="backToStudio"
        ></v-btn>
        <v-text-field
          density="compact"
          variant="outlined"
          label="Untitled"
          single-line
          hide-details
          style="max-width: 150px"
          class="ml-15"
          v-model="state.projectInfor.pname"
        ></v-text-field>

        <v-btn variant="outlined" class="ml-5" @click="saveProjet()"
          >Save</v-btn
        >
      </v-app-bar>

      <v-row no-gutters>
        <v-col cols="2" style="height: 100%; background: yellowgreen">
          <file
            :pid="id"
            :videos="state.videos"
            :drawer="menuContentsLeft[0].status"
            @moveSourceVideo="moveSourceVideo"
            @removeVideo="removeVideo"
          />
          <record-and-create :drawer="menuContentsLeft[1].status" />
          <teamplate-video :drawer="menuContentsLeft[2].status" />
        </v-col>

        <v-col cols="8" style="height: 100%; background-color: #161616">
          <v-row no-gutters>
            <v-col cols="2"> </v-col>
            <v-col cols="8" class="mt-7">
              <video-player
                class="mt-5"
                :sources="sourceVideo"
                :vid="vid"
                @add-frames="addFrames"
                :currentt="currentt"
                :pause="pause"
                :time-change="timeChange"
                :position-image="positionImage.value"
                @add-image-postion="positionImgToEdit"
              />
              <div class="d-flex flex justify-center">
                <v-btn
                  class="mx-3"
                  style="background-color: #161616"
                  icon="mdi-skip-backward"
                  @click="firstTimeVid"
                  variant="text"
                ></v-btn>
                <v-btn
                  class="mx-3"
                  style="background-color: #161616"
                  icon="mdi-rewind-outline"
                  @click="minusTimeSecond"
                  variant="text"
                ></v-btn>
                <v-btn
                  class="mx-3"
                  style="background-color: #161616"
                  :icon="pause"
                  @click="changeButton"
                  variant="text"
                ></v-btn>
                <v-btn
                  class="mx-3"
                  style="background-color: #161616"
                  icon="mdi-fast-forward-outline"
                  @click="addTimeSecond"
                  variant="text"
                ></v-btn>
                <v-btn
                  class="mx-3"
                  style="background-color: #161616"
                  icon="mdi-skip-forward"
                  @click="endTimeVid"
                  variant="text"
                ></v-btn>
              </div>
            </v-col>
            <v-col cols="2"> </v-col>
          </v-row>
        </v-col>

        <v-col cols="2" style="height: 100%; background-color: paleturquoise">
          <video-edit
            :param-video="paramsVideoSrc"
            :sources="sourceVideo"
            :vid="vid"
            :start-time-vid="startTime"
            :end-time-vid="endTime"
            @position-image="positionImgToPlayer"
            :position-imageeeee="pImg.value"
          />
        </v-col>
      </v-row>
    </v-layout>
    <v-footer class="bg-grey-darken-3 text-center d-flex flex-column">
      <video-trimmer
        v-if="check"
        :frames="videos.frames"
        :videoDuration="videos.duration"
        @trim-start="trimStart"
        @trim-end="trimEnd"
        @current-time="currentTime"
        :default-trim="defaultTrim"
      />
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref, reactive } from "vue";
import File from "@/views/navigation_left/File.vue";
import RecordAndCreate from "@/views/navigation_left/RecordAndCreate.vue";
import TeamplateVideo from "@/views/navigation_left/TeamplateVideo.vue";
import VideoMain from "@/components/VideoMain.vue";
import VideoEdit from "@/views/navigation_right/VideoEdit.vue";
import { useRoute } from "vue-router";
import axios from "axios";
import router from "@/router";
import VideoPlayer from "@/layouts/Canvas/VideoPlayer.vue";
import VideoTrimmer from "@/layouts/Canvas/VideoTrimmer.vue";
let loading = ref(false);

let menuContentsLeft = reactive([
  { id: 1, status: true },
  { id: 2, status: false },
  { id: 3, status: false },
]);
let paramsVideoSrc = reactive({});
let sourceVideo = reactive([]);
const pause = ref("mdi-play");

const route = useRoute();
const id = Number(route.params.id);

let state = reactive({
  videos: [],
  projectInfor: {
    pid: id,
    pname: "",
    metadata: {},
  },
});

let vid = ref(0);
let defaultTrim = reactive({})
axios
  .get(`/projects/${id}`)
  .then((response) => {
    state.projectInfor.pname = response.data.project.project_name
      ? response.data.project.project_name
      : "Untitled";
    let pInfor = JSON.parse(response.data.project.project_information);
    if (Object.keys(pInfor).length !== 0) {
      defaultTrim.start = pInfor.video.vid_start
      defaultTrim.end = pInfor.video.vid_end 
      startTime.value = pInfor.video.vid_start;
      endTime.value = pInfor.video.vid_end;
      let srcVid = {
        id: pInfor.video.vid_id,
        src: pInfor.video.vid_src,
        type: pInfor.video.vid_type,
        pId: route.params.id,
        pName: response.data.project.project_name
      };
      paramsVideoSrc.src =  pInfor.video.vid_src
      paramsVideoSrc.name = pInfor.video.vid_name
      sourceVideo.push(srcVid);
    }
    // for videos
    let videos = response.data.videos ? response.data.videos : [];
    state.videos = videos.map((video, index) => {
      return {
        id: video.id,
        title: video.video_name,
        src: video.s3_url,
        flex: 6,
        type: video.video_type,
      };
    });
  })
  .catch(function (error) {
    console.log(error);
  });


const moveSourceVideo = (src, id, type) => {
  let srcVid = {
    id: id,
    src: src,
    type: type,
    pId: route.params.id,
    pName: state.projectInfor.pname,
  };
  sourceVideo = []
  sourceVideo.push(srcVid);
  vid.value = id;
  if (type == "mp4") {
    paramsVideoSrc.src = src;
    paramsVideoSrc.name = src.slice(85);
  }
};

const removeVideo = (id) => {
  state.videos = state.videos.filter((video) => video.id != id);
  axios
    .patch(`videos/${id}`)
    .then((response) => {
      console.log(response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
};

const backToStudio = () => {
  window.location.href = "/studio";
};

const check = ref(false);
const videos = reactive({
  frames: [],
  duration: 0,
  vid: 0,
});
const addFrames = (player) => {
  videos.frames = player.frames;
  videos.duration = player.duration;
  videos.vid = player.vid;

  if (videos.frames.length) {
    check.value = true;
  }
};

const saveProjet = () => {
  let hienTai = {
    video: {
      vid_start: startTime.value,
      vid_end: endTime.value,
      vid_src: paramsVideoSrc.src,
      vid_type: "mp4",
      vid_id: vid.value,
      vid_name: paramsVideoSrc.src.slice(85),
      vid_length: videos.duration
    },
  };
  console.log(222, hienTai);
  state.projectInfor.metadata = JSON.stringify(hienTai);
  axios
    .put(`/projects/${id}`, state.projectInfor)
    .then((response) => {
      console.log(9999, response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
};

const startTime = ref(0);
const trimStart = (start) => {
  startTime.value = parseFloat(start.toFixed(1));
};

const endTime = ref(0);
const trimEnd = (end) => {
  endTime.value = parseFloat(end.toFixed(1));
};

const currentt = ref(0);
const currentTime = (curTime) => {
  currentt.value = curTime;
};

const changeButton = () => {
  pause.value = pause.value == "mdi-pause" ? "mdi-play" : "mdi-pause";
};

const timeChange = ref(0);
const firstTimeVid = () => {
  timeChange.value = timeChange.value == 1 ? 5 : 1;
};
const minusTimeSecond = () => {
  timeChange.value = timeChange.value == 2 ? 6 : 2;
};
const addTimeSecond = () => {
  timeChange.value = timeChange.value == 3 ? 7 : 3;
};
const endTimeVid = () => {
  timeChange.value = timeChange.value == 4 ? 8 : 4;
};

let positionImage = reactive({});
const positionImgToPlayer = (posImg) => {
  positionImage.value = posImg;
};

let pImg = reactive({});
const positionImgToEdit = (posImg) => {
  pImg.value = posImg;
};
</script>

<style>
.fs-text {
  font-size: 0.5rem !important;
  white-space: normal !important;
}
</style>
