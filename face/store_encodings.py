#store the encodings and names of all criminals in encoding.txt

import pickle

from set_mongo import criminal_records,candidate_records

def store():
    print("enter into store function")
    knownEncodings=[]
    knownNames=[]

    #get all criminal records from mongodb collection
    results=criminal_records.find({})
    for result in results:
      knownEncodings.append(result["encodings"])
      knownNames.append(result["name"])

    #using pickle to write data in binary mode.
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("encoding.txt", "wb")
    f.write(pickle.dumps(data))
    f.close()

    print("encodings written to file")
