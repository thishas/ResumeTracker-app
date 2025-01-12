@echo off
echo Building Resume Tracker Application...
pyinstaller --clean --noconfirm ResumeTracker.spec
echo Build complete! Check the 'dist' folder for the executable.
