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
    mounted() {
        axios.get('/class/member')
            .then(resp => {
                if (resp.data.code === 200)
                    this.members = resp.data.members;
            }).finally(this.loading);
    }
});
