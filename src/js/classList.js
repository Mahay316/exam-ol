import Vue from 'vue';
import axios from "axios";
import subjectList from "../../static/js/subjects";
import navBar from "../component/NavBar";
import sideBar from "../component/SideBar";
import mainFooter from "../component/Footer";

new Vue({
    el: '#pane',
    data: {
        classes: [],
        subjects: subjectList,
        curr: 0,
        className: ''
    },
    components: {
        navBar,
        sideBar,
        mainFooter
    },
    methods: {
        mapColor(idx) {
            let colorClass = ['bg-info', 'bg-primary', 'bg-danger', 'bg-warning'];
            return colorClass[idx % 4];
        },
        addCourse() {
            this.classes.push({
                cno: (this.curr + 1) * 10,
                cname: this.className,
                csubject: this.curr + 1
            });
        }
    },
    mounted() {
        axios.get('class/list').then(resp => {
            let data = resp.data;
            if (data.code === 200) {
                this.classes = data.classes;
            }
        });
    }
});
