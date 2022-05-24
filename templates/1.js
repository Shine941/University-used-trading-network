var app= new Vue({
    el:'#app',
    data(){
        return{
            list:[], //用于结构渲染
            allArr:[],  //存储每次上传的所有flie，
            limitNum:9, //限制数量
        }
    },
    methods:{        
    //添加图片
        addImg(){
            let that = this;
            var obj = that.getId('add-pic-btn'),
                obArr =  obj.files,
                length = obArr.length,
                arr = [],
                limitNum = that.limitNum;
            console.log(obj);
            for(let x of obArr){
                var params = {name: x.name, src:''};
                arr.push(params);
            }
            that.allArr = [...that.allArr,...arr];
            //定义一个函数作回调
            const Pro = function () {
                return new Promise(function (resolve, reject) {
                    arr.forEach((v,i,array)=>{
                        resolve(array)
                    });
                })
            };
            Pro().then((newArr)=>{
                //console.log(newArr);
                for(let i=0; i<newArr.length; i++) {
                    var reader = new FileReader();
                    if (!reader) {
                        console.log('对不起，您的浏览器不支持！请更换浏览器试一下');
                        return
                    }
                    //读取成功
                    reader.onload = function(e) {
                        //console.log(e)
                        var _src = e.target.result;
                        console.log(_src);
                        newArr[i].src = _src;
                        that.clearVal();
                    };
                    reader.onloadstart=function(){
                        //console.log('开始')
                    };
                    reader.onprogress=function(e){
                        if(e.lengthComputable){
                            //console.log("正在读取文件")
                        }
                    };
                    reader.error = function(){
                        console.log("读取异常")
                    };
                    reader.readAsDataURL(obj.files[i]);
                }
                //合并数组,先合并在删除多余；
                var len1 = that.list.length,
                    len2 = newArr.length;
                var d = [...that.list,...newArr];
                that.list = d;
                // console.log(len1,len2,d)
                if(d.length > limitNum){
                    alert(`最多只能上传${limitNum}张图片`);
                    that.list.splice(limitNum,d.length-limitNum);
                    // console.log(that.list)
                }
            });
        },
        //删除图片
        delImg(i){
            var flag = confirm(`确认要删除名为：${this.list[i].name}的图片？`);
            if(flag) {
                this.list.splice(i,1);
                this.allArr.splice(i,1);
            }
            //这个得清空，不然全部被删除后，无法再次上传同一图片
           if(this.list.length<=0){
               this.clearVal();
           }
        },
        //每次上传完清除一下value
        clearVal(){
            this.getId('add-pic-btn').value = null;
        },
        //dom
        getId(id){
            return document.getElementById(id);
        }
    }
})