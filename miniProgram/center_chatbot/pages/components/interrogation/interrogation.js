// pages/components/interrogation/interrogation.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;

function ajaxData(time,openid){
    var dataCon={
      logic_type: 'ency',
      type: "get_inquiry_record"
    }
    dataCon.year=time.year;//用户对话
    dataCon.month=time.month;//用户对话
    if(openid!=""){
      dataCon.openid=openid;//用户openid
    }
  return dataCon
}
// 数字小于10加0
function toStr(num){
  if(num<10){
    return "0"+num
  }else{
    return num
  }
}
// 设置时间选择器数据
function setpicker(_this,minDate,maxDate){
    // 转换成num
    minDate[0]=parseInt(minDate[0])
    minDate[1]=parseInt(minDate[1])
    // console.log(minDate)
    // 多级下拉列表数据
    var multiArray=[];
    // 多级下拉列表  年 初始
    var yearSelect=[];
    // 多级下拉列表  月  初始
    var daySelect=[];
    // 多级下拉 “年” 对应的月份 动态
    var ObjmultiArray=[];
    // 便利最小年份  到最大年份 区间年份
    for(var i=minDate[0]; i<=maxDate[0]; i++){
      // 对应年份的月份区间 
      var startM=1;
      var endM=12;
      // 对应年份的月份列表
      var monthList=[];
      // 判断当前年份是否是最小年份
      if(i==minDate[0]){
        // 最小年份的起始月份
        startM=minDate[1];
      }
      // 判断当前年份是否是最大年份
      if(i==maxDate[0]){
        // 最大年份的最大月份
        endM=maxDate[1];
      }
      // 便利对应年份的月份列表
      for(var y=startM; y<=endM; y++){
        monthList.unshift(y);
      }
      // 存储年份列表
      yearSelect.unshift(i)
      // 存储月份列表
      ObjmultiArray.unshift(monthList);
    }
    // 便利默认年份的月列表
    for(var j=maxDate[1]; j<=maxDate[1]; j++){
      daySelect.unshift(j)
    }
    // 默认选中列表
    multiArray.push(yearSelect,daySelect);
    // 渲染数据
    _this.setData({
      multiArray: multiArray,
      ObjmultiArray:ObjmultiArray,
    })
}
function getPageData(date,callback){
  var openid=wx.getStorageSync("openid");//用户openid
  var requestData=ajaxData(date,openid);
  console.log(requestData)
  console.log("---ajaxData---")
  wx.request({
    url: baseUrl + 'wechat/chat-api/applets',
    data: requestData,
    header: {
      "Content-Type": "application/json"
    },
    method: 'POST',
    dataType: 'json',
    success: function (res) {
      var data = res.data.list;
      console.log(res.data)
      console.log("---callbackData---")
      var minDate=res.data.old_time.split("-");
      minDate.splice(minDate.length-1,1);
      // 获取记录最后一条数据下标
      for (var i in data) {
        var M_D = data[i].day.split(" ")[0].split("-");
        M_D.splice(0, 1);
        data[i].day = M_D[0] + "月" + M_D[1] + "日";
      }
      callback(data,minDate)
    }
  })
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    load:true,
    navBerActive:1,
    navBer:["11月记录","本月记录"],
    pageData:{
      _thisMonth:[],
      prevMonth:[]
    },
    // prevMonthPageData:"",
    multiArray:[],
    ObjmultiArray:[],
    _thisMonth:"",//本月
    prevMonth:""//上一月
  },
  // 卡片点击
  report:function(e){
    var val=JSON.stringify(e.currentTarget.dataset.val);//获取所有卡片信息
    var id=e.currentTarget.dataset.id;//获取用户点击卡片的id
    var index=e.currentTarget.dataset.index;//获取用户点击的卡片下标     跳转到  自诊报告页面   默认展开的下标
    wx.navigateTo({
      url: '../report/report?id='+id+'&val='+val+'&show='+index,
    })
  },
  nav_item:function(e){
    var _this=this;
    var index=e.currentTarget.dataset.index;
    _this.setData({
      navBerActive:index
    })
    
  },
  time_list_change:function(e){
    var _this=this;
    // 获取默认显示的数据列表
    var multiArray=_this.data.multiArray;
    // 获取对应的二级联动列表
    var ObjmultiArray=_this.data.ObjmultiArray
    // 获取改变的列数
    var col=e.detail.column;
    // 获取改变当前列数下改变的下标
    var val=e.detail.value;
    // 判断当前改变的列是否是第一列
    if (col==0){
      // 对应第一列的二级列表
      multiArray[1]=ObjmultiArray[val];
      console.log(multiArray)
      // 渲染页面
      _this.setData({
        multiArray:multiArray
      })
    }
  },
  time_list_ajax:function(e){
    var _this=this;
    // 获取默认显示的数据列表
    var multiArray=_this.data.multiArray;
    // 获取时间实例
    var date=new Date;
    // 获取当前年
    var Getyear=date.getFullYear();
    // 获取月
    var Getmonth=date.getMonth()+1
    // 选中的时间数组
    var colNum=e.detail.value; //array
    // 选中的年份
    var year=multiArray[0][colNum[0]];
    // 选中的月份
    var month=multiArray[1][colNum[1]];

  //TODO 如果 colNum 有一个返回的是null 这是小程序编辑器的bug  不要再查了
    // 按钮内容     本月
    var _thisMonthT=toStr(month)+"月记录"
    // 按钮内容     上个月
    var prevMonthT=toStr(month-1<=0?12:month-1)+"月记录"
    // 如果当前选中的是现在的月份
    if (year==Getyear&&month-0==Getmonth){
      _thisMonthT="本月记录"
    }
    // 更新按钮内容
    var navBer=[prevMonthT,_thisMonthT];
    // 本月请求数据
    var _thisMonthObj={
      year:year,
      month:toStr(month)
    }
    // 上月请求数据
    var prevMonthObj={
      year:month-1<=0?year-1:year,
      month:toStr(month-1<=0?12:month-1)
    }
    // 更新按钮内容  按钮默认选中
    _this.setData({
      navBer:navBer,
      navBerActive:1
    })
    // 请求选中月份数据
    getPageData(_thisMonthObj,function(data,minDate){
      // 设置数据  上个月的内容清空
      var pageData={
        _thisMonth:data,
        prevMonth:[]
      }
      // 渲染页面数据 
      _this.setData({
        pageData: pageData,
      })
      // 判断 当前月份-1是否是 最小月份 如果不是请求上月的数据
      if((minDate[0]==year&&(minDate[1]-0)<month-1)||minDate[0]<year){
        getPageData(prevMonthObj, function (data, minDate) {
          // 获取选中月份的数据
          var _thisMonth = _this.data.pageData._thisMonth;
          // 设置数据
          var pageData = {
            _thisMonth:_thisMonth,
            prevMonth: data
          }
          // 渲染页面
          _this.setData({
            pageData: pageData,
          })
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this=this;
    // 获取时间实例
    var date=new Date;
    // var prevNum=null;
    // 获取当前年
    var year=date.getFullYear();
    // 获取月
    var month=date.getMonth()+1;
    // console.log(month)
    // 按钮内容
    var navBer=[toStr(month-1<=0?12:month-1)+"月记录","本月记录"];
    // 本月请求数据
    var _thisMonthObj={
      year:year,
      month:toStr(month)
    }
    // 上月请求数据
    var prevMonthObj={
      year:month-1<=0?year-1:year,
      month:toStr(month-1<=0?12:month-1)
    }
    // 渲染到页面
    _this.setData({
      navBer:navBer
    })
    // console.log(month)
    // 当前月份
    var maxDate=[year,month]
    // 获取本月数据
    getPageData(_thisMonthObj,function(data,minDate){
      var navBer=[toStr(month-1<=0?12:month-1)+"月记录","本月记录"];
      // console.log(minDate)
      // 设置数据
      var pageData={
        _thisMonth:data,
        prevMonth:[]
      }
      // 渲染到页面
      _this.setData({
        pageData: pageData,
        navBer:navBer
      })
      setpicker(_this, minDate, maxDate);
      // 判断最小月份是否小于当前月份-1
      if((minDate[0]==year&&(minDate[1]-0)<month-1)||minDate[0]<year){
        getPageData(prevMonthObj, function (data, minDate) {
          var _thisMonth = _this.data.pageData._thisMonth;
          var pageData = {
            _thisMonth: _thisMonth,
            prevMonth: data
          }
          _this.setData({
            pageData: pageData,
            load: false
          })
        })
      }else{
        _this.setData({
          load: false
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