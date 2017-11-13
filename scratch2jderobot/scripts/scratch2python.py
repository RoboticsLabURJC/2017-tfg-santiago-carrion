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
    ['if {} then', 'if %s:'],
    ['else', 'else:'],
    ['repeat {}', 'for i in range(%s):'],
    ['say {}', 'print(%s)'],
    ['set {} to {}', '%s = %s'],
    ['wait {} secs', 'time.sleep(%s)'],
]

ROBOTICS = [

    # movement blocks
    ['move robot {}', 'robot.move("%s")'],
    ['move drone {} speed {}', 'robot.move("%s", %s)'],
    ['move robot {} speed {}', 'robot.move("%s", %s)'],
    ['stop robot-drone', 'robot.stop()'],
    ['turn drone {} speed {}', 'robot.turn("%s", %s)'],
    ['turn robot {} speed {}', 'robot.turn("%s", %s)'],
    ['take off drone', 'robot.take_off()'],
    ['land drone', 'robot.land()'],
    ['move robot {} meters {}', 'robot.move_meters("%s", %s)'],
    ['frontal laser distance', 'robot.get_laser_distance()'],
    ['get {} of object {}', 'robot.get_object("%s","%s")'],
    ['get pose3d {}', 'robot.get_pose3d("%s")'],
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


def similar(a, b):
    """
    Returns the ratio value comparing two sentences.

    @param a: First sentence.
    @param b: Second sentence.
    @return: The ratio of the similarity.
    """

    print ">>> ratio of similarity betwen:",a,"--and--",b,"-->",SequenceMatcher(None, a, b).ratio()
    return SequenceMatcher(None, a, b).ratio()


def sentence_mapping(sentence, threshold=None):
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
        if elem[0][:3] == sentence.replace('    ', '')[:3]:
            options.append(elem)
            found = True


    # then look for robotics blocks
    for elem in ROBOTICS:
        if elem[0][:3] == sentence.replace('    ', '').replace('(', '')[:3]:
            options.append(elem)
            found = True

    if found:
        # select the option that better fits
        l = [(m[0], m[1], similar(sentence, m[0])) for m in options]
        original, translation, score = max(l, key=lambda item: item[2])
        print ">>> original, translation, score:", original, translation, score
        if threshold and score < threshold:
            return None, None


        # extract arguments
        p = compile(original)
        print ">>> compile:", original, "--return--",p, sentence   #compile bien

        args = p.parse(sentence.replace('    ', ''))
        print ">>> p.parse(sentence) sentence:",sentence, args #no parsea


        if args:
            args_aux = list(args)
            print ">>> args encontrados:",list(args)

            # look for more blocks
            for idx in range(len(args_aux)):
                print ">>> looking for more blocks:",args_aux[idx]
                new_ori, new_trans = sentence_mapping(args_aux[idx]) #sentence_mapping(args_aux[idx],0.8) --old
                print ">>> new sentence_mapping of:",args_aux[idx],"--return--",new_ori, new_trans
                if new_trans != None:
                    print ">>> frase en la que reemplazar:",args_aux[idx]
                    args_aux[idx] = args_aux[idx].replace(new_ori, new_trans) #replace(args_aux[idx], new_trans)
                    print ">>> reemplazando:",new_ori,"--with--", new_trans

            translation = translation % tuple(args_aux)
            print ">>> traduccion final:", translation, tuple(args_aux)

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
import time\n\n\
def execute(robot):\n\
\ttry:\n\
\t%s\
except KeyboardInterrupt:\n\
\t\traise\n\
"

        # load the scratch project
        p = kurt.Project.load(open_path + sys.argv[1])

        # show the blocks included
        for scriptable in p.sprites + [p.stage]:
            for script in scriptable.scripts:
                # exclude definition scripts
                if "define" not in script.blocks[0].stringify():
                    s = script

        print
        print("Stringify:")
        sentences = []
        for b in s.blocks:
            print(b.stringify())
            sentences += b.stringify().split('\n')
        print

        tab_seq = "\t"
        python_program = ""

        for s in sentences:
            # count number of tabs
            num_tabs = s.replace('    ', tab_seq).count(tab_seq)

            python_program += tab_seq * (num_tabs + 1)

            # pre-processing if there is a condition (operators and types)
            print ">>>"
            print ">>>"
            print ">>>----------- Processing sentence:",s,"----------"
            print ">>>"
            print ">>"
            if is_conditional(s):
                s = s.replace("'", "").replace("=", "==")
            # mapping
            original, translation = sentence_mapping(s)

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

        # save the code in a python file
        f = open(save_path + "scratch.py", "w")
        f.write(file_text)
        f.close()

    else:
        print(
            "ERROR: Number of parameters incorrect. Example:\n\tpython scratch2python.py hello_world.sb2")
