from curses.ascii import isalnum, isupper
import os
import re
from tabulate import tabulate

def remove_punctuations(document: str) -> str:
    allowed_characters = {" ", ".", ",", ";", "\n"}
    #We remove unnecesary, repeated texts
    document = document.replace("(inaudible)", "").replace("(Inaudible)", "")

    #If the document have a colon, we remove anything before it's appearance
    document = re.sub(r'^.*?:', ':', document)
    #If the document have leading or ending whitespaces, we remove them
    document = document.strip()

    #We initialize an empty string, here, we will store the data without the characters that are not alphanumeric
    filtered_document = ""
    
    #We iterate on each character of the token
    for i in range(0, len(document)):
        #Here, we avoid leading whitespaces by preventing them to be added if the filtered_document doesn't have any other character yet.
        if len(filtered_document) == 0 and document[i] == " ":
            continue

        #If the character is alphanumeric, we add it to the string.
        if document[i].isalnum() or document[i] in allowed_characters:
            filtered_document += document[i]
    
    #We remove the tracing whitespaces
    filtered_document = filtered_document.rstrip()
    
    return filtered_document.lower()



base_path = "transcriptions"
base_cleaned_path = "cleaned_transcriptions"
#We iterate on all paths within the folder
for i, element_in_dir in enumerate(os.listdir(base_path)):
    #We create the path of the element and new element by concatenating its base path
    path_of_element = base_path + "/" + element_in_dir
    path_of_cleaned_element = base_cleaned_path + "/" + element_in_dir
    
    #If the path is a file and it's a txt file
    if os.path.isfile(path_of_element) and ".txt" in path_of_element:

        #We open the origin file in read mode
        corpus = open(path_of_element, "r")

        #And we open the destination file in write mode
        cleaned_file = open(path_of_cleaned_element, "w")

        #We iterate on each line of the origin file
        for document in corpus.readlines():
            #We remove the punctuations on each line by calling our remove_punctuations method
            filtered_document = remove_punctuations(document) 
            #If the length of the returned string is bigger than  0, we add it to our destination file
            if len(filtered_document) > 0:
                cleaned_file.write(filtered_document + "\n")
        
        #We close the streams of both files
        corpus.close()
        cleaned_file.close()
