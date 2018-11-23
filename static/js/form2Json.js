//表单转Json字符串
//encodeURIComponent
function form2JsonStrOrg(formName) {
    var form = document.getElementById(formName);
    var sb = new StringBuilder();
    var rcs = new Map();
    //alert(form.elements.length)
    for (var i = 0; i < form.elements.length; i++) {
        var element = form.elements[i];
        var name = element.name;
        var id=element.id;
        //console.log(element.tagName+":"+id+":"+$("#"+id).val());
        if (typeof(name) === "undefined" || (name === null) || (name.length === 0)) {
            continue;
        }

        var tagName = element.tagName;
        if (tagName === 'INPUT' || tagName === 'TEXTAREA') {
            var type = element.type;
            if ((type === 'text') || (type === 'password') || (type === 'hidden') || (type === 'number') || (tagName === 'TEXTAREA')) {
            		//console.log(element.value);
                sb.append("\"" + name + "\":\"" + (element.value.replace(/\r\n/ig, "")) + "\"");
            } else if ((type === 'checkbox') || (type === 'radio')) {
                rcs.putOverride(name, type);
            } else {
                continue;
            }
        } else if (tagName === 'SELECT') {
	        	var selectValue=$("#"+id).val();
	        	if (selectValue==null){
	        		selectValue=""
	        	}
	        	sb.append("\"" + name + "\":\"" + (selectValue) + "\"");
//          var oc = element.options.length;
//          var ifSelect=false;
//          for (var j = 0; j < oc; j++) {
//              //if (element.options[j].selected){sb.append("\""+name+"\":\""+(element.value)+"\"");}
//              //if (element.options[j].selected){sb.append("\""+name+"\":\""+(element.value.replace(/\r\n/ig,""))+"\"");}
//              if (element.options[j].selected){
//              	ifSelect=true;
//              	sb.append("\"" + name + "\":\"" + (element.value.replace(/\r\n/ig, "")) + "\"");
//              }
//          }
//          if (!ifSelect){
//              sb.append("\"" + name + "\":\"\"");
//          }
        }
    }
    if (rcs.size() > 0) {
        for (var i = 0; i < rcs.size(); i++) {
            var r = rcs.element(i);
            var radio = "";
            var d = document.getElementsByName(r.key);
            if (r.value === "radio") {
                for (j = 0; j < d.length; j++) {
                    //if(d[j].checked){radio=d[j].value;}
                    if (d[j].checked) {
                        radio = d[j].value.replace(/\r\n/ig, "");
                    }
                }
            } else {
                for (j = 0; j < d.length; j++) {
                    //if(d[j].checked){radio+=","+d[j].value;}
                    if (d[j].checked) {
                    		if (radio==""){
                    			radio = d[j].value.replace(/\r\n/ig, "");
                    		}else{
                    			radio += "," + d[j].value.replace(/\r\n/ig, "");
                    		}
                    }
                }
                radio.substr(1);
            }
            sb.append("\"" + r.key + "\":\"" + radio + "\"");
        }
    }
    return "{" + sb.toJsonString() + "}";
}

function form2JsonStr(formName){
	var str = form2JsonStrOrg(formName);
	//return encodeURIComponent(str);
    return str;
}

//表单转Json对象
function form2JsonObj(formName){
	var str=form2JsonStrOrg(formName)
	var obj = eval('(' + str + ')');
	return obj;
}


function StringBuilder(){
    this._element_ = new Array();
    this.append = function(item) {
        this._element_.push(item);
    }
    this.toString = function() {
        return this._element_.join("");
    }
    this.toJsonString = function() {
        return this._element_.join(",");
    }
    this.join = function(separator) {
        return this._element_.join(separator);
    }
    this.length = function() {
        return this._element_.length;
    }    
}

function Map() {
    this.elements = new Array();
    // 获取MAP元素个数
    this.size = function() {
        return this.elements.length;
    }
    // 判断MAP是否为空
    this.isEmpty = function() {
        return (this.elements.length < 1);
    }
    // 删除MAP所有元素
    this.clear = function() {
        this.elements = new Array();
    }
    // 向MAP中增加元素（key, value)
    this.put = function(_key, _value) {
        this.elements.push({key : _key,value : _value});
    }    
    //增加元素并覆盖
    this.putOverride = function(_key,_value){
        this.remove(_key);
        this.put(_key,_value);
    }
    // 删除指定KEY的元素，成功返回True，失败返回False
    this.remove = function(_key) {
        var bln = false;
        try {
            for (i = 0; i < this.elements.length; i++) {
                if (this.elements[i].key == _key) {
                    this.elements.splice(i, 1);
                    return true;
                }
            }
        } catch (e) {
            bln = false;
        }
        return bln;
    }

    // 获取指定KEY的元素值VALUE，失败返回NULL
    this.get = function(_key) {
        try {
            for (i = 0; i < this.elements.length; i++) {
                if (this.elements[i].key == _key) {
                    return this.elements[i].value;
                }
            }
        } catch (e) {
            return null;
        }
    }
    // 获取指定索引的元素（使用element.key，element.value获取KEY和VALUE），失败返回NULL
    this.element = function(_index) {
        if (_index < 0 || _index >= this.elements.length) {
            return null;
        }
        return this.elements[_index];
    }
    // 判断MAP中是否含有指定KEY的元素
    this.containsKey = function(_key) {
        var bln = false;
        try {
            for (i = 0; i < this.elements.length; i++) {
                if (this.elements[i].key == _key) {
                    bln = true;
                }
            }
        } catch (e) {
            bln = false;
        }
        return bln;
    }
    // 判断MAP中是否含有指定VALUE的元素
    this.containsValue = function(_value) {
        var bln = false;
        try {
            for (i = 0; i < this.elements.length; i++) {
                if (this.elements[i].value == _value) {
                    bln = true;
                }
            }
        } catch (e) {
            bln = false;
        }
        return bln;
    }
    // 获取MAP中所有VALUE的数组（ARRAY）
    this.values = function() {
        var arr = new Array();
        for (i = 0; i < this.elements.length; i++) {
            arr.push(this.elements[i].value);
        }
        return arr;
    }
    // 获取MAP中所有KEY的数组（ARRAY）
    this.keys = function() {
        var arr = new Array();
        for (i = 0; i < this.elements.length; i++) {
            arr.push(this.elements[i].key);
        }
        return arr;
    }
}
