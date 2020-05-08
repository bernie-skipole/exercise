

############
#
# when deploying, use this shebang, and make executable
#
#!/home/master/exvenv/bin/python3




import os, sys, json


######### If using local development version of skipole
#
# skipole_package_location = "/home/bernard/git/skipole"
#
# if skipole_package_location not in sys.path:
#    sys.path.insert(0,skipole_package_location)
#


from skipole import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, set_debug


PROJECTFILES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJECT = 'exercise'

##### Deployment version
# JSON_DIRECTORY = "/home/master/exercise/jsonfiles"


##### Development version
JSON_DIRECTORY = "/home/bernard/git/exercise/jsonfiles"


def start_call(called_ident, skicall):
    "When a call is initially received this function is called."
    return called_ident


def submit_data(skicall):
    "This function is called when a Responder wishes to submit data for processing in some manner"
    if skicall.submit_list[0] == "index":
        _index_page(skicall)
    elif skicall.submit_list[0] == "audiotest":
        _audiotest_page(skicall)
    elif skicall.submit_list[0] == "get_exercise":
        _get_exercise_page(skicall)
    elif skicall.submit_list[0] == "start_exercise":
        # an exercise page is shown and started
        _start_exercise_page(skicall)
    elif skicall.submit_list[0] == "run_exercise":
        # update the running exercise with JSON
        _run_exercise_page(skicall)
    elif skicall.submit_list[0] == "skip":
        _skip_page(skicall)
    elif skicall.submit_list[0] == "pauseplay":
        _pauseplay_page(skicall)



def end_call(page_ident, page_type, skicall):
    """This function is called at the end of a call prior to filling the returned page with skicall.page_data,
       it can also return an optional session cookie string."""
    return


def _index_page(skicall):
    "Lists buttons to the exercises"
    # number_of_exercises
    skicall.page_data["exlink", 'multiplier'] = len(skicall.proj_data)
    exlist = [ skicall.proj_data[exercise]['exdef'] for exercise in skicall.proj_data ]
    # exlist is a list of exercises, each element in the list being itself
    # a list of ['filename', 'large text', 'small text', 'time']
    exlist.sort(key=lambda x: x[0])
    for index, exercise in enumerate(exlist):
        section_name = "exlink_" + str(index)
        skicall.page_data[section_name, 'ex1', "button_text"] = exercise[1]
        skicall.page_data[section_name, 'ex1', "get_field1"] = exercise[0]
        skicall.page_data[section_name, 'description', "para_text"] = exercise[2]
        skicall.page_data[section_name, 'time', "para_text"] = "Duration : %s minutes" % (int((exercise[3]+30)/60),)



def _audiotest_page(skicall):
    "JSON audio test"
    skicall.page_data['audiolink','play'] = True


def _get_exercise_page(skicall):
    "Gets the exercise page, with its description and start button"
    # an exercise description and start button is shown
    received = skicall.submit_dict.get('received')
    if not received:
        raise FailPage("Exercise not recognised")
    exercise = None
    for valu in received.values():
        if valu:
            exercise = valu
            break
    if not exercise:
        raise FailPage("Exercise not recognised")
    if exercise in skicall.proj_data:
        exdef = skicall.proj_data[exercise]['exdef']
    else:
        raise FailPage("Exercise not defined")
    skicall.page_data['ex1','large_text'] = exdef[1]
    skicall.page_data['ex1','small_text'] = exdef[2]
    skicall.page_data['time', "para_text"] = "Duration : %s minutes" % (int((exdef[3]+30)/60),)
    skicall.page_data['start','get_field1'] = exdef[0]
    skicall.page_data['ident_data'] = exdef[0] + "_0_0_play"    # item zero, start time zero
 

