
//刷新bootstrap-table
function refreshTable(tableId){
	$('#'+tableId).bootstrapTable(('refresh'));
}


function myAlert(htmlStr,fontSize,fontColor){
	if (fontSize==""){
		fontSize=14
	}
	if (fontColor==""){
		fontColor="black"
	}
	var alertStr="<div style='text-align: center;font-weight: bold;font-size: "+fontSize+"px;color:"+fontColor+"'>"+htmlStr+"</div>"
	bootbox.alert({
		size: "small",
		buttons: {
            ok: {
				label: '确定'
				//className: 'btn-myStyle'
            }
        },
		title: "操作提示",
        message: alertStr
	})
}

function myAlertBack(htmlStr,fontSize,fontColor){
	if (fontSize==""){
		fontSize=14
	}
	if (fontColor==""){
		fontColor="black"
	}
	var alertStr="<div style='text-align: center;font-weight: bold;font-size: "+fontSize+"px;color:"+fontColor+"'>"+htmlStr+"</div>"

	bootbox.alert({
		size: "small",
		buttons: {
            ok: {
				label: '确定'
				//className: 'btn-myStyle'
            }
        },
		title: "操作提示",
        message: alertStr,
        callback: function() {
            history.back()
        }
	})
}


function myAlertAutoClose(htmlStr,sec){
	if (htmlStr==""){
		return;
	}
	if (sec == ""){
		sec = 5
	}
	$.jGrowl(htmlStr, {
		header: '操作提示',
		life: sec*1000,
		theme:  'manilla',
//		position: 'center',
		speed:  'slow',
//		beforeOpen: function(e,m,o) {
//			console.log("I am going to be opened!", this);
//		},
//		open: function(e,m,o) {
//			console.log("I have been opened!", this);
//		},
//		beforeClose: function(e,m,o) {
//			console.log("I am going to be closed!", this);
//		},
//		close: function(e,m,o) {
//			console.log("I have been closed!", this);
//		},
		animateOpen: { 
			height: "show",
			width: "show"
		},
		animateClose: { 
			height: "show",
			width: "show"
		}
	});
}

function myConfirm(htmlStr,fontSize,fontColor){
	if (fontSize==""){
		fontSize=14
	}
	if (fontColor==""){
		fontColor="black"
	}
	var alertStr="<div style='text-align: center;font-weight: bold;font-size: "+fontSize+"px;color:"+fontColor+"'>"+htmlStr+"</div>"
	bootbox.confirm({
		size: "small",
	  	title: "操作提示",
	  	message: alertStr
	})
}



function findDimensions(widthOrheight) //函数：获取尺寸 
{
	var winWidth = 0;
	var winHeight = 0;
    //获取窗口宽度 
    if (window.innerWidth) winWidth = window.innerWidth;
    else if ((document.body) && (document.body.clientWidth)) winWidth = document.body.clientWidth;
    //获取窗口高度 
    if (window.innerHeight) winHeight = window.innerHeight;
    else if ((document.body) && (document.body.clientHeight)) winHeight = document.body.clientHeight;
    //通过深入Document内部对body进行检测，获取窗口大小 
    if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
        winHeight = document.documentElement.clientHeight;
        winWidth = document.documentElement.clientWidth;
    }
    if (widthOrheight=="width"){
    		return winWidth;
    }else{
    		return winHeight;
    }
}

//获取浏览可视范围高度
function getWidth(){
	return findDimensions("width");
}
//获取浏览可视范围高度
function getHeight(){
	return findDimensions("height");
}

//将tab重置到第指定个tab
function setTabDefault(tabsIdName,contentIdName,num){
    $("#"+tabsIdName+" li").removeClass("active");
    $("#"+tabsIdName+" li").eq(num).addClass("active");
    $("#"+contentIdName+" .tab-pane").removeClass("active");
    $("#"+contentIdName+" .tab-pane").eq(num).addClass("active");
    $("#submitForm").removeAttr("disabled");
    $("#tip").html("");
}

