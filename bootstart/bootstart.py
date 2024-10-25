#!/usr/bin/env python3

import os
import argparse
import platform

from   p3lib.uio import UIO
from   p3lib.helper import logTraceBack
from   p3lib.boot_manager import BootManager
from   subprocess import check_call

class Executioner(object):
    """@brief Responsible for running the command/script file."""

    def __init__(self, uio, options):
        """@brief Constructor
           @param uio A UIO instance handling user input and output (E.G stdin/stdout or a GUI)
           @param options An instance of the OptionParser command line options."""
        self._uio = uio
        self._options = options

    def run(self):
        """@brief A command that runs indefinitely."""

        self._uio.debug(f"CMD: command/script file: {self._options.file}")
        check_call(self._options.file)

def check(options):
    """@brief Perform some checks before attempting to run."""

    if options.file is None:
        raise Exception("The --file argument is not set.")

    # If command file not present
    if not os.path.isfile(options.file):
        raise Exception(f"{options.file} file not found.")
    
    if platform.system() == 'Linux' and not os.access(options.file, os.X_OK):
        raise Exception(f"{options.file} file not not executable.")
    
def main():
    """@brief Program entry point"""
    uio = UIO()

    try:
        parser = argparse.ArgumentParser(description="A simple way of running a command/script on a Linux system using systemd when the computer starts. The output (stdout) from the executed script is sent to syslog.",
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--debug",    action='store_true', help="Enable debugging.")
        parser.add_argument("-f", "--file",     help="The command/script file to execute. No arguments can be passed to this command/script.", default=None)
        parser.add_argument("-s", "--seconds",  type=float, help="The restart delay for the command/script in seconds (default=1.0). If the script file stops running for any reason then an attempt to restart it will be made after this delay.", default=1.0)
        parser.add_argument("-n", "--name",     help="The name of the service to be created. If this is left blank the name of the service name is the filename of the command/script file.", default=None)
        BootManager.AddCmdArgs(parser)

        options = parser.parse_args()
        
        uio.enableDebug(options.debug)
        uio.logAll(True)
        uio.enableSyslog(True)

        check(options)
        
        if options.name:
            serviceName = options.name
        else:
            serviceName = os.path.basename(options.file)
                
        handled = BootManager.HandleOptions(uio, options, True, serviceName=serviceName, restartSeconds=options.seconds)
        if not handled:
            executioner = Executioner(uio, options)
            executioner.run()

    #If the program throws a system exit exception
    except SystemExit:
        pass

    #Don't print error information if CTRL C pressed
    except KeyboardInterrupt:
        pass

    except Exception as ex:
        logTraceBack(uio)

        if options.debug:
            raise
        else:
            uio.error(str(ex))

if __name__== '__main__':
    main()
