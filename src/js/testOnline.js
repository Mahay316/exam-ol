import Vue from 'vue';
import $ from 'jquery';
import axios from 'axios';
import Swal from 'sweetalert2';
import {parseSearchParam} from './util';

// 设置Toast用于提示考试时间节点
const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-start',
    showConfirmButton: false,
    showCloseButton: true,
});

new Vue({
    el: '#pane',
    data: {
        testName: '',
        timeLeft: 0,
        timer: -1,
        questions: [],
        answers: {}, // answers用于缓存已作答的题目答案,
        marked: [],  // 保存标记了的题号
        notifyFlag: [false, false]  // 分别记录距考试结束15和3分钟是否提醒过
    },
    methods: {
        submitPaper() {
            // 提示正在提交试卷
            Swal.fire({
                title: '提示',
                html: '正在提交试卷',
                didOpen: () => {
                    Swal.showLoading()
                }
            });
            axios.get('/exam/grading?tno=' + this.params['tno']).then(resp => {
                console.log(resp.data);
                if (resp.data.code === 200) {
                    // 提示试卷提交成功
                    Swal.fire({
                        icon: 'success',
                        title: '试卷提交成功',
                        showConfirmButton: false,
                        timer: 1500
                    }).then(res => {
                        location.href = '/exam/detail?tno=' + this.params['tno'];
                    });
                }
            });
        },
        handleSubmit() {
            Swal.fire({
                icon: 'question',
                title: '提交试卷',
                text: '提交后无法修改，是否继续？',
                showConfirmButton: true,
                showCancelButton: true,
                confirmButtonText: '提交',
                cancelButtonText: '取消'
            }).then(res => {
                if (res.isConfirmed)
                    this.submitPaper();
            });
        },
        handleMark(idx) {
            // 调用一次标记指定题目，再调用取消标记
            let i = this.marked.indexOf(idx);
            if (i < 0)
                this.marked.push(idx);
            else
                this.marked.splice(i, 1);
            console.log(this.marked);
        },
        handleFillAnswer(item, index, event) {
            let targetAnswer = this.answers[item.questionID];
            let val = event.target.value;
            // 不进行无用请求
            if (!val && targetAnswer.choice[index] === val)
                return;

            targetAnswer.choice[index] = val;
            // 由于多层嵌套的数组更新并不引起重绘，因此强制要求刷新
            this.$forceUpdate();

            // 更新提交时间戳
            targetAnswer.submitTime = Date.now();
            this.cacheQuestion([targetAnswer]);
        },
        handleSelectAnswer(item, event) {
            let targetAnswer = this.answers[item.questionID];

            // 单项选择题只允许缓存一个答案
            // 但为了和其他题型的一致性，仍使用数组缓存其答案
            if (item.type === 'select') {
                if (targetAnswer.choice.includes(event.target.value))
                    return;  // 不对重复点击相同选项做响应，以提高性能
                targetAnswer.choice.pop();
                targetAnswer.choice.push(event.target.value);
            } else if (item.type === 'multi') {
                let idx = targetAnswer.choice.indexOf(event.target.value);
                // 对于多选题点击两次选项将取消选择
                if (idx < 0) targetAnswer.choice.push(event.target.value);
                else targetAnswer.choice.splice(idx, 1);
            }

            // 更新提交时间戳
            targetAnswer.submitTime = Date.now();
            // 由于多层嵌套的数组更新并不引起重绘，因此强制要求刷新
            this.$forceUpdate();

            this.cacheQuestion([targetAnswer]);
        },
        cacheQuestion(res) {
            // 向服务器提交当前题目作答情况
            $.ajax({
                url: '/exam/questions',
                method: 'POST',
                data: {
                    examID: this.params['tno'],
                    result: JSON.stringify(res)
                },
                success(resp) {
                    // TODO: 需要考虑提交失败情况，进行重试操作
                    console.log(resp.code);
                }
            });
        },
        toLetter(idx) {
            return String.fromCharCode('A'.charCodeAt(0) + idx);
        },
        calibrateTime() {
            if (this.timer > 0)  // 清除之前的计时器
                clearInterval(this.timer);
            axios.get('/exam/time?examID=' + this.params['tno']).then(resp => {
                let data = resp.data;
                if (data.code === 200) {
                    this.questions = data.questions;
                    this.testName = data.tname;
                    this.timeLeft = data.timeLeft.toFixed(0);

                    // 限时的考试需要倒计时
                    if (this.timeLeft > 0) {
                        this.timer = setInterval(() => {
                            this.timeLeft--;
                            if (this.timeLeft <= 0) {
                                clearInterval(this.timer);
                                // 考试结束
                                this.submitPaper();
                            } else if ((this.timeLeft > 3 && this.timeLeft < 15 * 60) && !this.notifyFlag[0]) {
                                // 先判断15分钟是为了使提示的显示顺序正确
                                // 进行考试结束前15分钟提醒
                                Toast.fire({
                                    icon: 'warning',
                                    title: '考试剩余时间已少于15分钟'
                                });
                                this.notifyFlag[0] = true;
                            } else if (this.timeLeft < 3 * 60 && !this.notifyFlag[1]) {
                                // 进行考试结束前3分钟提醒
                                Toast.fire({
                                    icon: 'warning',
                                    title: '考试剩余时间已少于3分钟'
                                });
                                this.notifyFlag[1] = true;
                            }
                        }, 1000);
                    }
                }
            });
        },
        loadQuestions() {
            axios.get('/exam/questions?examID=' + this.params['tno']).then(resp => {
                let data = resp.data;
                if (data.code === 200) {
                    this.questions = data.questions;

                    // 在加载题目时，对题目做一些预处理
                    for (let item of this.questions) {
                        let cachedChoice = [];
                        if (item.type === 'fill') {
                            let target = /\[填空\]/g;

                            // 由于填空题的答案是有序且数量固定的，因此进行预分配空间
                            let count = item.stem.match(target).length;
                            item.blankNum = count;
                            cachedChoice = Array(count);

                            // 匹配填空题所有的空，并逐一替换
                            item.stem = item.stem.replace(target, '_______');
                        }

                        // 如果服务器有缓存，则加载缓存
                        cachedChoice = item.cache ? item.cache.choice : cachedChoice;
                        this.answers[item.questionID] = {
                            questionID: item.questionID,
                            choice: cachedChoice
                        };

                        // 多层嵌套数组的更新无法触发重绘，强制刷新
                        this.$forceUpdate();
                    }
                    console.log(this.questions);
                }
            });
        }
    },
    computed: {
        questionStat() {
            let res = {
                select: [],
                multi: [],
                fill: []
            };
            // 防止报错，貌似计算属性先于普通属性创建
            if (!this.questions)
                return res;

            // 分别记录选择题、多选题和填空题对应的题号
            for (let i = 0; i < this.questions.length; i++) {
                let tmp = {idx: i + 1, questionID: this.questions[i].questionID};
                switch (this.questions[i].type) {
                    case 'select':
                        res.select.push(tmp);
                        break;
                    case 'multi':
                        res.multi.push(tmp);
                        break;
                    case 'fill':
                        res.fill.push(tmp);
                        break;
                }
            }
            return res;
        }
    },
    filters: {
        typeToStr(type) {
            let res = '';
            switch (type) {
                case 'select':
                    res = '单项选择题';
                    break;
                case 'multi':
                    res = '多项选择题';
                    break;
                case 'fill':
                    res = '填空题';
                    break;
            }

            return res;
        },
        formatTime(seconds) {
            let n = 2;
            let hours = String((seconds / 3600).toFixed(0));
            seconds %= 3600;
            let minutes = (Array(n).join('0') + String(parseInt(seconds / 60))).slice(-n);
            seconds %= 60;
            seconds = (Array(n).join('0') + String(parseInt(seconds))).slice(-n);


            return `${hours}:${minutes}:${seconds}`;
        }
    },
    mounted() {
        this.params = parseSearchParam();
        this.loadQuestions();

        this.calibrateTime();
        // 对于限时的考试，每5分钟向服务器进行一次时间校正
        if (this.timeLeft)
            setInterval(() => this.calibrateTime(), 300);
    }
});
