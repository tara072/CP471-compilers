class doubleBuffer:
    def __init__ (self, inputStr):
        self.inputStr = inputStr
        self.bufferOne = ''
        self.bufferTwo = ''
        self.currentBuff = 1

    # switch between buffers
    def bufferSwitch (self):
        if self.currentBuff == 1: self.currentBuff = 2
        else: self.currentBuff = 1
    
    # read a chunk of data into current buffer
    def bufferFill (self):
        if self.currentBuff == 1: self.bufferOne = self.inputStr.read(2048)
        else: self.bufferTwo = self.inputStr.read(2048)
    
    # def getTokens (self):
    #     if self.currentBuff == 1:
    #         print(self.bufferOne)
    #         token, self.bufferOne = self.bufferOne[0], self.bufferOne[1:]
    #     else:
    #         print(self.bufferTwo)
    #         token, self.bufferTwo = self.bufferTwo[0], self.bufferTwo[1:]

    #     if not token:
    #         self.bufferFill()
    #         self.bufferSwitch()
    #         return self.getTokens()

    #     return token