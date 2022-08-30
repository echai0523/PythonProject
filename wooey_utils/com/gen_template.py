# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-10-15 16:26
Short Description:

Change History:
- 通用的生成模版工具


'''

import re



class GEN_CONFIG():


    def __str__(self):
        pass


    def unit_parse(self,unit_text):
        # 移动性 [TrafficLightMobility]
        m = re.match(r"^(.*)?\[(.*)\]$", unit_text)
        print(m.groups())
        label = ''
        value = ''


    def parse_label(self,text):
        # 信号灯[Sign]

        pass

from pydub import  AudioSegment

# rs = requests.get(audio_url, stream=True)
# assert rs.status_code == 200, "请求失败"
# rs_bytes = [chunk for chunk in rs.iter_content(chunk_size=1024)]
# bytes_data= b''.join(rs_bytes)
# audio = AudioSegment(data = bytes_data)

audio = AudioSegment.from_wav(origin_audio_path)
out_rs = audio[cut_start_ms*1000:cut_end_ms*1000]
out_rs.export(out_file,format="wav")
