import Vue from 'vue';
import $ from 'jquery';
import navBar from '../component/NavBar';
import sideBar from '../component/SideBar';
import mainFooter from '../component/Footer';

// 柱形图配置
let barChartCanvas = $('#barChart').get(0).getContext('2d')
let barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    datasetFill: false
}
// 饼图配置
let pieChartCanvas = $('#pieChart').get(0).getContext('2d')
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
        members: [],
        cacheMembers: []
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
        search() {
            // search按钮按一下搜索，再按一下清空搜索框
            if (this.searchSno.length && !this.adding) {
                this.adding = true;
                $.ajax({
                    url: '/student/search?cno=1&sno=' + this.searchSno,
                    method: 'GET',
                    success(resp) {
                        if (resp.code === 200) {
                            // 此处this无法引用到Vue实例
                            vue.members = [{sno: resp.sno, sname: resp.sname}];
                            vue.inClass = resp.in_class;
                        } else if (resp.code === 204) {
                            vue.members = [];
                        }
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
                    $.ajax({
                        url: '/class/member?cno=1&sno=' + item.sno,
                        method: 'DELETE',
                        success(resp) {
                            if (resp.code === 200)
                                vue.loadMember(1);
                        },
                        error(err) {
                            console.log(err);
                        }
                    });
                }
            });
        },
        loadMember(cno) {
            /* 向服务器请求班级成员列表并更新缓存 */
            this.loading = false;
            $.ajax({
                url: '/class/member?cno=' + cno,
                method: 'GET',
                success(resp) {
                    if (resp.code === 200) {
                        vue.members = resp.members;
                        // 缓存数据以减少向服务器请求的次数
                        vue.cacheMembers = resp.members;
                    }
                },
                error(err) {
                    console.log(err);
                },
                complete() {
                    vue.loading = false;
                }
            });
        }
    },
    loadStat() {
        $.ajax({
            url: '/exam?tno=1',
            method: 'GET',
            success(resp) {
                fillBarChart(barChartCanvas, barChartOptions, resp.segments, resp.pscore);
                fillPieChart(pieChartCanvas, pieOptions, resp.segments);
            },
            complete() {
                vue.loadingStat = false;
            }
        });
    },
    mounted() {
        this.loadMember(1);
        this.loadStat();
    }
});

function genLabels(maxScore, sliceNum) {
    let res = [];
    let step = maxScore / sliceNum;
    for (let i = 0; i < sliceNum - 1; i++) {
        res.push(`[${step * i}, ${step * (i + 1)})`);
    }
    res.push(`${step * (sliceNum - 1)}, ${step * sliceNum}`);

    return res;
}

function fillBarChart(canvas, options, segments, maxScore) {
    new Chart(canvas, {
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
    })
}


function fillPieChart(canvas, options, data) {
    // 将低6份成绩类别的学生合并成为不及格学生人数
    let processedData = [data.slice(0, 6).reduce((pre, e) => pre + e)].concat(data.slice(-4));
    new Chart(canvas, {
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
}
