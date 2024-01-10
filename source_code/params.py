def parse_data(file): 
    '''
    parses data from CSV file with format: (TBD)
    input: file --> str, location of csv file 
    output: 
        num_agents: int, number of agents desired 
        distance_threshold: int, distance (in feet) determining exposure 
        prob_transmission: float, probability of direct transmission given exposure 
    '''
    with open(file, 'r') as file: 
        lines = file.readlines()
        file.close() 

    
