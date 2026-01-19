from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



HEADER_SIZE = 54 # could be 138 if this does not work
BLOCK_SIZE_BYTES = 16

def ecb(outputFile, blocks, header):

    key = get_random_bytes(16)
    
    with open(outputFile, "wb") as f:
        f.write(header)
        for block in blocks:
            f.write(ecb_encrypt(block, key))

def ecb_encrypt(block, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)

def cbc():
    return 0

def convertToBits(fileName):

    # save the header
    # need to convert to bits
    # chop them into blocks of 128 bits (16 bytes)
    # any excess needs to be padded with PKCS#7 padding

    totalBytes = []
    with open(fileName, "rb") as f:
        totalBytes = f.read()
    
    print(type(totalBytes))
    header = totalBytes[:HEADER_SIZE]

    rest = totalBytes[HEADER_SIZE:]

    blocks = []    
    for i in range(0, len(rest), BLOCK_SIZE_BYTES):
        block = rest[i:i+BLOCK_SIZE_BYTES]
        blocks.append(block)
    
    if len(blocks) > 0:
        last_block = blocks[-1]
        if len(last_block) < BLOCK_SIZE_BYTES:
            padding_len = BLOCK_SIZE_BYTES - len(last_block)
            padding = bytes([padding_len] * padding_len)
            blocks[-1] = last_block + padding
        else:
            padding = bytes([BLOCK_SIZE_BYTES] * BLOCK_SIZE_BYTES)
            blocks.append(padding)
    
    return header, blocks



def main():
    fileName = "./mustang.bmp"

    header, blocks = convertToBits(fileName=fileName)

    ecb("mustangECB.bmp", blocks, header)

if __name__ == "__main__":
    main()