def _start_exercise_page(skicall):
    "Starts up the exercise page, including the initial audio play"
    exercise = skicall.call_data.get(('start','get_field1'))
    if not exercise:
        raise FailPage("Exercise not recognised")
    if exercise in skicall.proj_data:
        exdef = skicall.proj_data[exercise]['exdef']
    else:
        raise FailPage("Exercise not recognised")
    # get ident_data, and compare
    if skicall.ident_data != exdef[0] + "_0_0_play":
        raise FailPage("Exercise not recognised")
    skicall.page_data['ex1','large_text'] = exdef[1]
    skicall.page_data['ex1','small_text'] = exdef[2]
    skicall.page_data['bar','value'] = 0
    sections = skicall.proj_data[exercise]['sections']
    # sections[0] is the first item in the exercise
    skicall.page_data['ex2','large_text'] = sections[0][1]
    skicall.page_data['ex2','small_text'] = sections[0][2]
    skicall.page_data['ident_data'] = exdef[0] + "_0_5_play"    # item zero, start time 5 seconds
    next_section_number = skicall.proj_data[exercise]['next'][0]
    if next_section_number:
        skicall.page_data['next', 'para_text'] = "Next: " + sections[next_section_number][1]
        skicall.page_data['skip', 'get_field1'] = next_section_number
    else:
        skicall.page_data['skip', 'get_field1'] = 0  # This get field of zero is used to 'skip' back to previous page
    # set sound files for the first section
    skicall.page_data['audiolink','play'] = _sound_urls(skicall, exercise, 0)
    # The major section bar displays the time taken for the current 'major' section
    skicall.page_data['major_section','value'] = 0



def _run_exercise_page(skicall):
    """Fill a JSON page to run the exercise"""
    # get exercise from ident_data
    try:
        exercise, section, seconds, pauseplay = skicall.ident_data.split("_")
        section = int(section)
        seconds = int(seconds)
        exdef = skicall.proj_data[exercise]['exdef']
    except:
        raise FailPage("Exercise not recognised")
    if pauseplay == "pause":
        return
    skicall.page_data['ex1','large_text'] = exdef[1]
    skicall.page_data['ex1','small_text'] = exdef[2]
    sections = skicall.proj_data[exercise]['sections']
    # sections is a list of all the exercise parts, each part being [time, title, description, mp3file, wavfile, oggfile]
    active_section = sections[section]
    # get current length of time taken
    if section:
        exercisetime = 0
        for sectn in sections[0:section]:
            exercisetime += sectn[0]
        exercisetime += seconds
    else:
        exercisetime = seconds
    skicall.page_data['bar','value'] = int(exercisetime * 100 / exdef[3])
    if seconds < active_section[0]:
        skicall.page_data['ident_data'] = exdef[0] + "_" + str(section) + "_" + str(seconds + 5) + "_play"
        next_section_number = skicall.proj_data[exercise]['next'][section]
        if next_section_number:
            next_section_title = sections[next_section_number][1]
        else:
            next_section_title = None
    else:
        if section+1 >= len(sections):
            # no more sections
            skicall.page_data['JSONtoHTML'] = "home"
            return
        skicall.page_data['ident_data'] = exdef[0] + "_" + str(section+1) + "_5_play"
        skicall.page_data['ex2','large_text'] = sections[section+1][1]
        skicall.page_data['ex2','small_text'] = sections[section+1][2]
        next_section_number = skicall.proj_data[exercise]['next'][section+1]
        if next_section_number:
            next_section_title = sections[next_section_number][1]
        else:
            next_section_title = None
        # set sound files for the next section
        skicall.page_data['audiolink','play'] = _sound_urls(skicall, exercise, section+1)
    # show the next item
    if next_section_title is None:
        # no next sections
        skicall.page_data['next', 'para_text'] = "Last Section"
        skicall.page_data['skip', 'get_field1'] = 0
    else:
        skicall.page_data['next', 'para_text'] = "Next: " + next_section_title
        skicall.page_data['skip', 'get_field1'] = next_section_number
    # set the major section bar
    cumulative = skicall.proj_data[exercise]['cumulative']
    # exercisetime is the time so far
    if exercisetime in cumulative:
        skicall.page_data['major_section','value'] = "0.0"
        return
    lastmajorstarttime = 0
    for t in cumulative:
        if exercisetime < t:
            skicall.page_data['major_section','value'] = int((exercisetime - lastmajorstarttime) * 100 / (t-lastmajorstarttime))
            break
        lastmajorstarttime = t


def _pauseplay_page(skicall):
    "pause or play"
    pauseplay = skicall.call_data.get(('pause','get_field1'))
    if pauseplay is None:
        return
    try:
        exercise, section, seconds, pauseplayfromident = skicall.ident_data.split("_")
        section = int(section)
        sections = skicall.proj_data[exercise]['sections']
    except:
        raise FailPage("Exercise not recognised")

    if pauseplay == 'pause':
        skicall.page_data['pause', 'get_field1'] = "play"
        skicall.page_data['pause', 'button_text'] = "Play"
        skicall.page_data['ident_data'] = exercise + "_" + str(section) + "_" + seconds + "_pause"
        skicall.page_data['ex2','small_text'] = "STOPPED"
    elif pauseplay == 'play':
        skicall.page_data['pause', 'get_field1'] = "pause"
        skicall.page_data['pause', 'button_text'] = "Pause"
        skicall.page_data['ident_data'] = exercise + "_" + str(section) + "_" + seconds + "_play"
        skicall.page_data['ex2','small_text'] = sections[section][2]



