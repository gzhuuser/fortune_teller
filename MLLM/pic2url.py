import oss2
from itertools import islice
import os

# 1 代码嵌入方式配置
def pic2url(path):
    # 填写RAM用户的访问密钥（AccessKey ID和AccessKey Secret）。
    accessKeyId = os.getenv("accessKeyId")
    accessKeySecret = os.getenv("accessKeySecret")
    # 使用代码嵌入的RAM用户的访问密钥配置访问凭证。
    auth = oss2.Auth(accessKeyId, accessKeySecret)

    # endpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    endpoint = "http://oss-cn-beijing.aliyuncs.com"

    # 填写Bucket名称。
    bucketName = "image-bed-datawhale"
    bucket = oss2.Bucket(auth, endpoint, bucketName)

    # 上传文件到OSS。
    # objectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
    objectName = "test/" + path.split("/")[-1]
    # localFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    localFile = path
    bucket.put_object_from_file(objectName, localFile)
    # 生成下载链接
    fileLink = "https://" + bucketName + ".oss-cn-beijing.aliyuncs.com/" + objectName
    print(fileLink)
    return fileLink


if __name__ == "__main__":
    pic2url("./myhand.png")
