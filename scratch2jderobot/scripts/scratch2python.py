#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Raul Perula-Martinez"
__copyright__ = "JdeRobot project"
__credits__ = ["Raul Perula-Martinez"]
__license__ = "GPL v3"
__version__ = "0.0.0"
__maintainer__ = "Raul Perula-Martinez"
__email__ = "raules@gmail.com"
__status__ = "Development"

import kurt
import os
import sys

from difflib import SequenceMatcher
from parse import parse, compile
from termcolor import cprint

GENERAL = [
    ['end', ''],
    ['forever', 'while True:'],
    ['if {} then', 'if {l[0]}:'],
    ['if {} > {} then', 'if {l[0]} > {l[1]}:'],
    ['if {} < {} then', 'if {l[0]} < {l[1]}:'],
    ['else', 'else:'],
    ['repeat {}', 'for i in range({l[0]}):'],
    ['say {}', 'print({l[0]})'],
    ['set {} to {}', '{l[0]} = {l[1]}'],
    ['wait {} secs', 'time.sleep({l[0]})'],
    ['length of {}', 'len({l[0]})'],
    ['insert {} at {} of {}', '{l[2]}.insert({l[1]}, {l[0]})'],
    ['item {} of {}', '{l[1]}[0][{l[0]}]'],
    ['add {} to {}', '{l[1]}.append({l[0]})'],
    ['delete {} of {}', '{l[1]}.pop({l[0]})'],
]

ROBOTICS = [
    ['move robot {}', 'robot.move("{l[0]}")'],
    ['move drone {}', 'robot.move("{l[0]}")'],
    ['move drone {} speed {}', 'robot.move("{l[0]}", {l[1]})'],
    ['move robot {} speed {}', 'robot.move("{l[0]}", {l[1]})'],
    ['stop robot-drone', 'robot.stop()'],
    ['turn drone {} speed {}', 'robot.turn("{l[0]}", {l[1]})'],
    ['turn robot {} speed {}', 'robot.turn("{l[0]}", {l[1]})'],
    ['take off drone', 'robot.take_off()'],
    ['land drone', 'robot.land()'],
    ['frontal laser distance', 'robot.get_laser_distance()'],
    ['color detection {}', 'robot.detect_object("{l[0]}")'],
    ['size of object', 'robot.get_size_object()'],
    ['x position of object', 'robot.get_x_position()'],
    ['y position of object', 'robot.get_y_position()'],
]

def is_conditional(sentence):
    """
    Returns if a sentence is conditional or not.

    @param sentence: The sentence to check.
    @return: True if it has a conditional, False otherwise.
    """
    if "if" in sentence:
        return True

    return False
   

def is_list(sentence):
    """
    Returns if a sentence use list or not.

    @param sentence: The sentence to check.
    @return: True if it has a list, False otherwise.
    """
    if "insert" in sentence:
        return True
    if "add" in sentence:
	return True

    return False


def similar(a, b):
    """
    Returns the ratio value comparing two sentences.

    @param a: First sentence.
    @param b: Second sentence.
    @return: The ratio of the similarity.
    """
    return SequenceMatcher(None, a, b).ratio()


def sentence_mapping(sentence, threshold=0.0):
    """
    Maps a sentence and returns the original and the mapped.

    @param sentence: The sentence to map.
    @return: The original sentence and the mapped sentence.
    """

    found = False
    options = []
    original = None
    translation = None

    # first look for general blocks
    for elem in GENERAL:
        if elem[0][:3] == sentence.replace('    ', '').replace('(', '')[:3]:
            options.append(elem)
            found = True

    # then look for robotics blocks
    if not found:
        for elem in ROBOTICS:
            if elem[0][:3] == sentence.replace('    ', '').replace('(', '')[:3]:
                options.append(elem)
                found = True

    if found:
        # select the option that better fits
        l = [(m[0], m[1], similar(sentence, m[0])) for m in options]
        original, translation, score = max(l, key=lambda item: item[2])

        if score < threshold:
            return None, None

        # clean sentence
        s = sentence.replace('    ', '').replace('(', '').replace(')', '')

        # extract arguments
        p = compile(original)
        args = p.parse(s)

        if args:
            args_aux = list(args)

            # look for more blocks
            for idx in range(len(args_aux)):
                new_ori, new_trans = sentence_mapping(args_aux[idx], 0.6)

                if new_trans != None:
                    # print "args: ",idx, args_aux[idx]
                    # print "trans: ",new_trans
                    args_aux[idx] = new_trans

            # print "trans: ",translation
            # print "args: ",args_aux
            translation = translation.format(l=args_aux)

    return original, translation



