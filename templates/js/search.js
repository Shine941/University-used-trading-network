window.onload = function(){
    var vm = new Vue({
        el:'#app',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            host,
            username:'',
            query:'',
            ser_goods:[],
            searchkey:'',
            count:0,  //总数量
        },
        mounted(){
             // 获取cookie中的用户名
            this.username = getCookie('username');
            this.query = get_query_string('q');
            //获取商品
            this.get_search_result();
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
            // 请求查询结果
            get_search_result(){
                var url = this.host+'/search/'
                axios.get(url, {
                        params: {
                            q: this.query,
                        },
                        responseType: 'json',
                        withCredentials:true,
                    })
                    .then(response => {
                        this.ser_goods = [];
                        // this.count = response.data.count;
                        this.count = 0
                        var results = response.data;
                        for(var i=0; i< results.length; i++){
                            var goods = results[i];
                            goods.url = '/detail.html'+ "?q=" + goods.id ;
                            this.searchkey = goods.searchkey
                            this.ser_goods.push(goods);
                            this.count += goods.count
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    })
            },
            sub_search(){
                var sub = document.getElementById("sub_search");
                sub.submit();
            },
            title_search(){
                var sub = document.getElementById("title_search");
                sub.submit();
            }

        },
    })
}