//自动填充表单
$.fn.setForm = function(jsonStr){
	var formObj = this;
	var obj = eval("("+jsonStr+")");
	var key,value,tagName,type,arr;
	for(x in obj){
		key = x;
		value = obj[x];
		var $oinput = formObj.find("[name='"+key+"'],[name='"+key+"[]']");
		$oinput.each(function(){
			tagName = $(this)[0].tagName;
			type = $(this).attr('type');
			if(tagName=='INPUT'){
				if(type=='radio'){
					$(this).attr('checked',$(this).val()==value);
				}else if(type=='checkbox'){
					arr = value.split(',');
					for(var i =0;i<arr.length;i++){
						if($(this).val()==arr[i]){
							$(this).attr('checked',true);
							break;
						}
					}
				}else{
					$(this).val(value);
				}
			}else if(tagName=='SELECT' || tagName=='TEXTAREA'){
				$(this).val(value);
			}
			
		});
	}
}

//全局替换
String.prototype.replaceAll = function(s1,s2){
//	console.log(s1)
//	console.log(s2)
//	return this.replace(new RegExp(s1,"gm"),s2);
	var tempStr = this;
	if (tempStr!=""){
		var newStr="";
		tempArray=tempStr.split(s1);
		for (i=0;i<tempArray.length;i++){
			if (i==0){
				newStr=tempArray[i];
			}else{
				newStr += s2 + tempArray[i];
			}
		}
		return newStr;
	}else{
		return ""
	}
}

//设置cookie
function setCookie(name,value,days)//两个参数，一个是cookie的名子，一个是值  
{ 
   var Days = days; //此 cookie 将被保存 30 天  
   var exp = new Date(); //new Date("December 31, 9998");  
   exp.setTime(exp.getTime() + Days*24*60*60*1000); 
   document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString(); 
}

//读取cookie
function getCookie(name)//取cookies函数     
{ 
   var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)")); 
   if(arr != null) return unescape(arr[2]); return null; 

}

//删除cookie
function delCookie(name)//删除cookie  
{ 
   var exp = new Date(); 
   exp.setTime(exp.getTime() - 1); 
   var cval=getCookie(name); 
   if(cval!=null) document.cookie= name + "="+cval+";expires="+exp.toGMTString(); 
} 


function clearSelect2(objId,ifShowSearch){
	if (ifShowSearch=="T"){
		$("#"+objId).val("").select2();
	}else{
		$("#"+objId).val("").select2({minimumResultsForSearch: -1});
	}
}

/*
 设置表单中元素是否可以用
 * */
function setFormElementDisabled(formId,trueOrFalse){
	var form = document.getElementById(formId);
    //alert(form.elements.length)
    for (var i = 0; i < form.elements.length; i++) {
	    	var element = form.elements[i];
	    	var id=element.id;
	    	if (id){
	    		$("[id='"+id+"']").each(function(index,ele){
				//alert(this.value)
				this.disabled=trueOrFalse;
			})
	//    		$("#"+id).attr("disabled",trueOrFalse);
	//  		if (trueOrFalse){
	//  			$("#"+id).attr("disabled","disabled");
	//  		}else{
	//  			console.log(id+":"+$("#"+id).attr("disabled"))
	//  			//$("#"+id).remove("disabled");
	//  			$("#"+id).attr("disabled",false);
	//  			console.log(id+":"+$("#"+id).attr("disabled"))
	//  		}
	    	}
    }
}

$._messengerDefaults = {
    extraClasses:'messenger-fixed messenger-theme-future messenger-on-bottom'
};

/*系统提示（自动关闭）*/
function showTip(htmlStr,sec){
	if (sec==""){
		sec=5;
	}
	$.globalMessenger().post(
		{
			message: htmlStr,
		    hideAfter: sec,
		    showCloseButton: true
		}
	);
}

/*
显示加载中的图标
selecter:选择器
topAdjust:调试距离调整
leftAdjust:左边距离调整
 * */
function progressStart(selecter,topAdjust,leftAdjust){
	NProgress.start();
	if (selecter!=""){
//	    console.log("top:"+$(selecter).offset().top);
//	    console.log("left:"+$(selecter).offset().left);
//	    console.log("width:"+$(selecter).width());
	    var top=$(selecter).offset().top;
	    var left=$(selecter).offset().left;
	    var width=$(selecter).width();
	    var positionTop=top+20;
	    var positionLeft=left+width-60;
	    
//	    console.log("positionTop:"+positionTop);
//	    console.log("positionLeft:"+positionLeft);
	    $(".spinner").css("top",positionTop);
	    $(".spinner").css("left",positionLeft);
	}else{
		$(".spinner").css("top",64);
	    $(".spinner").css("right",34);
	}
}


function progressEnd(){
	$(".spinner").hide();
	NProgress.done();
}


