//index.js
//获取应用实例
const app = getApp()
const baseUrl=app.globalData.baseUrl;//ajax请求链接
function ajaxData(code,userInfo){
  var dataCon={}
    dataCon.code=code;//用户code
  if (userInfo.avatarUrl!=""){
      dataCon.avatarUrl =userInfo.avatarUrl;//头像
    }
  if (userInfo.nickName!=""){
      dataCon.nickName=userInfo.nickName;//用户名称
    }
  if (userInfo.gender!=""){
      dataCon.gender=userInfo.gender;//用户性别
    }
  if (userInfo.country!=""){
      dataCon.country=userInfo.country;//用户所在国家
    }
  if (userInfo.province!=""){
      dataCon.province=userInfo.province;//用户所在省份
    }
  if (userInfo.city!=""){
      dataCon.city =userInfo.city;//用户所在城市
    }
  return dataCon
}
function getOpenID(userInfo){
  // 登录
  wx.login({
    success: res => {
      // console.log(res)
      console.log("用户code：" + res.code)
      wx.setStorageSync('UserCode', res.code)
      // 发送 res.code 到后台换取 openId, sessionKey, unionId
      wx.request({
        url:baseUrl+'wechat/chat-api/login',
        data:ajaxData(res.code,userInfo),
        header: {
          "Content-Type": "application/json"
        },
        method: 'POST',
        dataType: 'json',
        success: function(res) {
          const {data}=res;
          wx.setStorageSync('openid',data);
          wx.redirectTo({
            url: '../index/index',
          })
        }
      })
    }
  })
}
Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    tap:false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  // //事件处理函数
  // bindViewTap: function() {
  //   wx.navigateTo({
  //     url: '../logs/logs'
  //   })
  // },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  // 获取用户信息
  getUserInfo: function (e) {
    var _this=this;
    var tap=_this.data.tap;
    _this.setData({
      tap:true,
    })
    // 反之用户多次请求
    if(!tap){
      console.log('userInfo',e.detail.userInfo)
      // 判断用户信息有没有拿到
      if (e.detail.userInfo!=undefined && e.detail.userInfo!=null&&e.detail.userInfo!="") {
        var userInfo =e.detail.userInfo
        app.globalData.userInfo=userInfo
        // 获取用户授权
        wx.getSetting({
          success: res => {
            console.log(res)
            // 判读用户是否全部授权
            if(res.authSetting['scope.record']&&res.authSetting['scope.userInfo']){
              console.log("全有")
              getOpenID(userInfo)
            } else if(res.authSetting['scope.userInfo']){
              getOpenID(userInfo)
            }else{
              // 如果没有则重新让用户授权
              wx.openSetting({
                success(res) {
                  if(res.authSetting['scope.userInfo']){
                    getOpenID(userInfo)
                  }else{
                    _this.setData({
                      tap: false,
                    })
                  }
                }
              })
            }
          }
        })
      }else{
          wx.showToast({
            title: "如要试用该小程序请允许这些授权，否则您将会使用不了",
            icon: 'none',
            duration: 1500
          })
        _this.setData({
          tap: false,
        })
      }
    }


  }
})
