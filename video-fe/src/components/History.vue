<template>
  <div class="mx-auto martop" width="700">
    <h1> Đây là trang lịch sử </h1>

    <h3> Trang này hiện thị lịch sử những video đã xuất của người dùng </h3>
  </div>


  <div style="width: 50%;display: flex;align-items: center;justify-content: space-between; margin: auto; border: 1px solid black; background: #B4D5F1;">
    <div>
      <label>Từ ngày:</label>
    <input type="date" v-model="from">
    </div>
    <div>
      <label>Đến ngày:</label>
    <input type="date" v-model="to">
    </div>
    <v-btn class="ml-5" @click="search">Tìm kiếm</v-btn>
  </div>

<div style="width: 50%; margin: auto; background: #B4D5F1;">
    <table>
    <thead>
      <tr>
        <th>Tên project</th>
        <th>Link</th>
        <th>Trạng thái video</th>
        <th>Ngày tạo video</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.project_name">
        <td>{{ item.project_name }}</td>
        <td><a :href= "item.s3_url"> Link </a></td>
        <td>{{ item.status }}</td>
        <td>{{ item.modified_at }}</td>
      </tr>
    </tbody>
  </table>
</div>


</template>

<script>
import { useRoute } from "vue-router";
import axios from "axios";
import { format, parseISO } from 'date-fns';
import locale from 'date-fns/locale/vi';
export default {
  data() {
    return {
        from: '',
        to: '',
      items: [],
      projectss: []
    }
  },
  methods: {
    convertToDateObject (dateString) {
  const [datePart, timePart] = dateString.split(' ');
  const [day, month, year] = datePart.split('/');
  return new Date(year, month - 1, day);
},
    search() {
      if (this.from != '') {
        this.items = this.projectss.filter(item => {
          console.log(item.modified_at, this.from)
        return this.convertToDateObject(item.modified_at) >= this.convertToDateObject(this.from.replace(/-/g, '/') )
      })
      console.log(222, (this.projectss[0].modified_at), (this.from.replace(/-/g, '/')))
      }
      if (this.to != '') {
        this.items = this.projectss.filter(item => {
        return this.convertToDateObject(item.modified_at) <= this.convertToDateObject(this.to)
      })
      }

      if (this.from != '' && this.to != '') {
        this.items = this.projectss.filter(item => {
        return this.convertToDateObject(item.modified_at) >= this.convertToDateObject(this.from) && this.convertToDateObject(item.modified_at) <= this.convertToDateObject(this.to)
      })
      }
      
    }
  },
  mounted() {
  const route = useRoute();
  const id = Number(route.params.id);
  axios
  .get(`projects?user_id=${id}`)
  .then((response) => {
    let projects = response.data ? response.data : [];
    projects = projects.filter(item => item.s3_url !== '');
    
    projects.forEach(item => {
  item.status = 'done';
  item.modified_at = format(parseISO(item.modified_at), 'yyyy/MM/dd', { locale })
})
    this.items = projects
    this.projectss = projects
  })
  .catch(function (error) {
    console.log(error);
  });
  },
}
</script>

<style>
.martop {
  margin-top: 100px;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  border: 1px solid black;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

input {
  cursor: pointer;
}
</style>
