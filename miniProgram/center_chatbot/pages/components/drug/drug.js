// pages/components/drug/drug.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;
function ajaxData(name){
  var dataCon={
    logic_type: 'ency',
    type: "get_yao_ty",
    openid:wx.getStorageSync("openid"),
  }
  dataCon.search=name;//用户对话
    // dataCon.openid=openid;//用户openid
  return dataCon
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    load:true,
    name:"",
    pageData:""
  },
  toInfo:function(e){
    var id=e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '../drugInfo/drugInfo?id='+id,
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this=this;
    var name=options.name;
    var requestData = ajaxData(name)
    _this.setData({
      name: name
    })
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
        var pageData=data.info;//请求的页面数据
        // 错误的默认图片
        var gif="http://img.39.net/ypk/images/nopic.gif"
        // 把错误的默认图片改成正确的默认图片
        for (var i = 0; i <pageData.length; i++){
          if (pageData[i].img==gif){
            pageData[i].img=baseUrl+"img/drugs-default.svg"
          }
        }
          _this.setData({
            pageData: pageData,
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