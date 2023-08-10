<template>
  <v-container>
    <v-alert
      v-if="alertMessage.show"
      :type="alertMessage.type"
      :title="alertMessage.title"
    ></v-alert>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10">
        <v-card class="elevation-6 mt-10">
          <v-window v-model="step">
            <v-window-item :value="1">
              <v-row>
                <v-col cols="12" md="6">
                  <v-card-text class="mt-12">
                    <h4 class="text-center">Đăng nhập vào tài khoản của bạn</h4>
                    <v-alert v-if="error" type="error" dismissible>
                      {{ error }}
                    </v-alert>
                    <v-row align="center" justify="center">
                      <v-col cols="12" sm="8">
                        <v-text-field
                          label="Email"
                          outlined
                          dense
                          color="blue"
                          autocomplete="false"
                          class="mt-16"
                          v-model="userInfor.email"
                        />
                        <div class="error mb-2" v-if="errors.email">
                          {{ errors.email }}
                        </div>
                        <v-text-field
                          label="Password"
                          outlined
                          dense
                          color="blue"
                          autocomplete="false"
                          type="password"
                          v-model="userInfor.password"
                          @keyup.enter="onLogin()"
                        />
                        <div class="error mb-2" v-if="errors.email">
                          {{ errors.password }}
                        </div>
                        <v-btn color="blue" dark block tile @click="onLogin()"
                          >Đăng nhập</v-btn
                        >
                        <!-- <h5 class="text-center grey--text mt-4 mb-3">
                          Hoặc Đăng nhập bằng cách sử dụng
                        </h5>
                        <v-btn>
                          <v-icon color="red" icon="mdi-google"></v-icon>
                        </v-btn> -->
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-col>
                <v-col cols="12" md="6" class="blue rounded-bl-xl">
                  <div style="text-align: center; padding: 180px 0">
                    <v-card-text class="white--text">
                      <h3 class="text-center">Bạn vẫn chưa có tài khoản?</h3>
                    </v-card-text>
                    <div class="text-center">
                      <v-btn tile outlined dark @click="registerPage()">
                        Đăng ký
                      </v-btn>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SignupValidation from "@/services/SignupValidations";
import { mapState } from "vuex";
import axios from "axios";

export default {
  data: () => ({
    step: 1,
    userInfor: {
      email: null,
      password: null,
      name: null,
    },
    errors: [],
    alertMessage: {
      type: null,
      title: null,
      show: false,
    },
    error: null,
  }),
  methods: {
    registerPage() {
      window.location.href = "/register";
    },
    onLogin() {
      let validations = new SignupValidation(
        this.userInfor.email,
        this.userInfor.password
      );
      this.errors = validations.checkValidations();
      if (Object.keys(this.errors).length > 0) {
        return false;
      }

      let data = {
        name: this.userInfor.name,
        password: this.userInfor.password,
        email: this.userInfor.email,
      };

      axios
        .post("login", data)
        .then((response) => {
          if (response.data.message !== "thanh cong") {
            this.error = response.data.message;
            return;
          }
          localStorage.setItem("token", response.data.token);
          localStorage.setItem("userId", response.data.user.id);
          localStorage.setItem("email", response.data.user.mail);
          localStorage.setItem("image", response.data.user.image);
          localStorage.setItem("name", response.data.user.name);

          window.location.href = "/";
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  props: {
    source: String,
  },
  computed: {
    ...mapState("auth", {
      firstName: (state) => state.name,
    }),
  },
};
</script>
<style scoped>
.v-application .rounded-bl-xl {
  border-bottom-left-radius: 300px !important;
}
.v-application .rounded-br-xl {
  border-bottom-right-radius: 300px !important;
}
</style>
