var app = getApp();
Page({
    data: {
        list: [
            {
                date: "2020-11-11 22:30:23",
                order_number: "20201111223023001",
                content: "OAO",
            },
            {
                date: "2020-11-11 22:30:23",
                order_number: "20201111223023001",
                content: "QAQ",
            }
        ]
    },
    onLoad: function (options) {
        // 监听页面加载
    },
    onShow: function () {
        this.getCommentList();
    },
    getCommentList:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/my/comment/list"),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }

                that.setData({
                    list: resp.data.list
                });

            }
        });
    }
});
