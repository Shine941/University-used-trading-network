window.onload = function(){
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            username:'',
            mobile:'',
            stu_id:'',
            stu_name:'',
            stu_class:'',
            gender:'',
            avatarurl:'',
        },
        mounted(){
             // 获取cookie中的用户名
        	this.username = getCookie('username');
            this.get_person_info();//获取个人信息
        },
        methods: {
            //退出按钮
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
                    });
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
                        this.mobile = response.data.info_data.mobile;
                        this.stu_id = response.data.info_data.stu_id;
                        this.stu_name = response.data.info_data.stu_name;
                        this.stu_class = response.data.info_data.stu_class;
                        this.gender = response.data.info_data.gender;
                        this.avatarurl=response.data.info_data.avatar;
                    })
                    .catch(error => {
                        location.href = 'login.html'
                    })
            },
        },
    })
}