# Movie Trailer Website

Script that generates an analysis of the logs for the newspaper website.

## Installation
Running this program requires Python 3 and PostgreSQL to be installed on the target system. The files newsdata.sql must also be download from the Udacity source material.

Clone the GitHub repository in a directory of your choosing to install this project. 

Before running the script please load the data into the "news" database. To load the data, use the command psql -d news -f newsdata.sql.

```bash
git clone https://github.com/ajais/logs_analysis.git
```

## Usage
In the terminal go to the folder where the project is located and type the following command:

```bash
python3 logs_analysis.py
```
The 3 most popular articles of all time, the most popular authors of all time and the days where more than 1% of requests lead to errors will be displayed in the command line output. A text file "output.txt" with this information will also be generated.

## References
Udacity Full Stack Web Developper NanoDegree