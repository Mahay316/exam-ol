import Vue from 'vue';
import axios from "axios";
import navBar from '../component/NavBar';
import sideBar from '../component/SideBar';
import mainFooter from '../component/Footer';

new Vue({
    el: '#testStat',
    data: {
        loading: true,
        members: null
    },
    components: {
        navBar,
        sideBar,
        mainFooter
    },
    methods: {
        deleteMember(item) {
            console.log('deleting');
            bootbox.confirm(`是否将学生${item.sname}移出该班级？`, (res) => {
                if (res) {
                    axios.delete('/class/member', {data: {cno: 1, sno: item.sno}}).then(resp => {
                        if (resp.data.code === 200)
                            bootbox.alert('删除成功');
                    }).catch(err => {
                        console.log(err);
                    });
                }
            });
        }
    },
    mounted() {
        axios.get('/class/member?cno=1')
            .then(resp => {
                if (resp.data.code === 200)
                    this.members = resp.data.members;
            }).finally(() => this.loading = false);
    }
});
