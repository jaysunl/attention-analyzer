# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.
<<<<<<< HEAD
=======

>>>>>>> 13bb0fc51d5aa32b3cce450536224ea91397baf6
# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; unsetenv VIRTUAL_ENV_PROMPT; test "\!:*" != "nondestructive" && unalias deactivate'

# Unset irrelevant variables.
deactivate nondestructive

<<<<<<< HEAD
setenv VIRTUAL_ENV "/Users/jerryliang/projects/attention-analyzer/venv"
=======
setenv VIRTUAL_ENV "/Users/jamieanzai/hackathon/attention-analyzer/venv"
>>>>>>> 13bb0fc51d5aa32b3cce450536224ea91397baf6

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/bin:$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
    set prompt = "(venv) $prompt"
    setenv VIRTUAL_ENV_PROMPT "(venv) "
endif

alias pydoc python -m pydoc

rehash
