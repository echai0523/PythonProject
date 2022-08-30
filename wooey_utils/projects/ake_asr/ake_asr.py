from pydub import AudioSegment
from wooey_utils.com.base_tools import appen_url_to_temp_url
import platform
import requests
import os,sys
from math import ceil
import struct
import re

LANG_AUIDO_TYPE={
    "TYKY",
    "LYGW",
    "SZSJ",
    "SHJJ",
    "JYXX",
    "YLXG",
    "ZZWJ",
    "TYYL",
    "KJSM",
    "RMDM"
}


ALPHABET = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

def digit2alphabet(digit):
    """10进制 -> 26进制"""
    mod, remainder = divmod(digit, 26)
    alphabet = ALPHABET[remainder]
    while mod:
        mod, remainder = divmod(mod, 26)
        alphabet = ALPHABET[remainder] + alphabet
    return alphabet

def gen_six_alphstr_by_seq_num_p2(num:int):
    assert  num >=0 and num <= 26**6-1,"数字超出计算范围"

    alpstr = digit2alphabet(num)
    ### 不足六位时前面的用a代替
    pre_a = 'A'* ( 6-len(alpstr) )
    six_alpstr = pre_a+alpstr
    assert len(six_alpstr) ==6,"计算长度长度不是6"
    return six_alpstr

def decode_by_six_alphstr_p2(alphstr:str):
    alphstr = alphstr.strip()
    if re.match("^[A-Z]{6}$", alphstr) is None:
        return None
    else:
        alphstr= alphstr.lstrip("A")
        num = 0
        width = len(alphstr)
        for idx,code in enumerate(alphstr):
            num += 26**(width-idx-1) * ALPHABET.index(code)

        return num

import hashlib
def md5_file_by_bytes(bytes_str):
  '''
  GEN MD5
  WINDOWS CMD LINE :certutil -hashfile Filename MD5
  MAC/LINUX :md5sum Filename
  '''
  # import hashlib
  md5_l = hashlib.md5()
  # with open(filename,mode="rb") as f:
  #   data = f.read()
  md5_l.update(bytes_str)
  ret = md5_l.hexdigest()
  return ret

# def get_start_end(audio):
#     # audio = AudioSegment.from_wav(fl)
#     lst = [ abs(x[0]) for x in struct.iter_unpack("<h",audio.raw_data)]
#     un_lst = lst[::-1]
#
#     acc_start = 0
#     acc_end = 0
#
#     ### 客户要求每10ms 计算平均值
#     ### 采样率是16000，那么每10ms应该是百分之一，那么就是160个点算一次平均数
#
#     total = len(lst)
#     step = 160
#     for i in range(0,total,step):
#         cut = lst[i:i+step]
#         cut_avg = sum(cut)/len(cut)
#
#         if cut_avg !=0 and abs(cut_avg) >103:
#             break
#         else:
#             acc_start += 0.01  # 积累10ms
#
#     for i in range(0,total,step):
#         cut = un_lst[i:i+step]
#         cut_avg = sum(cut)/len(cut)
#
#         if cut_avg !=0 and abs(cut_avg) >103:
#             break
#         else:
#             acc_end += 0.01  # 积累10ms
#
#     audio_duration = audio.duration_seconds
#     valid_duration = max(round(audio_duration  - acc_start - acc_end, 2),0)
#
#     return round(acc_start,2), round(acc_end,2), audio_duration, valid_duration


def get_start_end(audio):
    # audio = AudioSegment.from_wav(fl)
    frame_count = int(audio.frame_count())
    # 16bit的 30ms
    step = 480 # 16bit的 30ms
    acc_start = 0
    acc_end = 0


    ##### 前静音计算逻辑
    for i in range(0,frame_count,step):
        # 如果大于说明最后一个窗口时间不足30ms
        if i + step <= frame_count:
            cut = audio.get_sample_slice( i, i+step )
            if cut.dBFS < -50:
                acc_start += 0.03
            else:
                # 大于等于-50 看下一个窗口如果大于说明，后一个窗口时间不足30ms
                if i + step * 2 <= frame_count:
                    next_c = audio.get_sample_slice(i + step, i + step * 2)
                    if next_c.dBFS >= -50:
                        break
                    else:
                        acc_start += 0.03

    ##### 后静音计算逻辑，从后往前算
    for i in range(frame_count,0,-step):
        # 不符合说明最后一个窗口时间不足30ms
        if i - step >= 0:
            cut = audio.get_sample_slice( i-step, i )
            if cut.dBFS < -50:
                acc_end += 0.03
            else:
                # 大于等于-50 看下一个窗口 不符合说明，后一个窗口时间不足30ms
                if i - step * 2 >=0 :
                    next_c = audio.get_sample_slice(i - step*2, i -step)
                    if next_c.dBFS >= -50:
                        break
                    else:
                        acc_end += 0.03

    audio_duration = audio.duration_seconds
    valid_duration = max(round(audio_duration - acc_start - acc_end, 2), 0)

    return round(acc_start,2),round(acc_end,2),audio_duration, valid_duration



