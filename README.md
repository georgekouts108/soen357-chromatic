# soen357-chromatic

In order to run Chromatic, it is recommended, but not mandatory, that you have Visual Studio Code installed. The link to download it can be found here: 

https://code.visualstudio.com/
____________________________________________________________________________________

Additionally, you must make sure that you have Python and Flask installed:

**If you’re using MAC:**

1) Open “Terminal”
2) Run the command python3 —-version to check if python 3.0 or later is installed. If not yet installed, follow these steps to install the lastest version of Python:
	- navigate to https://www.python.org/
	- in the navigation bar, click on “Downloads”
	- under the “Download Python <version #> button, click on the “macOS” hyperlink
	- look for “Python 3.8.0 - Oct. 14, 2019” and click on macOS 64-bit installer
	- after the install package downloads, open it up and run the installation wizard
	- close the installation wizard once the installation is complete
	- open “Terminal” and rerun the command python3 —version to verify the installation success
	- run the command pip3 --version to check if the python package manager is installed
	- if pip3 is installed, run the command “pip3 install flask” to install the Flack package (if it is already installed, you should see reports reading “Requirement already satisfied”, but if not previously installed 	beforehand, you should see “Successfully installed flask-<version #>”)

**If you’re using WINDOWS 10:**

1) Open the Command Prompt
2) Run the command python —V to check if python is installed. If not yet installed, follow these steps to install the lastest version of Python 3.0:
	- navigate to https://www.python.org/
	- in the navigation bar, click on “Downloads”
	- under the “Download Python <version #> button, click on the “Windows” hyperlink
	- look for “Python 3.8.0 - Oct. 14, 2019” and click on its hyperlink
	- scroll down to the "Files" section and click and download the one that reads "Windows x86-64 executable installer", save it to a convenient location
	- in the installation wizard, check the box "Add Python 3.8 to PATH"
	- click on "Customize installation" and ensure that "pip" is selected, along with all other boxes, and click "Next"
	- check the box "Install for all users"
	- OPTIONAL: You may change the installation location by clicking on "Browse" and configuring the location
	- click on "Install"
	- once the installation was successful, close the wizard
	- verify the installation by opening the command prompt and running the command 'python --version' to check the version (should be Python 3.8.0)
	- run the command 'pip —version' to check if the python package manager is installed
	- to install flask, run the command: 'py -m pip install flask'
	- check the flask version by running the command: 'py -m flask --version'
____________________________________________________________________________________
  
After installing Visual Studio Code, Python 3 and Flask, follow these steps to run the project:

1) Fork and clone this repository into a convenient location on your local drive. The cloned repository’s directory should have the name “soen357-chromatic”
2) open a new terminal at this directory, or you may open the project in Visual Studio Code (if you open the project in VS Code, make sure you have the terminal view on, pointing to the directory)
3) Verify that the terminal is pointing to the directory by running the command “pwd”; the result should be a file path ending with “soen357-chromatic”
4) Run the project by entering the command “flask-run”
5) Open your browser, and route to “localhost:5000”. If you see a simple Login Page, you have done this correctly

____________________________________________________________________________________

You can now use the application in your browser. When you want to exit the application, do “CTRL-C” in the terminal. To run again, type “flask run”.
____________________________________________________________________________________

**References**

- https://www.w3schools.com/html/html_table_borders.asp
- https://www.youtube.com/watch?v=irvyVylgPRc&t=8s
- https://www.youtube.com/watch?v=rVuHKypjDMw
- https://www.youtube.com/watch?v=yIbS0fcUvVg
- https://www.youtube.com/watch?v=uxZuFm5tmhM
