
import os, json, shutil

json_directory = "/home/bernard/git/exercise/jsonfiles"

# each 'section' is defined by a list of
# [ section time in seconds, section title, section text, mp3 file, wav file, ogg file]
# If sound files are not available, leave as empty strings

# example:
# [20, "Recovery", "Take your time", "", "", ""]

# if a section is in a repeated part, then the time value can either be a number as above
# which will be repeated, or it can be a list of numbers, with list length matching
# the number of repeats

# example:
# [[30, 40, 50, 60], "Recovery", "Take your time", "", "", ""]


exercises = [

  ['ex1',                        # reference string, use ex2, ex3, .. etc for further exercises
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
   [5, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
   [15, "Recovery", "Take your time", "intervalintro.mp3", "intervalintro.wav", ""],

   ['repeat', 4,           # four exercise intervals

       [[30, 40, 50, 60], "Legs", "Alternate, leg climber", "", "", ""],
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
['ex2',                        # reference string, use ex2, ex3, .. etc for further exercises
   'Exercise Two',               # exercise title
   'More Hardcore circuit training - ten exercise stations, four time intervals',        # exercise description

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
   [20, "Stretches", "inner thigh stretch", "","",""],
   [5, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
   [15, "Recovery", "Take your time", "intervalintro.mp3", "intervalintro.wav", ""],

   ['repeat', 4,           # four exercise intervals

       [[30, 40, 50, 60], "Tricep Dips", "Deeply 'Dippy'", "", "", ""],
       [[30, 40, 50, 60], "Overhead Raises", "Go on.. lift a small weight too", "complete.mp3", "complete.oga", ""],

       [10, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [10, "Recovery", "Take your time", "skipburp.mp3", "skipburp.wav", ""],

       [[30, 40, 50, 60], "Woodchopper", "Chop chop...", "", "", ""],
       [[30, 40, 50, 60], "Press Ups with Leg Raises", "One leg at a time please!", "complete.mp3", "complete.oga", ""],

       [10, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [10, "Recovery", "Take your time", "dorsalcrunch.mp3", "dorsalcrunch.wav", ""],

       [[30, 40, 50, 60], "Skating", "Get arms and legs moving", "", "", ""],
       [[30, 40, 50, 60], "Burpees", "No pain, no gain", "complete.mp3", "complete.oga", ""],

       [10, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [10, "Recovery", "Take your time", "froglunge.mp3", "froglunge.wav", ""],

       [[30, 40, 50, 60], "Bent Over Row", "with weights", "", "", ""],
       [[30, 40, 50, 60], "Squats", "Never mind the energy release", "complete.mp3", "complete.oga", ""],

       [5, "Recovery", "Take your time", "complete.mp3", "complete.oga", ""],
       [15, "Recovery", "Take your time", "rowpress.mp3", "rowpress.wav", ""],

       [[30, 40, 50, 60], "Worm", "Not a parasite!", "", "", ""],
       [[30, 40, 50, 60], "Sprinting on the Spot", "One, two, one, two", "complete.mp3", "complete.oga", ""],

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
   [20, "Stretches", "inner thigh stretch", "","",""],
   [10, "Finish", "All Done", "finish.mp3", "finish.wav", ""],

]

]


if os.path.isdir(json_directory):
    # remove existing json files
    shutil.rmtree(json_directory)
os.mkdir(json_directory)

# Save each exercise in a json file

for obj in exercises:
    filename = os.path.join(json_directory, obj[0] + ".json")
    with open(filename, 'w') as fp:
        json.dump(obj, fp)


