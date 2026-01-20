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

def cbc(blocks, header, key = None, iv = None, outputFile=None):
    if key is None:
        key = get_random_bytes(16)

    if iv is None:
        iv = get_random_bytes(16)
    previous_block = iv
    cipher = AES.new(key, AES.MODE_ECB)
    
    ciphertext_blocks = []
    for block in blocks:
        ciphertext = cbc_encrypt(block, key, previous_block, cipher)
        previous_block = ciphertext
        ciphertext_blocks.append(ciphertext)
    
    # Combine all ciphertext blocks
    ciphertext_bytes = b''.join(ciphertext_blocks)
    
    # Write to file if outputFile is provided
    if outputFile is not None:
        with open(outputFile, "wb") as f:
            f.write(header)
            f.write(ciphertext_bytes)
    
    return ciphertext_bytes

def cbc_encrypt(block, key, previous_block, cipher):

    # need to xor the block with the previous block
    # run cbc encryption on the block with the key
    # return the cihpertext block
    xor_block = bytes([block[i] ^ previous_block[i] for i in range(len(block))]) 
    return cipher.encrypt(xor_block)

def convertToBits(input_data):

    # save the header
    # need to convert to bits
    # chop them into blocks of 128 bits (16 bytes)
    # any excess needs to be padded with PKCS#7 padding
    # Can accept either a file path (string) or bytes data directly

    # Check if input is a file path (string) or bytes data
    if isinstance(input_data, str):
        # File path: open file and read bytes
        with open(input_data, "rb") as f:
            totalBytes = f.read()
        header = totalBytes[:HEADER_SIZE]
        rest = totalBytes[HEADER_SIZE:]
    elif isinstance(input_data, bytes):
        # Bytes data: no header, process all bytes
        header = b''
        rest = input_data

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

    headerMustang, blocksMustang = convertToBits(mustangFileName)
    headerCpLogo, blocksCpLogo = convertToBits(cpLogoFileName)

    ecb("mustangECB.bmp", blocksMustang, headerMustang)

    cbc(blocksMustang, headerMustang, outputFile="mustangCBC.bmp")
    
    cbc(blocksCpLogo, headerCpLogo, outputFile="cpLogoCBC.bmp")

    ecb("cpLogoECB.bmp", blocksCpLogo, headerCpLogo)


if __name__ == "__main__":
    main()
