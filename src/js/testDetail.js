import Vue from 'vue';
import axios from "axios";
import moment from 'moment';
import sideBar from '../component/SideBar';
import {parseSearchParam} from './util';

new Vue({
    el: '#pane',
    data: {
        examInfo: {}
    },
    components: {
        sideBar
    },
    computed: {
        testDuration() {
            if (this.examInfo.tend < 0)
                return '不限时';
            let start = moment.unix(this.examInfo.tstart);
            let end = moment.unix(this.examInfo.tend);
            let d = moment.duration(end.diff(start));
            return `${d.hours()} 小时 ${d.minutes()} 分钟`;
        }
    },
    methods: {
        handleClick() {
            if (this.examInfo.over) {
                // TODO: 实现查看试卷功能（需要复用试卷预览功能）
                console.log('查看试卷');
            } else {
                // 跳转到在线考试test_online页面
                location.href = '/exam/paper?tno=' + this.params['tno'];
            }
        }
    },
    mounted() {
        this.params = parseSearchParam();
        axios.get('/exam/?tno=' + this.params['tno']).then(resp => {
            if (resp.data.code === 200) {
                this.examInfo = resp.data;
                console.log(resp.data);
            }
        });

        // 设置moment格式化是的locale
        moment.updateLocale('cn', {
            weekdays: [
                "星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"
            ]
        });
        moment.locale('cn');
    },
    filters: {
        formatDateTime(timestamp) {
            if (timestamp < 0)
                return '不限时';
            return moment.unix(timestamp).format('YYYY-MM-DD / HH:mm / dddd');
        }
    }
});