#
#/bin/python3

import struct
import smbus
import time


bus = smbus.SMBus(1)
address = 0x68


I2C_SLV0_ADDR  =  37
I2C_SLV0_REG = 38
I2C_SLV0_CTRL= 39

I2C_SLV0_RW=1   # write = 1 read = 0
I2C_SLV0_ADDR= 0x0d
I2C_SLV0_REG=0x06
I2C_SLV0_EN=True
I2C_SLV0_BYTE_SW=False
I2C_SLV0_REG_DIS = True  

'''   # When I2C_SLV0_REG_DIS is set to 1, the transaction will read or write data only. When cleared to 0, the transaction will write a register address prior to reading or writing data. This bit should equal 0 when specifying the register address within the Slave device to/from which the ensuing data transaction will take place.
'''

I2C_SLV0_LEN=1




def temperature():
        temp_H = bus.read_byte_data(address, 0x41)
        temp_L = bus.read_byte_data(address, 0x42)
        myfunc =  (struct.unpack('l',struct.pack('P',(temp_H << 8 | temp_L)))[0])/340 
        # print(bin(temp_H ))
        # print((temp_L))
        # print(bin((temp_H << 8 | temp_L)))
        return myfunc

def bearing256():
        bear = bus.read_byte_data(address, 0x44)
        return bear

# def readExt():
    # return bus.read_byte_data()

def setup():
    continous = bus.write_byte_data(address, 0x19,0x00) # smp div
    continous = bus.write_byte_data(address, 0x1b, 0x00) #config
    continous = bus.write_byte_data(address, 0x6b, 0x01) #pwr
    print(bin( bus.read_byte_data(address, 0x24))) #pwr

    bus.write_byte_data(address, I2C_SLV0_ADDR , I2C_SLV0_RW << 7 | I2C_SLV0_ADDR)

    continous = bus.write_byte_data(address, 0x6A, 0b01100000) #set master
    continous = bus.write_byte_data(address, 0x23, 0b11111111) #set master
    # continous = bus.write_byte_data(address, 0x24, 0b00011101) #set master
    continous = bus.write_byte_data(address, 0x25, 0b10001101) #set sl0 read
    continous = bus.write_byte_data(address, 0x26, 0x06) #set sl0 iregister address
    continous = bus.write_byte_data(address, 0x27, 0b10010001) #set sl0 read
    continous = bus.read_byte_data(address, 0x27) #pwr



setup()
while True:
        bear256 = bearing256()      #this returns the value as a byte between 0 and 255. 
        print('temp')
        print temperature()
        print(bus.read_byte_data(address, 0x63)) #pwr
        print(bus.read_byte_data(address, 0x38)) #pwr
        print(bus.read_byte_data(address, 0x27)) #pwr
        # for i in range(255):
        #
        #     print('val ' + str(i))
        #     print(bus.read_byte_data(address, i)) #pwr

        # print(read_ext())
        # print('gyro')
        # print bear256
        time.sleep(1)
