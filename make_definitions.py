


import os, json, shutil

json_directory = "/home/bernard/exercise/jsonfiles"

# each 'section' is defined by a list of
# [ section time in seconds, section title, section text, mp3 file, wav file, ogg file]
# If sound files are not available, leave as empty strings


recovery1 = [20, "Recovery", "Take your time", "", "", ""]


exercises = [

  ['ex1',                      # filename
   'Exercise One',               # exercise title
   'Hardcore circuit training - ten exercise stations, four time intervals',        # exercise description
   [300, "Warm up", "Jogging on the spot or Skipping", "warmup.mp3", "warmup.wav"],
   [20, "Recovery", "Take your time", "stretchintro.mp3", "stretchintro.wav", ""],
   [20, "Stretches", "hamstrings - left", "", "", ""],
   [20, "Stretches", "hamstrings - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "calfs - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "calfs - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "thighs - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "thighs - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "rotate ankles", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "glutes - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "glutes - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "squats", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "lunges - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "lunges - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "shoulder rolls", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "triceps - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "triceps - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "hip flexor - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "hip flexor - right", "complete.mp3", "complete.oga", ""],
   [20, "Recovery", "Take your time", "intervalintro.mp3", "intervalintro.wav", ""],
   ['repeat', 4,           # four exercise intervals

       [[30, 40, 50, 60], "Legs", "Alternate, leg climber", "complete.mp3", "complete.oga", ""],
       [[30, 40, 50, 60], "Squats", "Get down", "complete.mp3", "complete.oga", ""],

       [10, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [10, "Recovery", "Take your time", "skipburp.mp3", "skipburp.wav", ""],

       [[30, 40, 50, 60], "Skipping", "Get that rope moving", "", "", ""],
       [[30, 40, 50, 60], "Burpees", "Pardon", "complete.mp3", "complete.oga", ""],

       [10, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [10, "Recovery", "Take your time", "dorsalcrunch.mp3", "dorsalcrunch.wav", ""],

       [[30, 40, 50, 60], "Dorsal raises", "Uh ?", "", "", ""],
       [[30, 40, 50, 60], "Crunches", "Grind those bones", "complete.mp3", "complete.oga", ""],

       [10, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [10, "Recovery", "Take your time", "froglunge.mp3", "froglunge.wav", ""],

       [[30, 40, 50, 60], "Frog leaps", "(plyo)", "", "", ""],
       [[30, 40, 50, 60], "Dynamic Lunges", "Woooo", "complete.mp3", "complete.oga", ""],

       [5, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [15, "Recovery", "Take your time", "rowpress.mp3", "rowpress.wav", ""],

       [[30, 40, 50, 60], "bent over row", "with weights", "", "", ""],
       [[30, 40, 50, 60], "Press-ups", "Option: Spiderman", "complete.mp3", "complete.oga", ""],

       [[5, 5, 5, 0], "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [[15, 15, 15, 0], "Recovery", "Take your time", "nextinterval.mp3", "nextinterval.wav", ""] 
   ],

   [180, "Cool Down", "Jogging on the spot", "coolstretch.mp3", "coolstretch.wav", ""],

   [20, "Stretches", "hamstrings - left", "finalstretches.mp3", "finalstretches.wav", ""],
   [20, "Stretches", "hamstrings - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "calfs - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "calfs - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "thighs - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "thighs - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "rotate ankles", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "glutes - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "glutes - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "squats", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "lunges - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "lunges - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "shoulder rolls", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "triceps - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "triceps - right", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "hip flexor - left", "complete.mp3", "complete.oga", ""],
   [20, "Stretches", "hip flexor - right", "complete.mp3", "complete.oga", ""],
   [10, "Finish", "All Done", "finish.mp3", "finish.wav", ""],
  ],

# further exercises would go here


]


if os.path.isdir(json_directory):
    # remove existing json files
    shutil.rmtree(json_directory)
os.mkdir(json_directory)


for obj in exercises:
    filename = os.path.join(json_directory, obj[0] + ".json")
    with open(filename, 'w') as fp:
        json.dump(obj, fp)


