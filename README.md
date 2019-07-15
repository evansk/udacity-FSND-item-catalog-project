# Library Catalog
## Udacity Full Stack Nano Degree Item Catalog Project

## About
This is a RESTful web application built using the Flask Framework and SQLAlchemy. It accesses a database that populates each function with the required data. Additionally it provides CRUD functionality and implements oAuth2 using Google Accounts.

This web application is designed as an internal library catalog. A librarian can browse through the books, authors, and genres available at the library. After logging in they can also see patron information and which books are currently checked out and by whom. They can also check out and return books for patrons as well as update book and patron information.

### Features
- CRUD support using Flask and SQLAlchemy
- JSON endpoints
- Implements oAuth using the Google Sign-In API
- Authentication and Authorization checks

## Getting Started

### Prerequisites
- Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). This software allows you to run the virtual machine
- Download and Install [Vagrant](https://www.vagrantup.com/). This software sets up the virtual machine and allows you to share files between the VM and your host file system
- [Udacity FSND Vagrant File](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) - You can download the Udacity Vagrant file or fork it from this [Github repository](https://github.com/udacity/fullstack-nanodegree-vm)
- Python 2.7
- Update Flask using `pip install --upgrade flask`
- A Google account for logging in

### VM and File Set-up

1. After downloading the necessary files and software, navigate to the `vagrant` directory in the Udacity Vagrant file.
2. Use the `vagrant up` command to install the virtual machine. (This may take a few minutes)
3. Use `vagrant ssh` to log in to the virtual machine
4. Download or clone the git repository into the `vagrant` directory
5. Navigate to the `catalog` directory
6. Use `python database_setup.py` then `python library_data.py` to set up the database

## Run the Project
1. Use `python library_catalog.py` to run the program
2. Visit `http://localhost:8000` in your favorite web browser
