//app.js
App({
  globalData: {
    userInfo: null,
    SystemInfo:null,
    PhoneX:null,
    // baseUrl:"http://admin.ccc.org/"//http://admin.ccc.org/   https://dev.centerai.cn/
    baseUrl:"https://dev.centerai.cn/"//http://admin.ccc.org/   https://dev.centerai.cn/
  },
  onLaunch: function () {
    var _this=this;
    // 获取用户手机系统信息
    wx.getSystemInfo({
      success: function(res) {
        _this.globalData.SystemInfo=res
      },
    })
    _this.globalData.PhoneX=_this.globalData.SystemInfo.model.search("iPhone X")!=-1?"68":"0";
    // 登录
    wx.login({
      success: res => {
        // console.log(res)
        console.log("用户code："+res.code)
        wx.setStorageSync('UserCode',res.code)
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo
              // wx.setStorageSync('userImg', res.userInfo.avatarUrl)
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
            
          })
        }
         if(!res.authSetting['scope.record']){
           wx.authorize({
            scope: 'scope.record',
            success () {
              // 用户已经同意小程序使用录音功能，后续调用 wx.startRecord 接口不会弹窗询问
              // wx.startRecord
            }
          })
        }
        if(res.authSetting['scope.record']&&res.authSetting['scope.userInfo']){
          // console.log(wx.getStorageSync("openid"))
          if(wx.getStorageSync("openid")!=""&&wx.getStorageSync("openid")!=undefined&&wx.getStorageSync("openid")!=null){
            wx.redirectTo({
              url: '../index/index',
            })
          }
        }
      }
    })
   
  }
})