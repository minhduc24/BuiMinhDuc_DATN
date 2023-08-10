<template>
  <div>
    <canvas ref="canvas" width="640" height="360"></canvas>

    <video width="0" height="0" ref="videoPlayer"></video>

    <div>Thời gian {{ showTime.toFixed(1) }} / {{ durationT.toFixed(1) }}</div>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
export default {
  name: "VideoPlayer",
  props: {
    sources: {
      type: Array,
      default: [],
    },
    vid: {
      type: Number,
      default: 0,
    },
    currentt: {
      type: Number,
      default: 0,
    },
    pause: {
      type: String,
      default: "mdi-play",
    },
    timeChange: {
      type: Number,
      default: 0,
    },
    positionImage: {
      type: Object,
      default: {},
    },
  },
  data() {
    return {
      player: null,
      canvas: null,
      context: null,
      numFrames: 14,
      trimmerData: {},
      durationT: 0,
      videoUrl: null,
      canvasDisplay: null,
      imgPosition: {
        start: null,
        end: null,
        x: 160,
        y: 90,
        height: 180,
        width: 320,
        scale: 0.5,
        horizontal: 0,
        vertical: 0,
        src: "",
      },
      showTime: 0,
    };
  },
  methods: {
    extractFrames() {
      let sources = this.vid == 0 ? this.sources : this.sources.filter((src) => src.id == this.vid);
      const video = document.createElement("video");
      video.crossOrigin = "anonymous";
      video.volume = 0;
      video.src = sources[0].src;
      video.play();
      const handleDurationChange = () => {
        const duration = video.duration;
        this.durationT = video.duration;
        const interval = duration / this.numFrames;
        let currentTime = 0;
        const frames = [];
        const actualVideoHeight = video.videoHeight;
        const actualVideoWidth = video.videoWidth;
        const thumbnailWidth = 200;
        const thumbnailHeight =
          (thumbnailWidth / actualVideoWidth) * actualVideoHeight;
        this.canvas.width = thumbnailWidth;
        this.canvas.height = thumbnailHeight;
        const extractFrame = () => {
          console.log(4444, currentTime);
          if (currentTime > duration || frames.length === this.numFrames) {
            this.trimmerData["frames"] = frames;
            this.trimmerData["duration"] = duration;
            this.trimmerData["vid"] = this.vid;
            this.$emit("add-frames", this.trimmerData);
            video.currentTime = 0;
            return;
          }
          currentTime += interval;
          video.currentTime = currentTime;
          this.context.drawImage(video, 0, 0, thumbnailWidth, thumbnailHeight);
          const dataUrl = this.canvas.toDataURL();
          frames.push(dataUrl);
          video.requestVideoFrameCallback(extractFrame);
        };
        video.requestVideoFrameCallback(extractFrame);
        video.currentTime = 0;
      };
      video.addEventListener("durationchange", handleDurationChange);
    },
    drawVideoToCanvas() {
      const ctx = this.canvasDisplay.getContext("2d");
      const width = this.canvasDisplay.width;
      const height = this.canvasDisplay.height;
      const video = this.player;
      video.onloadedmetadata = function () {
        function drawFrame() {
          requestAnimationFrame(drawFrame);
          ctx.drawImage(video, 0, 0, width, height);
        }
        drawFrame();
      };
    },
    drawImageToCanvas(posImg) {
      const ctx = this.canvasDisplay.getContext("2d");
      const image = new Image();
      image.src = this.videoUrl;
      posImg.height = this.canvasDisplay.height * posImg.scale;
      posImg.width = this.canvasDisplay.width * posImg.scale;
      this.imgPosition.vertical = +(
        (posImg.x * posImg.scale) /
        posImg.width
      ).toFixed(2);
      this.imgPosition.horizontal = -(
        (posImg.y * posImg.scale) /
        posImg.height
      ).toFixed(2);
      this.imgPosition.src = this.videoUrl;
      image.onload = function () {
        function drawFrame() {
          requestAnimationFrame(drawFrame);
          // ctx.drawImage(video, 0, 0, width, height)
          ctx.drawImage(image, posImg.x, posImg.y, posImg.width, posImg.height);
        }
        drawFrame();
      };
      this.$emit("add-image-postion", this.imgPosition);
    },
  },
  watch: {
    sources: {
      deep: true,
      handler: function (newValue) {
        console.log(2222, newValue)
        let id = this.vid == 0 ? newValue[0].id : this.vid;
        // console.log(22222, newValue[0], id)
        let videoSrc = newValue.filter((src) => src.id == id);
        // console.log(22111, videoSrc)
        if (videoSrc.length > 0) {
          if (videoSrc[0].type == "mp4") {
            this.player.src = videoSrc[0].src;
            this.player.load();
            this.extractFrames();
          } else {
            this.videoUrl = videoSrc[0].src;
            this.drawImageToCanvas(this.imgPosition);
          }
        }
      },
    },
    positionImage: {
      deep: true,
      handler: function (newValue) {
        this.imgPosition.start = parseFloat(newValue.start);
        this.imgPosition.end = parseFloat(newValue.end);
        this.imgPosition.x = Number(newValue.horizontal);
        this.imgPosition.y = Number(newValue.vertical);
        this.imgPosition.height = Number(newValue.height);
        this.imgPosition.width = Number(newValue.width);
        this.imgPosition.scale = Number(newValue.scale);
        this.drawImageToCanvas(this.imgPosition);
      },
    },
    currentt(newValue, oldValue) {
      this.player.currentTime = newValue;
      this.showTime = this.player.currentTime;
    },
    pause: {
      handler: function (newValue) {
        if (
          newValue == "mdi-play" &&
          this.player.src !=
            "https://videoaws.s3.ap-southeast-1.amazonaws.com/default.mp4"
        )
          this.player.pause();
        if (
          newValue == "mdi-pause" &&
          this.player.src !=
            "https://videoaws.s3.ap-southeast-1.amazonaws.com/default.mp4"
        )
          this.player.play();
      },
    },
    timeChange: {
      handler: function (newValue) {
        if (newValue == 1 || newValue == 5) this.player.currentTime = 0;
        if (newValue == 2 || newValue == 6) {
          let prevTime = this.player.currentTime - 5;
          this.player.currentTime = prevTime;
        }
        if (newValue == 3 || newValue == 7) {
          let prevTime = this.player.currentTime + 5;
          this.player.currentTime = prevTime;
        }
        if (newValue == 4 || newValue == 8)
          this.player.currentTime = this.durationT;
      },
    },
  },
  mounted() {
    this.canvas = document.createElement("canvas");
    this.context = this.canvas.getContext("2d");

    this.player = this.$refs.videoPlayer;
    this.player.src =
      "https://videoaws.s3.ap-southeast-1.amazonaws.com/default.mp4";

    this.player.ontimeupdate = () => {
      this.$store.commit("setCurrentTime", this.player.currentTime);
      this.showTime = this.player.currentTime;
    };

    this.canvasDisplay = this.$refs.canvas;
    this.drawVideoToCanvas();
  },
  beforeDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  },
};
</script>
