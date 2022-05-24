window.onload = function(){
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            username:'',
            avatarurl:'',
            chatting:[],
        },
        mounted(){
             // 获取cookie中的用户名
        	this.username = getCookie('username');
            this.get_person_info();
            this.get_chatting();
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
            //获取用户消息室
            get_chatting(){
                if(this.username){
                    var url=this.host+'/getchat/'
                    axios.get(url, {
                        responseType: 'json',
                        withCredentials:true,
                    })
                        .then(response => {
                            if(response.data.message);  //有消息的话
                                this.chatting =response.data.message;
                        })
                        .catch(error => {
                            console.log(error.response);
                        })
                }
            },
        },
    })
}