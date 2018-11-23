
//设置表格需要隐藏的列
function setTableColumnForHide(tableId,field){
	if (field!="operate"){
		var fieldList=getCookie(tableId);
		if (fieldList==null){
			setCookie(tableId,field)
		}else{
			//判断是否已经存在
			if ((","+fieldList+",").indexOf(","+field+",")==-1){
				fieldList=fieldList+","+field;
				setCookie(tableId,fieldList)
			}
		}
	}
}

//设置表格取消隐藏的列
function setTableColumnForHideCancel(tableId,field){
	if (field!="operate"){
		var fieldList=getCookie(tableId);
		var fieldListNew="";
		if (fieldList!=null){
			tempArray=fieldList.split(",")
			for (i=0;i<tempArray.length;i++){
				if (tempArray[i]!=field){
					if (fieldListNew==""){
						fieldListNew=tempArray[i];
					}else{
						fieldListNew=fieldListNew+","+tempArray[i];
					}
				}
			}
		}
		if (fieldListNew==""){
			fieldListNew=null
		}
		setCookie(tableId,fieldListNew);
	}
}


//自动调整内容区域高度
window.onresize = autoSetcontentHeight;
function autoSetcontentHeight(){
	var height=getHeight();
	$("#contentMain").css("height",height-155);
	//console.log($("#tab_1_1").children().css("padding-right"))
	//console.log(height)
	$(".tab-content").css("height",height-270);
	$(".modal-body").css("height",height-200);
	//alert(width);
}



$(function(){
	
	
	//保存选择为不显示的数据列（以cookie方式保存）
	var width=getWidth();
	//alert(width)
	if (width<768){
		$("table[id^='cusTable']").each(function (index,domEle) { 
			var objId=$(domEle)[0].id//$(domEle).id
			//alert(objId)
			// domEle == this 
			//$(domEle).css("backgroundColor", "yellow");  
			//if ($(this).is("#stop")) { 
			//$("span").text("Stopped at div index #" + index); 
			//return false; 
			//} 
			//如果设备宽度小768，小型设备访问，如手机，表格众向显示数据
			$('#'+objId).bootstrapTable("toggleView");
			//自动隐藏上次选择为不显示的列
			var fieldListForHide=getCookie(objId);
			//console.log("fieldListForHide-A:"+fieldListForHide)
			if (fieldListForHide!=null){
				tempArray=fieldListForHide.split(",")
				for (i=0;i<tempArray.length;i++){
					$('#'+objId).bootstrapTable("hideColumn",tempArray[i]);
				}
			}
		});		
	}else{
		//自动隐藏上次选择为不显示的列
		$("table[id^='cusTable']").each(function (index,domEle) { 
			var objId=$(domEle)[0].id//$(domEle).id
			//console.log(objId)
			//alert(objId)
			// domEle == this 
			//$(domEle).css("backgroundColor", "yellow");  
			//if ($(this).is("#stop")) { 
			//$("span").text("Stopped at div index #" + index); 
			//return false; 
			//} 
			//自动隐藏上次选择为不显示的列
			var fieldListForHide=getCookie(objId);
			//console.log("fieldListForHide-B:"+fieldListForHide)
			if (fieldListForHide!=null){
				tempArray=fieldListForHide.split(",")
				for (i=0;i<tempArray.length;i++){
					//console.log(tempArray[i])
					$('#'+objId).bootstrapTable("hideColumn",tempArray[i]);
					
				}
			}
		});
	}
})


$(document).on('show.bs.modal', '.modal', function(event) {
        $(this).appendTo($('body'));
    }).on('shown.bs.modal', '.modal.in', function(event) {
        setModalsAndBackdropsOrder();
    }).on('hidden.bs.modal', '.modal', function(event) {
        setModalsAndBackdropsOrder();
    });


function setModalsAndBackdropsOrder() {  
    var modalZIndex = 1040;
    $('.modal.in').each(function(index) {
        var $modal = $(this);
        modalZIndex++;
        $modal.css('zIndex', modalZIndex);
        $modal.next('.modal-backdrop.in').addClass('hidden').css('zIndex', modalZIndex - 1);
    });
    $('.modal.in:visible:last').focus().next('.modal-backdrop.in').removeClass('hidden');
}