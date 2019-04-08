// pages/components/chat/chat.js
const app=getApp();
const baseUrl=app.globalData.baseUrl;//ajax请求链接
const userInfo=app.globalData.userInfo;//用户信息
const SystemInfo=app.globalData.SystemInfo;//用户手机信息
const recorderManager=wx.getRecorderManager()//全局唯一录音
const innerAudioContext = wx.createInnerAudioContext();//全局唯一播放
/**
 * 
 * quary 用户说的话,
 * quary_type 话的状态 is not ask_sex ask_age answer answers
 * quaryInfo 用户说的话的信息  用户选择男女的信息
 * code 用户code
 * avatarUrl 头像
 * nickName 名称
 * gender 性别  0 未知 1男 2女
 * country 国家
 * province 省
 * city 城市
 * openid 用户openid
 * session_key 用户session_key
 */
function ajaxData(quary,quary_type,quaryInfo,voice,openid,toAsk){
    var dataCon={
      logic_type:'inquiry'
    }
    dataCon.quary=quary;//用户对话
    if(quary_type!=""){
      dataCon.quary_type=quary_type;
    }
    if (toAsk!=""){
      dataCon.to_wenzhen=toAsk;
    }
    if(quaryInfo!=""){
      dataCon.quary_info=quaryInfo;//用户对话
    }
    if(voice!=""){
      dataCon.voice=voice
    }
    if(openid!=""){
      dataCon.openid=openid;//用户openid
    }
  return dataCon
}
// 手机型号信息 提交
function PhoneInfo(talkid){
  var ajaxData={
    os:SystemInfo.system,
    model:SystemInfo.model,
    openid:wx.getStorageSync("openid"),
    logic_type:"inquiry",
    quary_type:"model",
    talkid:talkid
  }
  wx.request({
    url: baseUrl+'wechat/chat-api/applets',
    data: ajaxData,
    header: {
      "Content-Type": "application/json"
    },
    method: 'POST',
    dataType: 'json',
    success: function(res) {
      console.log(res)
    }
  })
}
// 聊天请求
/**
 * _this  this
 * sendVal 用户输入的消息
 * valType 消息类型   is  还是别的  用户输入的都是is 
 * valInfo 选择男女标签   传 1 or 2  1是男
 * voice  语音链接
 * bubbleType,本条消息是语音消息还是其他的消息
 * time 语音消息时长
 */
