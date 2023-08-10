<template>
  <div>
    <ul>
      <context-menu v-for="(item, index) in items" :key="index" :item="item" />
    </ul>

    <button v-on:click="addItem">Add Item</button>
  </div>
</template>

<script>
import ContextMenu from './ContextMenu.vue';
export default {
  components: {
    ContextMenu
  },
  data() {
    return {
      items: [
        { id: 1, name: "Item 1", description: "Description 1" },
        { id: 2, name: "Item 2", description: "Description 2" },
        { id: 3, name: "Item 3", description: "Description 3" }
      ]
    };
  },
  methods: {
    addItem() {
      const newItem = {
        id: this.items.length + 1,
        name: "New Item",
        description: "New Description"
      };
      this.items.push(newItem);
    }
  }
};
</script>