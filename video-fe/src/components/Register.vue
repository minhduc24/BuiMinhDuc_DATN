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
            <v-window-item :value="2">
              <v-row>
                <v-col cols="12" md="6" class="blue rounded-br-xl">
                  <div style="text-align: center; padding: 180px 0">
                    <v-card-text class="white--text">
                      <h3 class="text-center">Đã đăng ký?</h3>
                    </v-card-text>
                    <div class="text-center">
                      <v-btn tile outlined dark @click="loginPage()"
                        >Đăng nhập</v-btn
                      >
                    </div>
                  </div>
                </v-col>

                <v-col cols="12" md="6">
                  <v-card-text class="mt-12">
                    <h4 class="text-center">Đăng kí một tài khoản</h4>

                    <v-row align="center" justify="center">
                      <v-col cols="12" sm="8">
                        <v-row>
                          <v-col cols="12">
                            <v-text-field
                              label="Tên"
                              outlined
                              dense
                              color="blue"
                              autocomplete="false"
                              class="mt-4"
                              v-model="userInfor.name"
                            />
                          </v-col>
                        </v-row>
                        <v-text-field
                          label="Email"
                          outlined
                          dense
                          color="blue"
                          autocomplete="false"
                          v-model="userInfor.email"
                        />
                        <div class="error mb-2" v-if="errors.email">
                          {{ errors.email }}
                        </div>
                        <v-text-field
                          label="Mật khẩu"
                          outlined
                          dense
                          color="blue"
                          autocomplete="false"
                          type="password"
                          v-model="userInfor.password"
                        />
                        <div class="error mb-4" v-if="errors.password">
                          {{ errors.password }}
                        </div>

                        <v-btn color="blue" dark block tile @click="onSigup"
                          >Đăng ký</v-btn
                        >
                      </v-col>
                    </v-row>
                  </v-card-text>
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
  }),
  methods: {
    loginPage() {
      window.location.href = "/login";
    },
    onSigup() {
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
        image: "",
        email: this.userInfor.email,
      };
      axios
        .post("users", data)
        .then((response) => {
          (this.alertMessage.type = response.data.type),
            (this.alertMessage.title = response.data.status);
          this.alertMessage.show = true;
          this.userInfor.email = "";
          this.userInfor.password = "";
          this.userInfor.name = "";
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
