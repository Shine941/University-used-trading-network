window.onload = function(){
	var vm = new Vue({
		el: '#app',
    	data: {
        	host: host,
        	nameError: "",
        	checkError:"",
        	//value
        	username: '',
        	password: '',
        	remember: false
    	},
    	methods: {
    		 // 获取url路径参数
        	get_query_string: function (name) {
            	var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            	var r = window.location.search.substr(1).match(reg);
            	if (r != null) {
            	    return decodeURI(r[2]);
            	}
            	return null;
        	},
    		//********************************用户名**********************
    		//v-model="username"@blur="check_username"@focus="checkname_focus" nameError 
        	// 检查数据
        	check_username_fd () {
        	    if (!this.username) {
        	        this.nameError = "请输入用户名";
        	    } else {
        	        this.nameError = "";
        	    }
        	},
    		checkname_focus_fd(){
				this.nameError = "";
    		},
    		//*********************************密码***********************
    		//v-model="password" @blur="check_pwd" @focus="checkpwd_focus"checkError
        	check_pwd_fd(){
        	    if (!this.password) {
        	        this.checkError = "请输入密码";
        	    } else {
        	        this.checkError = "";
        	    }
        	},
    		checkpwd_focus_fd(){
    			this.checkError = "";
    		},
    		//**********************************记录密码*********************
    		//v-model="remember"
        	test(){
        	    console.log(123)
        	},
        	// 表单提交
        	on_submit(){
        		this.checkname_focus_fd();
        	    this.check_username_fd();
        	    this.checkpwd_focus_fd();
        	    this.check_pwd_fd();
        	    if (this.nameError == "" && this.checkError == "") {
        	        axios.post(this.host + '/login/', {
        	            username: this.username,
        	            password: this.password,
        	            remembered:this.remember,
        	        }, {
        	            responseType: 'json',
        	            // 发送请求的时候, 携带上cookie
        	            withCredentials: true,
        	            // crossDomain: true
        	        })
        	            .then(response => {
        	                if (response.data.code == 0) {
        	                    // 跳转页面
        	                    var return_url = this.get_query_string('next');
        	                    if (!return_url) {
        	                        return_url = '/center.html';
        	                    }
        	                    location.href = return_url;
        	                } else if (response.data.code == 400) {
        	                    this.checkError = '用户名或密码错误';
        	                }
        	            })
        	            .catch(error => {
        	                if (error.response.status == 400) {
        	                    this.checkError = '用户名或密码错误';
        	                } else {
        	                   this.checkError = '服务器错误';
        	                }
         	               this.checkError = "";
        	            })
        	    }
        	},
    	}

	})
}