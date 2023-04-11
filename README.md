# Lazor_Project

This will be a program that automatically finds solutions to the “Lazor” game on iOS and Andriod.
Within this program we:
* Analyze bff file content that contains level data:
    * Creates a dictionary that contains the information from the bff file
* Create laser movement logic
    * Defines the movement of the lazor within a grid read from the bff file
* Define block classes to define the how blocks will interact with the laser
* Solves the all the different levels automatically under 2 minutes
* Generated an output format to show the original level and the solved level
    * Saves the solved level to a png file within the parent folder
Instructions for use:
* All modules for this project are stored in this folder
* Running the Lazor_Class_and_Logic.py file will display the images from each level and save outputs to .png files with the level name
    * You can comment out specific levels if you wish only specific levels to run
    * Running this file will call on modules in the folder
