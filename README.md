DefecatingCat
=============

This is a continuing project to weaponize an arduino driven airsoft gun on a pan/tilt platform. It consists of two python scripts and an arduino sketch. Fire_control.py is used to drive the Arduino and position the airsoft and engage the target. Monitor.py is the motion tracking component based off of OpenCV, it finds the center point of target movement, positions the airsoft, and fires a 500ms burst.

Usage: python monitor.py
