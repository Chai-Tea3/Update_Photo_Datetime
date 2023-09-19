import os
from datetime import datetime
from exif import Image
from exif import DATETIME_STR_FORMAT

#Stores files from the recursive method in a list
list_of_files = []

#Recursive method that retrieves all the files from the parent directory and all sub-directories
def get_file_dir(path):
    for file_dir in os.listdir(path):
        cur_path = os.path.join(path,file_dir) #Appends the name of the current file/directory to the end of the parent path

        if(os.path.isdir(cur_path)): #If it is a directory...
            get_file_dir(cur_path) #Recursive call
        
        else: #If it is a file, adds to the list of files
            list_of_files.append(cur_path)


#Extracts the date and time from the file name and returns an array in the order year, month, day, hour, min, sec
def get_date_time(file_name):
    index = file_name.rfind("_", 0, len(file_name) - 10) #Finds the last "_" in the path/file name

    year = int(file_name[index - 8:index - 4])
    month = int(file_name[index - 4:index - 2])
    day = int(file_name[index - 2:index])
    hour = int(file_name[index + 1:index + 3])
    min = int(file_name[index + 3:index + 5])
    sec = int(file_name[index + 5:index + 7])

    return [year,month,day,hour,min,sec]


#Uses the date in the file name to update the photo metadata
def change_creation_date():

    working_dir = input("Please enter the exact path to the directory containing photos: ")
    if(os.path.isdir(working_dir)):
        get_file_dir(working_dir)
    else:
        print("Could not find directory. Format should be C:\ ... \ ")


    for file in list_of_files:

        #Detects the naming convention of the photos (IMG_YYYYMMDD_HHMMSS)
        if(file.rfind("IMG_20") > 0):
            dt = get_date_time(file)
        elif(file.find("Screenshot_") > 0):
            dt = get_date_time(file)
        elif(file.find("20") == (file.find(".") - 15)):
            dt = get_date_time(file)
        else:
            #If the file does not match the above parameters, skips to the next file
            continue

        datetime_original = datetime(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5])

        try:
            with open(file, "rb") as image_file:
                img = Image(image_file)

                #Sets the appropriate date into the file's metadata
                img.datetime_original = datetime_original.strftime(DATETIME_STR_FORMAT)
                img.datetime_digitized = datetime_original.strftime(DATETIME_STR_FORMAT)

                #Overwrites the old file with the new file
                with open(file, "wb") as new_image:
                    new_image.write(img.get_file())
                    new_image.close()

                image_file.close()               
        except:
            pass

        print(file)

    print("*** Done ***")

change_creation_date()