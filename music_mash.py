
import wave, struct, os, random, sys
from pydub import AudioSegment

d = {}

#set length of the key
if len(sys.argv) > 2:
	max_output_length = int(sys.argv[2])
else:
	max_output_length = 1000000 #number of frames

if len(sys.argv) > 1:
	if sys.argv[1] in ["-h", "-H", "--help"]:
		print "Usage: ", sys.argv[0], "[n] [number of output frames]"
		sys.exit(0)
	
	n = int(sys.argv[1])
else:
	n = 5

wav_frame_list = []
for files in os.listdir("."):
	if files.endswith(".mp3") and files != "using.mp3":
		print "Using", files
		#lower quality on mp3
		AudioSegment.from_mp3(files).export("using.mp3", format="mp3", parameters=["-ac", "1", "-ar", "11025"])
		AudioSegment.from_mp3("using.mp3").export("test.wav", format="wav", parameters=["-ac", "1", "-ar", "11025"])
		waveFile = wave.open('test.wav', 'r')

		
		length = waveFile.getnframes()

		for i in range(0,length):
			waveData = waveFile.readframes(1)
			data = struct.unpack("<H", waveData)[0]
			wav_frame_list.append(str(data))

		print "Done reading", length, "frames"
		print "Tidying files"
		os.remove("using.mp3")

print "Building dictionary"

for i, frame in enumerate(wav_frame_list):
	key = " ".join(wav_frame_list[i:i+n])
	if i+n+1 > len(wav_frame_list): break

	if i < len(wav_frame_list) - 1:
		if key in d:	
			d[key].append(wav_frame_list[i+n])
		else:
			d[key] = []
			d[key].append(wav_frame_list[i+n])
		d[key] = list(set(d[key]))

#print multi paths
# for key, value in d.items():
# 	if len(value) > 1: print key, value
print len([v for v, k in d.items() if len(v) > 1]), "multipaths found"


print "Performing random walk"
output = []


start_key = random.choice(list(d.keys()))
print "Using start key:", start_key
output.extend(start_key.split())

key = start_key
while len(output) < max_output_length:

	new_byte = random.choice(d[key])
	output.append(new_byte)

	key = " ".join(key.split()[1:]) + " " + new_byte


#check
# for o in output:
# 	try:
# 		x = int(o)
# 	except:
# 		print "*** bad output", o


#======================
#OUTPUT
#======================
#to by pass
# output = wav_frame_list

nchannels, sampwidth, framerate, nframes, comptype, compname = waveFile.getparams()
print "Original wav properties"
print "nchannels", nchannels, "sampwidth",sampwidth, "framerate",framerate, "nframes",nframes, "comptype",comptype, "compname", comptype


noise_output = wave.open('output.wav', 'w')
noise_output.setparams(waveFile.getparams())

for i in range(0, max_output_length):
	value = int(output[i])
	packed_value = struct.pack('<H', value)
	noise_output.writeframes(packed_value)
	# noise_output.writeframes(packed_value)

# value_str = ''.join(values)
# noise_output.writeframes(value_str)

noise_output.close()
print "Done creating new file output.wav"
