import os
import subprocess
from PyQt5 import QtWidgets, QtCore

class MinecraftLauncherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.profiles = self.scan_and_create_batch_files()

    def init_ui(self):
        self.setWindowTitle("Minecraft Profile Launcher")
        self.setGeometry(300, 300, 400, 300)
        layout = QtWidgets.QVBoxLayout(self)
        
        self.list_widget = QtWidgets.QListWidget(self)
        layout.addWidget(self.list_widget)

        self.launch_button = QtWidgets.QPushButton("Launch Selected Profile", self)
        layout.addWidget(self.launch_button)

        self.launch_button.clicked.connect(self.launch_selected_profile)
        self.setLayout(layout)

    def scan_and_create_batch_files(self):
        usb_root = os.getcwd()  # Get current directory (assuming the script is run from the USB drive)
        instances_dir = os.path.join(usb_root, "Instances")
        batch_files_dir = os.path.join(usb_root, "ProfileBatchFiles")
        launcher_path = os.path.join(usb_root, "Launcher", "Minecraft.exe")
        profiles = [d for d in os.listdir(instances_dir) if os.path.isdir(os.path.join(instances_dir, d))]
        
        # Ensure ProfileBatchFiles directory exists
        os.makedirs(batch_files_dir, exist_ok=True)

        # Ensure there's a batch file for each profile
        for profile in profiles:
            batch_file_path = os.path.join(batch_files_dir, f"{profile}.bat")
            work_dir = os.path.join(instances_dir, profile)

            # Write/update the batch file
            with open(batch_file_path, "w") as batch_file:
                batch_file.write(f'@echo off\nstart "" "{launcher_path}" --workDir "{work_dir}"\n')
        
        # Add profiles to list widget for selection
        self.list_widget.addItems(profiles)
        return profiles

    def launch_selected_profile(self):
        selected_profile = self.list_widget.currentItem().text()
        if not selected_profile:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a profile to launch.")
            return

        usb_root = os.getcwd()
        batch_files_dir = os.path.join(usb_root, "ProfileBatchFiles")
        batch_file_path = os.path.join(batch_files_dir, f"{selected_profile}.bat")

        # Launch the selected batch file
        try:
            subprocess.Popen([batch_file_path], shell=True)
            self.close()  # Close the GUI after launching
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to launch profile: {e}")

app = QtWidgets.QApplication([])
window = MinecraftLauncherApp()
window.show()
app.exec_()
