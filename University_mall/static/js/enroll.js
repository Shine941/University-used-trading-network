window.onload = function(){
	var vm = new Vue({
		el: '#app',
		data: {
			host:host,
			phoneErrorSpan:"",
			stuidErrorSpan:"",
			nameErrorSpan:"",
			usernameErrorSpan:"",
			pwdErrorSpan:"",
			checkErrorSpan:"",
			sms_code_tip: "获取短信验证码",
			sending_flag: false, // 正在发送短信标志
			show_num:[],
			//value值
			phone_value:"",
			stu_id:'',
			name:"",
			stu_class:"",
			username_value:"",
			userpwd:"",
			confirmpwd:"",
			gender:'male',
			check_code:"",
			sms_code:"",
		},
		methods: {
			//验证码获取
			draw() {
				var canvas_width=document.getElementById('canvas').clientWidth;
				var canvas_height=document.getElementById('canvas').clientHeight;
				var canvas = document.getElementById("canvas");//获取到canvas的对象
				var context = canvas.getContext("2d");//获取到canvas画图的环境
				canvas.width = canvas_width;
				canvas.height = canvas_height;
				var sCode = "A,B,C,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,W,X,Y,Z,1,2,3,4,5,6,7,8,9,0";
				var aCode = sCode.split(",");
				var aLength = aCode.length;//获取到数组的长度
				for (var i = 0; i <= 3; i++) {
					var j = Math.floor(Math.random() * aLength);//获取到随机的索引值
					var deg = Math.random() * 30 * Math.PI / 180;//产生0~30之间的随机弧度
					var txt = aCode[j];//得到随机的一个内容
					var r = Math.floor(Math.random() * 256);
					var g = Math.floor(Math.random() * 256);
					var b = Math.floor(Math.random() * 256);
					this.show_num[i] = txt;
					var x = 10 + i * 20;//文字在canvas上的x坐标
					var y = 20 + Math.random() * 8;//文字在canvas上的y坐标
					context.font = "bold 23px 微软雅黑";
					context.translate(x, y);
					context.rotate(deg);
					context.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
					context.fillText(txt, 0, 0);
					context.rotate(-deg);
					context.translate(-x, -y);
				}
			},
			//验证码验证
			checkError_fd(){
				var num = this.show_num.join("");
				if(this.check_code==""){
					this.checkErrorSpan= "请输入验证码";
				}else if(this.check_code == num){
					this.checkErrorSpan ="";
				}else{
					this.checkErrorSpan= "验证码输入错误！";
					this.check_code = '';
					draw();
				}
			},
			// 获得焦点:清空span的错误信息
			check_focus(){
				this.checkErrorSpan= "";
			},
			//表单验证
			//手机号
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
				var check_code_id = this.show_num.join("");
				// 向后端接口发送请求，让后端发送短信验证码
				this.draw();
				var url = this.host + '/sms_codes/' + this.phone_value + '/' + '?check_code=' + this.check_code
					+ '&check_code_id=' + check_code_id
				axios.get(url, {
					responseType: 'json',
					withCredentials:true,
				})
					.then(response => {
						// 表示后端发送短信成功
						// 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
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
			smsFocus_fd(){
				this.smsErrorSpan = "";
			},
			//用户名验证
			usernameError_fd(){
				// 去除掉前后空白
				this.username_value = this.username_value.trim();
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
			//整体验证
			on_submit(){
				// 验证用户名,让用户名文本框失去焦点
				this.check_focus();
				this.checkError_fd();//触发文本框的获取焦点事
				this.phoneFocus_fd();
				this.phoneError_fd();
				this.smsFocus_fd();
				this.send_sms_code();
				this.username_focus();
				this.usernameError_fd();
				this.pwdErrprFocus_fd()
				this.pwdError_fd();
				// 当所有的span都是空的表示表单合法
				if(this.phoneErrorSpan=="" && this.usernameErrorSpan== "" && this.pwdErrorSpan== "" && this.checkErrorSpan == ""){
					//提交
					var formObj = document.getElementById("userForm");
					// 通过调用submit()方法来完成表单的提交
					formObj.submit();
					console.log("好了好了好了好了好了好了好了好了好了好了好了好了好了好了")
					axios.post(this.host + '/register/', {
						phone:this.phone_value,
						sms_code:this.sms_code,
						stu_id:this.stu_id,
						name:this.name,
						class:this.stu_class,
						username: this.username_value,
						password: this.userpwd,
						password2: this.confirmpwd,
						gender:this.gender,
						check_code: this.check_code,
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
		}

	})
}