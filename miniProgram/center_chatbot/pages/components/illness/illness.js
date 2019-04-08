// pages/components/illness/illness.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;
// 卡片切换
function scrollAnimation(_this,index,transition){
  // 获取卡片参数
  // 是否执行动画
  var animation=transition?"transition: transform .3s;":""
  // 切换卡片
    _this.setData({
      scrollX:"transform: translateX(-"+index*100+"%);"+animation
    })
}
function ajaxData(search_name,openid){
    var dataCon={
      logic_type: 'ency',
      type: "illness"
    }
    dataCon.search_name=search_name;//用户对话
    if(openid!=""){
      dataCon.openid=openid;//用户openid
    }
  return dataCon
}
Page({
  /**
   * 页面的初始数据
   */
  data: {
    load:true,
    illName:"",
    infoBtn:[
      {icon:"../../assets/img/z-jb-icon.svg",val:"疾病详情"},
      {icon:"../../assets/img/z-bz-icon.svg",val:"症状"},
      {icon:"../../assets/img/z-zl-icon.svg",val:"治疗"},
    ],
    btnIndex:1,//按钮选中
    pageData:"",//页面数据
    domH:0,//卡片高度
    scrollX:0,//滚动距离
    SclientX:0,//滚动的起始点
    SystemInfo:"",
    userInfo:"",
    PhoneX:""
  },
  //按钮切换   事件
  tabBar:function(e){
    var _this=this;
    // 获取当前点击下标
    var index=e.currentTarget.dataset.index;
    // 设置下标
    _this.setData({
      btnIndex: index
    })
    // 执行卡片切换动画
    scrollAnimation(_this,index,true)
  },
  // 侧滑开始 事件
  scrollStart:function(e){
    var _this=this;
    // 保存滚动起始点
    _this.setData({
      SclientX:e.changedTouches[0].clientX
    })
  },
  scrollEnd: function (e) {
    var _this=this;
    // 获取起始点坐标
    var Sx=_this.data.SclientX;
    // 获取终点坐标
    var Ex=e.changedTouches[0].clientX;
    // 获取当前按钮下标
    var index=_this.data.btnIndex;
    // 获取按钮数量
    var length=_this.data.infoBtn.length
    var i=null;
    // 判断起始点是否大于终点  右滑动   同理相反
    if(Sx-Ex>80){
      // 判断右滑动是否是最后一个卡片  最后一个不再左不滑动
      if(index+1>length-1){
        i=length-1;
      }else{
        i=index+1;
      }
    }else if(Ex-Sx>80){
      // 判断左滑动是否是第一个卡片  第一个不再左滑动
      if(index-1<0){
        i=0;
      }else{
        i=index-1;
      }
    }
    if(i!=null){
      // 执行滑动动画
      scrollAnimation(_this, i, true)
      // 改变按钮选中
      _this.setData({
        btnIndex: i
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this=this;
    var UserCode=wx.getStorageSync("UserCode");//用户code
    var openid=wx.getStorageSync("openid");//用户openid
    var userInfo=app.globalData.userInfo;
    // 获取聊天卡点点击的按钮
    var illName=options.name;
    // 根据点击按钮的id来显示页面   上一页用户点击按钮下标  这一页默认显示
    var btnIndex=options.id;
    // 登录
    var requestData=ajaxData(illName,openid)
    // 请求页面数据
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
        const headquery = wx.createSelectorQuery();
        var winH = app.globalData.SystemInfo.windowHeight;//窗口的高度
        // 获取切换按钮
        headquery.select("#head").boundingClientRect()
        headquery.exec(function (res) {
          // 设置内容部分的高度
          _this.setData({
            pageData:data,
            domH:winH-res[0].height
          },function(){
            _this.setData({
              load:false
            })
          })
        })
        // wx.setStorageSync("openid",data.openid);
        // 按钮切换  btnIndex显示的下标
        scrollAnimation(_this,btnIndex,false)
      }
    })
    // 根据点击按钮的id来显示页面
    _this.setData({
      btnIndex:btnIndex,
      illName:illName,
      userInfo:userInfo,
      SystemInfo: app.globalData.SystemInfo,
      PhoneX: app.globalData.PhoneX
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