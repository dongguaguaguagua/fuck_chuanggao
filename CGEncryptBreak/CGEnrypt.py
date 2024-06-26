# -*- coding: utf-8 -*-
import os
import jpype
import json
import Encrypt

# 获取jar包的路径
current_directory = os.path.dirname(os.path.realpath(__file__))
jar_path = os.path.join(current_directory, '../unidbg_jar/unidbg.jar')
# getDefaultJVMPath 获取默认的 JVM 路径
jvm_path = jpype.getDefaultJVMPath()
# startJVM() 启动 JAVA 虚拟机
jpype.startJVM(jvm_path, "-ea", "-Djava.class.path=%s" % (jar_path))


def json_dump(data):
    """特殊的json转字符串的方式: 不加空格, 而且没有中文字符"""
    return json.dumps(data, separators=(',', ':'), ensure_ascii=True)


def get_sign(interface, secret, jsonsport):
    # 通过包名, 实例化JAVA对象 括号内的是包名 后面的是类名+直接实例化
    crack_encrypt_class = jpype.JClass("com.cgencrypt.crack.crackEncrypt")
    api_url = interface + "?jsonsports="
    jsonsport_str = json_dump(jsonsport)
    print(jsonsport_str)
    if interface in ["/api/l/v6.1/prejudgment", "/api/l/v7/savesports"]:
        enc_secret = secret[:16].encode()
        arg2 = api_url + Encrypt.aes_encrypt(jsonsport_str, enc_secret)
    else:
        arg2 = api_url + Encrypt.get_enc_pwd(jsonsport_str)
    calculator = crack_encrypt_class(secret, arg2)  # 传入所需参数
    encypted_str = str(calculator.calc())

    return encypted_str.split("|")
