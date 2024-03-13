import csv 
import Barrier

def parse_data(file): 
    '''
    parses data from CSV file with format: (TBD)
    input: file --> str, location of csv file 
    # TODO: 
        output: 
            num_agents: int, number of agents desired 
            distance_threshold: int, distance (in feet) determining exposure 
            prob_transmission: float, probability of direct transmission given exposure 
    '''
    barriers = []
    with open(file, 'r') as file: 
        lines = csv.reader(file)
        next(lines, None)
        for line in lines: 
            A = [float(line[0]), float(line[1])]
            B = [float(line[2]), float(line[3])]
            print(A, B) 
            barriers.append(Barrier.Barrier(A, B))
        
        file.close() 
    return barriers 

if __name__ == "__main__": 
    file_path = "params2 - 10x10.csv"

    barriers = parse_data(file_path)
    print(barriers)
