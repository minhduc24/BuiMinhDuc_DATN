<template>
    <v-app-bar>
        <v-toolbar-title class="mouser title" @click="homePage">Video Application</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn-group v-if="!user.exitsUser">
      <v-btn color="primary" @click="loginPage">Đăng nhập</v-btn>
      <v-btn class="ml-3" color="secondary" @click="registerPage">Đăng ký</v-btn>
    </v-btn-group>
        <v-menu min-width="200px" rounded v-if="user.exitsUser">
            <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props">
                    <v-avatar color="blue" size="x-large">
                        <span class="text-h5">{{ user.fullName }}</span>
                    </v-avatar>
                </v-btn>
            </template>
            <v-card>
                <v-card-text>
                    <div class="mx-auto text-center">
                        <v-avatar color="blue" size="x-large">
                            <span class="text-h5">{{ user.fullName }}</span>
                        </v-avatar>
                        <h3>{{ user.fullName }}</h3>
                        <p class="text-caption mt-1">
                            {{ user.email }}
                        </p>
                        <v-divider class="my-3"></v-divider>
                        <v-btn rounded variant="text" @click="Account()">
                            Trang cá nhân
                        </v-btn>
                        <v-divider class="my-3"></v-divider>
                        <v-btn rounded variant="text" @click="logOut()">
                            Đăng xuất
                        </v-btn>
                    </div>
                </v-card-text>
            </v-card>
        </v-menu>
    </v-app-bar>
</template>

<script>
import router from '@/router'
export default {
    data: () => ({
        user: {
            image: '',
            fullName: '',
            email: '',
            exitsUser: false
        },
    }),
    created() {
        if (localStorage.getItem("token") != null) {
            this.user.image = localStorage.getItem('image')
            this.user.email = localStorage.getItem('email')
            this.user.exitsUser = true
            let fullName = localStorage.getItem('name').split(" ")
            this.user.fullName = fullName[fullName.length - 1]
        }
    },
    methods: {
            homePage() {
                router.push('/')
            },
            loginPage() {
                // router.push('/login')
                window.location.href="/login"
            },
            registerPage() {
                window.location.href='/register'
            },
            logOut() {
                localStorage.clear()
                window.location.href="/"
            },
            Account() {
                window.location.href="/profile"
            }
        }
}
</script>

<style>
.mouser{
    cursor: pointer;
}
</style>