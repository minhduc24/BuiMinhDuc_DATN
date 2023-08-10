<template>
  <canvas ref="rulerCanvas" :width="width" :height="height"></canvas>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      required: true
    },
    height: {
      type: Number,
      required: true
    },
    color: {
      type: String,
      default: '#000'
    },
    spacing: {
      type: Number,
      default: 10
    },
    unit: {
      type: String,
      default: 's'
    },
    timeScale: {
      type: Number,
      default: 1
    }
  },
  mounted() {
    this.drawRuler();
  },
  methods: {
    drawRuler() {
      const canvas = this.$refs.rulerCanvas;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = this.color;
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';

      const spacing = this.spacing * this.timeScale;
      const count = Math.ceil(this.width / spacing);

      for (let i = 0; i <= count; i++) {
        const x = i * spacing;
        const time = i * this.spacing;
        const text = time.toFixed(1) + ' ' + this.unit;

        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, 10);
        ctx.stroke();

        ctx.fillText(text, x, 12);
      }
    }
  }
}
</script>