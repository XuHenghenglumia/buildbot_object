import csv
import os.path

def export_data(head,data,filename):
    with open(filename, 'a', newline='') as csvfile:
        writter = csv.writer(csvfile)
        if not os.path.getsize(filename):
            writter.writerow(head)
        writter.writerow(data)