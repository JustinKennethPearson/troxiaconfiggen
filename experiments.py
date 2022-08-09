# Expeirments in Python for Auto Troxia
# current status
# create_config generates lists of things that can be used for the
# script field in the config objectt. You just need to turn it into JSON
# and see if it works.
# You need to write a function that checks that there are sound files
# and orbital files in the correct directory.
# Go through the satellite directory and delete things that don't
# have the corresponding file.
# create_config() generates mutlple lists of thing to schedule
# when the maximum number of spat inputs is reachered. 


import pandas as pd
import os.path
import copy
import sys
import json
internal_spreadsheet_file = './satcat2_80_VICC.ods'
internal_cvs_file = './satcat.csv'
def convert_to_csv(write_csv=True,
                   spreadsheet_file=internal_spreadsheet_file,
                   cvs_file=internal_cvs_file
                   ):
    print("Reading the spreadsheet this could take some time.")
    df = pd.read_excel(spreadsheet_file, engine='odf')
    print (df.head)
    print("File read.\n")
    # Project down on the columns we need.
    new_df = df[['Unnamed: 0' , 'Unnamed: 4','Unnamed: 30', 'Unnamed: 31']]
    # If there is an X or Kepler we keep it.
    keep =  new_df[(new_df['Unnamed: 0'] == "X") |  (new_df['Unnamed: 0'] == "Kepler")  ]
    keep = keep[['Unnamed: 4','Unnamed: 30', 'Unnamed: 31']]
    # Now we want to rename the columns
    keep = keep.rename(columns={'Unnamed: 4': 'SNDNAME' , 'Unnamed: 30' : 'Launch' ,
                        'Unnamed: 31': 'Delaunch' })
    if write_csv : 
        print("Writing to CSV.\n")
        keep.to_csv(cvs_file)
    return keep


#Reads the csv file into a panda data frame.
def read_csv(cvs_file=internal_cvs_file):
    print("Reading the csv file.")
    df = pd.read_csv(cvs_file)
    return df 

# Use dictionary comprehension and csv reader to make a dictionary out of
# the file.

#delaunch is the day we declaunce
def make_dict(df) :
    print("Turning the panda dataframe into a dictionary")
    # df is a panda data from
    sat_dict = {}
    for index , row  in df.iterrows() :
        l = int(row['Launch'])
        d = int(row['Delaunch'])
        info = {'Launch':l , 'Delaunch':d}
        sat_dict[row['SNDNAME']] =  info        
    return(sat_dict) 




#####
# Check what satellites actually have data files and delete them.

def check_exists(sat_dict,snd_file_dir,orb_file_dir,verbose=True) :
    print("Checking sound and orbit files.")
    sats_to_delete = []
    for sat in sat_dict :
        snd_file_name = snd_file_dir + sat + ".aif"
        orb_file_name = orb_file_dir + sat + ".txt"
        to_delete = False
        if not os.path.exists(snd_file_name) :
            if verbose : 
                print("Missing sound file for " , sat)
            to_delete = True
        if not os.path.exists(orb_file_name) :
            if verbose : 
                print("Missing orbit file for " , sat)
            to_delete = True
        if to_delete :
            sats_to_delete.append(sat)
    for sat in sats_to_delete :
        del sat_dict[sat]
    return sat_dict
        
# This is really bad programming, but I only do it once :-),
# I should really calculate it when I'm creating the dictionary
# and build some data structur.

#Returns the max number of days.

def max_days(sat_dict) :
    max_num_days = 0
    for sat  in sat_dict :
        info = sat_dict[sat] 
        if info['Delaunch'] > max_num_days : 
            max_num_days =  info['Delaunch'] 
    return (max_num_days)

# Takes a sat_dict and produces an array (list)
# Thinking about this, I can't think of a snappy fast an efficient
# algorithm than the inefficient quadaratic one below

def make_day_profile(sat_dict):
    print("Working out what is in space on what days.")
    max_num_days = max_days(sat_dict)
    day_profile = [None] * (max_num_days  + 1)
    for sat in sat_dict :
        current_sat = sat_dict[sat]
        current_launch   = current_sat['Launch']
        current_delaunch = current_sat['Delaunch']
        for i in range(current_launch,current_delaunch + 1) :
            if (day_profile[i] == None) :
                day_profile[i] = set([str(sat)])
            else:
                day_profile[i].add(str(sat))
    return(day_profile)


def max_number_in_orbit(day_profile) :
    max_in_orbit = 0
    for i in day_profile :
        if i != None : 
            if len(i) > max_in_orbit :
                max_in_orbit = len(i)
    return max_in_orbit


def create_profile_for_plotting(day_profile) :
    plt_profile = []
    for i in day_profile :
        if ( i == None) :
            plt_profile.append(0)
        else:
            plt_profile.append(len(i))
    return(plt_profile)


# Assumes that the cvs file has been created.


# Get rid of this soon.

