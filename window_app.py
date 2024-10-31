import win32serviceutil
import win32service
import win32event
import time
from PIL import ImageGrab
import configparser
import requests
import os

class ScreenCaptureService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ScreenCaptureService"
    _svc_display_name_ = "Screen Capture Service"
    _svc_description_ = "Captures the screen every 2 seconds and pushes images to Raspberry Pi."

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.config = self.load_config()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def push_image_to_pi(self, image_path):
        url = f"http://{self.config['raspberry_pi']['ip']}:{self.config['raspberry_pi']['port']}/upload"
        with open(image_path, "rb") as image_file:
            files = {'file': image_file}
            try:
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    print(f"Image {image_path} sent successfully!")
                else:
                    print(f"Failed to send image {image_path}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error sending image: {e}")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        output_dir = "C:\\ScreenCaptures"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        while self.is_running:
            screenshot_path = os.path.join(output_dir, f"screenshot_{int(time.time())}.png")
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            
            # Push image to Raspberry Pi
            self.push_image_to_pi(screenshot_path)
            
            time.sleep(2)

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ScreenCaptureService)
