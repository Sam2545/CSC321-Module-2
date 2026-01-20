from urllib.parse import quote
from task1 import convertToBits, cbc
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



def submit(data, key, iv):

    safe_encode = quote(data) # encodes the string to remove any ; and = characters
    
    inp = f"userid=456;userdata={data};session-id=31337"

    # convert to bytes

    input_bytes = inp.encode("utf-8")

    # pad the final text 
    header, blocks = convertToBits(input_bytes)
    # encrypt using CBC

    ciphertext = cbc(blocks, header, key, iv)

    # return the ciphertext

    return ciphertext

def verify(ciphertext, key, iv):

    # decrypt the string using AES CBC

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    plaintext_bytes = cipher.decrypt(ciphertext)
    plaintext_str = plaintext_bytes.decode("utf-8")

    # check if it contains “;admin=true;” and return T/F

    return ";admin=true;" in plaintext_str




def main():

    key = get_random_bytes(16)
    iv = get_random_bytes(16) # only for the first block

    data = "You’re the man now, dog"
    ciphertext = submit(data, key, iv)
    print(verify(ciphertext, key, iv))






if __name__ == "__main__":
    main()