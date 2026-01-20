from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



HEADER_SIZE = 54 # could be 138 if this does not work
BLOCK_SIZE_BYTES = 16

def ecb(outputFile, blocks, header):

    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    
    with open(outputFile, "wb") as f:
        f.write(header)
        for block in blocks:
            f.write(ecb_encrypt(block, key, cipher))

def ecb_encrypt(block, key, cipher):
    return cipher.encrypt(block)

def cbc(outputFile, blocks, header):
    key = get_random_bytes(16)
    iv = get_random_bytes(16) # only for the first block
    previous_block = iv
    cipher = AES.new(key, AES.MODE_ECB)
    with open(outputFile, "wb") as f:
        f.write(header)
        for block in blocks:
            ciphertext = cbc_encrypt(block, key, previous_block, cipher)
            previous_block = ciphertext
            f.write(ciphertext)

def cbc_encrypt(block, key, previous_block, cipher):

    # need to xor the block with the previous block
    # run cbc encryption on the block with the key
    # return the cihpertext block
    xor_block = bytes([block[i] ^ previous_block[i] for i in range(len(block))]) 
    return cipher.encrypt(xor_block)

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
    mustangFileName = "./mustang.bmp"
    cpLogoFileName = "./cp-logo.bmp"

    headerMustang, blocksMustang = convertToBits(fileName=mustangFileName)
    headerCpLogo, blocksCpLogo = convertToBits(fileName=cpLogoFileName)

    ecb("mustangECB.bmp", blocksMustang, headerMustang)

    cbc("mustangCBC.bmp", blocksMustang, headerMustang)

    ecb("cpLogoECB.bmp", blocksCpLogo, headerCpLogo)

    cbc("cpLogoCBC.bmp", blocksCpLogo, headerCpLogo)

if __name__ == "__main__":
    main()
