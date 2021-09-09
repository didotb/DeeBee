import vt, os

av = vt.Client(os.environ['vt_api-key'])

class ScanFile(client=av):
	def FileInfo(self, link:str):
		if link is None:
			return "Missing argument: <link> - Link to file is missing or invalid."
		try:
			file = av.get_object(link)
		except Exception as e:
			return e
		return {'size': file.size, 'hash': file.sha256, 'type': file.type_tag, 'stat': file.last_analysis_stats}

	def Scan(self, link:str):
		if link is None:
			return "Missing argument: <link> - Link to file is missing or invalid."

		fi = self.FileInfo(link)
		if type(fi) != 'dict':
			return f"Error parsing file: {fi}"
		
		#### check changelog.md -> To Do