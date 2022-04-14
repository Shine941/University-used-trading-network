/* 
（1）用户名不能为空
（2）用户名必须在2-14位之间
（3）用户名只能有数字和字母组成，不能含有其它符号（正则表达式）
（4）密码和确认密码一致
（5）统一失去焦点验证
（6）错误提示信息统一在span标签中提示，并且要求字体12号，红色。
（7）文本框再次获得焦点后，清空错误提示信息
（8）最终表单中所有项均合法方可提交
*/
window.onload = function(){
    //用户名验证
	var nameErrorSpan = document.getElementById("nameError");
    nameErrorSpan.className="nameError"
    // 给id="username"的节点绑定blur事件
    var usernameElt = document.getElementById("username");
	usernameElt.onblur = function(){
		// 获取用户名
		var username = usernameElt.value;
		// 去除掉前后空白
		username = username.trim();
		// 用户名不能为空,不能为空串
		//if(username.length == 0){}
		if(username == ""){
			nameErrorSpan.innerHTML = "用户名不能为空";
		}else{
			// 用户名不是空,继续判断长度是否合法
			if(username.length < 2 || username.length > 14){
				nameErrorSpan.innerHTML = "用户名长度必须在[2-14]之间";	
			}else{
				// 用户名不为空,并且长度也合法,接下来继续判断用户名中是否有特殊符号
				var regExp = /^[a-zA-Z0-9]+$/
				var ok = regExp.test(username)
				if(ok){
					// 合法
					nameErrorSpan.innerHTML = "";
				}else{
					// 不合法
					nameErrorSpan.innerHTML = "用户名只能由数字和字母组成";	
				}
			}
		}
	}
	usernameElt.onfocus= function(){
		nameErrorSpan.innerHTML = "";
    }
	document.getElementById("regbtn").onclick = function(){
		// 验证用户名,怎么验证用户名？让用户名文本框失去焦点
		// 重点:使用JS代码怎么触发事件？？？？？？
		usernameElt.focus(); //触发文本框的获取焦点事件
		usernameElt.blur();//触发文本框的失去焦点事件
		// 当所有的span都是空的表示表单合法
		if(nameErrorSpan.innerHTML == ""){
			//提交
			var formObj = document.getElementById("userForm");
			// 通过调用submit()方法来完成表单的提交
			formObj.submit();
		}
	}
}