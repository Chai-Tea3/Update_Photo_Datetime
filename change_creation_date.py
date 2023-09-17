import os
from datetime import datetime
from exif import Image
from exif import DATETIME_STR_FORMAT

#Uses the date in the file name to update the photo metadata
def change_creation_date():
    try:
        working_dir = input("Please enter the exact path to the directory containing photos: ")

        files = os.listdir(working_dir) #Retrieves all the files in the directory
    
    except:
        print("Could not find directory. Format should be C:\ ... \ ")
        exit()

    for file in files:

        #Detects the naming convention of the photos (IMG_YYYYMMDD_#######)
        if(file.startswith("IMG_20")):
            year = int(file[4:8])
            month = int(file[8:10])
            day = int(file[10:12])
        elif(file.startswith("Screenshot_")):
           year = int(file[11:15])
           month = int(file[15:17])
           day = int(file[17:19])
        else:
            #If the file does not match the above parameters, skips to the next file
            continue

        datetime_original = datetime(year=year,month=month,day=day)
        image_path = "{}{}".format(working_dir,file)
    
        print(image_path)

        try:
            with open(image_path, "rb") as image_file:
                img = Image(image_file)

                #Sets the appropriate date into the file's metadata
                img.datetime_original = datetime_original.strftime(DATETIME_STR_FORMAT)
                img.datetime_digitized = datetime_original.strftime(DATETIME_STR_FORMAT)

                #Overwrites the old file with the new file
                with open(image_path, "wb") as new_image:
                    new_image.write(img.get_file())
                    new_image.close()

                image_file.close()               
        except:
            pass
    print("*** Done ***")

change_creation_date()