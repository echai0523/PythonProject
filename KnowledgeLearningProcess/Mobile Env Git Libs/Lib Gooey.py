# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/19 9:34

input: 
output: 
Short Description: 

Change History:

"""
from gooey import Gooey, GooeyParser
from gooey.gui.util.freeze import getResourcePath


# https://blog.csdn.net/liluo_2951121599/article/details/119608197


@Gooey(
    f=None,
    # richtext_controls=False  打开/关闭控制台对终端控制序列的支持（对字体粗细和颜色的有限支持）
    advanced=True,       # 切换显示全部设置还是仅仅是简化版本
    language='english',  # 指定从 gooey/languages 目录读取哪个语言包
    auto_start=False,    # 跳过所有配置并立即运行程序 ， 曾经是 `show_config=True`
    target=None,
    program_name=None,   # GUI 窗口显示的程序名。默认会显 sys.argv[0]。
    program_description=None,  # Settings 窗口顶栏显示的描述性文字。默认值从 ArgumentParser 中获取。
    default_size=(610, 530),   # 工具窗口默认大小
    use_legacy_titles=True,
    required_cols=2,    # 设置必选参数行数。
    optional_cols=2,    # 设置可选参数行数。
    dump_build_config=False,  # 将设置以 JSON 格式保存在硬盘中以供编辑/重用。
    load_build_config=None,
    monospace_display=False,
    image_dir='::gooey/default',
    language_dir=getResourcePath('languages'),
    progress_regex=None,  # progress_regex=r"^progress: (\d+)%$",  # 正则，用于模式化运行时进度信息
    progress_expr=None,  # progress_expr="current / total * 100"
    hide_progress_msg=False,
    disable_progress_bar_animation=False,
    disable_stop_button=False,
    group_by_type=True,
    header_height=80,
    navigation='SIDEBAR',
    tabbed_groups=False,
    use_cmd_args=False)
def main():
    parser = GooeyParser(description='"工具说明:" + "\n" + "   " + "1.本工具仅作为xxx使用"')
    """metavar
    展示在前面的给用户看的，如果没有metavar的时候，第一个参数会展示到界面上。
    """

    """action
    store_true: 勾选选项
    """

    """gooey_options
    可以用来对用户输入的数据进行验证，如果不符合时会进行提示。
    """

    """ widget
    '控件名'： '控件类型'
    'CheckBox': '复选框',
    'DateChooser': '日期选择',
    'DirChooser': '目录选择器',
    'Dropdown': '下拉列表',
    'FileChooser': '文件选择器',
    'FileSaver': '文件保存',
    'MultiDirChooser': '目录多选器',
    'MultiFileChooser': '文件多选器',
    'RadioGroup': '单选框',
    'TextField': '文本输入框'
    """
    # "path": 要传递的参数变量
    # help/metavar:提示信息
    # widget:控件类型(这里使用的是文件夹选择器),一定要用双引号 不然没有这个属性
    # choices:选择列表
    # default:设置默认
    parser.add_argument('Date', widget="DateChooser")  # 日期选择框
    parser.add_argument(option_strings=['-u', '--username'], dest='账号', widget="TextField")  # - 可选 # 账号输入框
    parser.add_argument(option_strings=['-p', '--password'], dest='密码', widget="TextField")  # 密码输入框
    parser.add_argument(option_strings=['-v', '--verify_number'], dest='验证码', widget="TextField")  # 验证码输入框
    parser.add_argument('Filename', widget="FileChooser")  # 文件选择框
    parser.add_argument(option_strings=['-f', '--file_path'], dest="待匹配文件路径", widget="FileChooser")  # 文件选择框
    parser.add_argument("path", help="请选择要整理的文件路径：", widget="DirChooser")   # 文件夹选择框
    parser.add_argument('annotation_type', choices=['a', 'b', 'c', 'd'], default='a', metavar="annotation type", widget='Dropdown')  # 单选框下拉列表
    parser.add_argument(
        'reductionFactor',
        metavar='长宽压缩比',
        help='例如3，需要填入大于等于1的整数',
        gooey_options={
            'validator': {
                'test': '1 <= int(user_input)',     # 输入的值必须大于等于1
                'message': '长宽压缩比需大于等于1'      # 描述信息
            }
        })
    parser.add_argument(
        '-isConvertBlack',
        metavar='是否输出黑白版本',
        action='store_true',  # 定义为勾选选项
        help='需要输出黑白版本请勾选')

    parser.parse_args()   # 获取参数  # 也是运行的关键

    #     parser = GooeyParser(description="Extracting frames from a movie using FFMPEG")
    #     ffmpeg = parser.add_argument_group('Frame Extraction Util')
    #     ffmpeg.add_argument('-i',
    #                         metavar='Input Movie',
    #                         help='The movie for which you want to extract frames',
    #                         widget='FileChooser')
    #     ffmpeg.add_argument('output',
    #                         metavar='Output Image',
    #                         help='Where to save the extracted frame',
    #                         widget='FileSaver',
    #                         )
    #     ffmpeg.add_argument('-ss',
    #                         metavar='Timestamp',
    #                         help='Timestamp of snapshot (in seconds)')
    #     ffmpeg.add_argument('-frames:v',
    #                         metavar='Timestamp',
    #                         default=1,
    #                         gooey_options={'visible': False})
    #     parser.parse_args()


if __name__ == "__main__":
    main()
