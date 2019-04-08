// pages/components/drugInfo/drugInfo.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;
function ajaxData(id){
  var dataCon={
    logic_type:'ency',
    type:"get_yao_detail",
    openid:wx.getStorageSync("openid"),
  }
  dataCon.search=id;//用户对话
    // dataCon.openid=openid;//用户openid
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
    var id=options.id;
    var requestData=ajaxData(id)
    // _this.setData({
    //   name: name
    // })
    wx.request({
      url: baseUrl+'wechat/chat-api/applets',
      data:requestData,
      header: {
        "Content-Type": "application/json"
      },
      method: 'POST',
      dataType: 'json',
      success: function(res) {
        var data=res.data;
          // 设置内容部分的高度
        if (data["图片"]=="http://img.39.net/ypk/images/nopic.gif"){
          data["图片"]=baseUrl+"img/drugs-default.svg";
        }
          _this.setData({
            pageData:data,
          },function(){
            _this.setData({
              load:false,
            })
          })
      }
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