const app=getApp();
const baseUrl=app.globalData.baseUrl;
// pages/my/my.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo:"",
    SystemInfo:"",
    mylist:[
      {icon:'../assets/img/user-info-icon.svg',val:"个人信息",url:"../components/myInfo/myInfo"},
      {icon:'../assets/img/la-pj-icon.svg',val:"问诊记录",url:"../components/interrogation/interrogation"},
      {icon:'../assets/img/about-icon.svg',val:"关于我们",url:"../components/about/about"}
    ]
  },
  jumpTo:function(e){
    var url=e.currentTarget.dataset.url;
    if(url!=''&&url!=null&&url!=undefined){
      wx.navigateTo({
        url: url,
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;
    _this.setData({
      userInfo: app.globalData.userInfo,
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