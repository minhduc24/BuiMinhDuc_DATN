<template>
  <v-row no-gutters>
    <v-col cols="2"> </v-col>
    <v-col cols="8" class="mt-7">
      <Vue3CanvasVideoPlayer
        :src="srcOfVideoMain"
        :muted="true"
        :autoplay="true"
        :loop="false"
        :range="range"
        :fps="30"
        :bbox="{
          data: {
            100: [
              { label: 'stone', xywh: [0, 200, 100, 400] },
              { label: 'flower', xywh: [50, 250, 160, 450] },
            ],
            101: [
              { label: 'stone', xywh: [1, 201, 101, 401] },
              { label: 'flower', xywh: [51, 251, 151, 451] },
            ],
            102: [
              { label: 'stone', xywh: [2, 202, 102, 402] },
              { label: 'flower', xywh: [52, 252, 152, 452] },
            ],
          },
          textColor: '#fff',
          fillColor: 'rgba(0, 0, 255, 0.5)',
          borderSize: 1,
          borderColor: 'rgba(255, 0, 0, 0.5)',
        }"
        :type="'contain'"
        :messageTime="1000"
        :preview="true"
        :darkMode="true"
      />
    </v-col>
    <v-col cols="2"> </v-col>
  </v-row>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import Vue3CanvasVideoPlayer from "vue3-canvas-video-player";
import "vue3-canvas-video-player/dist/style.css";

const props = defineProps({
  source: {
    type: Array,
    default: [],
  },
  range: {
    type: Array,
    default: [0, 0],
  },
  vid: {
    type: Number,
    default: 0
  }
});

const srcOfVideoMain = ref('')

watch(props.source, (newVal) => {
      console.log(2222, newVal);
      let videoMains = newVal.filter(src => src.id == props.vid)
      srcOfVideoMain.value = videoMains[0].src
      // console.log(5555, valuee, props.vid)
      // Do something with the updated items
    });
</script>

<style>
.fs-text {
  font-size: 0.5rem !important;
  white-space: normal !important;
}
</style>
