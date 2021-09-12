import os, hashlib, virustotal3.core as core, virustotal3.errors as errors, time

API_KEY = os.environ['vt_api-key']
avFile = core.Files(API_KEY)

class ScanFile:
	def __init__(self, link:str):
		if not link:
			raise ValueError("Missing argument: <link> - URL or file is missing or invalid.")
		self.link = link
		self.info = None
		buffer = 65536
		sha256 = hashlib.sha256()
		with open(self.link, 'rb') as f:
			while True:
				bin = f.read(buffer)
				if not bin:
					break
				sha256.update(bin)
			self.hash = sha256.hexdigest()

	def FileInfo(self):
		try:
			self.info = avFile.info_file(self.hash)
		except errors.VirusTotalApiError:
			self.info = "File not found"
		return self.info

	def Scan(self):
		self.FileInfo()
		if self.info == "File not found":
			avFile.upload(self.link)
			time.sleep(3)
			self.FileInfo()
		attr = self.info["data"]["attributes"]
		return attr