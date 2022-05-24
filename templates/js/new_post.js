window.onload = function(){
     //使用vue
    var vm = new Vue({
        el:"#app",
        data:{
            host,
            username:'',
            avatarurl:'',
            list:[], //用于结构渲染
            allArr:[],  //存储每次上传的所有flie，
            limitNum:4, //限制数量
            goods_title:'',
            goods_text:'',
            goods_img:[],
            goods_category:'',
            goods_price:'',//价钱
        },
        mounted: function () {
        // 给 username 赋值:
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
            // 获取用户所有的头像资料
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
            //添加图片
            addImg(){
                var obj = document.getElementById('add-pic-btn'),
                    obArr =  obj.files,
                    length = obArr.length,
                    arr = [],
                    limitNum = this.limitNum;
                for(let x of obArr){
                    var params = {name: x.name, src:''};
                    arr.push(params);
                }
                this.allArr = [...this.allArr,...arr];
                //定义一个函数作回调
                const Pro = function () {
                    return new Promise(function (resolve, reject) {
                        arr.forEach((v,i,array)=>{
                            resolve(array)
                        });
                    })
                };
                Pro().then((newArr)=>{
                    this.list=[];
                    //console.log(newArr);
                    var a=[];
                    //第一次
                    if(newArr.length>4 && !this.list){
                        //alert("最多只能上传四张图片");
                        legth = 4;
                    }else if(newArr.length<4 && !this.list){
                        legth = newArr.length;
                    }else if(this.list.length+newArr.length>4){
                        //alert("最多只能上传四张图片");
                        legth=4-this.list.length;
                    }else{
                        legth=newArr.length;
                    }
                    for(let i=0; i<legth; i++) {
                        var reader = new FileReader();
                        if (!reader) {
                            console.log('对不起，您的浏览器不支持！请更换浏览器试一下');
                            return
                        }
                        //读取成功
                        reader.onload = function(e) {
                            
                            var _src = e.target.result;
                            newArr[i].src = _src;
                            a.push(_src);
                            console.log(a[i]);
                            document.getElementById('add-pic-btn').value = null;
                        };
                        reader.onloadstart=function(){
                            console.log('开始')
                        };
                        reader.onprogress=function(e){
                            if(e.lengthComputable){
                                console.log("正在读取文件")
                            }
                        };
                        reader.error = function(){
                            console.log("读取异常")
                        };
                        reader.readAsDataURL(obj.files[i]);
                    }
                    this.goods_img=a
                    //console.log(this.goods_img);
                    //合并数组,先合并在删除多余；
                    var len1 = this.list.length,
                        len2 = newArr.length;
                    var d = [...this.list,...newArr];
                    this.list = d;
                    // console.log(len1,len2,d)
                    if(d.length > limitNum){
                        alert(`最多只能上传${limitNum}张图片`);
                        this.list.splice(limitNum,d.length-limitNum);
                    };
                });
                //document.getElementById('add-pic-btn').value = null;
            },
            //删除图片
            delImg(i){
                    this.list.splice(i,1);
                    this.allArr.splice(i,1);
                //这个得清空，不然全部被删除后，无法再次上传同一图片
               if(this.list.length<=0){
                   document.getElementById('add-pic-btn').value = null;
               }
            },
            send_post(){
                if(!this.goods_title&&!this.goods_img&&!this.goods_price&&!this.goods_text&&!this.goods_category){
                    return alert('信息不全，请补全信息');
                }else{
                    console.log(this.goods_img.length);
                    axios.post(this.host + '/newgoods/', {
                        goods_img:this.goods_img,//商品图片
                        goods_title:this.goods_title,//商品标题
                        goods_price:this.goods_price,//商品价格
                        goods_text:this.goods_text,//商品介绍
                        goods_category:this.goods_category,//商品分类
                    }, {
                        responseType: 'json',
                        withCredentials:true,
                    })
                        .then(response => {
                            if (response.data.code==0) {
                               location.href = 'personal.html';
                            }
                            if (response.data.code == 400) {
                                alert(response.data.errmsg)
                                location.href = '404.html';
                            }
                        })
                }
            },
        },
    });
    
}