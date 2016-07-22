from PyQt4 import QtGui
from PyQt4.Qt import *
from Crypto.Cipher import AES
from PyQt4.QtCore import QThread
from PyQt4 import QtCore, QtGui
import os,random, struct, time, shutil, tkFileDialog, hashlib, hmac, sys
import design, enc_password, progressbar,dec_password

userKeys = []
filepaths = []

class Local_Encryption_App(QtGui.QMainWindow, design.Ui_MainWindow):

    def __init__(self,parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.encPasswordPopup = Encrypt_Password_Popup(self)
        #self.progressbar = Progressbar(self)
        self.Encrypt_Button.clicked.connect(self.pick_file_enc)
        self.Decrypt_Button.clicked.connect(self.pick_file_dec)

    def pick_file_dec(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self)
        if len(filepath) > 0:

            filepaths.append(filepath)
            self.dec_password_popup()
        else:
            self.destroy()
    def pick_file_enc(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self)
        if len(filepath) > 0:
            filepaths.append(filepath)
            self.enc_password_popup()
        else:
            self.destroy()

    def enc_password_popup(self):
        passwordPopup = Encrypt_Password_Popup(self)
        passwordPopup.show()
        #passwordPopup.exec_()

    def dec_password_popup(self):
        passwordPopup = Decrypt_Password_Popup(self)
        passwordPopup.show()
        #passwordPopup.exec_()

class Encrypt_Password_Popup(QtGui.QMainWindow, enc_password.Ui_passwordWindow):

    def __init__(self,parent=None):
        super(Encrypt_Password_Popup, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.getPassword)

    def check_password(self,password,confirm):
        if password == confirm:
            userKeys.append(password)
            return True
        else:
            QtGui.QMessageBox.information(self,"Password Incorrect", "The passwords you entered did not match please try again!")
            return False

    def getPassword(self):
        password = self.password.text()
        confirm = self.confirm.text()
        if self.check_password(password,confirm) == True:
            self.close()
            self.progressbar()

    def progressbar(self):
        progressbar = Progressbar(self)
        progressbar.show()
        #progressbar.exec_()

class Decrypt_Password_Popup(QtGui.QMainWindow, dec_password.Ui_passwordWindow):

    def __init__(self,parent=None):
        super(Decrypt_Password_Popup, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.getPassword)

    def check_password(self, password, confirm):
        if password == confirm:
            userKeys.append(password)
            return True
        else:
            QtGui.QMessageBox.information(self, "Password Incorrect",
                                          "The passwords you entered did not match please try again!")
            return False

    def getPassword(self):
        password = self.password.text()
        confirm = self.confirm.text()
        if self.check_password(password, confirm) == True:
            self.close()
            self.progressbar()

    def progressbar(self):
        progressbar = Dec_Progressbar(self)
        progressbar.show()
        #progressbar.exec_()


class Dec_Progressbar(QtGui.QMainWindow, progressbar.Ui_MainWindow):
    def __init__(self,parent=None):
        super(Dec_Progressbar, self).__init__(parent)
        self.setupUi(self)

        self.hidePB()


        self.myThread = Decrypter(userKeys[0],filepaths[0])
        self.connect(self.myThread,SIGNAL("Decrypt(QString)"), self.changeDecrypt)
        self.connect(self.myThread,SIGNAL("progress(QString)"),self.updateProgress)
        self.connect(self.myThread,SIGNAL("Done(QString)"), self.updateProgressDone)
        self.connect(self.myThread, SIGNAL("ResetVariables(QString)"), self.resetVariables)
        self.connect(self.myThread, SIGNAL("finished()"), self.done)

        self.myThread.start()

    def done(self):
        QtGui.QMessageBox.information(self,"Done!", "Done decrypting your file!")

    def hidePB(self):
        self.progressBar.hide()
        self.label.setText(
            "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Verifying File Signature and Password!</span></p></body></html>")
    def changeDecrypt(self,filesize):
        self.label.setText(
            "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Verified! Decrypting Now!</span></p></body></html>")
        self.progressBar.show()
        filesize = int(filesize)
        self.progressBar.setMaximum(filesize/100)
        self.progressBar.setValue(0)

    def updateProgress(self,progress):
        progress = int(progress)

        self.progressBar.setValue(self.progressBar.value() + progress/100)

    def updateProgressDone(self, done):
        self.label.setText(
            "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Done!!!</span></p></body></html>")

    def resetVariables(self, variable):
        del filepaths [:]
        del userKeys [:]


class Progressbar(QtGui.QMainWindow, progressbar.Ui_MainWindow):
    def __init__(self,parent=None):
        super(Progressbar, self).__init__(parent)
        self.setupUi(self)

        self.myThread = Encrypter(userKeys[0],filepaths[0])
        self.connect(self.myThread,SIGNAL("add_post(QString)"),self.setMaxProgressBar)
        self.connect(self.myThread,SIGNAL("progress(QString)"),self.updateProgress)
        self.connect(self.myThread,SIGNAL("StartSig(QString)"),self.updateSigGUI)
        self.connect(self.myThread,SIGNAL("SigProgress(QString)"), self.updateProgressSig)
        self.connect(self.myThread,SIGNAL("Done(QString)"),self.updateProgressDone)
        self.connect(self.myThread,SIGNAL("ResetVariables(QString)"), self.resetVariables)
        self.connect(self.myThread,SIGNAL("finished()"),self.done)
        self.myThread.start()

    def done(self):
        QtGui.QMessageBox.information(self,"Done!", "Done encrypting your file!")

    def setMaxProgressBar(self,fileSize):
        fileSize = int(fileSize)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(fileSize/100)

    def updateProgress(self, progress):
        progress = int(progress)
        self.progressBar.setValue(self.progressBar.value()+progress/100)

    def updateSigGUI(self,progress):
        self.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Signing with HMAC</span></p></body></html>")
        self.progressBar.setValue(0)

    def updateProgressSig(self,progress):
        progress = int(progress)
        self.progressBar.setValue(self.progressBar.value() + progress/100)

    def updateProgressDone(self,progress):
        self.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Done!!!</span></p></body></html>")

    def resetVariables(self, variable):
        del filepaths [:]
        del userKeys [:]

class Encrypter(QThread):
    def __init__(self,userKey, filepath):
        QThread.__init__(self)
        self.userkey = str(userKey)
        self.filepath = str(filepath)
        self.sig = hmac.new(self.userkey,'', hashlib.sha256)
    def __del__(self):
        self.wait()
    def run(self):
        self.encrypt_file(self.userkey,self.filepath)

    def split_path(self, filepath):
        dict = {}
        key = 0
        back_key = 0
        length_of_dict = 0
        filename = ''
        for char in filepath:
            dict[key] = char
            key += 1
        for x in dict:
            length_of_dict += 1
            if dict[x] == '/' and x != 0:
                back_key = x
        for x in dict:
            if x == back_key and back_key < length_of_dict - 1:
                back_key += 1
                item = dict[back_key]
                filename = filename + item
        return filename

    def encrypt_file(self, password,in_filename, out_filename=None, chunksize=64*1024):
        """
        :param key: String that is 16, 24, 32 bytes long.
        :param in_filename: Name of input file
        :param out_filename: If None, it will be "in_filename.enc" will be used.
        :param chunksize: Sets the size of the chunk that the function uses to encrypt the file.
        :return: None
        """

        if not out_filename:
            out_filename = in_filename + ".enc"

        iv = os.urandom(16)

        key = hashlib.sha256(password).digest()
        encryptor = AES.new(key, AES.MODE_CBC, iv)

        abspath = os.path.dirname(in_filename)
        os.chdir(abspath)
        new_filename = self.split_path(in_filename)
        file_size = os.path.getsize(new_filename)
        signal_file_size = str(file_size)
        self.emit(SIGNAL('add_post(QString)'),signal_file_size)
        with open(new_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', file_size))
                outfile.write(iv)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)
                    progress = str(len(chunk))
                    self.emit(SIGNAL("progress(QString)"), progress)
                    encrypted_data = encryptor.encrypt(chunk)
                    outfile.write(encrypted_data)
                outfile.close()
            infile.close()
            """
            with open(out_filename, 'rb') as outfile:
                started = "True"
                self.emit(SIGNAL("StartSig(QString)"),started)
                sig = ''
                while True:
                    chunk = outfile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)
                    self.sig.update(chunk)
                    sigProgress = str(len(chunk))
                    self.emit(SIGNAL("SigProgress(QString)"), sigProgress)
                outfile.close()
            with open(out_filename, 'a')as outfile:
                self.sig = self.sig.digest()
                self.sig
                outfile.write("Sig: "+self.sig)
                outfile.close()
            """
        os.remove(str(new_filename))
        finished = 'True'
        self.emit(SIGNAL("ResetVariables(QString)"), finished)
        self.emit(SIGNAL("Done(QString)"), finished)


class Decrypter(QThread):
    def __init__(self, UserKeys, filePaths):
        QThread.__init__(self)
        self.userkey = str(UserKeys)
        self.filepath = str(filePaths)
        self.verifySig = None
        self.sig = hmac.new(self.userkey, '', hashlib.sha256)
        self.head = ''

    def __del__(self):
        self.wait()

    def run(self):
        self.decrypt_file(self.userkey,self.filepath)
    def decrypt_file(self, password, in_filename, out_filename=None, chunksize=64 *1024):
        """
        :param key: Must be same key from encryption
        :param in_filename: File name of the file to be decrypted
        :param out_filename: If no name given it will be the same as the original
        :param chunksize: This is the size of the chunk to be decrypted
        :return: None
        """

        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
        abspath = os.path.dirname(in_filename)
        os.chdir(abspath)
        new_filename = self.split_path(in_filename)
        file_size = os.path.getsize(new_filename)
        with open(new_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
                iv = infile.read(16)
                key = hashlib.sha256(password).digest()
                decryptor = AES.new(key, AES.MODE_CBC, iv)
                self.emit(SIGNAL("Decrypt(QString)"), str(file_size))
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    progress = str(len(chunk))
                    self.emit(SIGNAL("progress(QString)"), progress)
                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(origsize)
            infile.close()
        outfile.close()
        finished = "done"
        self.emit(SIGNAL("Done(QString)"), finished)
        self.emit(SIGNAL("ResetVariables(QString)"), finished)


        """
            for line in infile:
                if "Sig: " in line:
                    self.head,sep,tail = line.partition("Sig: ")
                    self.verifySig = tail
            infile.close()
        with open(new_filename, "rb") as infile:
            with open("temp", "wb") as temp:
                for line in infile:
                    if "Sig: " not in line:
                        temp.write(line)
                temp.write(self.head)
                temp.close()
            infile.close()
            os.remove(new_filename)
            os.rename("temp",str(new_filename))
        with open(new_filename, 'rb') as infile2:
            while True:
                chunk = infile2.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                self.sig.update(chunk)
                infile.close()
            self.sig = self.sig.digest()
            #SIG_SIZE = len(self.sig)
            file_size = os.path.getsize(new_filename)
            if self.check_encrypt(new_filename) == True:
                print "Sig: " +self.sig
                print "Verify: " +self.verifySig
                if self.sig != self.verifySig:
                    print "message authentication failed"
                elif self.sig == self.verifySig:
                """



    def split_path(self, filepath):
        dict = {}
        key = 0
        back_key = 0
        length_of_dict = 0
        filename = ''
        for char in filepath:
            dict[key] = char
            key += 1
        for x in dict:
            length_of_dict += 1
            if dict[x] == '/' and x != 0:
                back_key = x
        for x in dict:
            if x == back_key and back_key < length_of_dict - 1:
                back_key += 1
                item = dict[back_key]
                filename = filename + item
        return filename

    def check_encrypt(self, path):
        dict = {}
        key = 0
        back_key = 0
        length_of_dict = 0
        filename = ''
        for char in path:
            dict[key] = char
            key += 1
        for x in dict:
            length_of_dict += 1
            if dict[x] == '.' and x != 0:
                back_key = x
        for x in dict:
            if x == back_key and back_key < length_of_dict - 1:
                back_key += 1
                item = dict[back_key]
                filename = filename + item
        if filename == 'enc':
            return True
        else:
            return False

def main():
    app = QtGui.QApplication(sys.argv)
    form = Local_Encryption_App()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()