function sendMsg(_this,sendVal,valType,valInfo,voice,bubbleType,time,toAsk){
  var userInfo=_this.data.userInfo;//用户信息
  // var UserCode=wx.getStorageSync("UserCode");//用户code
  var openid=wx.getStorageSync("openid");//用户openid
  var chatList=_this.data.chat;//聊天记录
  var keyboard=_this.data.keyboard;
  var firstvalType=_this.data.firstMsg?"first":valType
  // var requestData=null;//ajax请求数据
  //判断用户是否登录   未登录第一次提交用户的信息  登录过后只提交用户的openid
  // if(openid!=null&&openid!=undefined&&openid!=""){
  // 登录
  var requestData=ajaxData(sendVal,firstvalType,valInfo,voice,openid,toAsk);
  wx.request({
    url: baseUrl+'wechat/chat-api/applets',
    data: requestData,
    header: {
      "Content-Type": "application/json"
    },
    method: "POST",
    dataType: "json",
    success: function (res) {
      //返回的数据
      var data=res.data;
      //消息的类型
      var msgtype=data.type;
      //用来判断后台是否需要用户的手机信息
      var requ=data.require
      //问答卡片的信息  默认是空
      var cardInfo="";
      // 聊天记录
      chatList=_this.data.chat;
      
      /**
       * val 消息内容
       * talkid 消息id  只有推送的病症才有
       * msgType 页面渲染的类型, 就是页面显示什么样子
       * class 只有msgType=text的时候才用到的，chat-left是机器说的话的样子 ，chat-right 用户说的话
       * play  播放语音  只有消息是语音消息才用到
       */
      // TODO 如果这块不明白  你只需要在办公室大叫李沧海就行了   就有人给你解答这块的逻辑
      // 判断后台是否需要用户的手机信息
      if (data.require!=null&&data.require!=undefined&&data.require!=""){
        PhoneInfo(data.talkid);
      }
      // 判断是否是问答完毕    如果问答完毕则下次回话多添加 first字段
      if(msgtype=="answers"||msgtype=="answer"){
        _this.setData({
          firstMsg:true
        })
      }else{
        _this.setData({
          firstMsg:false
        })
      }
      if(msgtype=="answers"){ //识别的相似病情
      //"您可以继续问我其他问题哦~"
      // 提示语 和  病症卡片
        chatList.push({val:"已经根据您的描述和选择，推断出可能患有的病症~",class:"chat-left card-msg-animation",msgType:"text",play:false,tap:true},{val:data.msg,talkid:data.talkid,msgType:"card",play:false,tap:true})
            if(data["info-type"]=="drugs"||data["info-type"]=="foods"||data["info-type"]=="bec"||data["info-type"]=="pro"||data["info-type"]=="pre"||data["info-type"]=="inspect"){
              msg_Type = data["info-type"]
              if(data["info-type"]=="pre"||data["info-type"]=="inspect"){
                msg_Type ="text"
              }
              console.log(msg_Type)
              chatList.push({title:data.bing,val:data.info, class: "chat-left msg-animation", msgType: msg_Type, play: false, tap: true })
            }
            // 点赞和结束语
          chatList.push({val:"小森有帮助到您嘛？",talkid:data.talkid,msgType:"feedback",play:false,like:false,not:false,tap:true},{val: "您可以继续问我其他问题哦~",class:"chat-left card-footer-msg-animation",msgType:"text",play:false,tap:true})
      }else if(msgtype=="answer"||msgtype=="wenda"||msgtype=="end"){//最后未识别病情 返回字段
        chatList.push({val:data.msg,class:"chat-left msg-animation",msgType:"text",play:false,tap:true})
      }else if(msgtype=="baike"){
        // 默认是问信息
        var showval=data.info;
        var msg_Type="text";
        // 问药
        if(data["info-type"]=="drugs"||data["info-type"]=="foods"||data["info-type"]=="pro"||data["info-type"]=="bec"){
          msg_Type=data["info-type"];
        }else if(data["info-type"]==""||data["info-type"]==null||data["info-type"]==undefined){
          // 百科卡片
          showval=data.msg;
          msg_Type=msgtype
        }
        chatList.push({ title: data.bing,val:showval,name:data.bing,class: "chat-left msg-animation", msgType: msg_Type, play: false,tap:true})
        // 是否进入问诊
        if(data.can_wenzhen=="can_wenzhen"){
          chatList.push({val:sendVal,msgType:"can_wenzhen",tap:true})
        }
        
      }else{
        // 标签选择信息
        var showTitle=data.qus;
        var cardMsgType="text"
        if (msgtype=="ask_age"){ //年龄选择器
          cardInfo={}
          cardInfo.msgtype=msgtype;
          cardInfo.age=_this.data.age;
        }else if (msgtype=="ask_sex"){//性别 标签选择器
          cardInfo={}
          cardInfo.title=data.qus;
          cardInfo.msg=[{val:"男",sex:"1"},{val:"女",sex:"2"}]
          cardInfo.msgtype=msgtype;
          cardInfo.ans_type="";
        }else if(msgtype=="many"||msgtype=="wendas"){//询问病情   标签选择器
          cardInfo={}
          var msgJson=[];
          // 便利选择标签  给每个选择标签加个选中状态
          for (var i in data.msg) {
            var msgVal={checked:false,val:data.msg[i]}
            msgJson.push(msgVal)
          }
          if(data.choice!=undefined&&data.choice!=null&&data.choice!=""){
            showTitle={
              title:data.qus,
              msgTag:data.choice
            }
            cardMsgType="cardMsgTag"
          }
          cardInfo.title=data.qus;
          cardInfo.msgArr=data.msg;  //标签数组
          cardInfo.msgJson=msgJson;  //标签数组
          cardInfo.msgtype=msgtype; //数据类型
          cardInfo.ans_type=data.choice;
          cardInfo.ans_type=data.ans_type;
        }
        chatList.push({val:showTitle,class:"chat-left msg-animation",msgType:cardMsgType,play:false,tap:true})
      }
      // 渲染数据
      _this.setData({
        cardInfo:cardInfo,
        chat:chatList,
        age_picker:true,
        ageChecked: [24],
        showClear:msgtype=="many"||msgtype=="input"?true:false,
        inputT:msgtype=="input"?"input":"is"
      })
      // function(){
        _this.setData({
          tap:true,
          ClearTap:true,
          inputLoad:true
        })
      // }
      // 调整滚动条高度
      $scroll(_this)
    }
  })
  // 根据用户点击的按钮的状态值  渲染到页面上     除了点击以上都不是,其他的都是正常渲染,
  // 点击以上都不是要把所有按钮的值都提交到服务器,渲染到页面让则根据消息状态来渲染  "以上都不是"
  var showVal=null,msgType="text",msgClass="chat-right chat-right-bg msg-animation"

  if (bubbleType=="record"){
    msgType="record";
    msgClass="chat-right msg-animation";
    showVal={text:sendVal,url:voice,time:parseInt(time/1000)}
  }else{
    showVal=valType=="not"||valType=="tmp_not"?"以上都没有":sendVal;
  }
  // 用户主动关闭问答就不创建对话记录
  if(valType!="end"){
  // 创建聊天数据
  chatList.push({val:showVal,class:msgClass,msgType:msgType,play:false,tap:true})
  }
  // 渲染到页面上
  _this.setData({
    sendVal: "",
    chat:chatList,
    
  },function(){
    _this.setData({
      inputLoad: false,
    })
  })
  $scroll(_this)
}
// 页面滚动
function $scroll(_this){
    const query = wx.createSelectorQuery();
    var winH=SystemInfo.windowHeight;//窗口的高度
    // query.select("#robot_headImg").boundingClientRect()//头部机器人头像高度
    query.select("#sendBox").boundingClientRect()//输入框内容
    query.select("#scroll").boundingClientRect()//滚动条内容高度
    query.exec(function (res) {
      // 窗口高度-(头像高度+输入框高度)=用户对话内容的高度
      _this.setData({
        scrollH:winH-(res[0].height)
      })
      // 设置滚动条位置滚动到底部
      _this.setData({
        rollH:res[1].height
      })
    })
}
// 点赞
function setfeedback(talkid,evaluate,callback){
  wx.request({
    url: baseUrl+'wechat/chat-api/applets',
    data:{
      logic_type:'inquiry',
      quary_type:"evaluate",
      openid:wx.getStorageSync("openid"),
      talkid:talkid,
      evaluate:evaluate
    },
    header: {
      "Content-Type": "application/json"
    },
    method: 'POST',
    dataType: 'json',
    responseType: 'text',
    success: function(res) {
      var data=res.data;
      callback(data)
    }
  })
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    inputLoad:true,
    rollH:0,
    scrollH:'',
    sendVal:'',//用户输入的内容
    userInfo:"",//用户信息
    SystemInfo:"",//手机参数信息
    chat:[],// 聊天记录
    cardInfo:"",//选择信息
    showClear:false,//断开本次通话按钮
    ClearTap:true,//关闭按钮  是否可以点击
    VType:null,//消息状态
    checkTag:[],//多选选中的标签
    Itype: false,//输入方式  false 语音  true 键盘
    recordText:1, //录音  按钮显示的文字   1按住录音  2松开发送
    record:0,//是否录音  录音停止 0   录音  1  录音移动 2
    tap:false,//标签点击 false 可以点击  true 禁用点击
    cancel_record:false,//是否取消录音  false 不取消  true 取消
    PhoneX:"",//适配iphone x
    age:[],//年龄数据
    age_picker:true,//年龄选择器确定按钮
    ageChecked:[24],//年龄选择默认选中下标
    cardBtn:[
      {icon:'../../assets/img/z-jb-icon.svg',val:"疾病详情"},
      {icon:'../../assets/img/z-bz-icon.svg',val:"症状"},
      {icon:'../../assets/img/z-zl-icon.svg',val:"治疗"},
    ],
    cure_card:{
      foods:{
        class:"cure-green",
        info:"食疗方法"
      },
      bec:{
        class:"cure-blue",
        info:"病症原因"
      },
      pro:{
        class: "cure-violet",
        info: "治疗方法"
      }
    },
    talkid:"",
    feedbackSelectTag: [],//标签数据
    feedbackWinShow:false,//反馈窗口显示隐藏
    feedbackVal:"",//其他反馈原因
    feedbackCheckedTag:[],//不满意反馈 选中标签
    firstMsg:false,
    record_btn:true,//限制语音 不能多条连续发送
    inputT:"is"//用户输入类型 默认is 
  },
  // 输入事件
  sendInput:function(e){
    var _this=this;
    // 获取用户输入信息 保存到sendVal里面
    _this.setData({
      sendVal:e.detail.value
    })
  },
  //录音
  record_start:function(e){
    var _this=this;
    var recordS=_this.data.record_btn
    //设置录音文件信息
    const options = {
      duration: 60000,
      sampleRate: 16000,
      numberOfChannels: 1,
      encodeBitRate: 96000,
      format: 'mp3',
      frameSize: 50
    }
    if(recordS){
      recorderManager.start(options);
      // 开始录音
      recorderManager.onStart(()=>{
        // 设置状态 正在录音
        _this.setData({
          record:1,
          recordText:2,
          record_btn:true
        })
      })
        // 监听录音停止
      recorderManager.onStop((res) => {
        // 判断用户是否取消录音
        var cancel_record=_this.data.cancel_record;

        const {tempFilePath,duration}=res;
        // console.log(cancel_record)
        // 用户不取消录音，就上传语音文件，进行语音识别
        if(!cancel_record){
          _this.setData({
            record_btn: false,
          })
          wx.saveFile({
            tempFilePath: tempFilePath,
            success:function(res){
              const {savedFilePath}=res;
                wx.uploadFile({
                url: baseUrl+'wechat/chat-api/applets',
                filePath: savedFilePath,
                name: "record",
                formData: {
                  logic_type:"asr",
                  openid:wx.getStorageSync("openid")
                },
                success: function(res) {
                  const {text,voice}=JSON.parse(res.data);
                  // 根据识别的文字来问机器人，
                  sendMsg(_this,text,"is","",voice,"record",duration);
                  // 识别成功之后删除本地语音文件
                  wx.getSavedFileList({
                    success:function(res){
                      var fileList=res.fileList;
                      if (fileList.length > 0) {
                      for(var i=0; i<fileList.length;i++){
                        wx.removeSavedFile({
                          filePath:fileList[i].filePath
                        })
                      }
                    }
                    }
                  })
                },
                complete:function(){
                  _this.setData({
                    record_btn: true
                  })
                }
              })
            }
          })
        }
        // 设置状态  录音停止  是否取消录音 否
        _this.setData({
          record:0,
          recordText:1,
          cancel_record:false,
        })
      })
    }else{
      wx.showToast({
        title: "语音正在识别...",
        icon: 'none',
        duration: 1000
      })
    }
  },
  // 录音移动
  record_move:function(e){
    var _this=this;
    var record=_this.data.record;
    if(record==1||record==2){
      const query=wx.createSelectorQuery();
      var tapX=e.changedTouches["0"].clientY;//手指在页面中的坐标
      // 获取页面元素
      query.select(".send_Input").boundingClientRect(function(res){
        // 获取输入框距离顶部的高度
        const {top}=res
        record=_this.data.record;
        // 判断用户手指是否移出录音按钮   
        if(tapX<top){
          if (record!=2&&record!=0){
            // 设置状态 录音移动
            _this.setData({
              record:2
            })
            
          }
        }else{
          if (record!=1&&record!=0) {
            // 设置状态 录音中
            _this.setData({
              record:1 
            })
          }
        }
      }).exec()
    }
  },
  // 停止录音
  record_stop:function(){
    var _this=this;
    var record=_this.data.record;
    // 停止录音
    recorderManager.stop();
    // 判断用户手指是否移出录音按钮， 然后设置是否取消录音
    if(record==2){
      _this.setData({
        cancel_record: true
      })
    }
  },
  // 播放录音
  play_voice:function(e){
    var _this=this;
    // 获取播放音频链接
    var url=e.currentTarget.dataset.voiceurl;
    // 获取当前下标
    var index=e.currentTarget.dataset.index;
    // 获取当前播放状态
    var play=e.currentTarget.dataset.play;
    // 获取所有对话
    var chatData=_this.data.chat;
    // 便利所有对话
    for(var i in chatData){
      // 设置所有播放状态都为false
      chatData[i].play=false;
    }
    // 判断点击当前是播放状态还是费播放状态
    if(!play){
      // 设置播放音频链接
      innerAudioContext.src=baseUrl+url;
      // 开始播放
      innerAudioContext.play();
    }else{
      // 停止播放
      innerAudioContext.stop();
      chatData[index].play=false;
    }
    // 监听播放状态
    innerAudioContext.onPlay(() => {
      innerAudioContext.offPlay();
      // 设置播放音频动画
      chatData[index].play=true;
      // 渲染到页面
      _this.setData({
        chat:chatData
      })
    })
    // 监听停止
    innerAudioContext.onEnded(() =>{
      innerAudioContext.offEnded();
      // 停止执行音频动画
      chatData[index].play=false;
      // 渲染页面
      _this.setData({
        chat:chatData
      })
    })
    // 渲染页面
    _this.setData({
      chat:chatData
    })
  },
  // 切换输入方式
  input_type:function(){
    var _this=this;
    var Itype=_this.data.Itype;
    var haveAuth = false;
    if (Itype) {
      //转为文字 
      _this.setData({
        Itype: false
      })
    } else {
      //转为语音 先检查权限 
      wx.getSetting({
        success(res) {
          console.log(res)
          if (!res.authSetting['scope.record']) {
            wx.showToast({
              title: "如要使用语音聊天请先允许语音授权！",
              icon: 'none',
              duration: 1500
            })
            wx.openSetting({
              success(res) {
                if (!res.authSetting['scope.record']) {
                  //未取得语音权限 
                  wx.showToast({
                    title: "如要使用语音聊天请允许语音授权！",
                    icon: 'none',
                    duration: 1500
                  })
                } else {
                  // console.log("有权限了") 
                  // haveAuth = true; 
                  _this.setData({
                    Itype: true
                  })
                }
              }
            })
          } else {
            // console.log("有权限了") 
            // haveAuth = true; 
            _this.setData({
              Itype: true
            })
          }
        }
      })
    }
  },
  // 用户发送内容事件
  send_btn:function(){
    var _this=this;
    var send_val=_this.data.sendVal;//用户输入的内容
    var inputT=_this.data.inputT;
    var chat=_this.data.chat;
    if(send_val!=""&&send_val!=null&&send_val!=undefined){
      // 用户发送消息之后 让之前的按钮全部失效不能点击   除了点赞的按钮
      for(var i=0; i<chat.length; i++){
        if(chat[i].msgType!="feedback"){
          chat[i].tap = false
        }
      }
      // 渲染到页面
      _this.setData({
        chat:chat
      })
      // 请求机器人
      sendMsg(_this,send_val,inputT,"","","text");
    }else{
      wx.showToast({
        title: "内容不能为空",
        icon: 'none',
        duration: 1000
      })
    }
  },
  // 查看全部药品
  todrug:function(e){
    var name=e.currentTarget.dataset.name;
    wx.navigateTo({
      url: '../alldrug/alldrug?name='+name,
    })
  },
  // 查看单个药品列表
  todrugList:function(e){
    var name=e.currentTarget.dataset.name;
    wx.navigateTo({
      url: '../drug/drug?name='+name,
    })
  },
  // 点赞 和 不满意
  feedback_btn:function(e){
    var _this=this;
    var index=e.currentTarget.dataset.index;//获取本条消息的下标
    var talkid=e.currentTarget.dataset.talkid;//获取消息id
    var tap=e.currentTarget.dataset.tap;//获取用户是否点击过按钮
    var evaluate=e.currentTarget.dataset.evaluate;//获取按钮类型 是点赞  还是 不满意
    var chat=_this.data.chat;//获取聊天记录
    // 限制用户只能点击一次
    if(tap){
      // 第一次点击之后限制用户多次点击
      chat[index].tap=false;
      // 判断用户点击的是“点赞”还是“不满意” 1 点赞  3不满意
      if (evaluate==1){
        // 改变按钮样式
        chat[index].like=true;  
      }else if(evaluate==3){
        // 改变按钮样式
        chat[index].not=true;
      }
      // 渲染到页面上
      _this.setData({
        chat:chat,
      })
      // 把用户点击行为提交到后台
      setfeedback(talkid,evaluate,function(data){
        var feedbackWinShow;
        // 判断当前点击的是点赞还是不满意
        if (evaluate==1){
          // 提供点击反馈
          wx.showToast({
            title: "已收到您的反馈！",
            icon: 'none',
            duration: 1500
          })
          feedbackWinShow=false;
        }else if(evaluate==3){
          // 如果是不满意
          var feedbackSelectTag=data.case.case;
          // 整理数据  不满意推荐标签
          for(var i in feedbackSelectTag){
            feedbackSelectTag[i].checked=false
          }
          // 显示窗口
          feedbackWinShow=true;
          // 标签内容渲染到页面上
          _this.setData({
            feedbackSelectTag:feedbackSelectTag,
          })
        }
        // 渲染到页面上
        _this.setData({
          feedbackWinShow: feedbackWinShow,
          talkid:talkid
        })
      })
    }else{
      // 用户点击过之后就不能再点击了 
      wx.showToast({
        title: "您已经选择过了",
        icon: 'none',
        duration: 500
      })
    }
  },
  // 年龄选择   选择器滚动开始  禁用确定按钮    以防用户点击确定过快，选择不到内容
  age_picker_s:function(e){
    var _this=this;

    _this.setData({
      age_picker:false
    })
  },
  // 获取选择器改变后的值  保存
  age_picker_c:function(e){
    var _this=this;
    var age=_this.data.age;
    var index=e.detail.value[0];
    _this.setData({
      ageChecked:[index]
    })
    _this.setData({
      age_picker: true
    })

  },
  // 提交后台
  age_submit:function(){
    var _this=this;
    var age=_this.data.age;
    var ageChecked=_this.data.ageChecked;
    var age_picker=_this.data.age_picker;
    var val=age[ageChecked];
    if(age_picker){
      sendMsg(_this,val,"ask_age",val);
      _this.setData({
        age_picker:false,
      })
    }
    
    
  },
  // 标签选择
  tagSend_arr:function(e){
    var _this=this;
    var index=e.target.dataset.index;//用户输入的内容
    var send_val=e.target.dataset.val;//用户输入的内容
    var cardInfo=_this.data.cardInfo;
    var checkTag=_this.data.checkTag;
    
    // 判断多选标签是否选中，
    if (cardInfo.msgJson[index].checked){
      // 选中的把选中的记录删掉
      for(var i in checkTag){
        if(checkTag[i]==send_val){
          checkTag.splice(i,1)
        }
      }
      // 选中样式取消
      cardInfo.msgJson[index].checked=false;
    }else{
      checkTag.push(send_val)
      cardInfo.msgJson[index].checked=true;
    }
    
    _this.setData({
      cardInfo: cardInfo,
      checkTag:checkTag
    })
  },
  // 用户选择病症事件 和多选确定按钮
  tap_send:function(e){
    var _this=this;
    var send_val=e.target.dataset.val;//用户输入的内容
    var valInfo=e.target.dataset.sex;//性别
    var valType=e.target.dataset.vtype;//病症标签的类型
    var checkTag=_this.data.checkTag;//提交卡片
      // 点击状态，防止用户多次触发这个事件
      var tap=_this.data.tap
      if(tap){
        // 判断是否是多选 标签
        if(valType=="tmp_are"&&checkTag==""&&checkTag.length==0){
          wx.showToast({
            title: '请选择选项',
            icon: 'none',
            duration: 500
          })
        }else{
          var chat=_this.data.chat;
          for(var i=0; i<chat.length; i++){
            chat[i].tap=false
          }
          _this.setData({
            chat:chat,
            tap:false
          })
          // 根据用户点击标签，提交后台
          sendMsg(_this, send_val,valType,valInfo,"","text");
        }
      }else{
        wx.showToast({
        title: '已经选择过了',
        icon: 'none',
        duration: 500
      })
    }
    // 请求完毕之后清空页面标签选择数据
    _this.setData({
      checkTag: []
    })
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
  // 紫色卡片点击事件
  illPage: function (e) {
    var id = e.currentTarget.dataset.index;
    var name = e.currentTarget.dataset.name;
    // console.log(e)
    wx.navigateTo({
      url: '../illness/illness?id=' + id + "&name=" + name,
    })
  },
  // 不满意反馈框  输入事件
  feedback_val:function(e){
    var _this=this;
    var val=e.detail.value;
    _this.setData({
      feedbackVal:val
    })
  },
  // 关闭不满意反馈框
  clear_feedback:function(e){
    var _this=this;
    _this.setData({
      feedbackWinShow:false
    })
  },
  // 不满意反馈 原因标签点击事件
  feedback_tag:function(e){
    var _this=this;
    var selectTag=_this.data.feedbackSelectTag
    var checkedTag=_this.data.feedbackCheckedTag;
    var checked=e.currentTarget.dataset.tagchecked;
    var index=e.currentTarget.dataset.index;
    var id=e.currentTarget.dataset.id;
    if(checked){
      for(var i in checkedTag){
        if(checkedTag[i]==id){
          checkedTag.splice(i,1)
        }
      }
    }else{
      checkedTag.push(id);
    }
    selectTag[index].checked=selectTag[index].checked?false:true;
    _this.setData({
      feedbackSelectTag: selectTag,
      feedbackCheckedTag: checkedTag
    })
  },
  // 提交不满意原因
  submitFeedback:function(){
    var _this=this;
    var checkedTag=_this.data.feedbackCheckedTag;
    var val=_this.data.feedbackVal;
    var talkid=_this.data.talkid;
    if(checkedTag.length>=1||val!=""){
      wx.request({
      url: baseUrl+'wechat/chat-api/applets',
      data:{
        logic_type:'inquiry',
        quary_type:"feedback",
        openid:wx.getStorageSync("openid"),
        caseid:checkedTag,
        other:val,
        talkid:talkid
      },
        header: {
          "Content-Type": "application/json"
        },
        method: 'POST',
        dataType: 'json',
        success: function(res) {
          _this.setData({
            talkid:"",
            feedbackWinShow:false
          })
          wx.showToast({
            title: "已收到您的反馈！",
            icon: 'none',
            duration: 1500
          })
        }
      })
    }else{
      wx.showToast({
        title: '请选择或者输入不满意原因才能提交',
        icon: 'none',
        duration: 1000
      })
    }

  },

  // 百科卡片 是否进入问诊 按钮
  ask_btn:function(e){
    var _this=this;
    var tap=e.currentTarget.dataset.tap;
    var val=e.currentTarget.dataset.val;
    var index=e.currentTarget.dataset.index;
    var chat=_this.data.chat;
    // 判断按钮是否能点击
    if(tap){
      chat[index].tap=false;
      sendMsg(_this,val,"is","","","","","to_wenzhen");
      _this.setData({
        chat:chat
      })
    }else{
      wx.showToast({
        title: "此按钮已经失效",
        icon: 'none',
        duration: 1000
      })
    }
  },
  // 问诊关闭
  ClearChat:function(e){
    var _this=this;
    var ClearTap=_this.data.ClearTap;
    if(ClearTap){
      _this.setData({
        ClearTap:false
      })
      sendMsg(_this, "end", "end", "", "", "text");
    }
  },
  // 多意图点击
  msgTag:function(e){
    var _this=this;
    var index=e.currentTarget.dataset.index;
    var val=e.currentTarget.dataset.val;
    var tap=e.currentTarget.dataset.tap;
    var chat=_this.data.chat;
    if(tap){
      chat[index].tap=false;
      _this.setData({
        chat:chat,
        tap:false
      })
      sendMsg(_this, val,"is","","","text");
    }
  },
  // 长文本卡片
  cuerInfo:function(e){
    var _this=this;
    var title=e.currentTarget.dataset.title;
    var name=e.currentTarget.dataset.name;
    var val=e.currentTarget.dataset.val;
    wx.navigateTo({
      url: '../cureInfo/cureInfo?title='+title+'&name='+name+'&val='+val[0],
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this=this;
    var age=[];
    // 设置导航条
    wx.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: '#092b79'
    })
    for(var i=1; i<=100; i++){
      age.push(i)
    }
    // 保存个人信息
    _this.setData({
      userInfo: app.globalData.userInfo,
      SystemInfo: app.globalData.SystemInfo,
      PhoneX:app.globalData.PhoneX,
      age:age,
      inputLoad:false,
    })
    // 请求开头白
    wx.request({
      url: baseUrl+'wechat/chat-api/applets',
      data: {
        openid:wx.getStorageSync("openid"),
        logic_type: "inquiry",
        quary_type: "start",
      },
      header: {
        "Content-Type": "application/json"
      },
      method: 'POST',
      dataType: 'json',
      success: function(res) {
        var data=res.data;
        var chat=[];
        chat.push({val:data.msg,class:"chat-left msg-animation",msgType:"text",play: false,tap:true})
        _this.setData({
          chat:chat,
          firstMsg:true
        },function(){
          _this.setData({
            inputLoad:true
          })
        })
        $scroll(_this)
      },
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