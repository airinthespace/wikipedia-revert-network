from datetime import datetime
from math import log10

class RevertNetworkBuilder():
    
    def get_data(self, fname):
        """Open Wikipedia revert data in file fname and return
        list of formatted values."""
        
        with open(fname, 'r') as f:
            f.readline() 

            data = []
            title_indexed_data = {}
            for edit in f.readlines():
                title, dt, rev, version, user = edit.strip().split('\t')
                title = title.strip()
                record = [title, datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"), 
                            int(rev), int(version), user]
                data.append(record)
                if title not in title_indexed_data:
                    title_indexed_data[title] = []
                title_indexed_data[title].append(record)
        # Sort the matrix based on the second column (datetime)
        sorted_matrix = sorted(data, key=lambda row: row[1])        
        return (title_indexed_data, sorted_matrix)

    def update_num_of_edits(self, user, num_of_edits):
        """
        Update the number of edits for user in dictionary num_of_edits.
        
        If the user is already in the num_of_edits dictionary, increment their count by 1.
        If the user is not in the num_of_edits dictionary, add them with a count of 1.
        """
        if user in num_of_edits:
            num_of_edits[user] += 1
        else:
            num_of_edits[user] = 1
        
        return num_of_edits

    def create_network(self, file_path):
        """ 
        Create a network of reverts from the data in file_path. 
        """
        (title_indexed_data, sorted_matrix) = self.get_data(file_path)
        num_of_edits = {}
        network = []
        nodes = []
        for edit_record in sorted_matrix:
            editor = edit_record[4]
            num_of_edits = self.update_num_of_edits(editor, num_of_edits)
            # If revert equals to 1
            if edit_record[2]:
                # Creating article_data which is the list of all edits for the article
                article_data = title_indexed_data[edit_record[0]] 
                
                # Finding the index of the reverted edit
                revert_index = article_data.index(edit_record)
                temp_index = revert_index + 1
                while article_data[temp_index][3] != edit_record[3]:
                    temp_index += 1

                reverted_index = temp_index - 1
                    
                # If the edit is not self-reverted and reverted make an unmeaningful change not adding it to the network
                reverted = article_data[reverted_index][4]
                if editor != reverted and edit_record[3] != article_data[reverted_index][3]:
                    # Creates an edge list, where an edge goes from the "reverter" to the "reverted"
                    edge = {
                        'reverter': editor,
                        'reverted': reverted,
                        'time': edit_record[1],
                        'reverter_seniority': log10(num_of_edits[editor]),
                        'reverted_seniority': log10(num_of_edits[reverted]),
                    }
                    network.append(edge)
                    
                    # Add nodes to the list of nodes if they are not already in it 
                    if editor not in nodes:
                        nodes.append(editor)
                    if reverted not in nodes:
                        nodes.append(reverted)

        return (network, nodes)