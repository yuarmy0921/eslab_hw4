from bluepy.btle import Peripheral, UUID                                     
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):            
        def __init__(self):                                                  
                DefaultDelegate.__init__(self)  
                self.index = 0
                self.l = ['x', 'y', 'z']
        def handleDiscovery(self, dev, isNewDev, isNewData):                 
                if isNewDev:                                                 
                        print ("Discovered device", dev.addr)                
                elif isNewData:                                              
                        print ("Received new data from", dev.addr)     
        def handleNotification(self, cHandle, data):
            #super().handleNotification()
            if cHandle == 13:
                print("heart rate:", ord(data.decode()[-1]))
            else:
                '''
                print(data)
                first = data[1:2]
                #print(type(first))
                second = data[2:]
                new_byte_string = second + first
                print(first, second, new_byte_string)
                num = int.from_bytes(new_byte_string, 'big', signed=True)
                
                print(f"magnetic flux {self.l[self.index]}: {num}")
                  
                self.index += 1
                if self.index == 3:
                    self.index = 0
                '''
                flag = data[0:1]
                #print('x: ', data[1:3])
                x = data[1:3]
                y = data[3:5]
                z = data[5:]
                x = int.from_bytes(x, 'little', signed=True)
                y = int.from_bytes(y, 'little', signed=True)
                z = int.from_bytes(z, 'little', signed=True)
                print(f"magnetic flux (x, y, z): ({x}, {y}, {z})")


                
scanner = Scanner().withDelegate(ScanDelegate())                             
devices = scanner.scan(10.0)
#device.setDelegate(ScanDelegate)
n=0                                                                          
addr = []                                                                    
for dev in devices:                                                          
        print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
        addr.append(dev.addr)                                                
        n += 1                                                               
        for (adtype, desc, value) in dev.getScanData():                      
                print (" %s = %s" % (desc, value))                           
number = input('Enter your device number: ')                                 
print ('Device', number)                                                     
num = int(number)                                                            
print (addr[num])                                                            
#                                                                            
print ("Connecting...")
while True:
    try:
        dev = Peripheral(addr[num], 'random')
        break
    except:
        pass
dev.setDelegate(ScanDelegate())
#for ch in testService.getCharacteristics():
#                                                                            
print ("Services...")                                                        
for svc in dev.services:                                                     
    print (str(svc))

#                                                                            
#try:

#testService = dev.getServiceByUUID(UUID(0xfff0))
#for ch in testService.getCharacteristics():
#    print (str(ch))
                                                       
#ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0]
'''
handle = ch.getHandle() + 2
res = dev.writeCharacteristic(handle, b'\x02\x00', withResponse=True)
print('res: ', res)
#print(ch.read())
#ch.write(b'\x02')

while True:
    if dev.waitForNotifications(10.0):
        print('yay')
        break
'''
descriptors = dev.getDescriptors()
print(descriptors)


for i in descriptors:
    print('UUID: ', i.uuid)
    if i.uuid == UUID(0x2902):
        try:
            i.write(b'\x01\x00', withResponse=True)
            #print(res)
            value = i.read()
            print('value: ', value)
        
        except:
            print("except")

while True:
    if dev.waitForNotifications(10.0):
        continue
        
dev.disconnect()
