window.onload = function(){
    var imgurl;
    var avaturl;
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            username:'',
            afterphoto:'',
            mobile:'',
            gender:'',
            isActive:true,
            afpho_val:'',
            usernameErrorSpan:'',
            phoneErrorSpan:'',
            avatarurl:'',
        },
        mounted(){
             // 获取cookie中的用户名
            this.username = getCookie('username');
            this.get_person_info();//获取个人信息
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
                        this.mobile = response.data.info_data.mobile;
                        this.gender = response.data.info_data.gender;
                        this.avatarurl=response.data.info_data.avatar;
                    })
                    .catch(error => {
                        location.href = 'login.html'
                    })
            },
            //修改用户信息
            //用户名验证
            usernameError_fd(){
                // 去除掉前后空白
                this.username = this.username.trim();
                var re = /^[a-zA-Z0-9_-]{5,20}$/;
                var re2 = /^[0-9]+$/; //不能全为数字
                // 用户名不能为空,不能为空串
                if(this.username == ""){
                    this.usernameErrorSpan = "用户名不能为空";
                }else{
                    // 用户名不是空,继续判断长度是否合法
                    if(this.username.length < 2 || this.username.length > 14){
                        this.usernameErrorSpan = "用户名长度必须在[2-14]之间";    
                    }else{
                        // 用户名不为空,并且长度也合法,接下来继续判断用户名中是否有特殊符号
                        var regExp = /^[a-zA-Z0-9]+$/
                        var ok = regExp.test(this.username)
                        if(ok){
                            // 合法
                            this.usernameErrorSpan= "";
                        }else{
                            // 不合法
                            this.usernameErrorSpan = "昵称只能由数字和字母组成";    
                        }
                    }
                    if(this.usernameErrorSpan == ""){
                        var url = this.host + '/usernames/' + this.username + '/count/';
                        axios.get(url, {
                            responseType: 'json',
                            withCredentials:true,
                        })
                            .then(response => {
                                if (response.data.count > 1) {
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
            //***************************************************手机号********************************************
            phoneError_fd(){
                // 去除掉前后空白
                this.mobile = this.mobile.trim();
                if(this.mobile == ""){
                        this.phoneErrorSpan= "手机号不能为空";
                }else{
                    // 手机号不为空,并且长度也合法,接下来继续判断用户名中是否有特殊符号
                    var regExp =/^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/;
                    var ok = regExp.test(this.mobile)
                    if(ok){
                        // 合法
                        this.phoneErrorSpan = "";
                    }else{
                    // 不合法
                    this.phoneErrorSpan = "请输入正确手机号";   
                    }
                }
                if(this.phoneErrorSpan == ""){
                    var url = this.host + '/mobiles/' + this.mobile + '/count/';
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
            on_submit(){
                this.username_focus();
                this.usernameError_fd();
                this.phoneFocus_fd();
                this.phoneError_fd();
                // 当所有的span都是空的表示表单合法
                if(this.phoneErrorSpan=="" && this.usernameErrorSpan== ""){
                    //提交
                    //var formObj = document.getElementById("userForm");
                    // 通过调用submit()方法来完成表单的提交
                    //formObj.submit();
                    console.log("好了好了好了好了好了好了好了好了好了好了好了好了好了好了")
                    axios.put(this.host + '/changeinfo/', {
                        mobile:this.mobile, //手机号
                        username: this.username, //昵称
                        gender:this.gender,  //性别
                    }, {
                        responseType: 'json',
                        withCredentials:true,
                    })
                        .then(response => {
                            if (response.data.code==0) {
                               location.href = 'my_info.html';
                            }
                            if (response.data.code == 400) {
                                alert(response.data.errmsg)
                                location.href = '404.html';
                            }
                        })
                }
            },
            //修改图片
            preImg() { 
                var size = event.target.files[0].size / 1024 / 1024
                var fileName=document.getElementById("imgOne").value;
                console.log(fileName)
                //console.log(size)
                if(size<2){
                    if (navigator.userAgent.indexOf("MSIE")>=1) { // IE
                        imgurl = document.getElementById("imgOne").value;
                    } else if(navigator.userAgent.indexOf("Firefox")>0) { // Firefox
                        imgurl = window.URL.createObjectURL(document.getElementById("imgOne").files.item(0));
                    } else if(navigator.userAgent.indexOf("Chrome")>0) { // Chrome
                        imgurl = window.URL.createObjectURL(document.getElementById("imgOne").files.item(0));
                    }
                    console.log(imgurl)
                    this.isActive = !this.isActive;
                }else{
                    alert("图片过大，请重新选择")
                }
            }, 
            change_act(){
                this.isActive = !this.isActive;
            },

        },
    });
    //cropper裁减框
    const newimage=document.getElementById("workImg");
    var cropper = new Cropper(newimage,{
        aspectRatio:1/1,
        viewMode:1,
        checkCroppOrigion:true,
        guides:true,
        highlight:true,
        background:true,
        cropBoxMovable:true,
    });
    document.getElementById("urlchange").onclick = function(){
        newimage.cropper.replace(imgurl,false)
    },
    document.getElementById("uploadimg").onclick=function(){
        var avatarbase64 = newimage.cropper.getCroppedCanvas().toDataURL("image/jpg")
        if(avatarbase64 != ""){
                    var url = 'http://127.0.0.1:8000/avaupload/';
                    axios.put(url,avatarbase64, {
                        responseType: 'json',
                        withCredentials:true,
                    })
                        .then(response => {
                                vm.isActive = !vm.isActive;
                                avaturl=response.data.avatar
                                document.getElementById("afphoto").src= avaturl; 
                                document.getElementById("afphoto").value = avaturl;
                        })
                        .catch(error => {
                            console.log(error.response);
                        })
                }else{

                }
    }
}