//修改表字段值
function modifySingleValue(inputTip,tableName,fieldName,tableId){
	inputTip = unescape(inputTip);//空格处理
	bootbox.prompt({
		buttons: {
		   	confirm: {
				label: '确定'
		   	},
			cancel: {
				label: '取消'
		   	}
		},
		size: "small",
		title: inputTip,
		callback: function(result){
			/* result = String containing user input if OK clicked or null if Cancel clicked */ 
			if (result!=null){
                progressStart("","","");                
                result = encodeURIComponent(result);//中文编码转换                
                $.ajax({
					type: "POST",
					url: "../../common/ajax/ajax_saveSingleValue.asp",
					data: {tableName:tableName,tableId:tableId,fieldName:fieldName,newValue:result},
					async: false,//true：异步；false：同步
					success: function(msg){
						console.log(msg)
						progressEnd();
						if (msg!="F" && msg!="T"){
							myAlert(msg,"28","red");
						}else{
							if (msg=="F"){
								myAlert("操作失败！","28","red");
							}else{
								refreshTable()
							}
						}
					},
					error: function (jqXHR, textStatus, errorThrown) {
						progressEnd();
						alert(jqXHR.responseText);
						
						//alert("AJAX返回出错，请与技术人员联系！");
					}
                });	
			}			
		}
	})
}

//复选框设置值
function setCheckboxValue(objId,valueList){
	$("[id='"+objId+"']").each(function(index,ele){
		//alert(this.value)
		if ((","+valueList+",").indexOf(","+this.value+",")>=0){
			this.checked=true;
		}else{
			this.checked=false;
		}
	})
}


function fmoney(s, n)   
{   
   n = n > 0 && n <= 20 ? n : 2;   
   s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";   
   var l = s.split(".")[0].split("").reverse(),   
   r = s.split(".")[1];   
   t = "";   
   for(i = 0; i < l.length; i ++ )   
   {   
      t += l[i] + ((i + 1) % 3 == 0 && (i + 1) != l.length ? "," : "");   
   }   
   return t.split("").reverse().join("") + "." + r;   
}


//执行字符串JS代码
//使用方法：executeJs.Eval("字符串");
var executeJs={} //my namespace:) 
executeJs.Eval=function(code){
	//alert(code)
	if(!!(window.attachEvent && !window.opera)){ 
		//ie 
		execScript(code); 
	}else{ 
		//not ie 
		window.eval(code); 
	} 
}

var menuFavHtml = "";
//收藏菜单（快捷菜单）
function showMenuFav(fav,menuId){
	var eleObj = $(".widget.box .widget-header h4");
	var menuFavHtmlNew = "";
	if (menuFavHtml == ""){
		menuFavHtml = eleObj.html();
	}

	//console.log(menuFavHtml)
	if (menuId>0){
		if (fav){//fav=true
			menuFavHtmlNew = menuFavHtml + "<a class='bs-tooltip' data-html='true' data-original-title='取消快捷菜单' href=javascript:setMenuFav('"+menuId+"','cancel')><i class='icon-star'></i></a>"
		}else{
			menuFavHtmlNew = menuFavHtml + "<a class='bs-tooltip' data-html='true' data-original-title='设置快捷菜单' href=javascript:setMenuFav('"+menuId+"','set')><i class='icon-star-empty'></i></a>"
		}
		eleObj.html(menuFavHtmlNew)
	}
}

//设置取消快捷菜单
function setMenuFav(menuId,setOrCancel){
	$.ajax({
		type: "POST",
		url: "/common/setMenuFav/",
		data: {menuId:menuId,setOrCancel:setOrCancel},
		async: false,//true：异步；false：同步
		success: function(returnObj){
			//console.log(msg)
			progressEnd();

			if (returnObj.result == "T"){
				myAlertAutoClose(returnObj.scription,3);
				var fav;
				if (setOrCancel == "set"){
					fav = true;
				}else{
					fav = false;
				}
				showMenuFav(fav,menuId);
			}else{
				myAlert(returnObj.scription,"","")
			}
		},
		error: function (jqXHR, textStatus, errorThrown) {
			progressEnd();
			alert(jqXHR.responseText);

			//alert("AJAX返回出错，请与技术人员联系！");
		}
    });
}


//表格加载成功后的操作
function tableLoaded(data) {
	if (data.total == -1){
		myAlert(data.errorInfo,"","")
		setTimeout(function () {
			location.href="/system/login/"
		},3000)
	}
}

