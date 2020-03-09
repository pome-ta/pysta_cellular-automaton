from random import randint
import numpy as np
import scene, ui


SPEED = 1
SEED = 5
DIV = 32

c_back = 'black'
c_block = 'dimgray'
c_alive = 'palegreen'


class DebugLabel(scene.LabelNode):
  def __init__(self, p_parent, x, y):
    super().__init__()
    p_parent.add_child(self)
    self.font = ('Source Code Pro', 8)
    self.text = '{:02},{:02}'.format(x, y)


class Cell(scene.ShapeNode):
  def __init__(self, p_parent, x, y, d, set_size):
    super().__init__()
    p_parent.add_child(self)
    self.alpha = .5
    self.path = ui.Path.rounded_rect(0, 0, d, d, 2)
    #self.path = ui.Path.rect(0, 0, d, d)
    self.fill_color = c_block
    self.position = set_size
    self.position += (d*x, d*y)
    #DebugLabel(self, x,y)


class BackGround(scene.ShapeNode):
  def __init__(self, p_parent, size):
    super().__init__()
    p_parent.add_child(self)
    x, y = size
    self.path = ui.Path.rect(0,0,x,y)
    self.fill_color = c_back
    
class Life(scene.Node):
  def __init__(self, p_parent):
    super().__init__()
    p_parent.add_child(self)
    self.p_size = p_parent.size
    self.position = self.p_size / 2
    self.life_time = 0.0
    self.life_speed = SPEED / 100
    self.alive = []
    self.set_up()
    self.game_setup()
    self.draw_stage()
    
  def set_up(self):
    size = self.p_size
    self.bg = BackGround(self, size)
    self.set_cells(size)
    
  def set_cells(self, size):
    s_min = min(size[0], size[1])
    rect = s_min/DIV
    # todo: 切り上げ
    row = -(-(size[0])//rect)
    col = -(-(size[1])//rect)
    set_size = (row*rect/-2 + rect/2,
                col*rect/-2 + rect/2)
    self.ROWS = int(row)
    self.COLS = int(col)
    self.cells = np.array([[Cell(self.bg, x, y, rect, set_size) for y in range(self.COLS)]for x in range(self.ROWS)])
  
  def draw_stage(self):
    self.reset_color(self.alive)
    for y in range(0, self.ROWS):
      for x in range(0, self.COLS):
        if not self.data[y][x]: continue
        self.alive.append([y,x])
        self.cells[y][x].fill_color = c_alive
  
  def reset_color(self, alive):
    for a in alive:
      self.cells[a[0]][a[1]].fill_color = c_block
    self.alive = []
  
  def game_setup(self):
    # ステージデータ
    self.data = np.array([[randint(0, SEED)==0 for x in range(0, self.COLS)]for y in range(0, self.ROWS)])
    
  def check(self, x, y):
    # ゲーム実装
    cnt = 0
    tbl = np.array([(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)])
    for t in tbl:
      xx, yy = np.array([x + t[0], y + t[1]])
      if 0 <= xx < self.COLS and 0 <= yy < self.ROWS:
        if self.data[yy][xx]: cnt += 1
    if cnt == 3: return True  # 誕生
    if self.data[y][x]:
      if 2 <= cnt <= 3: return True   #生存
      return False  # 過疎 or 過密
    return self.data[y][x]
    
  def next_turn(self):
    _data = np.array([[self.check(x, y) for x in range(0, self.COLS)]for y in range(0, self.ROWS)])
    self.data = _data
  
  def reset_game(self):
    self.reset_color(self.alive)
    SEED = randint(1, 9)
    self.game_setup()
    self.draw_stage()
    
  def time(self, dt):
    self.life_time += dt
    if self.life_time > self.life_speed:
      self.next_turn()
      self.draw_stage()
      self.life_time = 0.0


class MyScene(scene.Scene):
  def setup(self):
    self.life = Life(self)

  def update(self):
    self.life.time(self.dt)
    
  def touch_began(self, touch):
    self.life.reset_game()
    

main = MyScene()
scene.run(main,
          #orientation=1,
          frame_interval=0,#2,
          show_fps=True)

