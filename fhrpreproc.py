import re
import numpy as np

class FHRpreproc:
    'Class to preprocess a wfdb-ctg physionet FHR record'
    def __init__(self,record):
        'Init with setting the record object to be preprocessed'
        self.record = record # Wfdb Intrapartum Record Object
        self.siglen = len(self.record.p_signals[:,0]) #Length of FHR Signal
        self.pH = None #pH
        self.delType = None #Delivery Type
        self.posStage2 = None #Sample location of the beginning of Staeg 2

    def parseHeader(self):
        'Function to parse additional Header info from record object'
        headerInfo=self.record.comments
        #Isolate pH
        pHstring = headerInfo[2]
        pHmatch=re.search('pH\s*(\d+.\d+)',pHstring)
        pHmatch2= re.search('pH\s*(\d+)',pHstring)
        if pHmatch != None:
            self.pH = float(pHmatch.group(1))
        elif pHmatch2 != None:
            self.pH = float(pHmatch2.group(1))
        else:
            self.pH = None
        #Pos stage II- This is position in raw signal sample not an index of
        # an array
        posStage2String = headerInfo[40]
        posStage2 = re.search('Pos. II.st.\s*(\d+)',posStage2String)
        if posStage2:
            self.posStage2 = int(posStage2.group(1))

        #Delivery Type
        delTypeString = headerInfo[36]
        delType = re.search('Deliv. type\s*(\d+)',delTypeString)
        if delType:
            self.delType = int(delType.group(1))

    def sepLaborSigs(self):
        """eparate FHR signal to each individual labor stage
        based on position of the beginning of the second stage of labor in
        header

        Return Tuple of Stage 1 Signal, Stage 1 Length, Stage 2 Signal, and
        Stage 2 length
        """
        #Separate Stage I Signal
        Stage1Sig = self.record.p_signals[0:self.posStage2,0]
        #length of Stage 1 Signal
        Stage1len = len(Stage1Sig)
        #Separate Stage II Signal
        Stage2Sig = self.record.p_signals[self.posStage2:,0]
        Stage2len = len(Stage2Sig)
        return (Stage1Sig, Stage1len, Stage2Sig, Stage2len)

    def trimSignal(self,signal,excTimeSecs):
        """Trim signal by removing excTime (seconds) samples from original
        signal"""
        excTimeSamp = excTimeSecs * self.record.fs #excluded number of samples
        trimSignal = signal[excTimeSamp:]
        return trimSignal

    def compSignal(self,signal):
        """Compress signal by removing all zero elements"""
        compSignal = signal[np.nonzero(signal)]
        return compSignal

    def calcFHRMean(self, signal):
        """Function to calculate mean of an FHR signal array"""
        FHRmean = np.mean(signal)
        return FHRmean

    def calcFHRVariability(self,signal):
        """Calculate FHR Signal Variability"""
        #Variability will be the standard deviation of the signal
        FHRvar = np.std(signal)
        return FHRvar

    def calcAcc(self,signal,FHRmean,minAccDur):
        """Calculate number of accelerations in an FHR Signal.
        Define each Acc to be 15 bpm > mean of HR Signal for at least
        minAccDur"""
        #Minimum duration in samples
        minAccSamp = minAccDur*self.record.fs
        count = 0
        nAcc = 0
        #Loop over data samples and count to see if they meet requirements of
        #being considered an accelerationsfor i in range(len(Stage1SigComp)):
        for i in range(len(signal)):
            if signal[i] > (FHRmean+15):
                count=count + 1
            else:
                if (count > minAccSamp):
                    nAcc = nAcc + 1
                count = 0
        return nAcc

    def calcDec(self,signal,FHRmean,minDecDurr):
        """Calculate number of decelerations in an FHR Signal.
        Define each Dec to be 15 bpm < mean of HR Signal for at least
        minDecDurr"""
        #Minimum duration in samples
        minDecSamp = minDecDurr*self.record.fs
        count = 0
        nDec = 0
        #Loop over data samples and count to see if they meet requirements
        #of being considered an accelerationsfor
        #i in range(len(Stage1SigComp)):
        for i in range(len(signal)):
            if signal[i] < (FHRmean-15):
                count=count + 1
            else:
                if (count > minDecSamp):
                    nDec = nDec + 1
                count = 0
        return nDec

    def calcEnergy(self,signal,FHRmean,VLF,LF,HF):
        """Calculate energy of frequency bands of an FHR signal
        Inputs:

        signal: FHR Signal
        VLF: Upper boundry of what to consider very low frequency
        LF: Upper boundary of what to consider low frequency
        HF: Upper boundary of what to consider high frequency
        """
        fs = self.record.fs #sampling frequency
        n = len(signal) #length of signal (number of datapoints)
        ts = 1/fs #sampling period
        t = np.arange(n) #time vector
        k = np.arange(n)
        T = n/fs #Transformation Constant
        frq = k/T # two sides frequency range
        frq = frq[range(int(n/2))] # one side frequency range
        Y = np.fft.fft(signal-FHRmean)/n # fft computing and normalization
        Y = abs(Y[range(int(n/2))]) #Unique Magnitude response
        P = np.power(Y,Y) #power

        VLFindex = np.argmax(frq>=VLF) #Vector index for VLF boundary
        EnVLF = np.sum(P[0:VLFindex]) #VLF Energy

        LFindex = np.argmax(frq>=LF) #Vector index for LF boundary
        EnLF = np.sum(P[VLFindex:LFindex]) #LF Energy

        #HFindex = len(frq)
        HFindex = np.argmax(frq>=HF) #Vector index for HF boundary
        EnHF = np.sum(P[LFindex:HFindex]) #HF Energy

        #fig, ax = plt.subplots(2, 1)
        #ax[0].plot(t,Stage1SigComp)
        #ax[0].set_xlabel('Time')
        #ax[0].set_ylabel('Amplitude')
        #ax[1].plot(frq[1:],P[1:],'r') # plotting the spectrum
        #ax[1].set_xlabel('Freq (Hz)')
        #ax[1].set_ylabel('|Y(freq)|^2')


        return (EnVLF, EnLF, EnHF)
