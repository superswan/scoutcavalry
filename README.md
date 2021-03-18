# scoutcavalry
masscan web interface / recon tool

# usage
1. clone repository
2. install any dependencies (```pip install -r requirements.txt```)
3. run ```python scoutcav.py```
4. open in browser
5. import masscan output .xml file from the import tab

# note
This program is in a very early stage of development and is not fully featured. You may experience some problems while using certain features.

Windows is currently unsupported 

You may have to create the ```data``` directory and subsequent directories yourself
```
data
├── db //
│   └── scans.db // default database
├── images // screenshots from http(s) and vnc are copied here
└── import // Scans are moved to this directory on import
```

Uses flask WSGI server for now

```masscan``` is ran as root and you will have to provide a valid sudo password in the terminal. edit the ```sudoers``` file to change this behavior. 


# TODO
* Database management 
    * ~~create~~ 
    * ~~save~~ 
    * selection
    * import
    * delete
* Enable scanning within interface
    * Specify interface
    * Target List
    * IP exclusions
    * Configuration from file
    * Resume
    * Scan by ASN #
    * Source address and User Agent support
    * Output format selection
* Screenshot backup
* Add configuration options for web interface
* ~~Requirements.txt~~
* VNC screenshots
* RDP screenshots
* Create appropriate responses after execution of operation (run scan, create database, etc.)
* Support additional masscan output options (binary, grepable, JSON, simple list)
* Host details page
* Logging
* External WSGI support
