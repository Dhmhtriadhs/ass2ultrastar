#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2017 Dimitris Dimitriadis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os, shutil, math

class ass2ultrastar:
	def __init__(self):
		# Αντιστοιχίες συχνότητας σε νότας
		ρίζα = pow(2,1/12.0)
		δυνάμεις = [1.0, ρίζα]
		νότες = {}
		for ι in range(11):
			δυνάμεις.append(δυνάμεις[-1]*ρίζα)

		# 65-130Hz
		μετρητής = -12
		for i in δυνάμεις:
			νότες[130*i/2.0]= μετρητής
			μετρητής += 1
		# 130-260Hz
		μετρητής = 0
		for i in δυνάμεις:
			νότες[130*i]= μετρητής
			μετρητής += 1
		# 260-520Hz
		counter = 12
		for i in δυνάμεις:
			νότες[130*i*2]= μετρητής
			μετρητής += 1
		self.νότες = νότες
		self.συχνότητες = list(νότες.keys())
		self.συχνότητες.sort()
		
	def parseASS(self, assFilename, επικεφαλίδα):
		# εισαγωγή: χρόνος, γραμμές, συλλαβές
		# έξοδος: [[χρόνος, συλλαβές] σειρά]
		def χρόνοςΣεΔευτερόλεπτα(κείμενο):
			# Μετατροπή χρόνου ωω:λλ:δδ.εε σε δευτερόλεπτα δδ.εε
			τμήματα = κείμενο.split(":")
			δευτερόλεπτα = 0.0
			δευτερόλεπτα = float(τμήματα[2])
			δευτερόλεπτα += int(τμήματα[1])*60
			δευτερόλεπτα += int(τμήματα[0])*60*60
			return δευτερόλεπτα
			
		if "-" in assFilename:
			showName = os.path.split(assFilename)
			parts = showName[1].split(".")[0].split("-")
			
			artist = parts[0]
			song = "-".join(parts[1:])
			επικεφαλίδα["ARTIST"] = artist.strip()
			επικεφαλίδα["TITLE"] = song.strip()
		f = open(assFilename)
		γραμμές = f.read().split("\n")
		f.close()
			
		επικεφαλίδα["GAP"] = None
		χρονοσειρά_συλλαβών = {"P1":[],"P2":[],"P3":[],} # txtdata
		ιδιότητες = {}
		effect = None
		currentVoice = "P1"
		for γραμμή in γραμμές:
			νέα_γραμμή = []
			if γραμμή and γραμμή[0] == ";":
				if "COVER:" in γραμμή[0]:
					επικεφαλίδα["COVER"] = γραμμή.split(":")[1].strip()
				elif "BACKGROUND:" in γραμμή:
					επικεφαλίδα["BACKGROUND"] = γραμμή.split(":")[1].strip()
				elif "MP3:" in γραμμή:
					επικεφαλίδα["MP3"] = γραμμή.split(":")[1].strip()
				elif "GENRE:" in γραμμή:
					επικεφαλίδα["GENRE"] = γραμμή.split(":")[1].strip()
				elif "LANGUAGE:" in γραμμή:
					επικεφαλίδα["LANGUAGE"] = γραμμή.split(":")[1].strip()
				elif "BPM:" in γραμμή:
					επικεφαλίδα["BPM"] = γραμμή.split(":")[1].strip()
			elif "Audio File: " == γραμμή[:12]:
				επικεφαλίδα["MP3"] = γραμμή[12:].split("/")[-1]
			elif "Video File: " == γραμμή[:12]:
				επικεφαλίδα["VIDEO"] = γραμμή[12:].split("/")[-1]
			elif "Format: " == γραμμή[:8] and "Text" in γραμμή:
				μετρητής = 0
				for ιδιότητα in γραμμή[8:].split(", "):
					ιδιότητες[μετρητής] = ιδιότητα
					μετρητής += 1
			elif "Dialogue: " == γραμμή[:10]:
				τμήματα = γραμμή[10:].split(",")
				if len(τμήματα)>len(ιδιότητες)-1:
					κείμενο = ",".join(τμήματα[len(ιδιότητες)-1:])
				else:
					κείμενο = τμήματα[len(ιδιότητες)-1]
				αρχή, τέλος = 0.0, 0.0
				for θέση in range(len(ιδιότητες)):
					if ιδιότητες[θέση]=="Start":
						αρχή = χρόνοςΣεΔευτερόλεπτα(τμήματα[θέση])
						if not επικεφαλίδα["GAP"]:
							επικεφαλίδα["GAP"] = int(αρχή*1000)
					elif ιδιότητες[θέση]=="End":
						τέλος = χρόνοςΣεΔευτερόλεπτα(τμήματα[θέση])
					elif ιδιότητες[θέση]=="Name":
						currentVoice = "P1"
						if τμήματα[θέση]=="P2":
							currentVoice = "P2"
						elif τμήματα[θέση]=="P3":
							currentVoice = "P3"
					elif ιδιότητες[θέση]=="Effect":
						effect = τμήματα[θέση]
					elif ιδιότητες[θέση]=="Text":
						if "{\k" in κείμενο:
							# προσθήκη κειμένου με συλλαβές καραόκε
							καραόκε = κείμενο.split("{\k")
							απόκλιση = αρχή
							for καρ in καραόκε:
								if καρ:
									υποτμήματα = καρ.split("}")
									διάρκεια = int(υποτμήματα[0])/100.0
									συλλαβή = υποτμήματα[1]
									νέα_γραμμή.append([απόκλιση, διάρκεια, συλλαβή, effect])
									απόκλιση += διάρκεια
						else:
							# προσθήκη κειμένου χωρίς καραόκε
							νέα_γραμμή.append([αρχή, τέλος-αρχή, κείμενο, effect])
						effect = None
			if νέα_γραμμή:
				χρονοσειρά_συλλαβών[currentVoice].append(νέα_γραμμή)
		return χρονοσειρά_συλλαβών
		
	def freq2note(self, συχνότητα):
		ελάχιστη_συχνότητα_νότας = 0
		ελάχιστο = 100000
		if 60 < συχνότητα and συχνότητα < 530:
			for συχνότητα_νότας in self.συχνότητες:
				if abs(συχνότητα_νότας-συχνότητα)<ελάχιστο:
					ελάχιστο = abs(συχνότητα_νότας-συχνότητα)
					ελάχιστη_συχνότητα_νότας = συχνότητα_νότας
			νέα_νότα = self.νότες[ελάχιστη_συχνότητα_νότας]
		else:
			νέα_νότα = None
		
		return νέα_νότα
		
	def stitch(self, γραμμές, νότες, bpm):
		# txts [start,duration, note]
		# pitches [start, note]
		νέες_γραμμές = {"P1":[],"P2":[],"P3":[],}
		κενό = {"P1":None,"P2":None,"P3":None,}
		for voice in ["P1","P2","P3"]:
			for γραμμή in γραμμές[voice]:
				νέα_γραμμή = []
				τέλος = 0
				for συλλαβές in γραμμή:
					αρχή, διάρκεια, συλλαβή, effect = συλλαβές
					if not κενό[voice]:
						κενό[voice] = αρχή
					τέλος = αρχή+διάρκεια
					#print(αρχή,round(αρχή*bpm),νότες[voice][int(round(αρχή*bpm))])
					#print(τέλος,round(τέλος*bpm),νότες[voice][int(round(τέλος*bpm))])
					# εύρεση νότας κατά την διάρκεια της συλλαβής
					χρόνοι_νότες = []
					end = int(round(τέλος*bpm))
					if end>len(νότες[voice]):
						print("ERROR LENGTH",end,len(νότες[voice]))
						end = len(νότες[voice])
					for θέση in range(int(round(αρχή*bpm)), end):
						χρόνοι_νότες.append(νότες[voice][θέση])
					if not χρόνοι_νότες:
						continue
						
					# έλεγχος για None
					μέση_νότα = 0.0
					μετρητής = 0.0
					έχει_τίποτα= False
					for χρόνο_νότα in χρόνοι_νότες:
						χρόνος_νότας, νότα = χρόνο_νότα
						if νότα!=None:
							μέση_νότα += νότα
							μετρητής += 1
						else:
							έχει_τίποτα = True
					
					if έχει_τίποτα:
						for ν in range(len(χρόνοι_νότες)):
							if χρόνοι_νότες[ν][1]==None:
								if μετρητής:
									μέση_νότα = int(round(μέση_νότα/μετρητής))
									χρόνοι_νότες[ν][1] = μέση_νότα
								else:
									print(χρόνοι_νότες)
							
					# δημιουργία μπιτ
					norm_pitch=[]
					προηγούμενη_νότα = χρόνοι_νότες[0][1]
					μπιτ = 1/bpm
					for χρόνος, νότα in χρόνοι_νότες[1:]:
						if νότα==προηγούμενη_νότα:
							μπιτ += 1/bpm
						else:
							if bpm*μπιτ/15<1:
								μπιτ += 1/bpm
								προηγούμενη_νότα = int(round((νότα+προηγούμενη_νότα)/2.0))
							else:
								norm_pitch.append([μπιτ, προηγούμενη_νότα])
								προηγούμενη_νότα = νότα
								μπιτ = 1/bpm
					
					if bpm*μπιτ/15>1:
						norm_pitch.append([μπιτ, προηγούμενη_νότα])
					
					νέα_γραμμή.append([αρχή, συλλαβή, norm_pitch, effect])
					
				νέα_γραμμή.append(τέλος)
				νέες_γραμμές[voice].append(νέα_γραμμή)
		ελάχιστο_κενό = κενό["P1"]
		if κενό["P2"] and ελάχιστο_κενό>κενό["P2"]:
			ελάχιστο_κενό = κενό["P2"]
		if κενό["P3"] and ελάχιστο_κενό>κενό["P3"]:
			ελάχιστο_κενό = κενό["P3"]
		for voice in ["P1","P2","P3"]:
			for x in range(len(νέες_γραμμές[voice])):
				for y in range(len(νέες_γραμμές[voice][x])):
					if νέες_γραμμές[voice][x][y].__class__==float:
						νέες_γραμμές[voice][x][y]-= ελάχιστο_κενό
					else:
						νέες_γραμμές[voice][x][y][0]-= ελάχιστο_κενό
			
		return νέες_γραμμές
		
	def makeUltrastar(self, bpm, new_text):
		ultratxt = {"P1":[],"P2":[],"P3":[]}
		for voice in ["P1","P2","P3"]:
			for line in new_text[voice]:
				for syllabe in line:
					if syllabe.__class__==int:
						continue
					if syllabe.__class__==float:
						s = int(round(syllabe*bpm/15.0))
						ultratxt[voice].append([s])
						continue
					
					start = int(round(syllabe[0]*bpm/15.0))
					txt = syllabe[1]
					notNone = None
					for p in range(len(syllabe[2])):
						if syllabe[2][p][1]!=None:
							notNone = syllabe[2][p][1]
					
					if len(syllabe[2])==0:
						continue
					duration = int(round(syllabe[2][0][0]*bpm/15.0))
					if syllabe[2][0][1]!=None:
						note = int(syllabe[2][0][1])
					else:
						note = notNone
					ultratxt[voice].append([start, duration, note, txt, syllabe[3]])
					newstart = start+duration
					for p in syllabe[2][1:]:
						duration = int(round(p[0]*bpm/15.0))
						if p[1]!=None:
							note = p[1]
						else:
							note = notNone
						ultratxt[voice].append([newstart, duration, note, "", syllabe[3]])
						newstart += duration
				
		return ultratxt
		
	def cleanUltra(self, ultratxt):
		for voice in ["P1","P2","P3"]:
			prev_note = None
			i=0
			while i<len(ultratxt[voice])-1:
				next_start = ultratxt[voice][i+1][0]
				start = ultratxt[voice][i][0]
				if len(ultratxt[voice][i])>1:
					dur = ultratxt[voice][i][1]
					if next_start-start<dur:
						ultratxt[voice][i][1] = next_start-start
				if len(ultratxt[voice][i])>1 and ultratxt[voice][i][1]<=0:
					print("remove :",ultratxt[voice][i])
					ultratxt[voice].remove(ultratxt[voice][i])
					i-=1
					
				i+=1
	
	def mergeUltra(self, ultratxt):
		for voice in ["P1","P2","P3"]:
			prev_note = None
			i=0
			while i<len(ultratxt[voice])-1:
				next_start = ultratxt[voice][i+1][0]
				start = ultratxt[voice][i][0]
				if len(ultratxt[voice][i])>1 and len(ultratxt[voice][i+1])>1:
					if ultratxt[voice][i][2]==ultratxt[voice][i+1][2] and ultratxt[voice][i+1][3]=="":
						ultratxt[voice][i][1] += ultratxt[voice][i+1][1]
						del ultratxt[voice][i+1]
						i-=1
					
				i+=1
					
	def compress(self, ultratxt):
		sz = len(ultratxt)
		for i in range(sz):
			if len(ultratxt[i])>1:
				if ultratxt[i][2] < 0:
					ultratxt[i][2] += 12
				ultratxt[i][2] += 6
				ultratxt[i][2] = ultratxt[i][2] % 12
	
	def fix_octaves(self, ultratxt):
		for voice in ["P1","P2","P3"]:
			prev_note = None
			i=1
			while i<len(ultratxt[voice])-2:
				if len(ultratxt[voice][i+1])<2 or len(ultratxt[voice][i])<2 or len(ultratxt[voice][i-1])<2:
					#print("ERROR",ultratxt[voice][i+1])
					#del ultratxt[voice][i+1]
					i+=1
					continue
				next_note = ultratxt[voice][i+1][1]
				prev_note = ultratxt[voice][i-1][1]
				current_note = ultratxt[voice][i][1]
				if current_note+12==next_note or current_note+12==prev_note:
					ultratxt[voice][i][1] += 12
				elif current_note-12==next_note or current_note-12==prev_note:
					ultratxt[voice][i][1] -= 12
				i+=1
				
	def writeUltrastar(self, header, ultratxt, assFile):
		d, f = os.path.split(assFile)
		ultra = header["ARTIST"] +" - "+header["TITLE"]
		newFolder = d
		if not newFolder.endswith(ultra):
			newFolder = os.path.join(newFolder, ultra)
		newUltra = os.path.join(newFolder, ultra+".txt")
		f = open(newUltra,'w')
		for k,v in header.items():
			if k=="BPM":
				BPM = "%2.2f" % v
				BPM = BPM.replace(".",',')
				f.write("#"+k+":"+BPM+"\n")
			elif k=="GAP" or k=="VIDEOGAP":
				f.write("#"+k+":"+str(v)+"\n")
			elif k in ["COVER", "BACKGROUND", "MP3", "VIDEO"]:
				name = os.path.split(v)[1]
				f.write("#"+k+":"+name+"\n")
			else:
				f.write("#"+k+":"+v+"\n")
		for voice in ["P1","P2","P3"]:
			if voice=="P1" and (len(ultratxt["P2"])>0 or len(ultratxt["P3"])>0):
				f.write("P1:\n")
			elif voice=="P2":
				if len(ultratxt["P2"])>0:
					f.write("P2:\n")
				else:
					continue
			elif voice=="P3":
				if len(ultratxt["P3"])>0:
					f.write("P3:\n")
				else:
					continue
			for u in ultratxt[voice]:
				if len(u)==1:
					f.write("- "+str(u[0])+"\n")
				else:
					type = ":"
					if u[4]:
						if u[4]=="F":
							type = "F"
						elif u[4]=="G":
							type = "*"
					f.write(type+" "+str(u[0])+" "+str(u[1])+" "+str(u[2])+" "+u[3]+"\n")
		f.write("E")
		f.close()
		
	def parsePraat(self, χρονοσειρά):
		χτδ = 0.0
		gap = 0.0
		μετρητής1 = 0
		μέγεθος = len(χρονοσειρά)
		χρόνος_νότες = {"P1":[],"P2":[],"P3":[],}
		while μετρητής< len(χρονοσειρά):
			γραμμή = χρονοσειρά[μετρητής1]
			if "dx"==γραμμή[:2]:
				χτδ = float(γραμμή.split("=")[1])
			if "x1"==γραμμή[:2]:
				gap = float(γραμμή.split("=")[1])
			if "frame [" in γραμμή:
				αριθμός = γραμμή.split("frame [")[1].split("]")[0]
				if len(αριθμός)>0:
					αριθμός = int(αριθμός)
					while "candidate [1]" not in γραμμή:
						μετρητής1 += 1
						γραμμή = χρονοσειρά[μετρητής1]
					μετρητής += 1
					γραμμή = χρονοσειρά[μετρητής1]
					if "frequency" in γραμμή:
						συχνότητα = float(γραμμή.split("=")[1])
						χρόνος_νότες["P1"].append([gap+αριθμός*χτδ, self.freq2note(συχνότητα)])
					
			μετρητής += 1
		
		bpm = 0
		if χτδ!=0:
			bpm = 1/χτδ
		return bpm, χρόνος_νότες
	
	def parseAubiopitch(self, χρονοσειρά):
		# εισαγωγή: χρονοσειράς συχνοτήτων
		# εξαγωγή: χρονοσειρά νότας
		προηγούμενος_χρόνος = 0.0
		χτδ = 0.0
		
		χρόνος_νότες = []
		for χρονός_συχνότητα in χρονοσειρά:
			if not χρονός_συχνότητα:
				continue
			χρόνος, συχνότητα = χρονός_συχνότητα.split(" ")
			χρόνος, συχνότητα = float(χρόνος), float(συχνότητα)
			χτδ = χρόνος-προηγούμενος_χρόνος
			προηγούμενος_χρόνος = χρόνος
			
			ελάχιστη_συχνότητα_νότας = 0
			ελάχιστο = 100000
			if 60 < συχνότητα and συχνότητα < 530:
				for συχνότητα_νότας in self.συχνότητες:
					if abs(συχνότητα_νότας-συχνότητα)<ελάχιστο:
						ελάχιστο = abs(συχνότητα_νότας-συχνότητα)
						ελάχιστη_συχνότητα_νότας = συχνότητα_νότας
				νέα_νότα = self.νότες[ελάχιστη_συχνότητα_νότας]
			else:
				νέα_νότα = None
			χρόνος_νότες.append([χρόνος, νέα_νότα])
		έξοδος = {"P1":χρόνος_νότες.copy(),"P2":χρόνος_νότες.copy(),"P3":χρόνος_νότες.copy()}
		
		return 1/χτδ, έξοδος
		
	def parseU2A(self, χρονοσειρά):
		χρόνος_νότες = {"P1":[],"P2":[],"P3":[]}
		voice = "P1"
		pitch = None
		προηγούμενος_χρόνος = None
		for χρονός_νότα in χρονοσειρά:
			if not χρονός_νότα:
				continue
			if "P1" in χρονός_νότα:
				voice = "P1"
				continue
			elif "P2" in χρονός_νότα:
				voice = "P2"
				continue
			elif "P3" in χρονός_νότα:
				voice = "P3"
				continue
			
			χρόνος, νότα = χρονός_νότα.split(" ")
			χρόνος = float(χρόνος)
			if "None" in νότα:
				νότα = None
			else:
				νότα = int(νότα)
				
			if προηγούμενος_χρόνος:
				if not pitch:
					pitch = χρόνος
				elif (χρόνος-προηγούμενος_χρόνος)<pitch:
					pitch = (χρόνος-προηγούμενος_χρόνος)
			else:
				προηγούμενος_χρόνος = χρόνος
			χρόνος_νότες[voice].append([χρόνος, νότα])
		
		bpm = abs(1/pitch)
		return bpm, χρόνος_νότες
		
	def parsePitch(self, pitchFilename, header):
		f = open(pitchFilename)
		pitch = f.read().split("\n")
		f.close()
		
		if ".u2a.pitch" in pitchFilename:
			bpm, pitches = self.parseU2A(pitch)
		elif "aubiopitch" in pitchFilename:
			bpm, pitches = self.parseAubiopitch(pitch)
		else:
			bpm, pitches = self.parsePraat(pitch)
		header["BPM"] = bpm
		return pitches
		
	
	def copyFiles(self, header, assFile):
		d, f = os.path.split(assFile)
		ultra = header["ARTIST"] +" - "+header["TITLE"]
		newFolder = d
		if not d.endswith(ultra):
			newFolder = os.path.join(d, ultra)
			if not os.path.exists(newFolder):
				os.mkdir(newFolder)
		# copy mp3, video, cover, background
		mp3 = os.path.split(header["MP3"])[1]
		if not os.path.exists(os.path.join(newFolder, mp3)):
			print("COPY", header["MP3"], newFolder)
			shutil.copy2(header["MP3"], newFolder)

		if "VIDEO" in header and header["VIDEO"]:
			video = os.path.split(header["VIDEO"])[1]
			if not os.path.exists(os.path.join(newFolder, video)):
				shutil.copy2(header["VIDEO"], newFolder)
		
		if "COVER" in header and header["COVER"]:
			cover = os.path.split(header["COVER"])[1]
			if not os.path.exists(os.path.join(newFolder, cover)):
				shutil.copy2(header["COVER"], newFolder)
		if "BACKGROUND" in header and header["BACKGROUND"]:
			background = os.path.split(header["BACKGROUND"])[1]
			if not os.path.exists(os.path.join(newFolder, background)):
				shutil.copy2(header["BACKGROUND"], newFolder)
		
	def ASS2Ultrastar(self, header, txtdata, pitches, assFile):
		new_txt = self.stitch(txtdata, pitches, header["BPM"])
		ultratxt = self.makeUltrastar( header["BPM"], new_txt)
		self.cleanUltra(ultratxt)
		self.cleanUltra(ultratxt)
		self.fix_octaves(ultratxt)
		self.mergeUltra(ultratxt)
		
		self.copyFiles(header, assFile)
		self.writeUltrastar(header, ultratxt, assFile)
		
if __name__=='__main__':
	a2u=ass2ultrastar()
	header = {"ARTIST":"A","TITLE":"B"}
	assFile = "somefile.ass"
	timeline = a2u.parseASS(assFile	,header)
	pitches = a2u.parsePitch("some.aubiopitch",	header)
	a2u.ASS2Ultrastar(header, timeline,pitches, assFile)
