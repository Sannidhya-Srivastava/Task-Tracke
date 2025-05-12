import sys
import os
import servicemanager
import win32serviceutil
import win32service
import win32event
from app import app
from waitress import serve

class TaskTrackerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TaskTrackerService"
    _svc_display_name_ = "Task Tracker Flask Service"
    _svc_description_ = "Flask Task Tracker Web Application Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        try:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            serve(app, host='0.0.0.0', port=5000)
        except Exception as e:
            servicemanager.LogErrorMsg(str(e))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TaskTrackerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TaskTrackerService)