if __name__ == "__main__":
    # get current working directory
    path = os.getcwd()
    open_path = path[:path.rfind('scripts')] + 'data/'
    save_path = path[:path.rfind('scripts')] + 'src/scratch2jderobot/'

    if len(sys.argv) == 2:
        # template creation

        template = "\
#!/usr/bin/env python\n\
# -*- coding: utf-8 -*-\n\n\
import time\n\
import config\n\
import sys\n\
import comm\n\
import os\n\
import yaml\n\n\
from drone import Drone\n\
from robot import Robot\n\n\
def execute(robot):\n\
\ttry:\n\
\t%s\
except KeyboardInterrupt:\n\
\t\traise\n\n\
if __name__ == '__main__':\n\
\tif len(sys.argv) == 2:\n\
\t\tpath = os.getcwd()\n\
\t\topen_path = path[:path.rfind('src')] + 'cfg/'\n\
\t\tfilename = sys.argv[1]\n\n\
\telse:\n\
\t\tsys.exit(\"ERROR: Example:python my_generated_script.py cfgfile.yml\")\n\n\
\t# loading the ICE and ROS parameters\n\
\tcfg = config.load(open_path + filename)\n\
\tstream = open(open_path + filename, \"r\")\n\
\tyml_file = yaml.load(stream)\n\n\
\tfor section in yml_file:\n\
\t\tif section == 'drone':\n\
\t\t\t#starting comm\n\
\t\t\tjdrc = comm.init(cfg,'drone')\n\n\
\t\t\t# creating the object\n\
\t\t\trobot = Drone(jdrc)\n\n\
\t\t\tbreak\n\
\t\telif section == 'robot':\n\
\t\t\t#starting comm\n\
\t\t\tjdrc = comm.init(cfg,'robot')\n\n\
\t\t\t# creating the object\n\
\t\t\trobot = Robot(jdrc)\n\n\
\t\t\tbreak\n\
\t# executing the scratch program\n\
\texecute(robot)\n\n\
"

        # load the scratch project
        p = kurt.Project.load(open_path + sys.argv[1])

        # show the blocks included
        for scriptable in p.sprites + [p.stage]:
            for script in scriptable.scripts:
                # exclude definition scripts
                if "define" not in script.blocks[0].stringify():
                    s = script
        print("Stringify:")
        sentences = []
        for b in s.blocks:
            print(b.stringify())
            sentences += b.stringify().split('\n')
        tab_seq = "\t"
        python_program = ""

        for s in sentences:
            # pre-processing if there is a condition (operators and types)
            if is_conditional(s):
                s = s.replace("'", "").replace("=", "==")
            # mapping
            original, translation = sentence_mapping(s)

            # count number of tabs
            num_tabs = s.replace('    ', tab_seq).count(tab_seq)
            
            # check if there is list
            
            if is_list(s):
	        python_program += tab_seq * (num_tabs + 1)
	        python_program += translation.split(".")[0]+" = []\n\t"

            python_program += tab_seq * (num_tabs + 1)

            # set the code		
            if translation != None:
                python_program += translation
            else:
                cprint("[WARN] Block <%s> not included yet" % s, 'yellow')
            python_program += "\n" + tab_seq

        # join the template with the code and replace the tabs
        file_text = template % python_program
        file_text = file_text.replace(tab_seq, ' ' * 4)

        print("\n-------------------")
        cprint(file_text, 'green')
        print("-------------------\n")

        # save the code in a python file with the same name as sb2 file
        file_name = sys.argv[1].replace('.sb2','.py')
        f = open(save_path + file_name, "w")
        os.chmod(save_path + file_name, 0775)
        f.write(file_text)
        f.close()

    else:
        print(
            "ERROR: Number of parameters incorrect. Example:\n\tpython scratch2python.py hello_world.sb2")
