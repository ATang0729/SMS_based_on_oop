'''数据加密与解密模块

模块功能：
1. 生成RSA公钥和私钥
2. 用AES密钥加密明文，并用RSA公钥加密AES密钥
3. 用RSA私钥解密被加密的AES密钥，再用解密后的AES密钥解密密文'''


from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
from os import path, mkdir

def key_generate(adminName:str)->tuple[str, str]:
    '''生成公钥和私钥函数
    
    生成私钥文件,返回公钥和存储私钥的文件名称
    
    adminName:管理员姓名'''
    key = RSA.generate(2048)
    private_key = key.export_key()
    # print(private_key)
    filename = "private_key/private_adminName_{0}.pem".format(adminName)
    if not path.exists('private_key'):
        mkdir('private_key')
    file_out = open(filename, "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    return public_key, filename

def aes_encrypt(adminName:str, password:str, public_key:str)->bool:
    '''加密函数
    
    adminName:管理员姓名
    password:明文
    public_key:RSA公钥

    先用AES密钥加密输入的密码，再用RSA公钥加密AES密钥，并将用于解密的信息写入文件file_out中
    若加密成功，返回存储信息的文件名，否则返回False'''
    # 打开用于存储密文的文件
    filename = "encrypted_data/encrypted_data_adminName_{0}.bin".format(adminName)
    if not path.exists('encrypted_data'):
        mkdir('encrypted_data')
    file_out = open(filename, "wb")
    # 明文编码
    password = password.encode("utf-8")
    # AES密钥生成
    aes_key = get_random_bytes(32)
    # AES密钥加密明文
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(password)
    # 用RSA公钥加密AES密钥
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    aes_key_enc = cipher_rsa.encrypt(aes_key)
    # 将加密后的AES密钥和密文等信息写入文件file_out中
    try:
        [ file_out.write(x) for x in (aes_key_enc, cipher_aes.nonce, tag, ciphertext) ]
        return filename
    except Exception as e:
        print(e)
        return False
    finally:
        file_out.close()
        

def aes_decrypt(filename:str, private_key:str)->str:
    '''解密函数
    
    filename:存储密文的文件的文件名
    private_key:RSA私钥

    读取文件后，先用RSA私钥解密AES密钥，再用解密后的AES密钥解密密文
    
    返回明文'''
    # 解密被加密的AES密钥
    print(private_key)

    file_in = open(filename, "rb")

    private_key = RSA.import_key(private_key)

    enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]    


    try:
        # 用RSA私钥解密AES密钥
        # print('----------------------')
        cipher_rsa = PKCS1_OAEP.new(private_key)
        # print('----------------------')
        AES_key = cipher_rsa.decrypt(enc_session_key)
        # AES密钥解密密文
        # print('----------------------')
        cipher_AES = AES.new(AES_key, AES.MODE_EAX, nonce=nonce)
        password_decrypt = cipher_AES.decrypt_and_verify(ciphertext, tag)
        # 明文解码
        # print('----------------------')
        password_decrypt = password_decrypt.decode("utf-8")
        return password_decrypt
    except Exception as e:
        print('解密失败:',e)
        return False

if __name__ == '__main__':
    k1,k2 = key_generate()
    print(k1.decode('utf-8').encode('utf-8'))
    AES_key_enc, nonce, tag, ciphertext = aes_encrypt('123456', k1)
    print(type(AES_key_enc))
    print(nonce)
    print(tag)
    print(ciphertext)
    print(str(nonce))
    print(str(tag))
    print(str(ciphertext))
    print(str(ciphertext).replace("\"","\"\"").replace("\'","\"").replace('\\','\\\\'))
