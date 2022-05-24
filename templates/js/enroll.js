window.onload = function(){
	var vm = new Vue({
		el: '#app',
		data: {
			host:host,
			phoneErrorSpan:"",
			stuidErrorSpan:"",
			nameErrorSpan:"",
			usernameErrorSpan:"",
			smsErrorSpan:"",
			pwdErrorSpan:"",
			checkErrorSpan:"",
			sms_code_tip: "获取短信验证码",
			sending_flag: false, // 正在发送短信标志
			image_code_id:'', //图形验证码
			image_code_url: '', //图形验证码
			//value值
			phone_value:'',
			stu_id:'',
			stu_name:'',
			stu_class:'',
			username_value:'',
			userpwd:'',
			confirmpwd:'',
			gender:'男',
			image_code:'',  //输入的验证码
			sms_code:'',  //输入的短信验证码
		},
		mounted: function(){
			// 向服务器获取图片验证码
			this.generate_image_code();
		},
		methods: {
			//***************************************************学号************************
			//v-model="stu_id" stuidErrorSpan @focus = "stu_id_focus_fd" @blur="stu_id_Error_fd" 
			stu_id_Error_fd(){
				this.stu_id = this.stu_id.trim();
				if(this.stu_id == ""){
						this.stuidErrorSpan= "学号不能为空";
				}else{
            		// 学号12位数字
					var regExp = /^[0-9]{12}$/
					var ok = regExp.test(this.stu_id)
					if(ok){
						// 合法
						this.phoneErrorSpan = "";
					}else{
					// 不合法
					this.stuidErrorSpan = "请输入正确学号";	
					}
				}
				if(this.phoneErrorSpan == ""){
					var url = this.host + '/stuIds/' + this.stu_id + '/count/';
					axios.get(url, {
						responseType: 'json',
						withCredentials:true,
					})
						.then(response => {
							if (response.data.count > 0) {
								this.stuidErrorSpan = "学号已注册";
							} else {
								this.stuidErrorSpan = "";
							}
						})
						.catch(error => {
							console.log(error.response);
						})
				}
    		},
			stu_id_focus_fd(){
				this.stuidErrorSpan ="";
			},

			//***************************************************姓名*************************
			//v-model="stu_name"@focus = "stu_name_focus_fd"@blur="stu_name_Error_fd"nameErrorSpan
			stu_name_Error_fd(){
				this.stu_name = this.stu_name.trim();
				if(this.stu_name == ""){
						this.nameErrorSpan= "姓名不能为空";
				}
    		},
			stu_name_focus_fd(){
				this.nameErrorSpan ="";
			},
			//*******************************************************************用户名****************
			//用户名验证
			usernameError_fd(){
				// 去除掉前后空白
				this.username_value = this.username_value.trim();
				var re = /^[a-zA-Z0-9_-]{5,20}$/;
            	var re2 = /^[0-9]+$/; //不能全为数字
				// 用户名不能为空,不能为空串
				if(this.username_value == ""){
					this.usernameErrorSpan = "用户名不能为空";
				}else{
					// 用户名不是空,继续判断长度是否合法
					if(this.username_value.length < 2 || this.username_value.length > 14){
						this.usernameErrorSpan = "用户名长度必须在[2-14]之间";	
					}else{
						// 用户名不为空,并且长度也合法,接下来继续判断用户名中是否有特殊符号
						var regExp = /^[a-zA-Z0-9]+$/
						var ok = regExp.test(this.username_value)
						if(ok){
							// 合法
							this.usernameErrorSpan= "";
						}else{
							// 不合法
							this.usernameErrorSpan = "昵称只能由数字和字母组成";	
						}
					}
					if(this.usernameErrorSpan == ""){
						var url = this.host + '/usernames/' + this.username_value + '/count/';
						axios.get(url, {
							responseType: 'json',
							withCredentials:true,
						})
							.then(response => {
								if (response.data.count > 0) {
									this.usernameErrorSpan = "昵称已存在";
								} else {
									this.usernameErrorSpan = "";
								}
							})
							.catch(error => {
								console.log(error.response);
							})
					}
				}
			},
			// 获得焦点:清空span的错误信息.
			username_focus(){
				this.usernameErrorSpan = "";
			},
			//密码验证
    		// 确认密码失去焦点就验证.
			pwdError_fd(){//进行比对 
				if(this.userpwd != this.confirmpwd){
					this.pwdErrorSpan = "密码和确认密码不一致";
				}else if(this.userpwd ==""){
					this.pwdErrorSpan= "请输入密码";
				}else{
					this.pwdErrorSpan = "";
				}
			},
			pwdErrprFocus_fd(){
				this.pwdErrorSpan = "";
			},

			//***************************************************手机号********************************************
    		phoneError_fd(){
				// 去除掉前后空白
				this.phone_value = this.phone_value.trim();
				if(this.phone_value == ""){
						this.phoneErrorSpan= "手机号不能为空";
				}else{
            		// 手机号不为空,并且长度也合法,接下来继续判断用户名中是否有特殊符号
					var regExp =/^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/;
					var ok = regExp.test(this.phone_value)
					if(ok){
						// 合法
						this.phoneErrorSpan = "";
					}else{
					// 不合法
					this.phoneErrorSpan = "请输入正确手机号";	
					}
				}
				if(this.phoneErrorSpan == ""){
					var url = this.host + '/mobiles/' + this.phone_value + '/count/';
					axios.get(url, {
						responseType: 'json',
						withCredentials:true,
					})
						.then(response => {
							console.log(response.data.count)
							if (response.data.count > 0) {

								this.phoneErrorSpan = "手机号已存在";
							} else {
								this.phoneErrorSpan = "";
							}
						})
						.catch(error => {
							console.log(error.response);
						})
				}
    		},
			// 获得焦点:清空span的错误信息.
			phoneFocus_fd(){
				this.phoneErrorSpan = "";
			},

			//***************************************************验证码*****************************
			// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
			generate_image_code: function(){
				// 生成一个编号 : 使用uuid保证编号唯一
				this.image_code_id = generateUUID();
				// 设置页面中图片验证码img标签的src属性
				this.image_code_url = this.host + "/image_codes/" + this.image_code_id + "/";
			},
			//验证码验证
			checkError_fd(){
				if(this.image_code==""){
					this.checkErrorSpan= "请输入验证码";
				}else{
					this.checkErrorSpan ="";
				}
				if(this.checkErrorSpan ==""){
					var url = this.host + "/image_codes/" + this.image_code_id + "/"+'?image_code=' + this.image_code;
					axios.post(url,{
						responseType: 'json',
						withCredentials:true,
					})
						.then(response => {
							if (response.data.code==0) {
							   this.smsErrorSpan="";
							   console.log('验证码ok')
							}else{
								this.smsErrorSpan=response.data.errmsg;
							}
						})
				}
			},
			// 获得焦点:清空span的错误信息
			check_focus(){
				this.checkErrorSpan= "";
			},
			//******************************************************短信验证码**********************
			// 发送手机短信验证码
			send_sms_code() {
				if (this.sending_flag == true) {
					return;
				}
				this.sending_flag = true;
				// 校验参数，保证输入框有数据填写
				this.phoneError_fd();
				if (this.phoneErrorSpan != "") {
					this.sending_flag = false;
					return;
				}
				// 向后端接口发送请求，让后端发送短信验证码
				var url = this.host + '/sms_codes/' + this.phone_value + '/' + '?image_code=' + this.image_code
                + '&image_code_id=' + this.image_code_id
				axios.get(url, {
					responseType: 'json',
					withCredentials:true,
				})
					.then(response => {
						// 表示后端发送短信成功
						// 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
						if(response.data.code==400){
							this.smsErrorSpan= response.data.errmsg;
						}
						var num = 60;
						// 设置一个计时器
						var t = setInterval(() => {
							if (num == 1) {
								// 如果计时器到最后, 清除计时器对象
								clearInterval(t);
								// 将点击获取验证码的按钮展示的文本回复成原始文本
								this.sms_code_tip = '获取短信验证码';
								// 将点击按钮的onclick事件函数恢复回去
								this.sending_flag = false;
							} else {
								num -= 1;
								// 展示倒计时信息
								this.sms_code_tip = num + '秒';
							}
						}, 1000, 60)
					})
					.catch(error => {
						if (error.response.status == 400) {
							this.smsErrorSpan = error.response.data.message;
							this.error_sms_code = true;
						} else {
							console.log(error.response.data);
						}
						this.sending_flag = false;
					})
			},
			smsError_fd(){
				if(!this.sms_code){
					this.smsErrorSpan="请输入短信验证码"
				}else {
					this.smsErrorSpan=""
				}
				if (this.smsErrorSpan=="") {
					var url = this.host +'/sms_codes/' + this.phone_value + '/'+'?sms_code=' + this.sms_code ;
				axios.post(url,{
						responseType: 'json',
						withCredentials:true,
					})
						.then(response => {
							if (response.data.code==0) {
							   this.smsErrorSpan="";
							   console.log('验证码ok')
							}else{
								this.smsErrorSpan=response.data.errmsg;
							}
						})
				}
				
			},
			smsFocus_fd(){
				this.smsErrorSpan = "";
			},
			
			//整体验证
			on_submit(){
				this.stu_id_focus_fd();//触发文本框的获取焦点事
				this.stu_id_Error_fd();
				this.stu_name_focus_fd();
				this.stu_name_Error_fd();
				this.username_focus();
				this.usernameError_fd();
				this.pwdErrprFocus_fd()
				this.pwdError_fd();
				this.phoneFocus_fd();
				this.phoneError_fd();
				this.check_focus();
				this.checkError_fd();
				this.smsFocus_fd();
				this.send_sms_code();
				this.smsError_fd();
				// 当所有的span都是空的表示表单合法
				if(this.phoneErrorSpan=="" && this.stuidErrorSpan =="" && this.nameErrorSpan =="" && this.usernameErrorSpan== "" && this.smsErrorSpan == "" && this.pwdErrorSpan== "" && this.checkErrorSpan == ""){
					//提交
					//var formObj = document.getElementById("userForm");
					// 通过调用submit()方法来完成表单的提交
					//formObj.submit();
					//console.log("好了好了好了好了好了好了好了好了好了好了好了好了好了好了")
					axios.post(this.host + '/register/', {
						phone:this.phone_value, //手机号
						sms_code:this.sms_code,  //短信验证码
						stu_id:this.stu_id,  //学号
						name:this.stu_name,  //名字
						class:this.stu_class, //班级
						username: this.username_value, //昵称
						password: this.userpwd, //密码
						password2: this.confirmpwd,  //密码验证
						gender:this.gender,  //性别
						image_code: this.image_code,  //验证码
					}, {
						responseType: 'json',
						withCredentials:true,
					})
						.then(response => {
							if (response.data.code==0) {
							   location.href = 'login.html';
							}
							if (response.data.code == 400) {
								alert(response.data.errmsg)
								location.href = '404.html';
							}
						})
				}
			},
		},
	})	
}