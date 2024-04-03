import csv 
import Barrier

def barrier_data(file): 
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
            # Barrier Data 
            A = [float(line[0]), float(line[1])]
            B = [float(line[2]), float(line[3])]
            barriers.append(Barrier.Barrier(A, B))

        file.close() 
    return barriers 


def parse_data(file): 
    '''
    parses rest of data with thresholds, etc. 
    '''
    with open(file, 'r') as file: 
        lines = csv.reader(file)
        next(lines, None) # header 
        for line in lines: 
            # Grid Dimensions
            min_x = float(line[0])
            max_x = float(line[1])
            min_y = float(line[2])
            max_y = float(line[3])

            # Thresholds
            DISTANCE_THRESHOLD = float(line[4])
            Symptom_threshold = float(line[5])
            masking = bool(line[6])
            immunity = bool(line[14])
            b0 = float(line[7])
            b1 = float(line[8])
            b2 = float(line[9])
            b3 = float(line[10])
            b4 = float(line[11])

            # Model Running Inputs
            num_agents = int(line[12])
            num_steps = int(line[13])

        xbounds = [min_x, max_x]
        ybounds = [min_y, max_y]
        file.close()
    
    return xbounds, ybounds, DISTANCE_THRESHOLD, Symptom_threshold, masking, b0, b1, b2, b3, b4, num_agents, num_steps, immunity

# if __name__ == "__main__": 
#     barrier_path = "params2 - 10x10.csv"
#     data_path = ""
#     barriers = barrier_data(barrier_path)
#     grid_dims, DISTANCE_THRESHOLD, PROB_TRANSMISSION, \
#         Asympt_ProbInfect, Sympt_ProbInfect = parse_data(data_path)
    