def _skip_page(skicall):
    """Fill a JSON page to skip to the next exercise"""
    # get exercise from ident_data
    try:
        exercise, section, seconds, pauseplay = skicall.ident_data.split("_")
        exdef = skicall.proj_data[exercise]['exdef']
        # skip button get_field is the section to jump to
        section = int(skicall.call_data.get(('skip','get_field1')))
    except:
        raise FailPage("Exercise not recognised")
    if not section:
        skicall.page_data['JSONtoHTML'] = "home"
        return
    
    sections = skicall.proj_data[exercise]['sections']
    # sections is a list of all the exercise parts, each part being [time, title, description, mp3file, wavfile, oggfile]

    # get current length of time taken
    exercisetime = 0
    for sectn in sections[0:section]:
        exercisetime += sectn[0]
    skicall.page_data['bar','value'] = int(exercisetime * 100 / exdef[3])

    skicall.page_data['pause', 'get_field1'] = "pause"
    skicall.page_data['pause', 'button_text'] = "Pause"

    skicall.page_data['ident_data'] = exdef[0] + "_" + str(section) + "_5_play"
    skicall.page_data['ex2','large_text'] = sections[section][1]
    skicall.page_data['ex2','small_text'] = sections[section][2]
    next_section_number = skicall.proj_data[exercise]['next'][section]
    if next_section_number:
        skicall.page_data['next', 'para_text'] = "Next: " + sections[next_section_number][1]
        skicall.page_data['skip', 'get_field1'] = next_section_number
    else:
        skicall.page_data['next', 'para_text'] = "Last Section"
        skicall.page_data['skip', 'get_field1'] = 0
    # set sound files for the section
    skicall.page_data['audiolink','play'] = _sound_urls(skicall, exercise, section)
    skicall.page_data['major_section','value'] = "0.0"



def _read_files():
    "Create proj_data directory by reading the JSON files"

    jsonfiles = [f for f in os.listdir(JSON_DIRECTORY) if os.path.isfile(os.path.join(JSON_DIRECTORY, f))]

    proj_data = {}

    for filename in jsonfiles:
        filepath = os.path.join(JSON_DIRECTORY, filename)
        with open(filepath, 'r') as fp:
            exerciselist = json.load(fp)
            exdef = []       # exercise strings
            sectionlist = []        # items expanded not including initial strings
            # expand exerciselist 'repeat' sections
            for item in exerciselist:
                if isinstance(item, str):
                    # first items, being filename, exercise title, description
                    exdef.append(item)
                else:
                    # item must be a list, could be a list containing items to be repeated
                    if isinstance(item[0], str) and (item[0] == 'repeat'):
                        # a list containing repeated items
                        intervals = item[1]          # item[1] is the number of intervals, i.e. typically 4
                        for interval in range(intervals):
                            # interval is typically 0, 1, 2, 3
                            for repeatitem in item[2:]:
                                if isinstance(repeatitem[0], int):
                                    # this item is repeated every time with the given time interval
                                    sectionlist.append(repeatitem)
                                elif isinstance(repeatitem[0], list):
                                    # this item is repeated with the given time intervals
                                    if len(repeatitem[0]) != intervals:
                                        print("Invalid repeat item times list")
                                        sys.exit(1)
                                    intervaltime = repeatitem[0][interval]
                                    if intervaltime:
                                        newitem = [intervaltime] + repeatitem[1:]
                                        sectionlist.append(newitem)
                                    # if intervaltime is zero for this interval, the item will not be added
                    else:
                        sectionlist.append(item)
            # get length of time for the exercise
            totaltime = 0
            for section in sectionlist:
                totaltime += section[0]
            exdef.append(totaltime)

            # exdef consists of filename, exercise title, description, total exercise time in seconds

            # get list, for each section, give the number of the next 'major' section
            # a major section being a section with a different title
            major_index = _next_major_section(sectionlist)

            # get list of cumulative times when each major section starts
            cumulative = _cumulative_major_intervals(totaltime, sectionlist, major_index)

            proj_data[exerciselist[0]] = {'exdef':exdef, 'sections':sectionlist, 'next':major_index, 'cumulative':cumulative}
    return proj_data


