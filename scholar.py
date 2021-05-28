from scholarly import scholarly
import datetime
import pickle

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
        self.total_citations=total_citations,
        self.authors=authors
    
    def __str__(self):
        return str(self.date) + ":" + str(self.total_citations) + ":" + str(self.authors)
    



def query_ucsd_scholars(scholar_names):
    affiliation = "UC San Diego"
    unknown_authors = []
    accepted_authors = []
    total_citations = 0
    for sa in people:
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
    le = LogEntry(date,total_citations,accepted_authors)
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

#TODOS
#scrape the total citations for a single person
#make a list of every author in the department
#scrape the total citations for every author in the department
#scrape the names from the sysnet site
#calculate the daily citation count.
    #write the scrape date to a log, author name, citation count perhaps
    #create python object to pickel for this to the log.
    #query the log
faculty = ["Joseph Pasquale", "Stefan Savage", "Aaron Schulman", "Alex C. Snoeren", "Geoffrey M Voelker", "Yiying Zhang", "Yuanyuan Zhou"]
faculty = ["Yiying Zhang", "Yuanyuan Zhou"]
postdocs = ["Grant Ho"]
phds = ["Gautam Akiwate","Lixiang Ao","Nishant Bhaskar","Zachary Blanco","Sunjay Cauligi","Sam Crow","Rajdeep Das","Alex Forencich","Alex Gamero-Garrido","Yibo Guo","Hadi Givehchian","Stewart Grant","Zhiyuan Guo","Haochen Huang","Yutong Huang","Evan Johnson","William Lin","Enze Alex Liu","Rob McGuinness","Ariana Mirian","Matthew Parker","Eric Mugnier","Audrey Randall","Keegan Ryan","Tianyi Shan","Yizhou Shan","Laura Shea","Bingyu Shen","Mingyao Shen","George Sullivan","Alisha Ukani","Shu-Ting Wang","Yudong Wu","Chengcheng Xiang","Anil Yelam","Zesen Zhang","Li Zhong"]

people = []
people.extend(faculty)
print(people)

filename = "citation.log"
complete_log = get_log_from_disk(filename)
le = query_ucsd_scholars(people)
complete_log.append(le)
write_log_to_disk(filename,complete_log)

for l in complete_log:
    print(l)


print(le)