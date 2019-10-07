import random
import copy
import numpy as np

rawData = []
f = open("output.txt", "w")
rawString = ""


def randomRuin(data, codeType):
    if codeType == "Hamming":
        for i in range(0, len(data)):
            if random.randint(0, 1):
                j = random.randint(0, 11)
                data[i][j] ^= 1
        return data
    elif codeType == "LinearBlock":
        for i in range(0, len(data)):
            if random.randint(0, 1):
                j = random.randint(0, 6)
                data[i][j] ^= 1
        return data
    elif codeType == "Cyclic":
        for i in range(0, len(data)):
            if random.randint(0, 1):
                j = random.randint(0, 6)
                data[i][j] ^= 1
        return data
    else:
        print("Error: Undifned Code Type !")
        return None


# for hamming(8,4)
class HammingCode():
    def __init__(self, rawData, rawLen=8):
        global f, rawString
        self.rawLen = rawLen
        self.data = [rawData[0+8*i:8+8*i]for i in range(0, int(self.rawLen/8))]
        self.data = [[-1, -1, self.data[i][0], -1, self.data[i][1], self.data[i][2], self.data[i][3], -1,
                      self.data[i][4], self.data[i][5], self.data[i][6], self.data[i][7]] for i in range(0, int(self.rawLen/8))]

    def encode(self):
        f.writelines(["Encoded Data:", "\n"])
        for d in self.data:
            hamming = []
            for j, c in enumerate(d):
                if c == 1:
                    hamming.append(j+1)
            hammingCode = 0
            for t in hamming:
                hammingCode ^= t
            hammingCode = bin(hammingCode)[2:].zfill(4)

            for t in range(0, len(hammingCode)):
                for j in range(len(d)):
                    if d[j] == -1:
                        d[j] = ord(hammingCode[-t-1]) - ord('0')
                        break
            # write to file
            f.writelines([str(c)
                          for c in d])

    def ruin(self):
        self.data = randomRuin(self.data, "Hamming")
        f.writelines(["\n", "Defective Data:", "\n"])
        f.writelines([str(self.data[i][j]) for j in range(12)
                      for i in range(int(self.rawLen/8))])

    def decode(self):
        f.writelines(["\n", "Decoded Data:", "\n"])
        errorCount = 0
        for i, d in enumerate(self.data):
            hamming = []
            for j, c in enumerate(d):
                if c == 1:
                    hamming.append(j+1)

            hammingCode = 0
            for t in hamming:
                hammingCode ^= t
            if hammingCode == 0:
                print("No error")
            else:
                print("Error at %s" % (hammingCode-1))
                errorCount += 1
                if hammingCode < 13:
                    d[hammingCode-1] ^= 1
                else:
                    print("Can not correct!")
            self.data[i] = [d[2], d[4], d[5], d[6], d[8], d[9], d[10], d[11]]
            f.writelines([str(c) for c in d])
        # print(self.data)
        f.writelines(["\n", "Number of Error:", str(errorCount),
                      ", Corrected: ", str(self.getData() == rawString), "\n"])

    def getData(self):
        s = ""
        for d in self.data:
            for c in d:
                s += str(c)
        return s

    # pass

# for linear block(7,4)


