import platform
import os
import win10toast
import time
import plyer.platforms.win.notification
from plyer import notification


def push(title, message, status):
    if status:
        try:
            plt = platform.system()
            if plt == "Darwin":
                command = '''
                osascript -e 'display notification "{message}" with title "{title}"'
                '''
            elif plt == "Linux":
                command = f'''
                notify-send "{title}" "{message}"
                '''
            elif plt == "Windows":
                path = r"../icons/main.ico"
                path = 'icon.ico'
                # win10toast.ToastNotifier().show_toast(title, message, duration=2, icon_path=None, threaded=False)
                notification.notify(title, message, timeout=2, app_name='TradingView', toast=True)
                return
            else:
                return
            os.system(command)
        except AttributeError:
            pass


if __name__ == '__main__':
    push('dfg', 'hgnf', True)
