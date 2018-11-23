var Login = function() {
    var b = function() {
        if ($.fn.uniform) {
            $(":radio.uniform, :checkbox.uniform").uniform()
        }
    };
    var c = function() {
        $(".sign-up").click(function(h) {
            h.preventDefault();
            $(".login-form").slideUp(350,
            function() {
                $(".register-form").slideDown(350);
                $(".sign-up").hide()
            })
        });
        $(".back").click(function(h) {
            h.preventDefault();
            $(".register-form").slideUp(350,
            function() {
                $(".login-form").slideDown(350);
                $(".sign-up").show()
            })
        })
    };
    var g = function() {
        $(".forgot-password-link").click(function(h) {
            h.preventDefault();
            $(".forgot-password-form").slideToggle(200);
            $(".inner-box .close").fadeToggle(200)
        });
        $(".inner-box .close").click(function() {
            $(".forgot-password-link").click()
        })
    };
    var e = function() {
        if ($.validator) {
            $.extend($.validator.defaults, {
                errorClass: "has-error",
                validClass: "has-success",
                highlight: function(k, i, j) {
                    if (k.type === "radio") {
                        this.findByName(k.name).addClass(i).removeClass(j)
                    } else {
                        $(k).addClass(i).removeClass(j)
                    }
                    $(k).closest(".form-group").addClass(i).removeClass(j)
                },
                unhighlight: function(k, i, j) {
                    if (k.type === "radio") {
                        this.findByName(k.name).removeClass(i).addClass(j)
                    } else {
                        $(k).removeClass(i).addClass(j)
                    }
                    $(k).closest(".form-group").removeClass(i).addClass(j);
                    $(k).closest(".form-group").find('label[generated="true"]').html("")
                }
            });
            var h = $.validator.prototype.resetForm;
            $.extend($.validator.prototype, {
                resetForm: function() {
                    h.call(this);
                    this.elements().closest(".form-group").removeClass(this.settings.errorClass + " " + this.settings.validClass)
                },
                showLabel: function(j, k) {
                    var i = this.errorsFor(j);
                    if (i.length) {
                        i.removeClass(this.settings.validClass).addClass(this.settings.errorClass);
                        if (i.attr("generated")) {
                            i.html(k)
                        }
                    } else {
                        i = $("<" + this.settings.errorElement + "/>").attr({
                            "for": this.idOrName(j),
                            generated: true
                        }).addClass(this.settings.errorClass).addClass("help-block").html(k || "");
                        if (this.settings.wrapper) {
                            i = i.hide().show().wrap("<" + this.settings.wrapper + "/>").parent()
                        }
                        if (!this.labelContainer.append(i).length) {
                            if (this.settings.errorPlacement) {
                                this.settings.errorPlacement(i, $(j))
                            } else {
                                i.insertAfter(j)
                            }
                        }
                    }
                    if (!k && this.settings.success) {
                        i.text("");
                        if (typeof this.settings.success === "string") {
                            i.addClass(this.settings.success)
                        } else {
                            this.settings.success(i, j)
                        }
                    }
                    this.toShow = this.toShow.add(i)
                }
            })
        }
    };
    var d = function() {
        if ($.validator) {
            $(".login-form").validate({
                invalidHandler: function(i, h) {
                    NProgress.start();
                    $(".login-form .alert-danger").show();
                    NProgress.done()
                },
                submitHandler: function(h) {
                    //window.location.href = "index.html"
                    var jsonObj=form2JsonObj("formLogin");
                    var jsonStr=form2JsonStr("formLogin");

                    //alert(jsonStr)
                    //开始服务器验证登录
                    //var jsonStr=encodeURIComponent(jsonStr);//中文编码转换

					//alert(jsonStr)
					$.ajax({
						url: "../../system/ajaxLogin/",
						type: "post",
						data: {data:jsonStr},
						success: function (text) {
							//alert("提交成功，返回结果:" + text);
							if (text=="T")
							{
								if (getCookie('username')==null){
									//alert("A:"+getCookie('username')+jsonObj.remember)
									setCookie("username",jsonObj.username,365);
									setCookie("password",jsonObj.password,365);
								}else{
									//alert("B:"+getCookie('username')+jsonObj.remember)
								}
								if (jsonObj.remember==""){
									//alert("ABCD")
									delCookie("username");
									delCookie("password");
								}
								setTimeout(function (){
									window.location = "/system/index/";
								}, 500);
							}else{
								alert(text)
							}
						},
						error:function(jqXHR, textStatus, errorThrown){
							alert(jqXHR.responseText);
							alert("AJAX返回出错，请与技术人员联系！");
						}
					});
                }
            })
        }
    };
    var f = function() {
        if ($.validator) {
            $(".forgot-password-form").validate({
                submitHandler: function(h) {
                    $(".inner-box").slideUp(350,
                    function() {
                        $(".forgot-password-form").hide();
                        $(".forgot-password-link").hide();
                        $(".inner-box .close").hide();
                        $(".forgot-password-done").show();
                        $(".inner-box").slideDown(350)
                    });
                    return false
                }
            })
        }
    };
    var a = function() {
        if ($.validator) {
            $(".register-form").validate({
                invalidHandler: function(i, h) {},
                submitHandler: function(h) {
                    window.location.href = "index.html"
                }
            })
        }
    };
    return {
        init: function() {
            b();
            c();
            g();
            e();
            d();
            f();
            a()
        },
    }
} ();


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
