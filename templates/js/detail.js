window.onload = function(){
    var vm = new Vue({
        el:'#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            username:'',
            query:'',
            goods:{},
        },
        mounted(){
             // 获取cookie中的用户名
            this.username = getCookie('username');
            this.query = get_query_string('q');
            this.get_person_info();
            //获取商品
            this.get_goods();
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
            // 获取用户所有资料
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
            // 请求查询结果
            get_goods(){
                var url = this.host+'/detail/'+this.query+'/';
                //console.log(this.query);
                axios.get(url, {
                        responseType: 'json',
                        withCredentials:true,
                    })
                        .then(response => {
                            this.goods = response.data.goods;
                        })
                        .catch(error => {
                            console.log(error);
                        })
            },
        },
    })
}