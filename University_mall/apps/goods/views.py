from django.shortcuts import render

# Create your views here.


# 上传图片代码测试
from fdfs_client.client import Fdfs_client
# 1.创建客户端
# 2.修改加载配置文件的路径
client=Fdfs_client('utils/fastdfs/client.conf')
# 3.上传图片
# 图片的绝对路径
# client.upload_by_filename('/home/malifei-py/图片/56c30bfc900250e264f5892b31ae89b5_482x264.jpg')
# 3.获取file_id.upload_by_filename上传成功会返回字典数据

