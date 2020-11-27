;
var rider_set_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_rider_set .save").click(function(){
            console.log("1111111111111111111111111");
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var uid_target = $(".wrap_rider_set input[name=uid]");
            var uid = uid_target.val();

            var rid_target = $(".wrap_rider_set input[name=rid]");
            var rid = rid_target.val();

            var nickname_target = $(".wrap_rider_set input[name=nickname]");
            var nickname = nickname_target.val();

            var mobile_target = $(".wrap_rider_set input[name=mobile]");
            var mobile = mobile_target.val();

            var adarea_target = $(".wrap_rider_set input[name=adarea]");
            var adarea = adarea_target.val();



            if( nickname.length < 1 ){
                common_ops.tip( "请输入符合规范的姓名~~",nickname_target );
                return false;
            }


            btn_target.addClass("disabled");

            var data = {
                uid: uid,
                nickname: nickname,
                mobile: mobile,
                adarea: adarea,
                rid:$(".wrap_rid_set input[name=rid]").val()
            };

            $.ajax({
                url:common_ops.buildUrl( "/rider/set" ),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/rider/index");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });


        });
    }
};

$(document).ready( function(){
    rider_set_ops.init();
} );