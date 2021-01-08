import Vue from 'vue';
import $ from 'jquery';
import axios from "axios";
import navBar from '../component/NavBar';
import sideBar from '../component/SideBar';
import mainFooter from '../component/Footer';
import {parseSearchParam} from './util';

import ('chart.js')

// 柱形图配置
let barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    datasetFill: false
}
// 饼图配置
let pieOptions = {
    maintainAspectRatio: false,
    responsive: true,
}

const vue = new Vue({
    el: '#testStat',
    data: {
        loadingMember: true,
        loadingStat: true,
        adding: false,
        inClass: false,
        searchSno: '',
        selectedTest: '',
        members: [],
        cacheMembers: [],
        exams: [],
        className: ''
    },
    components: {
        navBar,
        sideBar,
        mainFooter
    },
    methods: {
        handleInput(event) {
            this.searchSno = event.target.value;
            this.adding = false;
            this.members = this.cacheMembers;
        },
        handleChangeExam(event) {
            // 加载指定考试的统计信息
            this.loadStat(event.target.value, false);
        },
        search() {
            // search按钮按一下搜索，再按一下清空搜索框
            if (this.searchSno.length && !this.adding) {
                this.adding = true;
                axios.get('/student/search?cno=1&sno=' + this.searchSno)
                    .then(resp => {
                        let data = resp.data;
                        if (data.code === 200) {
                            this.members = [{sno: data.sno, sname: data.sname}];
                            this.inClass = data.in_class;
                        } else if (resp.data === 204) {
                            this.members.splice(0, this.members.length);
                        }
                    });
            } else if (this.adding) {
                this.searchSno = '';
                this.adding = false;
                this.members = this.cacheMembers;
            }
        },
        addMember(item) {
            $.ajax({
                url: '/class/member',
                method: 'POST',
                data: {
                    cno: 1,
                    sno: item.sno
                },
                success(resp) {
                    vue.adding = false;
                    vue.loadMember(1);
                }
            });
        },
        deleteMember(item) {
            console.log('deleting');
            bootbox.confirm(`是否将学生${item.sname}移出该班级？`, (res) => {
                if (res) {
                    axios.delete('/class/member?cno=1&sno=' + item.sno)
                        .then(resp => {
                            if (resp.data.code === 200)
                                this.loadMember(1);
                        }).catch(err => console.log(err));
                }
            });
        },
        loadMember(cno) {
            /* 向服务器请求班级成员列表并更新缓存 */
            this.loadingMember = true;
            axios.get('/class/member?cno=' + cno)
                .then(resp => {
                    let data = resp.data;
                    if (data.code === 200) {
                        this.members = data.members;
                        // 缓存数据以减少向服务器请求的次数
                        this.cacheMembers = data.members;
                    }
                }).catch(err => console.log(err))
                .finally(() => this.loadingMember = false);
        },
        loadStat(tno, create) {
            this.loadingStat = true;
            axios.get('/exam/?tno=' + tno)
                .then(resp => {
                    let data = resp.data;
                    if (data.code === 200) {
                        if (create) {
                            // create为true时创建Chart对象
                            this.barChart = fillBarChart($('#barChart').get(0).getContext('2d'),
                                barChartOptions, data.segments, data.pscore);
                            this.pieChart = fillPieChart($('#pieChart').get(0).getContext('2d'),
                                pieOptions, data.segments);
                        } else {
                            // create为false时更新Chart对象数据集
                            this.barChart.data.datasets[0].data = data.segments;
                            this.barChart.data.labels = genLabels(data.pscore, 10);
                            this.pieChart.data.datasets[0].data = [data.segments.slice(0, 6).reduce((pre, e) => pre + e)]
                                .concat(data.segments.slice(-4));

                            this.barChart.update();
                            this.pieChart.update();
                        }
                    }
                }).finally(() => this.loadingStat = false);
        },
        loadExam(cno) {
            axios.get('/class/exams?cno=' + cno).then(resp => {
                if (resp.data.code === 200) {
                    this.exams = resp.data.exams;
                    if (this.params['tno']) {
                        // 加载指定考试统计信息
                        this.loadStat(this.params['tno'], true);
                        // 同步更新下拉选择框
                        this.selectedTest = this.params['tno'];
                    } else if (this.exams.length) {
                        // 若未指定查看的考试，则默认选择第一场考试进行查看
                        this.loadStat(this.exams[0].tno, true);
                        this.selectedTest = this.exams[0].tno;
                    }
                }
            });
        }
    },
    mounted() {
        // 解析当前url的查询参数并保存
        this.params = parseSearchParam();
        if (this.params['cno']) {
            this.loadExam(this.params['cno']);
            this.loadMember(this.params['cno']);
            axios.get('/class/info?cno=' + this.params['cno']).then(resp => {
                let data = resp.data;
                console.log(data);
                if (data.code === 200) {
                    this.className = data.cname;
                }
            });
        }
    }
});

/**
 * 生成柱状图x轴的标签label
 */
function genLabels(maxScore, sliceNum) {
    let res = [];
    let step = maxScore / sliceNum;
    for (let i = 0; i < sliceNum - 1; i++) {
        res.push(`[${step * i}, ${step * (i + 1)})`);
    }
    res.push(`[${step * (sliceNum - 1)}, ${step * sliceNum}]`);

    return res;
}

/**
 * 根据输入数据和配置绘制柱状图
 * @param canvas 目标Canvas对象
 * @param options 绘图配置
 * @param segments 成绩数据，格式为0~maxScore分为10份，每份所占的人数
 * @param maxScore 考试总成绩，用于生成x轴的标签label
 */
function fillBarChart(canvas, options, segments, maxScore) {
    let barChart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: genLabels(maxScore, 10),
            datasets: [
                {
                    label: '考试成绩直方图',
                    backgroundColor: 'rgba(60,141,188,0.9)',
                    borderColor: 'rgba(60,141,188,0.8)',
                    pointRadius: false,
                    pointColor: '#3b8bba',
                    pointStrokeColor: 'rgba(60,141,188,1)',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(60,141,188,1)',
                    data: segments
                }
            ]
        },
        options: options
    });

    return barChart;
}


/**
 * 根据输入数据和配置绘制饼图
 * @param canvas 目标Canvas对象
 * @param options 绘图配置
 * @param data 成绩数据，格式为0~maxScore分为10份，每份所占的人数
 */
function fillPieChart(canvas, options, data) {
    // 将低6份成绩类别的学生合并成为不及格学生人数
    let processedData = [data.slice(0, 6).reduce((pre, e) => pre + e)].concat(data.slice(-4));
    let pieChart = new Chart(canvas, {
        type: 'pie',
        data: {
            labels: ['不及格', '合格', '中等', '良好', '优秀'],
            datasets: [
                {
                    data: processedData,
                    backgroundColor: ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc'],
                }
            ]
        },
        options: options
    });

    return pieChart;
}
