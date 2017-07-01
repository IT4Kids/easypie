# coding=utf-8
from utils import maus, run, Animation

animation = Animation()

animation.add(maus.move, 30)
animation.add(maus.turn, 20)
run(animation) 
