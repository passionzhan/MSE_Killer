# MSE_Killer
剑桥通用五级英语考级报名抢报脚本。

1. ### 运行环境

   windows7 64位，python3.6版本，Firefox(70.0.1)、geckodriver([v0.26.0](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0))环境下测试通过。			

2. ### 依赖库:

   requirements.txt

3. ### 脚本使用说明
   1. 配置环境：安装firefox(不能直接拷贝绿色版)。下载geckodriver.exe([v0.26.0](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0))将其放置脚本根目录。
   2. 根据requirements.txt安装依赖包
   3. 在user_config.cfg中填入用户名、密码。
   4. 根据mse考试页面实际情况，填入对应的考试名称、考试城市、考试地点、考试科目等信息，需要与网页上文字完全一致。
   5. 运行main.py，开始报名。
   6. 根据提示，输入登录验证码。
   7. 抢报成功会提示：恭喜你，报名成功！请抓紧填写报名信息并在24小时内确认缴费，此时根据网页提示，填入个人信息，确认信息缴费后在输入yes退出抢报程序。



#### **祝君好运。**