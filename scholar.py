from scholarly import scholarly
import datetime
import pickle

import os.path
from os import path
import sys

import numpy as np
import matplotlib.pyplot as plt

#TODOS
#scrape the total citations for a single person
#make a list of every author in the department
#scrape the total citations for every author in the department
#scrape the names from the sysnet site
#calculate the daily citation count.
    #write the scrape date to a log, author name, citation count perhaps
    #create python object to pickel for this to the log.
    #query the log

class Scholar:
    def __init__(self, name, citations):
        self.name = name
        self.citations = citations
    def __str__(self):
        return "(" + str(self.name) + "," + str(self.citations) + ")"
    def __repr__(self):
        return str(self)

class LogEntry:
    def __init__(self, date ,total_citations, authors):
        self.date=date
        self.total_citations=total_citations
        self.authors=authors
    
    def __str__(self):
        return str(self.date) + ":" + str(self.total_citations) + ":" + str(self.authors)

faculty = ["Joseph Pasquale", "Stefan Savage", "Aaron Schulman", "Alex C. Snoeren", "Geoffrey M Voelker", "Yiying Zhang", "Yuanyuan Zhou"]
postdocs = ["Grant Ho"]
phds = ["Gautam Akiwate","Lixiang Ao","Nishant Bhaskar","Zachary Blanco","Sunjay Cauligi","Sam Crow","Rajdeep Das","Alex Forencich","Alex Gamero-Garrido","Yibo Guo","Hadi Givehchian","Stewart Grant","Zhiyuan Guo","Haochen Huang","Yutong Huang","Evan Johnson","William Lin","Enze Alex Liu","Rob McGuinness","Ariana Mirian","Matthew Parker","Eric Mugnier","Audrey Randall","Keegan Ryan","Tianyi Shan","Yizhou Shan","Laura Shea","Bingyu Shen","Mingyao Shen","George Sullivan","Alisha Ukani","Shu-Ting Wang","Yudong Wu","Chengcheng Xiang","Anil Yelam","Zesen Zhang","Li Zhong"]

citation_log_file = "citation.log"
citation_chart_file = "citations.pdf"


def query_ucsd_scholars(scholar_names):
    affiliation = "UC San Diego"
    unknown_authors = []
    accepted_authors = []
    total_citations = 0
    for sa in scholar_names:
    #for sa in full_list:
        try:
            search_query = scholarly.search_author(sa + "," + affiliation)
            author = scholarly.fill(next(search_query))
            #print(author)
            author_cites = 0
            for pub in author['publications']:
                #print(pub['num_citations'])
                author_cites = author_cites + int(pub['num_citations'])
            print(sa,author_cites)
            total_citations = author_cites + total_citations
            scholar = Scholar(sa,author_cites)
            accepted_authors.append(scholar)
        except:
            print("Author: ",sa," not found and error thrown")
            scholar = Scholar(sa,0)
            unknown_authors.append(sa)
    print(total_citations)

    date = datetime.datetime.now()
    print("Unknown Authors: ", unknown_authors)
    print("Accepted Authors: ", accepted_authors)
    accepted_authors.extend(unknown_authors)
    le = LogEntry(date,int(total_citations),accepted_authors)
    return le

def get_log_from_disk(filename):
    try:
        file = open(filename,'rb')
        log = pickle.load(file)
        file.close()
        return log
    except: 
        print ("ERROR: Unable to extract log from file: ",filename)
        return []

def write_log_to_disk(filename, log):
    try:
        file = open(filename,'wb')
        pickle.dump(log,file)
        file.close()
    except: 
        print ("ERROR: Unable to write to file: ",filename)

def update_log(log_file):
    people = []
    people.extend(faculty)
    people.extend(postdocs)
    people.extend(phds)
    print(people)

    filename = log_file
    complete_log = get_log_from_disk(filename)
    le = query_ucsd_scholars(people)
    print("NEW LOG ENTRY ",le)
    complete_log.append(le)
    write_log_to_disk(filename,complete_log)

    for l in complete_log:
        print(l)

def get_daily_diff(log_file):
    filename = log_file
    complete_log = get_log_from_disk(filename)
    print(complete_log)
    if(len(complete_log) < 2):
        print("Log to short to make diff")
        return -1

    b = complete_log[len(complete_log)-1]
    a = complete_log[len(complete_log)-2]
    print("Ultimate: ", b)
    print("Penultimate: ", a)
    return b.total_citations - a.total_citations

def plot_citations_per_day(log_file,plot_file):
    filename = log_file
    complete_log = get_log_from_disk(filename)
    x = []
    y = []
    last_days_citations=0
    #todo actually take the date into account
    for le in complete_log:
        if last_days_citations != 0:
            x.append(le.date)
            y.append(le.total_citations - last_days_citations)
        last_days_citations = le.total_citations
    print(x,y)

    #do the plotting
    plt.plot(x,y, marker="x")
    plt.savefig(plot_file)

def parse_args():
    dir_path = ""
    if len(sys.argv) != 2:
        dir_path = os.getcwd()
        print("No path suppiled writting to this directory", path)
        return path
    else:
        test_path = sys.argv[1]
        if not path.exists(test_path):
            dir_path = os.getcwd()
            print("Argument ", test_path, "is not a valid directory, writing to this directory ", path)
        dir_path = test_path
    return dir_path


#the only argument that I'm gong to take is the path to the directory we want to write to.
dir_path = parse_args()

citation_log_file=dir_path+"/"+citation_log_file
citation_chart_file=dir_path+"/"+citation_chart_file

update_log(citation_log_file)
plot_citations_per_day(citation_log_file,citation_chart_file)