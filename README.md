# troxiaconfiggen

Python code to generate json config files from the satellite
spreadsheet for the Max/MSP troxia project. Not much use to anybody
really, but made public so it is easy to clone.



# Instructions and notes on how to use the Python stuff.


1. Do it by hand Create a virtual environment,activate it and build
   everything that you need.

```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt 
pyinstaller --onefile experiments.py 
```

2. Or use the Makefile
```
make standalone
```
In the build directory you should find a standalone executable.


## How to use the package 
Either run experiments.py in a virtual environment or the standalone
executable. 

### Create the config file for the max file.
Note that it skips when there is no soundfile or no orbitfile
```
../dist/experiments create SPREADSHEET SOUNDDIR ORBITDIR base_config_name MAXINPUTS
``` 
### Check what sound or orbit files are missing
```
../dist/experiments check SPREADSHEET SOUNDDIR ORBITDIR
```

### Create the config file for the max file with optional start day
Note that it skips when there is no soundfile or no orbitfile
```
../dist/experiments create SPREADSHEET SOUNDDIR ORBITDIR base_config
MAXINPUTS start_day 
``` 
### Create the config file for the max file with optional start/end day
Note that it skips when there is no soundfile or no orbitfile
```
../dist/experiments create SPREADSHEET SOUNDDIR ORBITDIR base_config
MAXINPUTS start_day end_day
``` 



## Assumptions on the spreadsheet.

1. The launch date is a day from day 0.
2. The delaunch column is the day the satellite goes down.


## Stuff for Justin
Use the package emacs package `pyvenv` You need to active it it
`M-x pyvenv-mode` then active it `M-x pyvenv-active` point it the
right environment and every thing seems to be ok.




## Things to look at
A number of entries in the spreadsheet have a delaunch date of 22903
which is 62 years.  Looking at the spreadsheet that just means it 
is still in earth orbit.
```
sat_dict['S000005']
{'Launch': 164, 'Delaunch': 22903}
```



