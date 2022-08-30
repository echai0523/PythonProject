# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-05-05 06:39
Short Description:
-env
pip install aliyun-python-sdk-sts


Change History:

'''
import json
import os
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import oss2
import base64
from wooey_utils.com.config import OSS_AK,OSS_SK,OSS_REGION
from urllib.parse import quote


def gen_uuid():
    import uuid
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid


# python oss https://help.aliyun.com/document_detail/32033.html?spm=a2c4g.11174283.6.1214.4ff97da2RYEXjM

# 以下代码展示了STS的用法，包括角色扮演获取临时用户的密钥、使用临时用户的密钥访问OSS。

# STS入门教程请参看  https://yq.aliyun.com/articles/57895
# STS的官方文档请参看  https://help.aliyun.com/document_detail/28627.html

# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
# 注意：AccessKeyId、AccessKeySecret为子用户的密钥。
# RoleArn可以在控制台的“访问控制  > 角色管理  > 管理  > 基本信息  > Arn”上查看。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。
class StsToken(object):
    """AssumeRole返回的临时用户密钥
    :param str access_key_id: 临时用户的access key id
    :param str access_key_secret: 临时用户的access key secret
    :param int expiration: 过期时间，UNIX时间，自1970年1月1日UTC零点的秒数
    :param str security_token: 临时用户Token
    :param str request_id: 请求ID
    """
    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.expiration_str = ''
        self.security_token = ''
        self.request_id = ''

class OSS_STS_AUTH_Authorize():
    def __init__(self,oss_path_str,auth_type='readonly',region='cn-shanghai',ak="LTAI4GGpV2FB3UcvEJBjhAu7",sk="zbRKd60LpBQTWOu5fD59tpy1B7sziE"):
        self.oss_path_str =oss_path_str
        self.bucket_name,self.folder_name = self.parse_from_oss_path(oss_path_str)
        self.auth_list = self.parse_auth_type_list(auth_type)
        self.ak =ak
        self.sk=sk
        self.endpoint = f"http://oss-{region}.aliyuncs.com"
        self.sts_role = "acs:ram::5201445100659186:role/pe-test"
        self.region =region

    def parse_from_oss_path(self,oss_path_str):
        #oss://appendc/ASR_1/JAP_ASR001_CN/
        assert oss_path_str.startswith("oss://")==True,"路径不是以oss://开头,请检查"
        assert oss_path_str.endswith("/")==True,"路径必须以/结尾"
        oss_path_str=oss_path_str.replace("oss://","")
        route_list=oss_path_str.split("/")

        bucket_name = route_list[0]
        folder_name = '/'.join(route_list[1:])
        assert folder_name!='','必须指定文件夹路径，不能授权整个bucket!'
        return bucket_name,folder_name

    def parse_auth_type_list(self,auth_type):
        '''
        支持两种形式，只读和读写
        其中只读就是只有下载权限，读写就是可以上传下载，但是不能删除文件
        '''
        assert auth_type in ("readonly","canupload")
        if auth_type =='readonly':
            return [
                "oss:Get*",
                "oss:List*"
            ]
        elif auth_type =="canupload":
            return [
                "oss:Get*",
                "oss:List*",
                "oss:Put*",
                "oss:AbortMultipartUpload"
            ]

    def fetch_sts_token(self):
        clt = client.AcsClient(self.ak, self.sk, self.region)
        req = AssumeRoleRequest.AssumeRoleRequest()
        req.set_DurationSeconds(43200)  ### 设置过期时间 最大是43200  也就是最长12个小时

        req.set_accept_format('json')
        req.set_RoleArn(self.sts_role)
        req.set_RoleSessionName('oss-python-sdk-example')

        policy_dict = {
              "Version": "1",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": [
                    "oss:ListObjects"
                  ],
                  "Resource": [
                    f"acs:oss:*:*:{self.bucket_name}"
                  ],
                  "Condition": {
                    "StringLike": {
                      "oss:Prefix": f"{self.folder_name}*"
                    }
                  }
                },
                {
                  "Effect": "Allow",
                  "Action":self.auth_list,
                  "Resource": [
                    f"acs:oss:*:*:{self.bucket_name}/{self.folder_name}*"
                  ]
                }
              ]
        }
        req.set_Policy(json.dumps(policy_dict,ensure_ascii=False))
        body = clt.do_action_with_exception(req)
        j = json.loads(oss2.to_unicode(body))
        token = StsToken()
        token.access_key_id = j['Credentials']['AccessKeyId']
        token.access_key_secret = j['Credentials']['AccessKeySecret']
        token.security_token = j['Credentials']['SecurityToken']
        token.request_id = j['RequestId']
        token.expiration_str = j['Credentials']['Expiration'] #2021-04-16T03:10:27Z
        token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ') #1620213952 时间戳数字

        return token

    def get_auth_str(self):
        print("授权路径:")
        print(self.oss_path_str)
        token = self.fetch_sts_token()
        opt = {
            "id": token.access_key_id,
            "secret": token.access_key_secret,
            "stoken": token.security_token,
            "privilege": '1',
            "expiration": token.expiration_str,
            "osspath": self.oss_path_str,
            "region": f'oss-{self.region}'
        }
        base_auth_str = base64.b64encode(json.dumps(opt).encode('utf-8')).decode('utf-8')
        print(f"请复制下方的授权码，使用oss登陆,授权码将在12小时后过期，请尽快使用!")
        print(base_auth_str)
        return base_auth_str



#
# if __name__=="__main__":
#     # oss_authorize = OSS_STS_AUTH_Authorize("oss://appendc/ASR_1/keda_36_langs_sample/")#只读
#     oss_authorize = OSS_STS_AUTH_Authorize("oss://projecteng/Sample_test/qunying_data/",auth_type='canupload') #可上传
#     oss_authorize.get_auth_str()
#
class OSS_API():
    def __init__(self,bucket_name='projecteng'):
        self.bucket_name = bucket_name
        self.auth = oss2.Auth(OSS_AK, OSS_SK)
        self.bucket = oss2.Bucket(self.auth, OSS_REGION, bucket_name)

    def list_bucket_files_deep(self, oss_path, suffix='',with_bucket_name=False):
        ### 忽略临时文件和隐藏文件,忽略文件夹
        if oss_path.endswith("/") ==False:
            oss_path = oss_path+"/"

        path_list = []
        ignore_list = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=oss_path):
            if obj.key.endswith("/")==False and obj.key!=oss_path and obj.key.endswith(suffix):
                basename =obj.key.split("/")[-1]
                if basename.startswith((".","~")):
                    ignore_list.append((obj.key))
                else:
                    path_list.append(obj.key)

        if len(ignore_list)!=0:
            print(f"!请注意:{oss_path}下已自动忽略文件: {ignore_list}")

        if with_bucket_name ==True:
            return [ f"/{self.bucket_name}/"+x  for x in path_list]
        elif with_bucket_name ==False:
            return path_list
        else:
            raise Exception("oss api with_bucket_name定义错误")




    def list_bucket_current(self, oss_path,list_type,suffix='',full_path=True):  ### suffix只有list_type是文件的时候才生效
        ### list_type 是 folder或者file
        if oss_path.endswith("/") == False:
            oss_path = oss_path + "/"
        if list_type =='folder':
            fd_list =  [obj.key for obj in oss2.ObjectIterator(self.bucket,prefix=oss_path, delimiter= '/') if obj.key.endswith("/")==True and obj.key!=oss_path]
            if full_path ==True:
                return fd_list
            elif full_path==False:
                ##截取调最后的/再
                return [os.path.basename(x[:-1]) for x in fd_list]
            else:
                raise Exception("oss api参数定义错误")
        elif list_type =='file':
            path_list = []
            ignore_list = []
            for obj in  oss2.ObjectIterator(self.bucket, prefix=oss_path, delimiter='/'):## 只遍历当前文件夹
                if obj.key.endswith("/")==False and obj.key != oss_path and obj.key.endswith(suffix):
                    basename = obj.key.split("/")[-1]
                    if basename.startswith((".", "~")):
                        ignore_list.append((obj.key))
                    else:
                        path_list.append(obj.key)

            if len(ignore_list) != 0:
                print(f"!请注意:{oss_path}下已自动忽略文件: {ignore_list}")
            return path_list


    # meta_header {'Content-Type': 'image/jpg', "Content-Disposition": "inline", "Cache-Control": "no-cache"}
    # meta_header设置为空 {}
    def set_obj_meta(self,filename_list,meta_header):
        print(f"即将更新meta信息 {meta_header} ,文件数量{len(filename_list)},过程可能较长")
        for fl in filename_list:
            self.bucket.update_object_meta(fl,headers=meta_header)
        print('meta信息更新完成.')

    def save_to_oss_url(self, bytes_data, oss_path=None, suffix_type=None, force=False):
        '''返回url'''
        if oss_path is None:
            if suffix_type is None:
                raise Exception("路径不指定的情况，必须指定后缀类型")
            elif suffix_type.startswith(".") == False:
                raise Exception("后缀必须以.结尾")
            else:
                oss_path = f"upload_url/{gen_uuid()}/{gen_uuid()}{suffix_type}"

        ### 检查文件是否已存在
        if force == False:
            if self.bucket.object_exists(oss_path) is True:
                raise Exception("文件已存在请确认")

        ### 写入文件
        rs = self.bucket.put_object(oss_path, bytes_data)
        if rs.status != 200:
            raise Exception("OSS数据写入失败")

        prefix_url = f"https://{self.bucket_name}.oss-cn-shanghai.aliyuncs.com/"
        url = prefix_url + quote(oss_path)
        og_url = prefix_url + oss_path

        return url, og_url



class OssPath():
    def __init__(self,oss_path):
        oss_path = oss_path.strip()
        assert oss_path.startswith("oss://"), "路径必须以oss://开始"
        assert oss_path.endswith("/"), "路径必须以/结束"
        self.bucket_name = oss_path.replace("oss://", "").split("/")[0]
        self.oss_rel_path = "/".join(oss_path.replace("oss://", "").split("/")[1:])



if __name__ =="__main__":
    # oss_obj = OSS_API()
    # bin_full_files = oss_obj.list_bucket_current("haomo_3d/segmentation/YC20220114/61dffda4536633dcf229634f/point_cloud/bin_v1/",list_type="file",suffix=".bin")
    # print(bin_full_files)
    oss_path = OssPath("oss://appen-delivery/test/copytest/")
    print(oss_path.bucket_name,oss_path.oss_rel_path)