def ake_download_by_url(row):
    # url,folder,basename, cut_start,cut_end,checksum
    url = row["audio_path"]
    folder = row["save_folder"]
    basename = row["audio_name"]
    cut_start = row["cut_start"]
    cut_end = row["cut_end"]
    checksum = row["checksum"]

    batch_detail_id = row["batch_detail_id"]
    f_start = 0
    f_end =0
    f_total =0
    new_valid_s =0

    if url.startswith("/ac-efs/")==True:
        download_url = appen_url_to_temp_url(url.replace("/ac-efs/","appen://"))
    elif platform.system()=='Linux' and "oss-cn-shanghai.aliyuncs.com" in url:
        # 使用内网协议下载
        download_url = url.replace("oss-cn-shanghai.aliyuncs.com","oss-cn-shanghai-internal.aliyuncs.com")
    else:
        download_url =url

    try:
        out_file = os.path.join(folder,basename)
        rs = requests.get(download_url, stream=True)
        assert rs.status_code == 200, "请求失败"
        rs_bytes = [chunk for chunk in rs.iter_content(chunk_size=1024)]

        bytes_data= b''.join(rs_bytes)
        md5_of_data = md5_file_by_bytes(bytes_data)
        assert checksum == md5_of_data, "md5不相等，可能是数据下载不完整"

        audio = AudioSegment(data = bytes_data)
        # _,_,_, new_valid_s = get_start_end(audio)
        # if new_valid_s <2 or new_valid_s >8:
        #     return 0,batch_detail_id

        start_ms = ceil(cut_start * 1000)
        end_ms = ceil(cut_end * 1000)
        cut_rs = audio[start_ms:end_ms]

        f_start, f_end, f_total, new_valid_s = get_start_end(cut_rs)
        if new_valid_s < 2 or new_valid_s > 8 or f_start < 0.3 or f_end < 0.1:
            return 0, batch_detail_id,f_start, f_end, f_total, new_valid_s

        os.makedirs(folder,exist_ok=True)
        cut_rs.export(out_file, format="wav")
        # 1代表成功
        return 1,batch_detail_id,f_start, f_end, f_total, new_valid_s

    except Exception as e:
        print('error',e,file=sys.stderr)
        # 0代表失败
        return 0,batch_detail_id,f_start, f_end, f_total, new_valid_s




def ake_download_by_url_duration_invalid(row):
    # url,folder,basename, cut_start,cut_end,checksum
    url = row["audio_path"]
    folder = row["save_folder"]
    basename = row["audio_name"]
    cut_start = row["cut_start"]
    cut_end = row["cut_end"]
    checksum = row["checksum"]

    batch_detail_id = row["batch_detail_id"]
    f_start = 0
    f_end =0
    f_total =0
    new_valid_s =0

    if url.startswith("/ac-efs/")==True:
        download_url = appen_url_to_temp_url(url.replace("/ac-efs/","appen://"))
    elif platform.system()=='Linux' and "oss-cn-shanghai.aliyuncs.com" in url:
        # 使用内网协议下载
        download_url = url.replace("oss-cn-shanghai.aliyuncs.com","oss-cn-shanghai-internal.aliyuncs.com")
    else:
        download_url =url

    try:
        out_file = os.path.join(folder,basename)
        rs = requests.get(download_url, stream=True)
        assert rs.status_code == 200, "请求失败"
        rs_bytes = [chunk for chunk in rs.iter_content(chunk_size=1024)]

        bytes_data= b''.join(rs_bytes)
        md5_of_data = md5_file_by_bytes(bytes_data)
        assert checksum == md5_of_data, "md5不相等，可能是数据下载不完整"

        audio = AudioSegment(data = bytes_data)
        # _,_,_, new_valid_s = get_start_end(audio)
        # if new_valid_s <2 or new_valid_s >8:
        #     return 0,batch_detail_id

        start_ms = ceil(cut_start * 1000)
        end_ms = ceil(cut_end * 1000)
        cut_rs = audio[start_ms:end_ms]

        ## 不卡时长
        f_start, f_end, f_total, new_valid_s = get_start_end(cut_rs)
        # if new_valid_s < 2 or new_valid_s > 8 or f_start < 0.3 or f_end < 0.1:
        #     return 0, batch_detail_id,f_start, f_end, f_total, new_valid_s

        os.makedirs(folder,exist_ok=True)
        cut_rs.export(out_file, format="wav")
        # 1代表成功
        return 1,batch_detail_id,f_start, f_end, f_total, new_valid_s

    except Exception as e:
        print('error',e,file=sys.stderr)
        # 0代表失败
        return 0,batch_detail_id,f_start, f_end, f_total, new_valid_s
