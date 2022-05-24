window.onload = function(){
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            socket:'',
            text:'',
            query:'',//路由中的变量
            //我的
            username:'', //我的昵称
            userid:'',//我的id
            mystuid:'',//我的学号
            myavatar:'', //我的头像
            //对面的
            oppavatar:'',//对面的头像
            //卖家的
            solderavatar:'',  //卖家头像
            solderstuid:'',//卖家学号
            soldername:'',//卖家姓名
            //买家的
            buyeravatar:'', //买家头像
            buyerid:'',//买家的id
            buyerstuid:'',//买家的学号
            buyerclass:'',//买家的班级
            buyername:'',//买家的姓名
            goods:{},  //商品
            goodsid:'',  //商品id
            thetime:'',
            messageAll:[],
            tag:true,  //看进来的是什么人；默认是买家
        },
        mounted(){
             // 获取cookie中的用户名
            this.username = getCookie('username');
            this.query = get_query_string('q');
            this.get_time();  //获取现在时间
            this.get_person_info();//获取个人信息
            this.get_goods_info();//获取商品信息
            this.get_buyer_info();//获取买家信息
            this.get_message();//获取之前消息
            this.getsocket();
        },
        methods:{
            get_time(){
                var myDate = new Date();
                this.thetime=myDate.toLocaleString();
            },
            // 获取登录用户所有的资料
            get_person_info() {
                var url = this.host + '/userinfo/';
                this.goodsid=this.query.split("-");
                this.buyerid=this.goodsid[1];//买家id
                this.goodsid=this.goodsid[0];//商品id
                axios.get(url, {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        console.log("登录用户get_person_info");
                        this.username = response.data.info_data.username;
                        this.myavatar=response.data.info_data.avatar;
                        this.mystuid=response.data.info_data.stu_id;
                        this.userid=response.data.info_data.id;
                    })
                    .catch(error => {
                        location.href = 'login.html'
                    })
            },
            //获取之前消息
            get_message(){
                var url=this.host+'/ureadmessage/'+this.query+'/';
                axios.get(url, {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        console.log('get_message');
                        this.messageAll=response.data.message;
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
                console.log("你好");
                //滚动条置底
                document.querySelector(".content").scrollTop = document.querySelector('.content').scrollHeight;
            },
            logoutfunc(){
                this.onclose();
                var url = this.host + '/logout/';
                axios.delete(url, {
                    responseType: 'json',
                    withCredentials:true,
                })
                    .then(response => {
                        location.href = 'login.html';
                    })
                    .catch(error => {
                        location.href='404.html'
                    })
            },
            personal(){
                this.onclose();
                location.href='personal.html';
            },
            enroll(){
                this.onclose();
                location.href='enroll.html';
            },
            center(){
                this.onclose();
                location.href='center.html';
            },
            new_post(){
                this.onclose();
                location.href='new_post.html';                
            },
            get_goods_info(){
                var url = this.host+'/chatgoods/'+this.goodsid+'/';
                axios.get(url, {
                        responseType: 'json',
                        withCredentials:true,
                    })
                        .then(response => {
                            console.log("商品信息get_goods_info");
                            this.goods = response.data.goods;
                            this.solderstuid = this.goods.stuid;
                            this.solderavatar=this.goods.useravatar;
                        })
                        .catch(error => {
                            console.log(error);
                        })
                document.querySelector(".content").scrollTop = document.querySelector('.content').scrollHeight;
            },
            //买家信息
            get_buyer_info() {
                var url = this.host + '/userid/'+this.buyerid+'/';
                axios.get(url, {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        console.log("买家信息get_buyer_info");
                        this.setinfo();
                        this.buyeravatar=response.data.info_data.avatar;
                        this.buyerstuid=response.data.info_data.stu_id;
                        this.buyername=response.data.info_data.stu_name;
                        this.buyerclass=response.data.info_data.stu_class;
                    })
                    .catch(error => {
                        console.log(error)
                    })
                document.querySelector(".content").scrollTop = document.querySelector('.content').scrollHeight;                
            },
            setinfo(){
                console.log("这是setinfo");
                if(this.mystuid==this.solderstuid){ //我是卖家
                    this.tag=false;
                    console.log("setinfo()我是卖家");
                    this.oppavatar=this.buyeravatar;  //对面的是买家
                }else{  //我是买家
                    this.tag=true;
                    this.oppavatar=this.solderavatar;//对面的头像就是卖家的
                    console.log("setinfo()我是买家");
                }
            },
            getsocket(){
                if(typeof(WebSocket) === "undefined"){
                    alert("您的浏览器不支持socket")
                }else{
                    //websocket请求就是默认ws://url
                    // 实例化socket
                    console.log("getsocket");
                    var path='ws://127.0.0.1:8000/chat/'+this.goodsid+'/';
                    this.socket = new WebSocket(path);
                    // 监听socket连接
                    this.socket.onopen = this.onopen
                    // 监听socket错误信息
                    this.socket.onerror = this.error
                    // 监听socket消息
                    this.socket.onmessage = this.onmessage
                    //socket关闭
                    this.socket.onclose=this.onclose
                }
                document.querySelector(".content").scrollTop = document.querySelector('.content').scrollHeight;
            },
            sendMessage(){
                if(this.mystuid==this.solderstuid){ //我是卖家
                    this.tag=false;
                    console.log("sendMessage我是卖家");
                    this.oppavatar=this.buyeravatar;  //对面的是买家
                }else{  //我是买家
                    this.tag=true;
                    this.oppavatar=this.solderavatar;//对面的头像就是卖家的
                    console.log("sendMessage我是买家");
                }
                //console.log("sendMessage");
                var texttag = document.getElementById('textarea');
                var mystr=this.buyerid+"@#*/"+this.userid+"@#*/"+this.tag+"@#*/"+texttag.value;
                //如果有消息向服务端发消息
                if(texttag.value){
                    this.socket.send(mystr);
                }
            },
            //创建好连接之后自动触发（服务端执行self.accept())
            onopen(){
                if(this.mystuid==this.solderstuid){ //我是卖家
                    this.tag=false;
                    console.log("setinfo()我是卖家");
                    this.oppavatar=this.buyeravatar;  //对面的是买家
                }else{  //我是买家
                    this.tag=true;
                    this.oppavatar=this.solderavatar;//对面的头像就是卖家的
                    console.log("setinfo()我是买家");
                }
                console.log("socket来了")
            },
            onmessage(event){
                //当websocket接收到服务端发来的消息时，自动会触发这个函数
                booltext=event.data.split("@#*/")[2];
                this.tag=String(this.tag);
                var textdata=event.data.split("@#*/")[3];
                if(booltext==this.tag){  //是我的消息
                    this.creatm(textdata);
                }else{ //不是我的消息
                    this.creato(textdata);
                }
                document.querySelector('#textarea').value = '';
                document.querySelector('#textarea').focus();
                //滚动条置底
                document.querySelector(".content").scrollTop = document.querySelector('.content').scrollHeight;
            },
            //服务端主动断开连接时，这个方法会被触发
            onclose(){
                var url=this.host+'/onreadmes/'+this.query+'/';
                axios.get(url, {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        console.log('连接断开');
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            },
            //给我创建消息
            creatm(textdata){
                    let item = document.createElement('div');
                    item.className = 'item item-right';
                    item.innerHTML = `<div class="bubble bubble-right">${textdata}</div>`;
                    let imgdiv= document.createElement('div');//里层图片div
                    imgdiv.className='avatar';
                    let img = document.createElement('img');//里层图
                    img.src= this.myavatar;
                    imgdiv.appendChild(img);
                    item.appendChild(imgdiv);
                    document.querySelector('.content').appendChild(item);
            },
            //给别人创建消息
            creato(textdata){
                    let item = document.createElement('div');
                    item.className = 'item item-left';
                    let imgdiv= document.createElement('div');//里层图片div1
                    imgdiv.className='avatar';
                    let img = document.createElement('img');//里层图
                    img.src= this.oppavatar;
                    imgdiv.appendChild(img);
                    itemtext = document.createElement('div');
                    itemtext.className='bubble bubble-left';
                    itemtext.innerHTML = `${textdata}`;
                    item.appendChild(imgdiv);
                    item.appendChild(itemtext);
                    document.querySelector('.content').appendChild(item); 
            },
        },
    })
}
