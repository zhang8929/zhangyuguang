// pages/components/symptoms/symptoms.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;
function ajaxData(search_name,code,avatarUrl,nickName,gender,country,province,city,openid,session_key){
    var dataCon={
      logic_type: 'ency',
      type: "illness"
    }
    dataCon.search_name=search_name;//用户对话
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
    load:true,
    pageData:""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this=this;
    var name=options.name;
    var UserCode=wx.getStorageSync("UserCode");//用户code
    var openid=wx.getStorageSync("openid");//用户openid
    var userInfo=app.globalData.userInfo;
    console.log(userInfo)
    var requestData=null;//ajax请求数据
    //判断用户是否登录   未登录第一次提交用户的信息  登录过后只提交用户的openid
    if(openid!=null&&openid!=undefined&&openid!=""){
    // 登录
    requestData=ajaxData(name,"","","","","","","",openid,"")
    }else{
      // 未登录
    requestData=ajaxData(name,UserCode,userInfo.avatarUrl,userInfo.nickName,userInfo.gender,userInfo.country,userInfo.province,userInfo.city,"","")
    }
    wx.request({
      url:baseUrl+'wechat/chat-api/applets',
      data:requestData,
      header: {
        "Content-Type": "application/json"
      },
      method: 'POST',
      dataType: 'json',
      success: function(res) {
        // 保存用户id
        // wx.setStorageSync("openid",res.data.openid);
        // 渲染数据
        _this.setData({
          pageData:res.data
        },function(){
          _this.setData({
            load: false
          })
        })
      }
    })
    // 保存用户信息和用户手机信息
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