class LinearBlock():
    def __init__(self, rawData, rawLen=8):
        global f, rawString
        self.rawLen = rawLen
        self.data = [rawData[0+4*i:4+4*i]for i in range(0, int(self.rawLen/4))]
        self.data = np.reshape(self.data, (int(self.rawLen/4), 4))
        self.rawdata = copy.deepcopy(self.data)
        self.G = [[1, 0, 0, 0, 1, 1, 0],
                  [0, 1, 0, 0, 0, 1, 1],
                  [0, 0, 1, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 0, 1]
                  ]
        self.G = np.reshape(self.G, (4, 7))
        self.Ht = [[1, 0, 1, 1, 1, 0, 0],
                   [1, 1, 1, 0, 0, 1, 0],
                   [0, 1, 1, 1, 0, 0, 1]
                   ]
        self.Ht = np.reshape(self.Ht, (3, 7))
        self.Ht = np.transpose(self.Ht)
        self.errorMap = {6: 0,
                         3: 1,
                         7: 2,
                         5: 3,
                         4: 4,
                         2: 5,
                         1: 6
                         }

    def encode(self):
        f.writelines(["Encoded Data:", "\n"])
        temp = np.zeros((int(self.rawLen/4), 7), 'i')
        for i, d in enumerate(self.data):
            temp[i] = (np.dot(d, self.G) % 2)
        self.data = temp

        for d in self.data:
            f.writelines(str(c) for c in d)

    def ruin(self):
        self.data = randomRuin(self.data, "LinearBlock")
        f.writelines(["\n", "Defective Data:", "\n"])
        for d in self.data:
            f.writelines(str(c) for c in d)

    def decode(self):
        f.writelines(["\n", "Decoded Data:", "\n"])
        errorCount = 0
        temp = np.zeros((int(self.rawLen/4), 4), 'i')
        for i, d in enumerate(self.data):
            eHT = np.dot(d, self.Ht) % 2
            if (np.sum(eHT) != 0):
                errorCount += 1
                eNum = self.errorMap[eHT[0] << 2 ^ eHT[1] << 1 ^ eHT[2]]
                # print("Error at %s !" % eNum)
                d[eNum] ^= 1
            temp[i] = d[:4]
        self.data = temp
        for d in self.data:
            f.writelines(str(c) for c in d)

        f.writelines(["\n", "Number of Error:", str(errorCount),
                      ", Corrected: ", str(self.getData() == rawString), "\n"])

    def getData(self):
        s = ""
        for d in self.data:
            for c in d:
                s += str(c)
        return s

# for cyclic(7,4)


