# time_logger_joker
to start the sql server on arch based systems:
``` 
systemctl start mysqld.service
```

## Getting started 
Getting the development environment up is pretty straight forward.
1. Install python [here](https://www.python.org/) 
2. Install mysql, we are using v5.7 currently
3. Copy the settings.exapmle file and rename it to settings.py, change all of the parameters to the ones you chose setting up mysql
4. Run the setup script for the database
5. Run the script `python cli.py`

## Usage
* Login using the a admin userid and password
* `t` to log time, using card ids, first input starts a timelog the second finishes it
* `r` to register a new user
* `e` to edit a user
you can at any time input q to either go back one step in the menu or quit the program
