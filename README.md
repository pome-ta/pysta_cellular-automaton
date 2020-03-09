# pysta_cellular-automaton

Pythonista でcellular automaton(Life Game) を作る


## Main logic

### 参照先

[ゼロからはじめるPython(9) 生物集団の栄枯盛衰"ライフゲーム"を作ってみよう](https://www.google.co.jp/amp/s/news.mynavi.jp/article/zeropython-9:amp/) をPythonista へ移植



## `scene`module

`scene.ShapeNode` を `cell` として、作成

- `SPEED`
	- `100` が大体 1秒
	- (`50` で 0.5秒)
	- フレームレートを変えても同じ秒間
- `SEED`
	- 初期値生まれる`cells` 調整
		- 数値が少ない程生まれる可能性があがる
	- 画面タップで再度生成
		- 生まれる確率は
			- n > 初期値
- `DIV`
	- 画面内分割数
		- 画面サイズ縦横の小さい方を基準にして、正方形を生成
		- `self.ROWS` = `DIV`
	- 64 を超えてくるとドキドキする


## `np_list`, `py_list`

`scene.ShapeNode` の描画がネックなのか、どこまで早くなるのか確認



今のところ、`py_list` の方が早い？



### `np_list`

NumPy 初挑戦 🤗


とりあえず手当たり次第、`list` もので変換できるものは`np.` を使ってNumPy化


### `py_list`

内包表記できそうなものはとりあえず、内包表記化

