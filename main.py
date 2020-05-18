import os
import pickle


class SearchEngine:
    def __init__(self):
        self.file_index = []  # directory listing returned by os.walk()
        self.results = []  # search results returned from search method
        self.matches = 0  # count of records matched
        self.records = 0  # count of records searched

    def create_new_index(self, root_path):
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]
        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        try:
            with open('file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)

        except:
            self.file_index = []

    def search(self, term, search_type='contains'):
        self.results.clear()
        self.matches = 0
        self.records = 0

        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if (search_type == 'contains' and term.lower() in file.lower() or
                    search_type == 'startswith' and file.lower().startswith(term.lower()) or
                    search_type == 'endswith' and file.lower().endswith(term.lower())):

                    result = path.replace('\\', '/') + '/' + file
                    self.results.append(result)
                    self.matches += 1
                else:
                    continue

        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')


def main():
    s = SearchEngine()
    s.load_existing_index()  # path of the directory
    s.search('calculator')    # search term

    print()
    print('>> There were {:,d} matches out of {:,d} records searched'.format(s.matches, s.records))
    print()
    print('>> This query produced the following matches: \n')
    for match in s.results:
        print(match)


main()


