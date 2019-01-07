import os
for root, dirs , files in os.walk(r'C:\Users\nandpara\PycharmProjects\Network_Access1\tests\suites\network_access\uplift_test'):
	for file in files:
		file_path = os.path.join(root, file)
		OFile = open(file_path, 'r+')
		try :
			for line in list(OFile.readlines()):
				if "UiLib.networkDevices_setDefaultDevice" in line:
					print(file)
					OFile.close()
					break
		except:
			print("Error")
