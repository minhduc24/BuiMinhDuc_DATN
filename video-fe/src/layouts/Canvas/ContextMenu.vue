<template>
    <li>
      <h2>{{ item.name }}</h2>
      <p>{{ item.description }}</p>
    </li>
  </template>
  
  <script>
  export default {
    props: {
      item: Object
    }
  };
  </script>
  
  <style>
  li {
    padding: 4px;
    border: 1px solid #ccc;
    background-color: #fff;
  }
  </style>