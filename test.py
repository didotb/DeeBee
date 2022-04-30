import os

d = "./weather/img"
f = [os.path.join(d,files) for files in os.listdir(d)]

c=0
for i in f:
	os.rename(i, str(os.path.join(d,"0"+str(c)+".jpg")))
	c+=1

print(os.listdir(d))