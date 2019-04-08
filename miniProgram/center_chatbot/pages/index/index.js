// pages/index/index.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;
const SystemInfo=app.globalData.SystemInfo;//用户手机信息
function ajaxData(logic_type,type,name,openid){
    var dataCon={
      logic_type: logic_type,
      type: type
    }
    if (type =="illness"){
      dataCon.search_name=name;//用户对话
    }else if(type=="get_office_by_ill"){
      dataCon.office_name=name;
    }
    dataCon.openid=openid;//用户openid
  return dataCon
}
function getHotSearch(_this){
  var openid = wx.getStorageSync("openid");//用户openid
  wx.request({
    url: baseUrl + 'wechat/chat-api/applets',
    data: {
      logic_type:"ency",
      openid:openid,
      type:"get_search"
    },
    header: {
      "Content-Type": "application/json"
    },
    method: 'POST',
    dataType: 'json',
    success: function(res) {
      var hot_search=res.data.hot_search;
      _this.setData({
        hot_search:hot_search
      },function(){
        _this.setData({
          load:false,
        })
      })
    }
  })
}
function search(_this,val){
  var openid=wx.getStorageSync("openid");//用户openid
  var SearchList=wx.getStorageSync("SearchList");//用户openid
  var requestData=ajaxData("ency","illness",val,openid)
  wx.request({
    url: baseUrl+'wechat/chat-api/applets',
    data:requestData,
    header: {
      "Content-Type": "application/json"
    },
    method: 'POST',
    dataType: 'json',
    success: function (res) {
      var data =res.data;
      var data_type = data.tab;
      var card = {}
      // 判断搜索出来的内容属于是症状还是疾病   ill疾病   sym症状
      if (data_type=="ill") {
        var ill_data=data.illness_desc
        var alias_arr = ill_data.alias
        alias_arr = alias_arr.replace(/[\'\[\]]/g, "")
        alias_arr = alias_arr.split(",")
        card.title=ill_data.name;
        card.tags = alias_arr;
        card.desc=ill_data.desc;
        card.type=data_type;
      } else if(data_type == "sym"){
        var alias_arr = data.alias
        alias_arr = alias_arr.replace(/[\'\[\]]/g, "")
        alias_arr = alias_arr.split(",")
        card.tags = alias_arr;
        card.title=data.name;
        card.desc=data.definition;
        card.type=data_type;
      }else{
        card.type="";
      }
      // 渲染到页面上
      _this.setData({
        cardData: card
      })
    }
  })
  // 创建搜索历史列表
  var Search_item={val:val,index:0}
  if (SearchList!=""&&SearchList!=undefined&&SearchList!=null){
    
    for(var i=0; i<SearchList.length; i++){
      if (val.indexOf(SearchList[i].val)!=-1){
        SearchList.splice(i,1);
        if(i>1){
          i--;
        }
      }else{
        SearchList[i].index=i+1;
      }
    }
   SearchList.unshift(Search_item);
    wx.setStorageSync("SearchList",SearchList);//用户openid
  }else{
    var Search=[];
    // Search_item.index=0;
    Search.push(Search_item);
    wx.setStorageSync("SearchList",Search);//用户openid
  }
  // 控制页面显示 index 首页    search 搜索页面   card搜索内容页面
  _this.setData({
    pageShow:"card"
  })
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    load:true,
    winH:0,
    pageShow:"index",
    input:false,
    search:"",//搜索输入框内容
    navBtn:[
      {icon:"../assets/img/angiocarpy-icon.svg",val:"心血管内科"},
      {icon: "../assets/img/breathing-icon.svg", val: "呼吸内科" },
      {icon: "../assets/img/oral-icon.svg", val: "口腔科" },
      {icon: "../assets/img/obstetric-icon.svg", val: "产科" },
      {icon: "../assets/img/eye-icon.svg", val: "眼科" },
      {icon: "../assets/img/dermatology-icon.svg", val: "皮肤科" },
      {icon: "../assets/img/pediatric-icon.svg", val: "儿科" },
      {icon: "../assets/img/male-icon.svg", val: "男科" }
    ],
    cardBtn:[
      {icon:'../assets/img/z-jb-icon.svg',val:"疾病详情"},
      {icon:'../assets/img/z-bz-icon.svg',val:"症状"},
      {icon:'../assets/img/z-zl-icon.svg',val:"治疗"},
    ],
    cardData:null,//卡片信息
    scrollData:"",
    scrollShowView:"",
    hot_search:[],//热搜
    searchList:[],
  },
  jumpTo:function(e){
    var url=e.currentTarget.dataset.url;
    wx.navigateTo({
      url: url
    })
  },

  // 疾病按钮 打开本页面 
  scroll_btn:function(e){
    var _this=this;
    const query = wx.createSelectorQuery();
    var winH = SystemInfo.windowHeight;//窗口的高度
    var openid=wx.getStorageSync("openid");//用户openid
    var val=e.currentTarget.dataset.val;
    // 请求数据
    var requestData=ajaxData("ency","get_office_by_ill",val,openid)
    //滚动条内容高度
    query.select(".scroll_search").boundingClientRect()
    _this.setData({
      pageShow: "scroll",
      load:true,
    })
    query.exec(function (res) {
      _this.setData({
        winH:winH-res[0].height
      })
    })

    wx.request({
      url: baseUrl+'wechat/chat-api/applets',
      data: requestData,
      header: {
        "Content-Type": "application/json"
      },
      method: "POST",
      dataType: "json",
      success: function (res) {
        const {data}=res;
        delete data.openid;
        // 渲染页面
        _this.setData({
          scrollData:data
        },function(){
          _this.setData({
            load:false,
          })
        })
      }
    })
  },
  // 疾病列表页内跳转
  scroll_to:function(e){
    var _this=this;
    var to=e.target.dataset.to;
    var showToast=to=="top"?"#":to
    wx.showToast({

      
      title: showToast,
      icon: 'none',
      duration: 300
    })
    _this.setData({
      scrollShowView:to
    })
  },
  // 输入框输入内容
  search_val:function(e){
    var _this=this;
    var val=e.detail.value;
    _this.setData({
      search:val
    })
  },
  // 首页输入框点击事件
  show_search:function(){
    var _this=this;
    var searchList=wx.getStorageSync("SearchList");
    getHotSearch(_this);//获取热搜内容
    _this.setData({
      pageShow:"search",
      input:true,
      searchList:searchList
    })
  },
  // 搜索
  send_search_btn:function(){
    var _this=this;
    // 用户输入内容
    var val=_this.data.search;
    if (val!=''&&val!=undefined&&val!=null){
      search(_this,val);
    }else{
      wx.showToast({
        title: '请输入您要搜索的内容',
        icon: 'none',
        duration: 1000
      })
    }
  },
  // 热门搜索点击
  hot_search_btn:function(e){
    var _this=this;
    var val=e.currentTarget.dataset.val;
    _this.setData({
      search:val
    })
    search(_this,val);
  },
  // 删除全部历史记录
  history_all_clear:function(e){
    var _this=this;
    wx.removeStorageSync("SearchList");
    _this.setData({
      searchList:[]
    })
    // var searchList=wx.getStorageSync("SearchList");
  },
  // 删除历史记录
  history_item_clear:function(e){
    var _this=this;
    var searchList=wx.getStorageSync("SearchList");
    var index=e.currentTarget.dataset.index;
    searchList.splice(index,1);
    for(var i in searchList){
      searchList[i].index=i;
    }
    wx.setStorageSync("SearchList",searchList)
    _this.setData({
      searchList: searchList
    })
  },
  // 卡片点击事件
  card_btn:function(e){
    var ctype=e.currentTarget.dataset.ctype;
    var name=e.currentTarget.dataset.name;
    var url=null;
    if(ctype=="ill"){
      url= '../components/illness/illness?id=0&name='+name;
    }else if(ctype=="sym"){
      url='../components/symptoms/symptoms?name='+name;
    }
    wx.navigateTo({
      url: url,
    })
  },
  // 紫色卡片点击事件
  illPage:function(e){
    var id=e.currentTarget.dataset.index;
    var name=e.currentTarget.dataset.name;
    // console.log(e)
    wx.navigateTo({
      url: '../components/illness/illness?id='+id+"&name="+name,
    })
  },
  // 返回首页
  back_index:function(){
    var _this=this;
    _this.setData({
      pageShow: "index",
      input: false,
      search:"",
      cardData:null,
      scrollData:"",
      scrollShowView: ""
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;
    var winH=SystemInfo.windowHeight;//窗口的高度
    console.log(1231231);

    try {//取得openid，没有就跳转到登录
      const openId = wx.getStorageSync('openid')
      console.log(openId);
      if (!openId) {
        wx.reLaunch({
          url: '../login/login'
        })
      }
    } catch (e) {
      wx.reLaunch({
        url: '../login/login'
      })
    }
    getHotSearch(_this);//获取热搜内容
      _this.setData({
        userInfo: app.globalData.userInfo,
        SystemInfo: app.globalData.SystemInfo,
        PhoneX:app.globalData.PhoneX
      })
    // 抑郁症    耳痛
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