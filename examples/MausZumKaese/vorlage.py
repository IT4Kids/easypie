# coding=utf-8
from examples.MausZumKaese.maus_zum_kaese_main import maus, run, Animation

animation = Animation()

animation.add(maus.move, 150)
animation.add(maus.turn, 90)
animation.add(maus.move, 520)
animation.add(maus.turn, -90)
animation.add(maus.move, 1000)
run(animation)