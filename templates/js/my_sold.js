window.onload = function(){
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            username:'',
            mysold:[],
            avatarurl:'',
        },
        mounted(){
             // 获取cookie中的用户名
            this.username = getCookie('username');
            this.get_person_info();
            this.getgoods();
        },
        methods: {
            logoutfunc() {
                var url = this.host + '/logout/';
                axios.delete(url, {
                    responseType: 'json',
                    withCredentials:true,
                })
                    .then(response => {
                        location.href = 'login.html';
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            
            },
            // 获取用户所有的资料
            get_person_info() {
                var url = this.host + '/userinfo/';
                axios.get(url, {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        if (response.data.code == 400) {
                            location.href = 'login.html'
                            return
                        }
                        this.username = response.data.info_data.username;
                        this.avatarurl=response.data.info_data.avatar;
                    })
                    .catch(error => {
                        location.href = 'login.html'
                    })
            },
            getgoods(){
                var url=this.host+'/MySolds/';
                axios.get(url,{
                    responseType:'json',
                    withCredentials:true,
                })
                    .then(response => { 
                        this.mysold=response.data.mygoods;
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            },
        },
    })
}