from py2neo import Graph, Node, Relationship

def exportCSV(file):
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            i = 0
            query = '''USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"file:///Users/sarvani/Desktop/workspace/chembl/Csv_files/'''
            for word in line.split():
                if i==0:
                    query = query + word + ".csv\" AS row FIELDTERMINATOR '\t' CREATE (:"+word+"{"
                    i=i+1
                else:
                    query = query + word + ":row." + word + ", "
            query = query[:-2]
            query = query + "});"
            i=0
            graph.run(query)

def deleteProcessed():
        query = "match (n:Processed) with n limit 100000 remove n:Processed return count(*) as processed"
        if query != "":
            value = graph.run(query)
            while(value==100000):
                value = graph.run(query)


def relationships():
    csv = []
    keys = []
    with open("primarykey.txt") as f:
        lines = f.readlines()
        for line in lines:
            i=0
            for word in line.split():
                if i==0:
                    csv.append(word)
                    i=i+1
                else:
                    keys.append(word)
    with open("sch.txt") as f:
        lines = f.readlines()
        for line in lines:
            i=0
            query = ""
            for word in line.split():
                if i==0:
                    file = word
                    i=i+1
                else:
                    for key in range(0, len(keys)):
                        if keys[key] == word and csv[key]!=file:
                            query = "MATCH (p:" + csv[key] + ") with p MATCH (c:"+ file + "{" + word + ": p." + word +"}) where not p:Processed with c,p limit 100000 merge (p)-[:child_of]->(c) set p:Processed return count(*) as processed"
                            value = graph.run(query)
                            while(value==100000):
                                value = graph.run(query)
                            deleteProcessed()

graph = Graph()
#exportCSV("sch.txt")
relationships()
