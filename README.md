# univ_modeling
Modeling University disease transmission with ABMs

Goal/Focus: 
- go in depth in transmission of COVID specifically 
    - transmission dynamics 
- add in vaccination status
- add in masking as a toggle (yes masks, masking in X scenarios?)
- analyzing data received from ABM (figures on time-based plots, etc. )  

## To-Do: 
- det_transmission: return True/False based on infected status (can seem misleading with function name)
- Each time step need to calculate exposure status (ie after 3 days exposure no transmission, go back to susceptible) 