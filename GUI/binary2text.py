import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Tkagg')
import itertools
import matplotlib.gridspec as gridspec
from pylab import *
import matplotlib.animation as animation
import json
"""
Class for getting data from a binary file and save it in a
text file to feed a script or kst for plotting the data
for each channel
The code assumes the following data structure:

startCode | window number| payload | endCode
"""
class binary2text():

    def __init__(self,file, plot=False):
        self.file = file
        self.int_array = np.fromfile(self.file, dtype = np.uint16) # asumes 16-bit data and create an integers array
        self.windowSize = 1030
        self.Vped = 1427

    def savetxt(self):        
        self.windowsNumbers = [self.int_array[x] for x in range(1,len(self.int_array), int(self.windowSize/2)) ] # create a list with the window numbers, byte 1 from each window
        print('windowsNumbers',self.windowsNumbers) 
        self.numberofWindows = len(self.windowsNumbers)
#        print(self.numberofWindows)
        payload = [self.int_array[x:x + 512] for x in range( 2,len(self.int_array), int(self.windowSize/2) ) ] # get the data from each window asumming a self.windowSize, payload[window][data]
    
        windows_and_channels = [ [ payload[self.numberofWindows- i-1][ x:x + 32] for x in range(0,len(payload[i]),32) ] for i in range(self.numberofWindows)] # create a nested list from the payload, windows_and_channels[window][channel][sample]
        self.data_by_channel = list()
        for i in range(len(windows_and_channels[0])): 
            self.data_by_channel.append( self.same_channel(i,self.numberofWindows,windows_and_channels).tolist() ) 
      #  out_file_name ='/home/idlab-52/data/'+'%s.txt'%(self.file.split('.')[0])
      # np.savetxt(out_file_name,np.array(self.data_by_channel).T-self.Vped, fmt='%s')
        
      #  with open(out_file_name, 'a') as out_file: 
            #for item in self.windowsNumbers:
      #       out_file.write(' '.join(str(item) for item in self.windowsNumbers))              
        #wn = np.asarray(self.windowsNumbers) 
        #np.savetxt(out_file,list(zip(wn)), delimiter= ' ', newline= os.linesep, fmt='%18g')
        #wn2 = [str(i) for i in self.windowsNumbers]
        
        #out_file.write('\n'.join(wn) )
        #out_file.close()
        #np.savetxt(out_file, windowsNumbers)
     #   print('file : ','%s'%(out_file_name), 'saved' )
        if plot == True:
        
            plt.suptitle('%s'%file)
            nPlots = 16
            gs = gridspec.GridSpec(nPlots,1)
            gs.update(hspace=0.1)
            plt.title('Windows')
            for i in range(0,nPlots,1):
                plt.subplot(nPlots,1,(i+1))
                ax = plt.subplot(gs[i,0])
                ax.clear()
                ax.plot(self.same_channel(i,self.numberofWindows,windows_and_channels))
                ax.set_ylabel('%s'%i, rotation = 0, color='red')
                plt.xlim([0,480])
                for j in range(16):
                    ax.axvline(j*32,color='k')
        plt.show()   
        return np.array(self.data_by_channel).T-self.Vped
    def same_channel(self, channel, numberWindows,list_to_flat):
        """
         Get the same channel from different windows
        """
        sameChannel=np.array([])
        for i in range(numberWindows):
            sameChannel = np.concatenate((sameChannel,list_to_flat[i][channel] ),axis = None  )
        return sameChannel

#binary2text('15_windows.bin')

