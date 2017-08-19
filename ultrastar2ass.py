#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2017 Dimitris Dimitriadis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from ffmpy import FFmpeg
from ass2ultrastar import ass2ultrastar

# ultrastar (start,duration, syllabe)
# -> start,end {\k#num}syllabe
# (seconds)*bpm/15.0 = bpms
# bpms*15/bpm = seconds
# -> start,dur, pitch
class ultrastar2ass:
	def readUltrastar(self, γραμμές):
		def decodeUltra(καθυστέρηση, bpm, γραμμή):
			τμήματα = γραμμή.split(" ") # 1-χρόνος 2-διάρκεια -3 νότα -4 συλλαβή
			αρχή = καθυστέρηση/1000.0+int(τμήματα[1])*15.0/bpm # χρόνος
			διάρκεια = int(τμήματα[2])*15.0/bpm
			νότα = int(τμήματα[3])
			συλλαβές = ""
			if len(τμήματα)>3:
				συλλαβές = " ".join(τμήματα[4:])
			return [αρχή, διάρκεια, νότα, συλλαβές]
			
		επικεφαλίδα = {"GAP":0}
		
		νέες_γραμμές = {"P1":[],"P2":[],"P3":[],}
		νέα_γραμμή = []
		voice = "P1"
		for γραμμή in γραμμές:
			if not γραμμή:
				continue
			if γραμμή[0]=="#":
				τμήματα = γραμμή[1:].split(":")
				if "GAP" in γραμμή or "BPM" in γραμμή:
					επικεφαλίδα[τμήματα[0]] = float(τμήματα[1].replace(",",".")) # ακρίβεια δεκαδικού
				else:
					επικεφαλίδα[τμήματα[0]] = τμήματα[1] # είναι κείμενο
			elif γραμμή[0].startswith("P1:"): # γραμμή κειμένο
				voice = "P1"
			elif γραμμή[0].startswith("P2:"): # γραμμή κειμένο
				voice = "P2"
			elif γραμμή[0].startswith("P3:"): # γραμμή κειμένο
				voice = "P3"
			elif γραμμή[0]=="*": # γραμμή κειμένο
				νέα_γραμμή.append(decodeUltra(επικεφαλίδα["GAP"], επικεφαλίδα["BPM"], γραμμή)+["G"])
			elif γραμμή[0]=="F": # γραμμή κειμένο
				νέα_γραμμή.append(decodeUltra(επικεφαλίδα["GAP"], επικεφαλίδα["BPM"], γραμμή)+["F"])
			elif γραμμή[0]==":": # γραμμή κειμένο
				νέα_γραμμή.append(decodeUltra(επικεφαλίδα["GAP"], επικεφαλίδα["BPM"], γραμμή)+[""])
			elif γραμμή[0]=="-": # διαχωριστικό γραμμής
				νέες_γραμμές[voice].append(νέα_γραμμή)
				νέα_γραμμή = []
			elif γραμμή[0]=="E": # το τέλος
				νέες_γραμμές[voice].append(νέα_γραμμή)
				break
			else:
				print("ERROR ultrastar:",γραμμή)
			
		return επικεφαλίδα, νέες_γραμμές
		
	def makeASSHeader(self, header):
		newHeader = "[Script Info]\n"
		if "COVER" in header:
			newHeader += "; COVER:"+header["COVER"]+"\n"
		if "BACKGROUND" in header:
			newHeader += "; BACKGROUND:"+header["BACKGROUND"]+"\n"
		if "VIDEO" in header:
			newHeader += "; VIDEO:"+header["VIDEO"]+"\n"
		if "MP3" in header:
			newHeader += "; MP3:"+header["MP3"]+"\n"
		if "GENRE" in header:
			newHeader += "; GENRE:"+header["GENRE"]+"\n"
		if "EDITION" in header:
			newHeader += "; EDITION:"+header["EDITION"]+"\n"
		if "BPM" in header:
			newHeader += "; BPM:"+str(header["BPM"])+"\n"
		if "LANGUAGE" in header:
			newHeader += "; LANGUAGE:"+header["LANGUAGE"]+"\n"
		newHeader += "Title: "+header["ARTIST"]+" - "+header["TITLE"]+"\n"
		newHeader += "ScriptType: v4.00+\n"
		newHeader += "WrapStyle: 0\n"
		newHeader += "ScaledBorderAndShadow: yes\n"
		newHeader += "YCbCr Matrix: None\n"
		newHeader += "[V4+ Styles]\n"
		newHeader += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n\n"
		newHeader += "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n"
		newHeader += "[Events]\n"
		newHeader += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
		
		return newHeader
		
	def ASSDialogs(self, γραμμές):
		def toTime(secs):
			# δευτερόλεπτα σε ω:λλ:δδ.χχ
			hours = int(secs/(60*60)) % (9*60*60)
			minutes = int(secs/60.0 - hours*60) % 60
			seconds = int(secs - hours*60*60-minutes*60) % 60
			milli = round((secs - hours*60*60-minutes*60-seconds)*1000)/10
			return str(hours)+":"+str("%02d" % minutes)+":"+str("%02d" % seconds)+"."+str("%02d" % milli)
		
		dialogs = ""
		συχνότητες = {"P1":[],"P2":[],"P3":[]}
		for voice in ["P1","P2","P3"]:
			lines = []
			for συλλαβές in γραμμές[voice]:
				acc_dur = 0
				startLine = None
				endLine = None
				syllabes = ""
				prev_syllabe = None
				προηγούμενο_τέλος = None
				τύπος = ""
				for τμήματα in συλλαβές:
					αρχή, διάρκεια, νότα, syllabe, τύπος = τμήματα
					
					if διάρκεια>0:
						συχνότητες[voice].append([αρχή, διάρκεια, νότα])
					
					if not startLine:
						startLine = αρχή
					
					if syllabe:
						if prev_syllabe:
							syllabes += "{\k"+str(int(acc_dur*100))+"}"+prev_syllabe
						if endLine and endLine<αρχή:
							syllabes += "{\k"+str(int((αρχή-endLine)*100))+"}"
						acc_dur = διάρκεια
						prev_syllabe = syllabe
					else:
						acc_dur  += διάρκεια
					endLine = αρχή+διάρκεια
				if prev_syllabe:
					syllabes += "{\k"+str(int(acc_dur*100))+"}"+prev_syllabe
					
				if startLine:
					lines.append([startLine, endLine, syllabes, τύπος, voice])
			
			for line in lines:
				dialogs += "Dialogue: 0,"+toTime(line[0])+","+toTime(line[1])+",Default,"+line[-1]+",0,0,0,"+line[-2]+","+line[2]+"\n"
		return [συχνότητες, dialogs]
		
	def writeASS(self, filename, assHeader, lines):
		filenameASS = filename.split(".")[0]+".ass"
		f = open(filenameASS,'w')
		f.write(assHeader)
		f.write(lines)
		f.close()
		
	def writePitches(self, filename, pitches):
		f = open(filename,'w')
		for voice in ["P1","P2","P3"]:
			f.write(voice+"\n")
			for pitch in pitches[voice]:
				f.write(str(pitch[0])+" "+str(pitch[1])+"\n")
		f.close()
		
	def unfoldPitches(self, pitches):
		new_pitches = {"P1":[],"P2":[],"P3":[]}
		for voice in ["P1","P2","P3"]:
			if not pitches[voice]:
				return new_pitches
						
			tick = pitches[voice][0][1]
			for p in pitches[voice][1:]:
				if p[1]<tick:
					tick = p[1]
			for p in pitches[voice]:
				times = int(round(p[1]/tick))
				start = p[0]
				note = p[2]
				for t in range(times):
					new_pitches[voice].append([start+t*tick, note])
				
		return new_pitches
	
	def aubioPitch(self, filename, header):
		pth = os.path.join("/tmp","a2u")
		if not os.path.exists(pth):
			os.mkdir(pth)
		
		ultrapath= os.path.split(filename)[0]
		mp3file = os.path.join(ultrapath, header["MP3"])
		tmpWAV = os.path.join(pth, header["MP3"].split(".")[0]+".wav")
		ff = FFmpeg(
			inputs={mp3file: None},
			outputs={ tmpWAV: ['-y',"-ac","1" ]})
		ff.run()
		
		tmpPitch = os.path.join(pth,'temp.aubiopitch')
		os.system('aubiopitch "'+tmpWAV+'" > "'+tmpPitch+'"')
		
		f=open(tmpPitch)
		lines = f.read().split("\n")
		f.close()
		
		a2u = ass2ultrastar()
		bpm, pitches = a2u.parseAubiopitch(lines)
		
		return bpm, pitches
		
	def mergePitches(self, aubioPitch, u2aPitch, bpm):
		newPitch = {"P1":aubioPitch.copy(), "P2":aubioPitch.copy(), "P3":aubioPitch.copy() }
		for voice in ["P1","P2","P3"]:
			for start, duration, note in u2aPitch[voice]:
				for position in range(int(round(start*bpm)),int(round((start+duration)*bpm))):
					newPitch[voice][position][1] = note
		return newPitch
		
	def Ultrastar2ASS(self, filename):
		f = open(filename)
		lines = f.read().split("\n")
		f.close()
		
		header, data = self.readUltrastar(lines)
		
		assHeader = self.makeASSHeader(header)
		
		u2aPitches, lines = self.ASSDialogs(data)
		
		bpm, aubioPitches = self.aubioPitch(filename, header)
		pitches = self.mergePitches(aubioPitches, u2aPitches, bpm)
		
		assFilename = filename.split(".")[0]+".ass"
		self.writeASS(assFilename, assHeader, lines)
		
		filenamePitch = filename.split(".")[0]+".u2a.pitch"
		self.writePitches(filenamePitch, pitches)
		
		return header,assFilename,filenamePitch

if __name__=='__main__':
	import os
	u = ultrastar2ass()
	u.Ultrastar2ASS("ultrastar.txt")