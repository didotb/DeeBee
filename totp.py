import hmac, struct, hashlib, time, base64

# https://reloc.tk/lKanYR/
def hotp(b64_key:str, interval:int):
	key = base64.b32decode(b64_key, True)
	msg = struct.pack(">Q", interval)
	h = hmac.new(key, msg, hashlib.sha1).digest()
	o = o = h[19] & 15
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
	return h

def totp(b64_key):
	t = str(hotp(b64_key, interval=int(time.time())//30))
	while len(t)!=6:
		t+='0'
	return t