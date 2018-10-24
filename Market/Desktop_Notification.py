# from PyQt5 import Qt
# import sys
# app = Qt.QApplication(sys.argv)
# systemtray_icon = Qt.QSystemTrayIcon(app, Qt.QIcon('C:\\Users\\nandpara\\Documents\\ISE SNAPSHOTS\\DB_restore_failed.jpg'))
# systemtray_icon.show()
# systemtray_icon.showMessage('Title', 'Content')


from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Hello World!!!",
              "Python is 10 seconds awsm!",
              icon_path="custom.ico",
              duration=10)
toaster.show_toast("Hello World!!!",
             "Python is awesome by default!")