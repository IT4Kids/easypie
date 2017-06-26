# coding=utf-8
from utils import maus, run, Animation

animation = Animation()

animation.add(maus.move, 150)
animation.add(maus.turn, 90)
animation.add(maus.move, 520)
animation.add(maus.turn, -90)
animation.add(maus.move, 1000)
run(animation)
