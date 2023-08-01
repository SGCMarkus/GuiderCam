from astropy import units as u
import sys, glob
import cv2
import serial

class Configuration:
	# Observer Position
	latitude = 47.06713 * u.deg
	longitude = 15.49343 * u.deg
	elevation = 493 * u.m
	
	# Angle for night determination
	night_angle = -6 * u.deg
	
	# Camera Resolution
	resolutionX = 720
	resolutionY = 480

	# Recording Settings
	day_averaging_frames = 100
	night_averaging_frames = 1
	default_storage_path = 'D:/Frames'
	day_time_between_frames = 20 # seconds
	night_time_between_frames = 0#1#0 # seconds
	frame_count = -1 # <= 0 means infinite
	show_recorded_frames = True
	store_in_subdirectory = True
	
	# Settings for dynamic night frame averaging
	dnfa_enabled = True
	dnfa_window_size = 150
	dnfa_min_med_diff_factor = 0.2
	dnfa_min_diff_value = 0.3
	dnfa_min_frames = 50
	dnfa_max_frames = 200
	
	# Camera Settings
	control_settings = True
	
	#serial_port = 'COM7'
	defaultSerialPort = "COM7"
	#serial_port = 10
	time_between_commands = 1.5 # seconds
	verbose_commands = True
	
	# these settings should be set and are the same for day and night: "BLC0", "FLC0", "PRAG", "CMDA", "GATB", "ENMI"
	day_settings = ["SSH0", "SSX0", "SAES", "AGC0"]
	night_settings = ["SSH1", "SSX7", "SALC", "ALC0", "AGC1"]
	# shooting star settings?
	#night_settings = ["SSH1", "SSX4", "SALC", "ALC0", "AGC1"]

	def getCameraPorts():
		"""
		Test the ports and returns a tuple with the available ports and the ones that are working.
		"""
		non_working_ports = []
		dev_port = 0
		working_ports = []
		available_ports = []
		while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
			camera = cv2.VideoCapture(dev_port)
			if not camera.isOpened():
				non_working_ports.append(dev_port)
				print("Port %s is not working." %dev_port)
			else:
				is_reading, img = camera.read()
				w = camera.get(3)
				h = camera.get(4)
				if is_reading:
					print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
					working_ports.append(dev_port)
				else:
					print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
					available_ports.append(dev_port)
			dev_port +=1
		return available_ports,working_ports,non_working_ports

	def getSerialPorts():
		""" Lists serial port names

			:raises EnvironmentError:
				On unsupported or unknown platforms
			:returns:
				A list of the serial ports available on the system
		"""
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result

# here is the configuration for my development machine which runs linux, not windows
if sys.platform == 'linux':
	# Recording Settings
	Configuration.default_storage_path = '.'
	Configuration.averaging_frames = 1
	
	# Camera Settings
	Configuration.control_settings = False
	Configuration.serial_port = '/dev/ttyS4'
	Configuration.log_file = './log.txt'
