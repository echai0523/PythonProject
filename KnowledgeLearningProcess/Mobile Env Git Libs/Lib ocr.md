# ddddocr安装
`pip install ddddocr=1.4.0`
 
# pytesseract安装
- 比较繁琐需要添加配置，不添加每次编写脚本使用时都要编写配置项

    `pip install pytesseract`
### 配置
- 环境变量：
```python
Administrator用户变量 > 新建 > {变量名:TESSDATA_PREFIX, 变量值: tessdata路径D:\Tesseract-OCR\tessdata}
```
- 修改文件：
```python
# tesseract_cmd为tesseract执行文件路径
pytesseract.py > 搜索'cmd'找到并修改tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  
```

 
# 模块导入
import ddddocr
import pytesseract