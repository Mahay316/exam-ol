<template>
  <aside class="main-sidebar sidebar-dark-primary elevation-4">
    <!-- Brand Logo -->
    <a href="#" class="brand-link">
      <img src="/static/img/logo_white.png" alt="Logo" class="brand-image img-md elevation-3"
           style="opacity: 0.8">
      <span class="brand-text font-weight-light">在线考试系统</span>
    </a>

    <!-- Sidebar -->
    <div class="sidebar">
      <!-- Sidebar user panel (optional) -->
      <div class="user-panel mt-3 pb-3 mb-3 d-flex">
        <div class="image">
          <img src="/static/img/avatar.png" class="img-circle elevation-2" alt="User Image">
        </div>
        <div class="info">
          <a href="#" class="d-block" v-if="role === 'mentor'">{{ username }}老师，您好！</a>
          <a href="#" class="d-block" v-else-if="role === 'student'">{{ username }}同学，您好！</a>
          <a href="#" class="d-block" v-else-if="role === 'admin'">{{ username }}管理员，您好！</a>
        </div>
      </div>

      <!-- Sidebar Menu -->
      <nav class="mt-2">
        <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu"
            data-accordion="false">
          <div v-if="role === 'mentor'">
            <li class="nav-header">管理</li>
            <li class="nav-item">
              <a href="/index" class="nav-link active">
                <i class="nav-icon fas fa-paper-plane"></i>
                <p>
                  班级管理
                </p>
              </a>
            </li>
            <li class="nav-item">
              <a href="/paper/manage" class="nav-link">
                <i class="nav-icon fas fa-paperclip"></i>
                <p>
                  试卷管理
                </p>
              </a>
            </li>
            <li class="nav-item">
              <a href="/question/manage" class="nav-link">
                <i class="nav-icon fas fa-pen"></i>
                <p>
                  试题管理
                </p>
              </a>
            </li>
          </div>
          <div v-else-if="role === 'student'">
            <li class="nav-item">
              <a href="/index" class="nav-link">
                <i class="nav-icon fas fa-paperclip"></i>
                <p>
                  我的班级
                </p>
              </a>
            </li>
          </div>
          <div v-else-if="role === 'admin'">
            <li class="nav-item">
              <a href="/mentor/manage" class="nav-link">
                <i class="nav-icon fas fa-paperclip"></i>
                <p>
                  教师管理
                </p>
              </a>
            </li>
            <li class="nav-item">
              <a href="/student/manage" class="nav-link">
                <i class="nav-icon fas fa-pen"></i>
                <p>
                  学生管理
                </p>
              </a>
            </li>
          </div>
          <li class="nav-header">账号</li>
          <li class="nav-item">
            <a href="#" class="nav-link" @click="logout">
              <i class="nav-icon fas fa-door-open"></i>
              <p>
                退出登录
              </p>
            </a>
          </li>
        </ul>
      </nav>
      <!-- /.sidebar-menu -->
    </div>
    <!-- /.sidebar -->
  </aside>
</template>

<script>
import axios from "axios";

export default {
  name: "side-bar",
  data() {
    return {
      username: '',
      role: this.myRole
    }
  },
  props: {
    myRole: {
      required: true,
      validator: function (value) {
        // 用户身份必须匹配下列字符串中的一个
        return ['mentor', 'student', 'admin'].indexOf(value) !== -1
      }
    }
  },
  methods: {
    logout() {
      axios.post('/auth/logout').then(resp => {
        if (resp.data.code === 200) {
          setTimeout(() => location.href = '/', 500);
        }
      });
    }
  },
  mounted() {
    axios.get('/auth/info').then(resp => {
      let data = resp.data;
      if (data.code === 200) {
        this.username = data.name;
        this.role = data.role;
      }
    });
  }
}
</script>

<style scoped>

</style>