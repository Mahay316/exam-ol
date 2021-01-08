import Vue from 'vue';
import axios from 'axios';
import moment from 'moment';
import bootbox from 'bootbox';
import navBar from '../component/NavBar';
import sideBar from '../component/SideBar';
import mainFooter from '../component/Footer';
import {parseSearchParam} from './util';

import ('bootstrap');

new Vue({
    el: '#pane',
    data: {
        exams: [],
        role: '',
        param: {}
    },
    components: {
        navBar,
        sideBar,
        mainFooter
    },
    methods: {
        deleteExam(item) {
            bootbox.confirm(`是否删除考试"${item.tname}"？`, (result) => {
                if (result) {
                    // TODO: 删除考试
                    axios.delete('/exam/?tno=' + item.tno).then(resp => {
                        if (resp.data.code === 200)
                            this.loadExam(this.params['cno']);
                        else if (resp.data.code === 403)
                            bootbox.alert('无权限删除考试！');
                    });
                }
            });
        },
        loadExam(cno) {
            axios.get('/class/exams?cno=' + cno).then(resp => {
                if (resp.data.code === 200) {
                    let sortedExams = resp.data.exams;
                    // 根据起始时间降序排列，最新的考试在最前面
                    // 排序是为了生成日期标签且方便查看
                    sortedExams.sort((a, b) => Number(b.tstart) - Number(a.tstart));

                    this.exams = sortedExams;
                    if (this.role === 'student') {
                        // 学生获取所有已经结束的考试的成绩
                        this.exams.forEach(ele => {
                            if (ele.over) {
                                axios.get('/exam/?tno=' + ele.tno).then(resp => {
                                    if (resp.data.code === 200) {
                                        this.$set(ele, 'score', resp.data.st_grade);
                                        this.$set(ele, 'maxScore', resp.data.pscore);
                                    }
                                });
                            }
                        });
                    }
                }
            });
        },
        loadRole() {
            axios.get('/auth/info').then(resp => {
                let data = resp.data;
                if (data.code === 200) {
                    this.role = data.role;
                }
            });
        },
        needLabel(timestamp) {
            let target = moment.unix(timestamp).format('YYYY/MM/DD');

            // 由于考试列表已经根据起始时间排序
            // 因此若当前项与前一项起始时间不在同一天，则加入一个时间label
            let res = target !== this.prvStamp;
            this.prvStamp = target;

            return res;
        }
    },
    filters: {
        formatDate(timestamp) {
            return moment.unix(timestamp).format('YYYY/MM/DD');
        },
        formatDateTime(timestamp) {
            if (Number(timestamp) < 0)
                return '不限时';
            return moment.unix(timestamp).format('YYYY/MM/DD HH:mm');
        }
    },
    mounted() {
        this.params = parseSearchParam();
        this.loadRole();
        this.loadExam(this.params['cno']);
    }
});