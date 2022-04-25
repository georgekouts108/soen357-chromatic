# soen357-chromatic

In order to run Chromatic, it is recommended, but not mandatory, that you have Visual Studio Code installed. The link to download it can be found here: 

https://code.visualstudio.com/
____________________________________________________________________________________

Additionally, you must make sure that you have Python and Flask installed:

If you’re using MAC:

1) Open “Terminal”
2) Run the command python3 —version to check if python 3.0 or later is installed. If not yet installed, follow these steps to install the lastest version of Python:
	2.2) navigate to https://www.python.org/
	2.3) in the navigation bar, click on “Downloads”
	2.4) under the “Download Python <version #> button, click on the “macOS” hyperlink
	2.5) look for “Python 3.8.0 - Oct. 14, 2019” and click on macOS 64-bit installer
	2.6) after the install package downloads, open it up and run the installation wizard
	2.7) close the installation wizard once the installation is complete
	2.8) open “Terminal” and rerun the command python3 —version to verify the installation success
	2.9) run the command pip3 —version to check if the python package manager is installed (you should see “pip 	<version #> from <path to pip>”
	2.10) if pip3 is installed, run the command “pip3 install flask” to install the Flack package (if it is already installed, you should see reports reading “Requirement already satisfied”, but if not previously installed 	beforehand, you should see “Successfully installed flask-<version #>”)

  
____________________________________________________________________________________
  
After installing Visual Studio Code, Python 3 and Flask, follow these steps to run the project:

1) Fork and clone this repository into a convenient location on your local drive. The cloned repository’s directory should have the name “soen357-chromatic”
2) open a new terminal at this directory, or you may open the project in Visual Studio Code (if you open the project in VS Code, make sure you have the terminal view on, pointing to the directory)
3) Verify that the terminal is pointing to the directory by running the command “pwd”; the result should be a file path ending with “soen357-chromatic”
4) Run the project by entering the command “flask-run”
5) Open your browser, and route to “localhost:5000”. If you see a simple Login Page, you have done this correctly

You can now use the application in your browser. When you want to exit the application, do “CTRL-C” in the terminal. To run again, type “flask run”
