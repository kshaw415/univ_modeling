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
            PROB_TRANSMISSION = float(line[5])
            Asympt_ProbInfect = float(line[6])
            Sympt_ProbInfect = float(line[7])
            me_i = float(line[8])
            me_j = float(line[9])
            b0 = float(line[10])
            b1 = float(line[11])
            b2 = float(line[12])
            b3 = float(line[13])
            b4 = float(line[14])

            # Model Running Inputs
            num_agents = float(line[15])
            num_steps = float(line[16])

            # extra stuff i keep forgetting
            symptom_threshold = float(line[17]) # is this a pmf tho. 

        grid_dims = [min_x, max_x, min_y, max_y]
        file.close()
    
    return grid_dims, DISTANCE_THRESHOLD, PROB_TRANSMISSION, Asympt_ProbInfect, Sympt_ProbInfect, me_i, me_j, b0, b1, b2, b3, b4, num_agents, num_steps

# if __name__ == "__main__": 
#     barrier_path = "params2 - 10x10.csv"
#     data_path = ""
#     barriers = barrier_data(barrier_path)
#     grid_dims, DISTANCE_THRESHOLD, PROB_TRANSMISSION, \
#         Asympt_ProbInfect, Sympt_ProbInfect = parse_data(data_path)
    
