# HelpHours

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![SamLab17](https://circleci.com/gh/SamLab17/HelpHours.svg?style=shield)](https://github.com/SamLab17/HelpHours)

![repo banner](.github/banner.png)

A web app for managing online help hours for CS courses at UT Austin.

The app is being hosted at: [https://www.utcshelphours.com](https://www.utcshelphours.com).

## Running the Application Locally

1. Clone the repo
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `./copy_dev_files.sh`
   
   (This will use the `development/empty.db` database file (which is empty). If you want to have
   a testing instructor account, use the `testing/testing.db` database instead.)
6. `flask run`