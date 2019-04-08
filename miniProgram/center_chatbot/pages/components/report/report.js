// pages/components/report/report.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;
function ajaxData(talkid,code,avatarUrl,nickName,gender,country,province,city,openid,session_key){
    var dataCon={
        logic_type: "inquiry",
        quary_type:"res"
    }
    dataCon.talkid=talkid;
    dataCon.code=code;//用户code；
    if(avatarUrl!=""){
      dataCon.avatarUrl=avatarUrl;//头像
    }
    if(nickName!=""){
      dataCon.nickName=nickName;//用户名称
    }
    if(gender!=""){
      dataCon.gender=gender;//用户性别
    }
    if(country!=""){
      dataCon.country=country;//用户所在国家
    }
    if(province!=""){
      dataCon.province=province;//用户所在省份
    }
    if(city!=""){
      dataCon.city=city;//用户所在城市
    }
    if(openid!=""){
      dataCon.openid=openid;//用户openid
    }
    if(session_key!=""){
      dataCon.session_key=session_key
    }
  return dataCon
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo:"",
    pageInfo:"",
    load:true
  },
  switch_btn:function(e){
    var _this=this;
    var pageInfo=_this.data.pageInfo;//获取页面数据
    var list=pageInfo.list;//获取可能患病列表
    var index=e.currentTarget.dataset.index;//获取当前点击下标
    var Bswitch=list[index].switch;//获取当前icon是关闭状态还是开的状态
    list[index].switch=Bswitch?false:true;//设置
    _this.setData({
      pageInfo:pageInfo
    })
  },
  details_btn:function(e){
    var _this=this;
    var name=e.currentTarget.dataset.val;
    wx.navigateTo({
      url: '../illness/illness?name='+name+'&id=0',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this=this;
    var talkid=options.id;
    var UserCode=wx.getStorageSync("UserCode");//用户code
    var openid=wx.getStorageSync("openid");//用户openid
    var userInfo=app.globalData.userInfo;
    var sick_list=JSON.parse(options.val);
    var show=options.show;//
    var requestData=null;//ajax请求数据=
    //判断用户是否登录   未登录第一次提交用户的信息  登录过后只提交用户的openid
    if(openid!=null&&openid!=undefined&&openid!=""){
    // 登录
    requestData=ajaxData(talkid,"","","","","","","",openid,"")
    }else{
      // 未登录
    requestData=ajaxData(talkid,UserCode,userInfo.avatarUrl,userInfo.nickName,userInfo.gender,userInfo.country,userInfo.province,userInfo.city,"","")
    }
    wx.request({//http://admin.ccc.org/   https://dev.centerai.cn/
      url: baseUrl+'wechat/chat-api/applets',
      data: requestData,
      header: {
        "Content-Type": "application/json"
      },
      method: "POST",
      dataType: "json",
      success: function (res) {
        var data=res.data;
        // 保存用户id
        // wx.setStorageSync("openid",data.openid);
        // 便利所有可能得的病列表
        for(var i=0; i<sick_list.length; i++){
          // 根据用户上一页点击的病症卡下标来默认展开
          if(show==i){
            sick_list[i].switch=true;
          }else{
            sick_list[i].switch=false;
          }
        }
        data.list=sick_list;
        _this.setData({
          userInfo:userInfo,
          pageInfo:data
        },function(){
          _this.setData({
            load:false
          })
        })
      }
    })
  _this.setData({
    userInfo: userInfo,
    SystemInfo: app.globalData.SystemInfo,
  })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})