import os
import sys

from sc2learner.bin.train_ppo import start_actor

def old_main():
    diff_array = ['1','2','4','6','9','A']
    for difficulty in diff_array:
        # debug purpose
        print("-----DEBUG-----")
        print("new actor starts with difficulty : {}".format(difficulty))
        os.system('python -m sc2learner.bin.train_ppo --job_name=actor --difficulty {} --learner_ip localhost'.format(difficulty))
        print("DEBUG : is difficulty {} game done? ".format(difficulty))


def main():
    start_actor()

if __name__ == "__main__":
    main()