from body.Listen import takecommand
from Body.Listen import MicExecution
from Body.Voice import Speak
from features.clap import Tester

MicExecution()
if 'Alice' in query:
    Speak("hello Sir")