def create_config() :
    csv_df   = read_csv()
    sat_dict = make_dict(csv_df)
    sat_dict = check_exists(sat_dict, "/Users/justin/Dropbox/MaxMSP/G/NotReady/Sounds/" , "/Users/justin/Dropbox/MaxMSP/G/NotRead/Orbits")
    day_profile = make_day_profile(sat_dict)
    print("Done preprocessing.")
    # Hard wireded. Change later.
    start_day = 1
    end_day = 200
    max_spat_inputs = 2
    next_free_spat_input = 0
    return(create_config_internal(sat_dict,day_profile,
                                  start_day,end_day,max_spat_inputs))


def create_config_internal(sat_dict,day_profile,
                           start_day,end_day,max_spat_inputs,deep_copy=True) :
    if deep_copy : 
        day_profile_copy = copy.deepcopy(day_profile)
        print("Done with the deepcopy")
    else :
        day_profile_copy = day_profile 
    sats_left = True
    dict_list = []
    while sats_left :
        print("Starting a new run through the days.")
        spat_script = config_run_through_days(day_profile_copy, sat_dict,
                                              start_day,end_day,max_spat_inputs)
        if spat_script : # If the list is non empty.
            return_dict = { 'script' : spat_script }
            dict_list.append(return_dict)
        else : # if the list is empty then exit the loop.
            sats_left = False
    return(dict_list)

                    

### Warning this function has multiple exit points
### I have a return inside the loop because I can't get
### the break statememt to work properly.
### Ugly, but otherwise I would have to refactor with lots
### more smaller functions.
def config_run_through_days(day_profile_copy ,sat_dict ,
                            start_day , end_day , max_spat_inputs ) :
    spat_script = []
    print("Runing through the days again")
    next_free_spat_input = 0 
    for day in range(start_day,end_day+1) :
        if day_profile_copy[day] != None :
                current_day_set = set(day_profile_copy[day])
                for sat in current_day_set :
#                    print("day = " , day , "sat = " , sat)
                    sat_data = (sat_dict[sat])
                    entry = [sat+".txt",sat+".aif",
                             next_free_spat_input , sat_data['Launch'] ,
                             sat_data['Delaunch'] ]
                    spat_script.append(entry)
                    # Now delete the current sat from the rest of the days.
                    for remove_day in range(day , end_day + 1) :
                        set_to_remove = day_profile_copy[remove_day]
                        set_to_remove.discard(sat)
                    #If we reach the max number of inputs
                    #then rest back to 0 and leave this loop.
                    next_free_spat_input = next_free_spat_input + 1
                    if next_free_spat_input == max_spat_inputs:
                        print("Max spat inputs reached.")
                        next_free_spat_input = 0
                        return(spat_script)
    return(spat_script)
    


# Function to write out file names.
def write_config_file(dict_list , snd_file_dir , orb_file_dir,config_base) :
    print("Generating Json files.")
    print(len(dict_list))
    for index , config_dict in enumerate(dict_list) :
        config_name = config_base + "_" + str(index) + ".json"
        print("Current file name = " , config_name)
        config_dict["snd_file_path"] = snd_file_dir
        config_dict["orb_file_path"] = orb_file_dir
        json_object = json.dumps(config_dict, indent = 2)
        with open(config_name , 'w') as f :
            f.write(json_object)

### Main function



def main_check() :
    if (len(sys.argv) == 5) : 
        spreadsheet_file = sys.argv[2]
        sound_file_dir   = sys.argv[3]
        orbit_file_dir   = sys.argv[4]
        df = convert_to_csv(False, spreadsheet_file)
        sat_dict = make_dict(df)
        check_exists(sat_dict , sound_file_dir , orbit_file_dir)
    else :
        print("Not enough arguments : "
              + sys.argv[0] + " check spreadsheet sound_dir orb_dir ")    

def main_config() :
    if (len(sys.argv) == 7) : 
        spreadsheet_file = sys.argv[2]
        sound_file_dir   = os.path.abspath(sys.argv[3]) + "/"
        orbit_file_dir   = os.path.abspath(sys.argv[4]) + "/"
        config_base_name = sys.argv[5]
        max_max_inputs   = int(sys.argv[6])
        print("Sound file dir = " , sound_file_dir)
        print("Orbit file dir = " , orbit_file_dir)
        df = convert_to_csv(False, spreadsheet_file)
        sat_dict = make_dict(df)
        sat_dict = check_exists(sat_dict , sound_file_dir ,
                                orbit_file_dir , False)
        max_number_days = max_days(sat_dict)
        print("Maximum number of days = " , max_number_days)
        day_profile = make_day_profile(sat_dict)
        dict_list = create_config_internal(sat_dict , day_profile ,
                                           1 , max_number_days,
                                           max_max_inputs , False)

        write_config_file(dict_list ,
                          sound_file_dir , orbit_file_dir,
                          config_base_name)        
    else :
        print("Not enough arguments : "
              +  sys.argv[0]
              + " check spreadsheet sound_dir orb_dir base_config max_inputs")    
def main() :
    if sys.argv[1]  == "check" :
        main_check()
    if sys.argv[1] == "create" :
        main_config()
    if sys.argv[1] == "help" :
        print("Some useful help information will come.")
    
    
if __name__ == '__main__':
    main()
    