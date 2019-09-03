from os.path import join, abspath, dirname
import os.path
import random
from adapt.tools.text.tokenizer import EnglishTokenizer
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_mp3
from mycroft.util.parse import fuzzy_match
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking
from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.context import *

class BedtimeStories(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):

        #Register list of story titles that are held in a padatious entity
        self.register_entity_file("title.entity")
        self.process = None

        #Build story list
        self.play_list = {
            'twas the night before christmas': join(abspath(dirname(__file__)), 'stories', 'twas_the_night_before_christmas.mp3'),
            'little red riding hood': join(abspath(dirname(__file__)), 'stories', 'little_red_riding_hood.mp3'),
            'the three bears': join(abspath(dirname(__file__)), 'stories', 'the_three_bears.mp3'),
            'hansel and gretel': join(abspath(dirname(__file__)), 'stories', 'hansel_and_gretel.mp3'),
            'the velveteen rabbit': join(abspath(dirname(__file__)), 'stories', 'the_velveteen_rabbit.mp3'),
            'rumplestiltskin': join(abspath(dirname(__file__)), 'stories', 'rumplestiltskin.mp3'),
            'the emporers new clothes': join(abspath(dirname(__file__)), 'stories', 'the_emporers_new_clothes.mp3'),
            'the princess and the pea': join(abspath(dirname(__file__)), 'stories', 'the_princess_on_the_pea.mp3'),
            'the elves and the shoemaker': join(abspath(dirname(__file__)), 'stories', 'the_elves_and_the_shoemaker.mp3'),
            'the three billy goats gruff': join(abspath(dirname(__file__)), 'stories', 'the_three_billy_goats_gruff.mp3'),
            'peter rabbit': join(abspath(dirname(__file__)), 'stories', 'peter_rabbit.mp3'),
        }

    #Play random story from list
    @intent_file_handler('stories.bedtime.intent')
    def handle_stories_bedtime(self, message):
        wait_while_speaking()
        self.speak_dialog('stories.bedtime')
        story_file = list(self.play_list.values())
        story_file = random.choice(story_file)
        print(story_file)
        #if os.path.isfile(story_file):
        wait_while_speaking()
        self.process = play_mp3(story_file)

    #Pick story by title
    @intent_file_handler('pick.story.intent')
    def handle_pick_story(self, message):
        self.speak_dialog('pick.story')
        wait_while_speaking()
        title = message.data.get('title')
        score = match_one(title, self.play_list)
        print(score)
        if score[1] > 0.5:
            self.process = play_mp3(score[0])
        else:
            return None
            self.speak('Sorry I could not find that story in my library')

    #List stories in library
    @intent_file_handler('list.stories.intent')
    def handle_list_stories(self, message):
        wait_while_speaking()
        story_list = list(self.play_list.keys())
        print(story_list)
        self.speak_dialog('list.stories', data=dict(stories=story_list))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

def create_skill():
    return BedtimeStories()

