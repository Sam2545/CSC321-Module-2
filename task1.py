from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



HEADER_SIZE = 54 # could be 138 if this does not work
BLOCK_SIZE = 128

def ecb(outputFile, blocks, header):
    return 0

def cbc():
    return 0

def convertToBits(fileName):

    # save the header
    # need to convert to bits
    # chop them into blocks of 128 
    # any excess needs to be padded with 128 - number of bits remaining

    totalBytes = []
    with open(fileName, "rb") as f:
        totalBytes = f.read()
    
    print(type(totalBytes))
    header = totalBytes[:HEADER_SIZE]

    rest = totalBytes[HEADER_SIZE:]

    blocks = []

    for i in range(0, len(rest), BLOCK_SIZE):
        blocks.append(rest[i:i+BLOCK_SIZE])
    
    if len(rest) % BLOCK_SIZE != 0:
        remaining = BLOCK_SIZE - (len(rest) % BLOCK_SIZE)
        blocks.append(rest[:(-1 * remaining)] + remaining * bytes([0x00])) # PKCS 7 padding need to fix



def main():
    fileName = "./mustang.bmp"

    header, blocks = convertToBits(fileName=fileName)

    ecb("ecbOutput.txt", blocks, header)







if __name__ == "__main__":
    main()
