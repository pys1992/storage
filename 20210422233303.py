import io
import os
import json
import time
import base64
import subprocess
import requests
import plistlib
import re
import codecs
# Pillow
from PIL import Image
from PIL import ImageGrab
# PyObjC
from AppKit import NSPasteboard, NSURLPboardType

def getPath():
    pb = NSPasteboard.generalPasteboard()

    url = pb.stringForType_(NSURLPboardType)

    if url is None:
        return None
    else:
        plistBytes = url.encode("utf-8")
        return codecs.decode(re.findall(rb'<string>file://(.+?)</string>', plistBytes)[0],'UTF-8')

def push(base64, filename):
    url = "https://api.github.com/repos/pys1992/storage/contents/" + filename

    headers = {"Authorization": "token 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"}

    data = json.dumps({
        "message": "auto commit",
        "committer": {
            "name": "pys",
            "email": "me@pys.im"
        },
        "content": base64
    })

    rawReponse = requests.put(url=url, data=data, headers=headers)

    if rawReponse.status_code != 201:
        raise RuntimeError("上传图片失败。")

def extension(path):
  return os.path.splitext(path)[1]

# 将文件转换为base64编码，上传文件必须将文件以base64格式上传
def bytesToBase64(data):
    return base64.b64encode(data).decode('utf-8')

def handleLocalFile(path):

    with open(path, 'rb') as f:
        base64 = bytesToBase64(f.read())
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + extension(path)
        push(base64, filename)

        return filename

def handleClipboard():
    return

def fullUrl(filename):
    return "https://cdn.jsdelivr.net/gh/pys1992/storage@main/" + filename

def markdown(filename):
    return "![]" + fullUrl(filename) + ")"

# https://developer.apple.com/documentation/appkit/nspasteboard/pasteboardtype
if __name__ == '__main__':
    path = getPath()

    if path is None:
        filename = handleClipboard()
    else:
        filename = handleLocalFile(path)

    print(fullUrl(filename))
    # print(path())
    # print(type(str(pbstring)))
    # text = pb.stringForType_(kUTTypeUTF8PlainText)
    # print(text)
    # plist1 = plistlib.load(pbstring)
    # print(plist1)
    # print(type(str(pbstring)))
    # print(pbstring.encode("utf-8"))
    # res = re.match(r'<string>.*</string>', str(pbstring))
    # print(res)

    # types = pb.types()

    # if isLocalFile(types):
    #     handleLocalFile()
    # else:
    #     handleClipboard()
# if "public.file-url" in types:

# items = pb.pasteboardItems()
# print(pb)
# print(_metadata)
# print(items)
# image = ImageGrab.grabclipboard()

# if not isinstance(image, Image.Image):
#     raise RuntimeError("输入的内容不是图片。")

# buffer = io.BytesIO()

# extension = "webp"

# image.save(buffer, extension)

# content = base64.b64encode(buffer.getvalue()).decode('utf-8')

# filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "." + extension

# url = "https://api.github.com/repos/pys1992/storage/contents/" + filename

# headers = {"Authorization": "token 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"}

# data = json.dumps({
#     "message": "auto commit",
#     "committer": {
#         "name": "pys",
#         "email": "me@pys.im"
#     },
#     "content": content
# })

# rawReponse = requests.put(url=url, data=data, headers=headers)

# if rawReponse.status_code != 201:
#     raise RuntimeError("上传图片失败。")

# url = "![](https://cdn.jsdelivr.net/gh/pys1992/storage@main/" + filename + ")"

# p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)

# p.stdin.write(url.encode("utf-8"))

# p.stdin.close()

# p.communicate()


# def isLocalFile(types):
#     return "public.file-url" in types
