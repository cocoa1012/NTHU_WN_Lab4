import random
import copy
import numpy as np

rawData = []
f = open("output.txt","w")

def randomRuin(data, codeType):    
    if codeType == "Hamming":
        for i in range(0, len(data)):
            if random.randint(0,1):
                j = random.randint(0,11)
                data[i][j] ^= 1
        return data
    elif codeType == "LinearBlock":
        pass
    elif codeType == "Cyclic":
        pass
    else:
        print("Error: Undifned Code Type !")
        return None


# for hamming(8,4)
class HammingCode():
    def __init__(self, rawData, rawLen=8):
        global f
        self.rawLen = rawLen
        # self.data = [[]]
        self.data = [rawData[0+8*i:8+8*i]for i in range(0,int(self.rawLen/8))]
        self.rawData = copy.deepcopy(self.data)
        # print(self.rawData)
        self.data = [[-1,-1,self.data[i][0],-1,self.data[i][1],self.data[i][2],self.data[i][3],-1,self.data[i][4],self.data[i][5],self.data[i][6],self.data[i][7]] for i in range(0,int(self.rawLen/8))]
        
    def encode(self):
        f.writelines(["Encoded Data:","\n"])
        for i in range(0, int(self.rawLen/8)):
            hamming = []
            for j in range(0, 12):
                if self.data[i][j] == 1:
                    hamming.append(j+1)
            hammingCode = 0
            for t in range (0, len(hamming)):
                hammingCode ^= hamming[t]
            hammingCode = bin(hammingCode)[2:].zfill(4)

            for t in range(0, len(hammingCode)):
                for j in range(0, 12):
                    if self.data[i][j] == -1:
                        self.data[i][j] = ord(hammingCode[-t-1]) - ord('0')
                        break
            # write to file
            f.writelines([str(self.data[i][j]) for j in range(len(self.data[i]))])

    def ruin(self):
        self.data = randomRuin(self.data,"Hamming")
        f.writelines(["\n","Defective Data:","\n"])
        f.writelines([str(self.data[i][j]) for j in range(12) for i in range(int(self.rawLen/8))])

    def decode(self):
        f.writelines(["\n","Decoded Data:","\n"])
        errorCount = 0
        for i in range(0,int(self.rawLen/8)):
            hamming = []
            for j in range(0, 12):
                if self.data[i][j] == 1:
                    hamming.append(j+1)
            
            hammingCode = 0
            for t in range (0, len(hamming)):
                hammingCode ^= hamming[t]
            if hammingCode == 0:
                print ("No error")
            else:
                print ("Error at %s" % (hammingCode-1))
                errorCount += 1
                if hammingCode < 13 :
                    self.data[i][hammingCode-1] ^= 1
                else:
                    print("Can not correct!")
            self.data[i] = [self.data[i][2], self.data[i][4], self.data[i][5], self.data[i][6], self.data[i][8], self.data[i][9], self.data[i][10], self.data[i][11]]
            f.writelines([str(self.data[i][j]) for j in range(len(self.data[i]))])
        # print(self.data)
        f.writelines(["\n","Number of Error:",str(errorCount),", Corrected: ",str(self.data == self.rawData),"\n"])

    def getData(self):
        return self.data


    # pass

# for linear block(7,4)
class LinearBlock():
    def __init__(self, rawData, rawLen=8):
        global f
        self.rawLen = rawLen
        self.data = [rawData[0+4*i:4+4*i]for i in range(0,int(self.rawLen/4))]
        self.rawdata = copy.deepcopy(self.data)
        self.G =    [   [1, 0, 0, 0, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1],
                        [0, 0, 1, 0, 1, 1, 1],
                        [0, 0, 0, 1, 1, 0, 1]
                    ]
        self.G = np.reshape(self.G,(4,7))
        print(self.data)

    def encode(self):
        f.writelines(["Encoded Data:","\n"])
        for i in range(0, int(self.rawLen/4)):
            print((np.dot(self.data[i], self.G))%2)
            # TODO need to conduct in GF(2)
        pass

    def ruin(self):
        pass

    def decode(self):
        pass

    def getData(self):
        pass


if __name__ == "__main__":
    rawData = [random.randint(0,1) for i in range(64)]
    f.writelines(["=========== Raw Data ===========","\n"])
    f.writelines(["Raw Data:","\n"])
    f.writelines([str(rawData[i]) for i in range(len(rawData))])
    f.writelines("\n")
    
    print ("=========== Raw Data ===========")
    print (rawData)
    print("=============Hamming Code =============")
    f.writelines(["=============Hamming Code =============","\n"])
    myHamming = HammingCode(rawData,64)
    myHamming.encode()
    myHamming.ruin()
    myHamming.decode()
    print (myHamming.getData())
    # print("=============Linear Block Code =============")
    # f.writelines(["=============Linear Block Code =============","\n"])
    # myLinearBlock = LinearBlock(rawData)
    # myLinearBlock.encode()
    pass