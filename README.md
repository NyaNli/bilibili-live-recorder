# B站直播间录制

基于Python3（好像没怎么见过2的程序了），写着玩的东西，不是很靠谱  
打开后输入直播间链接里的数字敲下回车就不用管了
不在py文件里设好Cookie的话就只能录制渣画质，懒得写登录，Cookie最好从开发者工具的Network选项卡里找，document.cookie没有HttpOnly的Cookie  
原理就是从直播间页面脚本的__NEPTUNE_IS_MY_WAIFU__（啧）里获取直播间的状态和直播源信息，然后直接下载直播源就完事了  
下载的文件跟直接在直播间看到的东西是一样的，不过直接播放的话时间轴可能会不太对就是，懒得管