# Speak.activity
# A simple front end to the espeak text-to-speech engine on the XO laptop
# http://wiki.laptop.org/go/Speak
#
# Copyright (C) 2008  Joshua Minor
# This file is part of Speak.activity
#
# Parts of Speak.activity are based on code from Measure.activity
# Copyright (C) 2007  Arjun Sarwal - arjun@laptop.org
# 
#     Speak.activity is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Speak.activity is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Speak.activity.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
from gettext import gettext as _

import logging
logger = logging.getLogger('speak')

import espeak

# Lets trick gettext into generating entries for the voice names we expect espeak to have
# If espeak actually has new or different names then they won't get translated, but they
# should still show up in the interface.
expectedVoiceNames = [
    _("Brazil"),
    _("Swedish"),
    _("Icelandic"),
    _("Romanian"),
    _("Swahili"),
    _("Hindi"),
    _("Dutch"),
    _("Latin"),
    _("Hungarian"),
    _("Macedonian"),
    _("Welsh"),
    _("French"),
    _("Norwegian"),
    _("Russian"),
    _("Afrikaans"),
    _("Finnish"),
    _("Default"),
    _("Cantonese"),
    _("Scottish"),
    _("Greek"),
    _("Vietnam"),
    _("English"),
    _("Lancashire"),
    _("Italian"),
    _("Portugal"),
    _("German"),
    _("Whisper"),
    _("Croatian"),
    _("Czech"),
    _("Slovak"),
    _("Spanish"),
    _("Polish"),
    _("Esperanto")
]

_allVoices = {}
_allVoicesByLang = {}
_defaultVoice = None

class Voice:
    def __init__(self, language, name, dialect=None):
        self.language = language
        self.name = name
        if dialect is not None and dialect != 'none':
            self.language = "%s-%s" % (self.language, dialect)

        friendlyname = name
        friendlyname = friendlyname.replace('-test','')
        friendlyname = friendlyname.replace('_test','')
        friendlyname = friendlyname.replace('en-','')
        friendlyname = friendlyname.replace('english-wisper','whisper')
        friendlyname = friendlyname.capitalize()
        self.friendlyname = _(friendlyname)

def _init_voice_cache():

    for language, name, dialect in espeak.voices():
        voice = Voice(language, name, dialect)
        _allVoices[voice.friendlyname] = voice
        _allVoicesByLang[voice.language] = voice

def allVoices():
    if _allVoices:
        return _allVoices

    _init_voice_cache()

    return _allVoices

def by_name(name):
    return allVoices().get(name, defaultVoice())

def allVoicesByLang():
    if _allVoicesByLang:
        return _allVoicesByLang

    _init_voice_cache()

    return _allVoicesByLang

def by_lang(lang):
    return allVoicesByLang().get(lang, defaultVoice())


def defaultVoice():
    """Try to figure out the default voice, from the current locale ($LANG).
       Fall back to espeak's voice called Default."""

    global _defaultVoice

    if _defaultVoice:
        return _defaultVoice

    voices = allVoices()

    def fit(a,b):
        "Compare two language ids to see if they are similar."
        as_ = re.split(r'[^a-z]+', a.lower())
        bs = re.split(r'[^a-z]+', b.lower())
        for count in range(0, min(len(as_),len(bs))):
            if as_[count] != bs[count]:
                count -= 1
                break
        return count
    try:
        lang = os.environ["LANG"]
    except:
        lang = ""

    try:
        best = voices[_("English")]  # espeak-ng 1.49.1
    except:
        best = voices[_("Default")]  # espeak 1.48
    for voice in voices.values():
        voiceMetric = fit(voice.language, lang)
        bestMetric  = fit(best.language, lang)
        if voiceMetric > bestMetric:
            best = voice

    _defaultVoice =  best
    return best
