import nltk 
from nltk.stem import PorterStemmer
from nltk.wsd import lesk 
import logging
import os


# Reads and returns the list of files from a directory
def read_directory(mypath):
    current_list_of_files = []

    while True:
        for (_, _, filenames) in os.walk(mypath):
            current_list_of_files = filenames
        logging.info("Reading the directory for the list of file names")
        return current_list_of_files


# Function you will be working with
def creating_subclusters(list_of_terms, name_of_file):
    # Your code that converts the cluster into subclusters and saves the output in the output folder with the same name as input file
    # Note the writing to file has to be handled by you.

    nltk.pos_tag(list_of_terms)
    sentence = " ".join(list_of_terms)
    list_of_terms2 = []
    stemmer = PorterStemmer()
    for word in list_of_terms:
        list_of_terms2.append(stemmer.stem(word))
   
    cluster = {}
    count = 0
    cluster[count] = []
    for k in range(len(list_of_terms2)):
        try:
            word = list_of_terms2[k]
        except IndexError:
            break
        a = lesk(sentence,word)
        cluster[count].append((list_of_terms[k]))
        for j in range(k+1,len(list_of_terms2)):
            try:
                word1 = list_of_terms2[j]
            except IndexError:
                break
            b = lesk(sentence,word1)
            try:
                if(a.path_similarity(b)>=0.5):
                    cluster[count].append((list_of_terms[j]))
                    count = count + 1
                    cluster[count]  = []
            except:
                continue
    completePath = os.path.join('output',name_of_file)
    file_object_w = open(completePath,'w')
    for key in cluster.keys():
        if(len(cluster[key])>1):
            for element in cluster[key]:
                file_object_w.write(element+' ')
            file_object_w.write('\n')
    file_object_w.close()
    pass


# Main function
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    # Folder where the input files are present
    mypath = "input"
    list_of_input_files = read_directory(mypath)
    for each_file in list_of_input_files:
        with open(os.path.join(mypath, each_file), "r") as f:
            file_contents = f.read()
        list_of_term_in_cluster = file_contents.split()

        # Sending the terms to be converted to subclusters in your code
        creating_subclusters(list_of_term_in_cluster, each_file)

