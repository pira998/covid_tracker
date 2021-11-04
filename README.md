![alt text](https://github.com/pira998/covid_tracker/blob/master/assets/global.png?raw=true)
# Start the Wave server
To start the Wave server, simply open a new terminal window and execute `waved` (or `waved.exe` on Windows).
`cd $HOME/wave`
`./waved`

# Set up a working directory
Next, let's set up a working directory to author our program.
## Create a directory
`mkdir  $HOME/wave-apps`
 `cd $HOME/wave-apps`

## Set up a virtual environment

A [virtual environment](https://docs.python.org/3/tutorial/venv.html) helps us manage our program's dependencies without interfering with system-wide packages.
For Linux,
`python3 -m venv venv`
`source venv/bin/activate`
For Windows,
`python3 -m venv venv`
`venv\bin\activate`

## Install the Wave Python driver
`pip install h2o_wave`

# Run your program
`python covid_tracker.py`
