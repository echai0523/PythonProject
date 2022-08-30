# -*- coding: utf-8 -*-

# Author: Eric
# CreateTime: 2021/11/5 2:07 下午
# File: amr_tools.py
# version:


import requests

from pydub import AudioSegment
# from bs4 import BeautifulSoup

from wooey_utils.com.config import AMR_API_HOST

'''
获取音频参数
@param:
    1.wav: 音频
@return:
    1.back_noise: 底噪
    2.snr_db: 信噪比
    3.numSec: 空音频
'''


def appen_url_to_json(wav):
    url = f"{AMR_API_HOST}/wav-info"
    data = {"wav": wav}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=data, headers=headers, timeout=60 * 90)
    if resp.status_code == 200:
        content = resp.json()["info"]
        json_dict = {'back_noise': content['back_noise'], 'snr_db': content['snr_db'], 'numSec': content['numSec']}
        return json_dict


'''
获取语料信息
    @param:
        1.temp_df: temp_script.csv临时脚本生成的DataFrame
        2.url: 音频链接
    @return:
        1.prompt: 语料
'''


def get_txt(temp_df, url):
    record_id = url.split("_")[-2]
    prompt = str(temp_df[temp_df["Corpus Code"] == record_id]["Prompt"].tolist()[0]).replace("\n", "")
    # soup = BeautifulSoup(prompt, "lxml")
    return prompt.split('<')[-4].split('>')[-1]


'''
前后添加0.5s空音频
    @param:
        1.path: 音频路径
        2.start_time: 起始时间
        3.end_time: 结束时间
        4.wav_time: 音频时长
    @return:
        1. 音频
'''


def empty_audio_add(path, start_time, end_time, wav_time):
    audio = AudioSegment.from_file(path, format="wav")
    if start_time < 500:
        start_time = 0
        start_empty_audio = AudioSegment.silent(duration=500 - start_time)
        if wav_time - end_time < 500:
            end_time = wav_time
            end_empty_audio = AudioSegment.silent(duration=end_time + 500 - wav_time)
            new_audio = audio[round(start_time): round(end_time)]
            start_audio = start_empty_audio + new_audio
            end_audio = start_audio + end_empty_audio
        else:
            end_time += 500
            new_audio = audio[round(start_time): round(end_time)]
            end_audio = start_empty_audio + new_audio
    else:
        start_time -= 500
        if wav_time - end_time < 500:
            end_time = wav_time
            end_empty_audio = AudioSegment.silent(duration=end_time + 500 - wav_time)
            new_audio = audio[round(start_time): round(end_time)]
            end_audio = new_audio + end_empty_audio
        else:
            end_time += 500
            end_audio = audio[round(start_time): round(end_time)]
    return end_audio.export(path, format="wav")
