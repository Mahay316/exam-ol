<template>
  <footer class="main-footer">
    <div class="float-right d-none d-sm-block">
      <b>Version</b> {{ version }}
    </div>
    <strong>2020 <a href="https://github.com/Mahay316/exam-ol">Exam_Online</a>.</strong> Practicum of Database.
  </footer>
</template>

<script>
export default {
  name: "main-footer",
  props: {
    version: {
      type: String,
      default: '1.0.0'
    }
  }
}
</script>
