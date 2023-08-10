<template>
  <v-navigation-drawer
        rail
        permanent
      >
        <v-list-item
          prepend-avatar="https://images.sftcdn.net/images/t_app-icon-m/p/08cdb3e2-d4b5-45b6-ba19-7b1912767f64/879597640/clipchamp-video-editor-logo"
          title="Clipchamp"
          nav
        >
          <template v-slot:append>
            <v-btn
              variant="text"
              icon="mdi-chevron-left"
            ></v-btn>
          </template>
        </v-list-item>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item
            v-for="(menu, i) in menus"
            :key = i 
            :value="menu"
            active-color="primary"
            @click="$emit('changeMenuLeft', menu.id)"
          >
            <v-icon :icon="menu.icon"></v-icon>
            <v-list-item-title class="fs-text" v-text="menu.title"></v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
</template>

<script setup>
import { reactive } from 'vue';
  const menus = reactive([
    {id: 1, title: 'Phuong tien', icon: 'mdi-folder' },
    {id: 2, title: 'Ghi & tao', icon: 'mdi-video' },
    {id: 3, title: 'Màu', icon: 'mdi-apps' },
  ])

</script>

<style>
.aaa {
  width: 66px !important;
}
</style>