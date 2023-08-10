<template>
    <v-navigation-drawer
        permanent
        theme="dark"
        class="ml"
        v-model="props.drawer"
    >
    </v-navigation-drawer>
</template>

<script setup>
    const props = defineProps({
        drawer: {
            type: Boolean,
            default: true
        }
    })
</script>

<style>

</style>
<!-- import 'video.js/dist/video-js.css'; -->