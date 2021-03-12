'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import smbus			#import SMBus module of I2C
from time import sleep, perf_counter
import matplotlib.pyplot as plt
import math

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

class ValueSmoother:
	def __init__(self, size):
		self.values = []
		self.smoother_size = size
		self.avg = 0
		self.currentIndex = 0
		for i in range (0, self.smoother_size):
			# initialize to all zeros
			self.values.append(0) 
	

	def AddValue(self, newvalue):
		self.values[self.currentIndex] = newvalue
		self.currentIndex = (self.currentIndex + 1) % self.smoother_size
		self.avg = sum(self.values) / float(self.smoother_size)

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

# Define constants
THRESHOLD = 100  # not actually used yet
MOV_AVG_SIZE = 10 # number of elements to include in the moving average

# Define variables
magVals = []
smoothVals = []
timeVals = []
startTime = perf_counter()
smoother = ValueSmoother(MOV_AVG_SIZE)


print (" Reading Data of Gyroscope and Accelerometer")
sleep(5)
print ("starting...")
try:
	while True:
		
		#Read Accelerometer raw value
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)

		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16384.0
		Ay = acc_y/16384.0
		Az = acc_z/16384.0

		mag = math.sqrt(Ax**2 + Ay**2 + Az**2)
		magVals.append(mag)

		smoother.AddValue(mag)
		smoothVals.append(smoother.avg)
		
		timeVals.append(perf_counter() - startTime)

		
		# #Read Gyroscope raw value
		# gyro_x = read_raw_data(GYRO_XOUT_H)
		# gyro_y = read_raw_data(GYRO_YOUT_H)
		# gyro_z = read_raw_data(GYRO_ZOUT_H)
		
		# Gx = gyro_x/131.0
		# Gy = gyro_y/131.0
		# Gz = gyro_z/131.0
		

		#print ("\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
		#if (perf_counter() - startTime) > 5:
		#	break

except KeyboardInterrupt:
	print("Exiting...")	

plt.plot(timeVals, magVals, label = "Raw Data")
plt.plot(timeVals, smoothVals, label = "Smoothed Data")
plt.title('Acceleration Magnitude')
plt.show()

