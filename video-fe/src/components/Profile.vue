<template>
  <div class="center-div">
    <v-alert v-if="showAlertOk" type="success" dismissible >
      Cập nhật thông tin người dùng thành công!
    </v-alert>
    <v-alert v-if="showAlertNok" type="error" dismissible >
      Cập nhật thông tin người dùng thất bại!
    </v-alert>
      <form @submit.prevent="submit">
    <v-text-field
      v-model="name.value.value"
      :counter="10"
      :error-messages="name.errorMessage.value"
      label="Tên người dùng"
    ></v-text-field>

    <v-text-field
      v-model="password.value.value"
      :counter="7"
      :error-messages="password.errorMessage.value"
      label="Mật khẩu"
    ></v-text-field>

    <v-text-field
      v-model="email.value.value"
      :error-messages="email.errorMessage.value"
      label="Email"
    ></v-text-field>

    <v-btn
      class="me-4"
      type="submit"
    >
      Thay đổi
    </v-btn>

    <v-btn @click="handleReset">
      Làm mới
    </v-btn>
  </form>
  </div>

</template>

<script setup>
  import { ref } from 'vue'
  import { useField, useForm } from 'vee-validate'
  import axios from 'axios';
  const { handleSubmit, handleReset } = useForm({
    validationSchema: {
      password (value) {
        if (value?.length > 5 && /[0-9-]+/.test(value)) return true

        return 'Mật khẩu phải có ít nhất 6 kí tự'
      },
      email (value) {
        if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true

        return 'Email không hợp lệ'
      },
    },
  })
  const name = useField('name')
  const password = useField('password')
  const email = useField('email')
  const showAlertOk = ref(false)
  const showAlertNok = ref(false)

  const submit = handleSubmit(values => {
    let params = {
      id: localStorage.getItem('userId'),
      name: name.value.value,
      password: password.value.value,
      email: email.value.value
    }

    axios.put(`/users/${params.id}`, params)
    .then((response) => {
      if(response.data.message == 'OK') {
        localStorage.setItem("name", name.value.value);
        showAlertOk.value = true
        location.reload()
      }
      if(response.data.message == 'NOK') showAlertNok.value = true
    })
    .catch(function (error) {
      console.log(error);
    });
  })

  if (localStorage.getItem("token") != null) {
      name.value.value = localStorage.getItem('name')
      email.value.value = localStorage.getItem('email')
    }
</script>

<style>

    .center-div {
      margin: auto;
      width: 450px;
    }
  </style>