class CyclicCode():
    def __init__(self, rawData, rawLen=8):
        global f, rawString
        self.rawLen = rawLen
        self.data = [rawData[0+4*i:4+4*i]for i in range(0, int(self.rawLen/4))]
        self.data = np.reshape(self.data, (int(self.rawLen/4), 4))
        self.rawdata = copy.deepcopy(self.data)
        # Note gx should be array below, but for convenience we assign another value
        # self.gx = np.array([0, 0, 0, 1, 0, 1, 1])
        self.gx = np.array([1, 0, 1, 1, 0, 0, 0])
        self.mappingTable = {0: [0, 0, 0, 0, 0, 0, 0],
                             1: [0, 0, 0, 1, 0, 1, 1],
                             2: [0, 0, 1, 0, 1, 1, 0],
                             3: [0, 0, 1, 1, 1, 0, 1],
                             4: [0, 1, 0, 0, 1, 1, 1],
                             5: [0, 1, 0, 1, 1, 0, 0],
                             6: [0, 1, 1, 0, 0, 0, 1],
                             7: [0, 1, 1, 1, 0, 1, 0],
                             8: [1, 0, 0, 0, 1, 0, 1],
                             9: [1, 0, 0, 1, 1, 1, 0],
                             10: [1, 0, 1, 0, 0, 1, 1],
                             11: [1, 0, 1, 1, 0, 0, 0],
                             12: [1, 1, 0, 0, 0, 1, 0],
                             13: [1, 1, 0, 1, 0, 0, 1],
                             14: [1, 1, 1, 0, 1, 0, 0],
                             15: [1, 1, 1, 1, 1, 1, 1]
                             }

        self.mappingTableBack = {0: [0, 0, 0, 0],
                                 11: [0, 0, 0, 1],
                                 22: [0, 0, 1, 0],
                                 29: [0, 0, 1, 1],
                                 39: [0, 1, 0, 0],
                                 44: [0, 1, 0, 1],
                                 49: [0, 1, 1, 0],
                                 58: [0, 1, 1, 1],
                                 69: [1, 0, 0, 0],
                                 78: [1, 0, 0, 1],
                                 83: [1, 0, 1, 0],
                                 88: [1, 0, 1, 1],
                                 98: [1, 1, 0, 0],
                                 105: [1, 1, 0, 1],
                                 116: [1, 1, 1, 0],
                                 127: [1, 1, 1, 1]
                                 }

        self.errorMap = {1: [0, 0, 0, 0, 0, 0, 1],
                         2: [0, 0, 0, 0, 0, 1, 0],
                         4: [0, 0, 0, 0, 1, 0, 0],
                         3: [0, 0, 0, 1, 0, 0, 0],
                         6: [0, 0, 1, 0, 0, 0, 0],
                         7: [0, 1, 0, 0, 0, 0, 0],
                         5: [1, 0, 0, 0, 0, 0, 0]
                         }

    def encode(self):
        f.writelines(["Encoded Data:", "\n"])
        temp = np.zeros((int(self.rawLen/4), 7), 'i')
        for i, d in enumerate(self.data):
            temp[i] = self.mappingTable[d[0] <<
                                        3 ^ d[1] << 2 ^ d[2] << 1 ^ d[3]]
        self.data = temp
        f.writelines([self.getData(), "\n"])

    def ruin(self):
        self.data = randomRuin(self.data, "Cyclic")
        f.writelines(["\n", "Defective Data:", "\n"])
        f.writelines([self.getData(), "\n"])

    def decode(self):
        f.writelines(["\n", "Decoded Data:", "\n"])
        errorCount = 0
        temp = np.zeros((int(self.rawLen/4), 4), 'i')
        for i, d in enumerate(self.data):
            remainder = (d[0] << 6) + (d[1] << 5) + (d[2] << 4) + \
                (d[3] << 3) + (d[4] << 2) + (d[5] << 1) + (d[6])
            temp_data = copy.deepcopy(self.data[i])
            roll = 0
            while remainder > 7:
                while temp_data[roll] != 1:
                    roll += 1
                gx = np.roll(self.gx, roll)
                temp_data = np.bitwise_xor(temp_data, gx)
                remainder = (temp_data[0] << 6) + (temp_data[1] << 5) + (temp_data[2] << 4) + (
                    temp_data[3] << 3) + (temp_data[4] << 2) + (temp_data[5] << 1) + (temp_data[6])

            if remainder != 0:
                print(d)
                print(self.errorMap[remainder])
                d = np.bitwise_xor(d, self.errorMap[remainder])
                print("Error Detect!")
                errorCount += 1
                print(d)

            temp[i] = np.array(self.mappingTableBack[(
                d[0] << 6) + (d[1] << 5) + (d[2] << 4) + (d[3] << 3) + (d[4] << 2) + (d[5] << 1) + (d[6])])

        self.data = temp
        f.writelines([self.getData(), "\n"])
        f.writelines(["\n", "Number of Error:", str(errorCount),
                      ", Corrected: ", str(self.getData() == rawString), "\n"])

    def getData(self):
        s = ""
        for d in self.data:
            for c in d:
                s += str(c)
        return s


if __name__ == "__main__":
    rawData = [random.randint(0, 1) for i in range(64)]
    rawString = "".join([str(c) for c in rawData])
    print(rawString)
    f.writelines(["=========== Raw Data ===========", "\n"])
    f.writelines(["Raw Data:", "\n"])
    f.writelines([str(rawData[i]) for i in range(len(rawData))])
    f.writelines("\n")

    print("=========== Raw Data ===========")
    print(rawString)
    print("============= Hamming Code =============")
    f.writelines(["============= Hamming Code =============", "\n"])
    myHamming = HammingCode(rawData, 64)
    myHamming.encode()
    myHamming.ruin()
    myHamming.decode()
    print(myHamming.getData())
    print("============= Linear Block Code =============")
    f.writelines(["============= Linear Block Code =============", "\n"])
    myLinearBlock = LinearBlock(rawData, 64)
    myLinearBlock.encode()
    myLinearBlock.ruin()
    myLinearBlock.decode()
    print(myLinearBlock.getData())
    print("============= Cyclic Code =============")
    f.writelines(["============= Cyclic Code =============", "\n"])
    myCyclic = CyclicCode(rawData, 64)
    myCyclic.encode()
    myCyclic.ruin()
    myCyclic.decode()
