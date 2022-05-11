# 0 写在前面
- 请勿猜测、寻找作者，尊重他人隐私
- 请勿宣传，如果觉得有帮助可以自己使用
- 云效其实挺好的
- 为了资本家手里的钱，冲啊！
# 1 功能

按照设定的调度时间打开登录云效，把所有“处理中”的任务的进度+5。

# 2 使用

环境：windows10 python3.7

pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install schedule -i https://pypi.tuna.tsinghua.edu.cn/simple

修改sched.py中的用户名密码

python sched.py

调度时间可以在sched.py中修改，默认工作日9点半，具体见代码

# 3 写在后面

最初版本运行+调试了一周左右。有bug的话，可以在issue里提，也可以pullrequest，大部分的pullrequest都接受，合并到master并保存一个tag

不足之处是无法识别节假日

之所以选python不用java 因为之后如果添加了登录的验证码，可以方便各位大佬加识别功能，我并不会写
