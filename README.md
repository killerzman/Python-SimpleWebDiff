# SimpleWebDiff

Fast, simple and configurable check for website changes

**IMPORTANT! THIS IS ONLY USEFUL FOR MOSTLY STATIC WEBPAGES!**

**THIS IS VERY SENSITIVE TO EVEN BITS OF INFORMATION BEING CHANGED!**

**DOES NOT SHOW ACTUAL CHANGES, JUST CHECKS FOR THEM!**

# More info
Supporting GUI functionality for easy multi-threading aka opening multiple processes! (windows only)

Actual multi-threading is still possible on every platform only through the terminal.

# Install
Python 3 required

    git clone https://github.com/killerzman/SimpleWebDiff.git
    cd SimpleWebDiff
    pip install -r requirements.txt
    pip install -r optional-requirements.txt

# Usage
Terminal-only:

    python web_diff.py -flags <website_url>

From terminal to GUI:

    python gui.py
    
GUI:

    Open runWIN.vbs

Flags:

    -r     -> check again even if differences are found
              default: false
              
    -o     -> open web browser when differences are found
              default: false
              
    -t int -> how often in seconds to check for differences
              default: 60
              
    -w     -> suppress warnings
              default: false
              WARNING!
              FLAG SHOULDN'T BE USED IF DEBUGGING
              
    -v     -> ignore verifying the SSL certificate
              default: false
              WARNING!
              TRY USING HTTP INSTEAD OF HTTPS
              USE THIS WITH -w
              USE THIS IF ALL ELSE FAILS

Example:

    python web_diff.py -o -t 30 https://en.wikipedia.org/wiki/Static_web_page
Example will check for differences every 30 seconds and will open the browser upon finding one.

