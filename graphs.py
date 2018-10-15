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
        query = "match (n:processed) with n limit 100000 remove n:processed return count(*) as processed"
        if query != "":
            values = graph.run(query).data()
            value = values[0]["processed"]
            while(value==100000):
                values = graph.run(query).data()
                value = values[0]["processed"]

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
                            query = "MATCH (a:"+csv[key] + ") WITH a MATCH (p:" + file + "{" + word + ": a." + word +"} ) WHERE NOT p:processed WITH a, p LIMIT 100000 MERGE (p) - [:child_of] -> (a) SET p:processed RETURN COUNT(*) AS processed"
                            #query = "MATCH (p:" + csv[key] + ") with p MATCH (c:"+ file + "{" + word + ": p." + word +"}) where not p:divya with c,p limit 100000 merge (p)-[:divya_of]->(c) set p:divya return count(*) as divya"
                            values = graph.run(query).data()
                            value = values[0]["processed"]
                            print value
                            while(value==100000):
                                print value
                                values = graph.run(query).data()
                                value = values[0]["processed"]
                            print value
                            deleteProcessed()
                            print "Deleted processed"
                            print csv[key] + word

def delete():
        query = "MATCH ()-[r:child_of]-() with r limit 100000 DELETE r return count(r) as deletedrelations"
        if query != "":
            values = graph.run(query).data()
            value = values[0]["deletedrelations"]
            while(value==100000):
                values = graph.run(query).data()
                value = values[0]["deletedrelations"]
                print value
            print "deleted"

graph = Graph()
exportCSV("sch.txt")
relationships()