def _next_major_section(sectionlist):
    "Returns a list of next major section numbers"

    length = len(sectionlist)

    if length == 1:
        return [None]

    if length == 2:
        if sectionlist[0][1] == sectionlist[1][1]:
            # only one title, repeated, so no next
            return [None, None]
        else:
            return [ 1, None ]

    # now for the case of more than two sections

    nextsections = [None] * length

    for counter in range(length-1):
        current_title = sectionlist[counter][1]  
        next_number = None
        for rst in range(counter+1, length):   # iterate through remaining numbers
            if sectionlist[rst][1] != current_title:
                next_number = rst
                break
        nextsections[counter] = next_number

    return nextsections


def _cumulative_major_intervals(totaltime, sectionlist, major_index):
    """Returns the cumulative time intervals
       such that [ t1, t2, t3...]
       t1 is time first major section ends, and second major section starts
       t2 is the time the second major section ends, and third major section starts
       t3 is the time the third major section ends, etc"""

    # a section in the sectionlist is
    # [ section time in seconds, section title, section text, mp3 file, wav file, ogg file]

    cumulative = []
    cumulative_time = 0

    for idx, section in enumerate(sectionlist):
        if major_index[idx] is None:
            # no further sections
            cumulative.append(totaltime)
            break
        cumulative_time += section[0]
        if major_index[idx] == idx+1:
            # The next section is flagged as the start of the next major section
            cumulative.append(cumulative_time)

    return cumulative



def _sound_urls(skicall, exercise, section):
    """Sets
       skicall.page_data['audiolink','src_mp3']
       skicall.page_data['audiolink','src_wav']
       skicall.page_data['audiolink','src_ogg']
       with appropriate url's, where section is the section number
       If none set returns False, otherwise True
       """
    sectiondefinition = skicall.proj_data[exercise]['sections'][section]
    # where a sectiondefinition is
    # [ section time in seconds, section title, section text, mp3 file, wav file, ogg file]

    sounds = sectiondefinition[3:6]

    projecturl = skicall.projectpaths()[skicall.project]

    soundset = False

    for sound in sounds:
       if not sound:
           continue
       if sound.endswith(".mp3"):
           skicall.page_data['audiolink','src_mp3'] = os.path.join(projecturl, "sounds", sound)
           soundset = True
       elif sound.endswith(".wav"):
           skicall.page_data['audiolink','src_wav'] = os.path.join(projecturl, "sounds", sound)
           soundset = True
       elif sound.endswith(".ogg") or sound.endswith(".oga"):
           skicall.page_data['audiolink','src_ogg'] = os.path.join(projecturl, "sounds", sound)
           soundset = True

    return soundset

     


##############################################################################
#
# The above functions will be inserted into the skipole.WSGIApplication object
# and will be called as required
#
##############################################################################


# load exercises, from each json file, and set into proj_data dictionary

proj_data = _read_files()


# create the wsgi application
application = WSGIApplication(project=PROJECT,
                              projectfiles=PROJECTFILES,
                              proj_data=proj_data,
                              start_call=start_call,
                              submit_data=submit_data,
                              end_call=end_call,
                              url="/exercise")


skis_code = os.path.join(PROJECTFILES, 'skis', 'code')
if skis_code not in sys.path:
    sys.path.append(skis_code)
import skis
skis_application = skis.makeapp(PROJECTFILES)
application.add_project(skis_application, url='/exercise/lib')



if __name__ == "__main__":



    ########### REMOVE WHEN YOU DEPLOY YOUR APPLICATION
    set_debug(True)
    skiadmin_code = os.path.join(PROJECTFILES, 'skiadmin', 'code')
    if skiadmin_code not in sys.path:
        sys.path.append(skiadmin_code)
    import skiadmin
    skiadmin_application = skiadmin.makeapp(PROJECTFILES, editedprojname=PROJECT)
    application.add_project(skiadmin_application, url='/exercise/skiadmin')
    ###########

    #### Deployment server
    #
    # from waitress import serve
    # serve(application, host='0.0.0.0', port=8000)
    #


    #### Development server
    
    from skipole import skilift
    host = "127.0.0.1"
    port = 8000
    print("Serving %s on port %s. Call http://localhost:%s/skiadmin to edit." % (PROJECT, port, port))
    skilift.development_server(host, port, application)


