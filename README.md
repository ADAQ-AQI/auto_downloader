# auto_downloader
Python scripts for automatically downloading air quality data from various UK sources.

CURRENTLY THIS IS ONLY FOR USE BY ELEANOR SMITH, AND I CANNOT SUPPORT ANYONE ELSE WHO WANTS TO USE IT. However, if you think it can be adapted to your uses and you would like my help, please contact me at corinne.bosley@metoffice.gov.uk

To Use:
1. Grab a fork of the repo and check it out to your location (this is an example of cloning via SSH, but you can use HTTP if you like):
$ git clone git@github.com:corinnebosley/auto_downloader.git

2. Run the wrapper script.  This will initialise your selenium environment and run the python script which runs the web driver:
$ cd auto_downloader
$ ./downloader.sh

3. See the webdriver hard at work finding all your data and downloading it.  Output will be directed to the following locations:
auto_downloader/confirmations: screenshots of successful data downloads (data itself will be emailed to you)
auto_downloader/errors: screenshots of any records that don't actually exist will be sent here
auto_downloader/denied_requests: screenshots showing the details of requests that exceeded data size limits are stored here.

4. Manually download any files that were too large in 5-year chunks.

5. Move data to sensible location (I intend to create a Power-Automate tool to do this for you soon).  

