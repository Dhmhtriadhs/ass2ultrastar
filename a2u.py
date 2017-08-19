# Copyright 2017 Dimitris Dimitriadis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, subprocess
from ass2ultrastar_gui import Ui_MainWindow
from ass2ultrastar import ass2ultrastar
from ultrastar2ass import ultrastar2ass
from ffmpy import FFmpeg
import sqlite3

class a2u(Ui_MainWindow):
	def __init__(self, dialog):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
		
		self.conn = sqlite3.connect('ultra.db')
		
		self.actionExit.triggered.connect(QtWidgets.qApp.quit)
		self.actionOpenASS.triggered.connect(self.openASSFile)
		self.actionOpenUltrastar.triggered.connect(self.u2a)
		
		self.ass2ultrar = ass2ultrastar()
		self.ultra2ass = ultrastar2ass()
		self.resetGUIData()
		
		self.coverPushButton.clicked.connect(self.openCover)
		self.backgroundPushButton.clicked.connect(self.openBackground)
		self.mp3PushButton.clicked.connect(self.openMP3)
		self.videoPushButton.clicked.connect(self.openVideo)
		self.pitchPushButton.clicked.connect(self.openPitchFile)
		self.u2aPushButton.clicked.connect(self.u2a)
		self.vaPushButton.clicked.connect(self.testva)
		self.ASSFilePushButton.clicked.connect(self.openASSFile)
		self.a2uPushButton.clicked.connect(self.makeUltrastar)
		self.genreComboBox.addItems(["","Alternative","Anime","Blues","Children’s Music","Classical","Comedy","Country","Dance","Easy Listening","Electronic","Pop","Folk","Hip-Hop/Rap","Holiday","Indie Pop","Industrial","Instrumental","J-Pop","Jazz","Latino","New Age","Opera","Pop","R&B/Soul","Reggae","Rock","Soundtrack","Vocal","World",])
		self.languageComboBox.addItems(["",'English','Afrikaans', 'Albanian', 'Amharic', 'Arabic (Egyptian Spoken)', 'Arabic (Levantine)', 'Arabic (Modern Standard)', 'Arabic (Moroccan Spoken)', 'Arabic (Overview)', 'Aramaic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Balochi', 'Bamanankan', 'Bashkort (Bashkir)', 'Basque', 'Belarusan', 'Bengali', 'Bhojpuri', 'Bislama', 'Bosnian', 'Brahui', 'Bulgarian', 'Burmese', 'Cantonese', 'Catalan', 'Cebuano', 'Chechen', 'Cherokee', 'Croatian', 'Czech', 'Dakota', 'Danish', 'Dari', 'Dholuo', 'Dutch', 'Esperanto', 'Estonian', 'Éwé', 'Finnish', 'French', 'Georgian', 'German', 'Gikuyu', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hawaiian Creole', 'Hebrew', 'Hiligaynon', 'Hindi', 'Hungarian', 'Icelandic', 'Igbo', 'Ilocano', 'Indonesian (Bahasa Indonesia)', 'Inuit/Inupiaq', 'Irish Gaelic', 'Italian', 'Japanese', 'Jarai', 'Javanese', 'K’iche’', 'Kabyle', 'Kannada', 'Kashmiri', 'Kazakh', 'Khmer', 'KhoekhoeKorean', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Macedonian', 'Maithili', 'Malagasy', 'Malay (Bahasa Melayu)', 'Malayalam', 'Mandarin (Chinese)', 'Marathi', 'Mende', 'Mongolian', 'Nahuatl', 'Navajo', 'Nepali', 'Norwegian', 'Ojibwa', 'Oriya', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romani', 'Romanian', 'Russian', 'Rwanda', 'Samoan', 'Sanskrit', 'SerbianShona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovene', 'Somali', 'Spanish', 'Swahili', 'Swedish', 'Tachelhit', 'Tagalog', 'Tajiki', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetic languages', 'Tigrigna', 'Tok Pisin', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Warlpiri', 'Welsh', 'Wolof', 'Xhosa', 'Yakut', 'Yiddish', 'Yoruba', 'Yucatec', 'Zapotec', 'Zulu'])

		
	def u2a(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open Ultrastar Song', '.', "*.txt")
		
		if fname[0]:
			self.resetGUIData()
			
			# update files
			self.ultrastarFilename = fname[0]
			self.statusbar.showMessage('Reading Ultrastar file')
			header, assFilename,filenamePitch = self.ultra2ass.Ultrastar2ASS(self.ultrastarFilename)
			self.pitchFilename = filenamePitch
			self.assFilename = assFilename
			showName = os.path.split(self.assFilename)
			self.ASSFilePushButton.setText(showName[1])
			
			# update headers
			pth = os.path.split(self.pitchFilename)[0]
			self.header["COVER"] = os.path.join(pth, header["COVER"])
			self.header["BACKGROUND"] = os.path.join(pth, header["BACKGROUND"])
			self.header["MP3"] = os.path.join(pth, header["MP3"])
			if "VIDEO" in header:
				self.header["VIDEO"] = os.path.join(pth, header["VIDEO"])
			self.gapLineEdit.setText(str(header["GAP"]))
			self.header["GAP"] = header["GAP"]
			self.bpmLineEdit.setText(str(header["BPM"]))
			self.header["BPM"] = header["BPM"]
			self.header["ARTIST"] = header["ARTIST"]
			self.header["TITLE"] = header["TITLE"]
			if "VIDEOGAP" in header and header["VIDEOGAP"]:
				self.header["VIDEOGAP"] = header["VIDEOGAP"]
			
			self.statusbar.showMessage('Updating data')
			self.updateGUIData(self.header)
			
			if not self.searchASS(self.assFilename, header):
				self.insertASS(self.assFilename, header)
				
		self.statusbar.showMessage('')
		
	def resetGUIData(self):
		# reset Files
		self.assFilename = ""
		self.ultrastarFilename = ""
		self.pitchFilename = ""
		
		# reset header
		self.header = {"ARTIST":"","TITLE":"","MP3":"","VIDEO":"", "VIDEOGAP":0,
		"COVER":"", "BACKGROUND":"","GENRE":"", "EDITION":"", "LANGUAGE":"",
		"BPM":0, "GAP":0, "VIDEOGAP":0}
		
		# reset text and pitch lines
		self.txt_syllabes = []
		self.pitches = []
		
		# reset GUI Files
		self.ASSFilePushButton.setText("ASS File")
		self.coverPushButton.setText("Cover File")
		self.backgroundPushButton.setText("Background File")
		self.mp3PushButton.setText("MP3 File")
		self.videoPushButton.setText("Video File")
		self.pitchPushButton.setText("Pitch File")
		
		# reset GUI Values
		self.artistLineEdit.setText("")
		self.titleLineEdit.setText("")
		self.genreComboBox.lineEdit().setText("")
		self.editionLineEdit.setText("")
		self.languageComboBox.setCurrentIndex(-1)
		self.videoGAPdoubleSpinBox.setValue(0)
		self.gapLineEdit.setText("0")
		self.bpmLineEdit.setText("0")
	
	def updateGUIData(self, header):
		# update Files and GUI Files
		if self.assFilename:
			showName = os.path.split(self.assFilename)
			self.ASSFilePushButton.setText(showName[1])
		
		if "COVER" in header and os.path.exists(header["COVER"]):
			cover = os.path.split(header["COVER"])[1]
			self.coverPushButton.setText(cover)
		else:
			header["COVER"] = ""
			self.coverPushButton.setText("")
			
		if "BACKGROUND" in header and os.path.exists(header["BACKGROUND"]):
			back = os.path.split(header["BACKGROUND"])[1]
			self.backgroundPushButton.setText(back)
		else:
			header["BACKGROUND"] = ""
			self.backgroundPushButton.setText("")
		
		if "MP3" in header and os.path.exists(header["MP3"]):
			mp3 = os.path.split(header["MP3"])[1]
			self.mp3PushButton.setText(mp3)
		else:
			header["MP3"] = ""
			self.mp3PushButton.setText("")
		
		if "VIDEO" in header and os.path.exists(header["VIDEO"]):
			video = os.path.split(header["VIDEO"])[1]
			self.videoPushButton.setText(video)
		else:
			header["VIDEO"] = ""
			self.videoPushButton.setText("")
		
		if self.pitchFilename and os.path.exists(self.pitchFilename):
			pitch = os.path.split(self.pitchFilename)[1]
			self.pitchPushButton.setText(pitch)
			self.pitches = self.ass2ultrar.parsePitch(self.pitchFilename, self.header)
			if self.header["BPM"]:
				BPM = "%2.2f" % self.header["BPM"]
				BPM = BPM.replace(".",',')
				self.bpmLineEdit.setText(BPM)
		
		# update Gui values
		self.artistLineEdit.setText(header["ARTIST"])
		self.titleLineEdit.setText(header["TITLE"])
		if "GENRE" in header:
			self.genreComboBox.lineEdit().setText(header["GENRE"])
		if "EDITION" in header:
			self.editionLineEdit.setText(header["EDITION"])
		if "LANGUAGE" in header:
			self.languageComboBox.setCurrentText(header["LANGUAGE"])
		if "VIDEOGAP" in header:
			self.videoGAPdoubleSpinBox.setValue(header["VIDEOGAP"])
		if "GAP" in header:
			self.gapLineEdit.setText(str(self.header["GAP"]))
		
	def searchASS(self, assFile, header, update = False):
		c = self.conn.cursor()
		
		c.execute("SELECT Artist, Title, Cover, Background, MP3, Video, Genre, Edition, Language, pitchFile, VideoGAP FROM assdata WHERE assFile=?", (assFile,))
		for row in c:
			if update:
				header["ARTIST"], header["TITLE"], self.coverFile, self.backgroundFile = row[0], row[1], row[2], row[3]
				self.mp3File, self.videoFile, header["GENRE"], header["EDITION"]  = row[4], row[5], row[6], row[7]
				header["LANGUAGE"], self.pitchFilename, header["VIDEOGAP"] = row[8], row[9], row[10]
				if self.coverFile:
					header["COVER"] = self.coverFile
				if self.backgroundFile:
					header["BACKGROUND"] = self.backgroundFile
				if self.mp3File:
					header["MP3"] = self.mp3File
				if self.videoFile:
					header["VIDEO"] = self.videoFile
			return True
		self.conn.commit()
		return False
	
	def insertASS(self, assFile, header):
		c = self.conn.cursor()
		artist, title, genre, edition, language = "", "", "", "", ""
		videogap = 0
		if header["ARTIST"]:
			artist = header["ARTIST"]
		if header["TITLE"]:
			title = header["TITLE"]
		if "GENRE" in header and header["GENRE"]:
			genre = header["GENRE"]
		if "EDITION" in header and header["EDITION"]:
			edition = header["EDITION"]
		if "LANGUAGE" in header and header["LANGUAGE"]:
			language = header["LANGUAGE"]
		if "VIDEOGAP" in header and header["VIDEOGAP"]:
			videogap = header["VIDEOGAP"]
		
		c.execute("INSERT INTO assdata (assFile, Artist, Title, Cover, Background, MP3, "+
			"Video, Genre, Edition, Language, pitchFile,VideoGAP) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", 
			[assFile, artist, title, header["COVER"], header["BACKGROUND"], header["MP3"], 
			header["VIDEO"], genre, edition, language,	self.pitchFilename, videogap])
		self.conn.commit()
		
	def updateDB(self, assFile, element, data):
		c = self.conn.cursor()

		# Insert a row of data
		txt ="UPDATE assdata SET "+element+"= ? WHERE assFile= ? "
		c.execute(txt, (data, assFile))

		# Save (commit) the changes
		self.conn.commit()

	def openCover(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open Cover Image', '.', "*.jpg *.png")
		if fname[0]:
			self.header["COVER"] = fname[0]
			self.updateDB(self.assFilename,"Cover",self.header["COVER"])
			showName = os.path.split(fname[0])
			self.coverPushButton.setText(showName[1])
			
	def openBackground(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open Background Image', '.', "*.jpg *.png")
		if fname[0]:
			self.header["BACKGROUND"] = fname[0]
			self.updateDB(self.assFilename,"Background",self.header["BACKGROUND"])
			showName = os.path.split(fname[0])
			self.backgroundPushButton.setText(showName[1])
			
	def openMP3(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open Song file', '.', "*.wav *.mp3 *.mp4 *.opus *.ogg *.webm *.mka")
		if fname[0]:
			self.header["MP3"] = fname[0]
			showName = os.path.split(fname[0])
			self.mp3PushButton.setText(showName[1])
			self.updateDB(self.assFilename,"MP3",self.header["MP3"])
			
			if self.pitchFilename:
				pth = os.path.join("/tmp","a2u")
				if not os.path.exists(pth):
					os.mkdir(pth)
				fname = os.path.split(self.header["MP3"])[1].split(".")[0]+".wav"
				outWav = os.path.join(pth, fname)
				ff = FFmpeg(
					inputs={self.header["MP3"]: None},
					outputs={ outWav: ['-y',"-ac","1" ]})
				ff.run()
				
				tmpPitch = os.path.join(pth,'temp.aubiopitch')
				os.system('aubiopitch "'+outWav+'" > "'+tmpPitch+'"')
				self.pitchFilename = tmpPitch
				outpf = os.path.split(self.pitchFilename)[1]
				self.pitchPushButton.setText(outpf)
			
	def openVideo(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open Video file', '.', "*.mp4 *.mkv *.webm *.avi *.mpg")
		if fname[0]:
			self.header["VIDEO"] = fname[0]
			showName = os.path.split(fname[0])
			self.videoPushButton.setText(showName[1])
			self.updateDB(self.assFilename,"Video",self.header["VIDEO"])
			if not self.header["MP3"]:
				self.testva()
		
	def openASSFile(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open ASS file', '.', "*.ass *.ssa")
		
		if fname[0]:
			# reset GUI
			self.resetGUIData()
			
			self.assFilename = fname[0]
			self.statusbar.showMessage('Reading ASS file')
			self.txt_syllabes = self.ass2ultrar.parseASS(fname[0], self.header)
			
			minGap = None
			for voice in ["P1","P2","P3"]:
				if self.txt_syllabes[voice]:
					value = self.txt_syllabes[voice][0]
					if not minGap:
						minGap = int(value[0][0]*1000)
					elif minGap>int(value[0][0]*1000):
						minGap = int(value[0][0]*1000)
			self.header["GAP"] = str(minGap)
			
			result = self.searchASS(fname[0], self.header, True)
			if result:
				self.updateGUIData(self.header)
			else:
				self.insertASS(fname[0], self.header)
			
			showName = os.path.split(fname[0])
			for file in os.listdir(showName[0]):
				if "jpg" in file or "png" in file:
					if not self.header["COVER"]:
						self.header["COVER"] = os.path.join(showName[0], file)
					elif not self.header["BACKGROUND"]:
						self.header["BACKGROUND"] = os.path.join(showName[0], file)
				elif "wav" in file or "m4a" in file or "mp4" in file or "mka" in file or "mp3" in file or "ogg" in file:
					if not self.header["MP3"]:
						self.header["MP3"] = os.path.join(showName[0], file)
				elif "mkv" in file or "mp4" in file or "avi" in file or "webm" in file or "mpg" in file:
					if not self.header["VIDEO"]:
						self.header["VIDEO"] = os.path.join(showName[0], file)
				elif file.endswith("itch"):
					if not self.pitchFilename:
						self.pitchFilename= os.path.join(showName[0], file)
			
			self.updateGUIData(self.header)
		self.statusbar.showMessage('')
		
	def openPitchFile(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), 'Open Pitch file', '.', "*.pitch *.aubiopitch")
		if fname[0]:
			self.pitchFilename = fname[0]
			showName = os.path.split(fname[0])
			self.pitchPushButton.setText(showName[1])
			
			self.pitches = self.ass2ultrar.parsePitch(fname[0], self.header)
			BPM = "%2.2f" % self.header["BPM"]
			BPM = BPM.replace(".",',')
			self.bpmLineEdit.setText(BPM)
			if self.assFilename:
				self.updateDB(self.assFilename, "pitchFile", self.pitchFilename)
				if self.txt_syllabes:
					self.gapLineEdit.setText(int(self.txt_syllabes[0][0][0]*1000))
			
	def testva(self):
		if not self.header["VIDEO"]:
			return
		process = subprocess.Popen(['ffmpeg',  '-i', self.header["VIDEO"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout, stderr = process.communicate()
		#output = result.communicate()
		type = None
		for s in str(stdout).split("Stream")[1:]:
			if "aac" in s:
				type = "mp4"
			elif "vorbis" in s:
				type = "ogg"
			elif "opus" in s:
				type = "mka"
		out = self.header["VIDEO"].split(".")[0]
		out += "."+type
		ff = FFmpeg(
			inputs={self.header["VIDEO"]: None},
			outputs={ out: ['-y', '-vn', '-acodec', 'copy', '-f', type]})
		ff.run()
		if os.path.exists(out):
			self.header["MP3"] = out
			mp3 = os.path.split(self.header["MP3"])[1]
			self.mp3PushButton.setText(mp3)
			
			pth = os.path.join("/tmp","a2u")
			if not os.path.exists(pth):
				os.mkdir(pth)
			fname = os.path.split(self.header["MP3"])[1].split(".")[0]+".wav"
			outWav = os.path.join(pth, fname)
			ff = FFmpeg(
				inputs={self.header["MP3"]: None},
				outputs={ out: ['-y',"-ac","1", outWav]})
			ff.run()
			
			tmpPitch = os.path.join(pth,'temp.aubiopitch')
			os.system('aubiopitch "'+outWav+'" > "'+tmpPitch+'"')
			self.pitchFilename = tmpPitch
			outpf = os.path.split(self.pitchFilename)[1]
			self.pitchPushButton.setText(outpf)
			
		
	def makeUltrastar(self):
		self.header["ARTIST"] = self.artistLineEdit.text()
		self.header["TITLE"] = self.titleLineEdit.text()
		self.header["GENRE"] = self.genreComboBox.currentText()
		self.header["EDITION"] = self.editionLineEdit.text()
		self.header["LANGUAGE"] = self.languageComboBox.currentText()
		self.header["GAP"] = int(float(self.gapLineEdit.text()))
		self.header["VIDEOGAP"] = float(self.videoGAPdoubleSpinBox.value())
		self.header["BPM"] = float(self.bpmLineEdit.text().replace(",","."))
		
		if not self.searchASS(self.assFilename, self.header):
			self.insertASS(self.assFilename, self.header)
		else:
			self.updateDB(self.assFilename,"Artist",self.header["ARTIST"])
			self.updateDB(self.assFilename,"Title",self.header["TITLE"])
			self.updateDB(self.assFilename,"Genre",self.header["GENRE"])
			self.updateDB(self.assFilename,"Edition",self.header["EDITION"])
			self.updateDB(self.assFilename,"Language",self.header["LANGUAGE"])
			self.updateDB(self.assFilename,"VideoGAP",self.header["VIDEOGAP"])
		
		tempHeaders = {}
		if not self.txt_syllabes:
			self.statusbar.showMessage('Reading ASS file')
			self.txt_syllabes = self.ass2ultrar.parseASS(self.assFilename, tempHeaders)
			self.header["GAP"] = str(int(self.txt_syllabes["P1"][0][0][0]*1000))
		if not self.pitches:
			self.statusbar.showMessage('Reading pitch file')
			self.pitches = self.ass2ultrar.parsePitch(self.pitchFilename, tempHeaders)
			self.header["BPM"] = self.header["BPM"]*2
		self.statusbar.showMessage('Create Ultrastar file')
		self.ass2ultrar.ASS2Ultrastar(self.header, self.txt_syllabes, self.pitches, self.assFilename)
		self.statusbar.showMessage('')
		
if __name__=='__main__':
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	
	prog = a2u(MainWindow)
	
	MainWindow.show()
	sys.exit(app.exec_())