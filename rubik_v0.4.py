import tkinter as tk
import math
import random

#正方形を描画する関数
#def draw_square(canvas, x):
#	canvas.create_rectangle(50, 50, 50 + x*20, 50 + x*20, fill="blue")

#ウィンドウを閉じる関数
def close_window():
    root.destroy()

#格子状の正方形を描画する関数
def draw_grid(canvas, geometric_net, color_bg, color_mask):
	print("geometric_net_quiz_index = "+ str(geometric_net_quiz_index))
#	geometric_net = geometric_net_pattern[geometric_net_quiz_index]
	canvas.create_rectangle(0, 0, 600,600, fill=color_bg)

    # 格子状の正方形を描画
	square_size = 30
	dw = 0
	dh = 0
	for w in range(4):
		dw = w * square_size * 3
		dw += (w+1) * 10
		for h in range(4):
			dh = h * square_size * 3
			dh += (h+1) * 10
#			print("["+str(dh)+"]["+str(dw)+"]")
			for i in range(3):
				for j in range(3):
					w1 = j * square_size + dw
					h1 = i * square_size + dh
					w2 = w1 + square_size
					h2 = h1 + square_size
#					print("  ["+str(3*h+i)+"]["+str(3*w+j)+"]="+str(matrix[3*h+i][3*w+j]))
					color = getColor(matrix[3*h+i][3*w+j])
					canvas.create_rectangle(w1, h1, w2, h2, outline="black", fill=color)

	w1 = 3 * square_size + 20
	h1 = 3 * square_size + 20
	w2 = w1 + 3 * square_size
	h2 = h1 + 3 * square_size
	#canvas.create_rectangle(w1, h1, w2, h2, outline="red")

	#以下の処理は空欄を作るわけではない、そもそも展開図以外の箇所も面の色を塗っているので、背景色に上塗りする必要がある
	draw_mask(canvas, geometric_net, color_mask) #"background") "alpha")

def change_grid(canvas, color_bg, color_mask):
	global geometric_net_quiz_index
	while True:
		geometric_net_quiz_index = random.randint(0, 23)
		if geometric_net_quiz_index != geometric_net_std_index:
			break
	print(">>>geometric_net_quiz_index = "+ str(geometric_net_quiz_index))
	#新しい展開図を塗る
	draw_grid(canvas, geometric_net_pattern[geometric_net_quiz_index], color_bg, color_mask)

	#新しい空欄を作って塗る
	change_blank(canvas, color_bg, color_mask)


def change_blank(canvas, color_bg, color_mask):
	global blank1
	global blank2

	blank_num1 = random.randint(1, 6)
	while True:
		blank_num2 = random.randint(1, 6)
		if blank_num2 != blank_num1:
			break
	geometric_net = geometric_net_pattern[geometric_net_quiz_index]
	for i in range(4):
		for j in range(4):
			if geometric_net[i][j] == blank_num1:
				blank1[0] = i
				blank1[1] = j
			elif geometric_net[i][j] == blank_num2:
				blank2[0] = i
				blank2[1] = j
	draw_blank()

#展開図にマスクを掛ける関数
def draw_mask(canvas, geometric_net, type):
    # 格子状の正方形を描画
	for w in range(4):
		for h in range(4):
			if geometric_net[h][w] > 0:
				#
				draw_geometric_net_outline(canvas, h, w)
			elif geometric_net[h][w] == 0:
				#draw_face関数
				#一面を塗る
				draw_face(canvas, h, w, type)

def draw_geometric_net_outline(canvas, h, w):
	square_size = 30
	w1 = w * square_size * 3
	w1 += (w+1) * 10
	h1 = h * square_size * 3
	h1 += (h+1) * 10

	w2 = w1 + square_size * 3
	h2 = h1 + square_size * 3
	canvas.create_rectangle(w1, h1, w2, h2, outline="black", width=5)

def draw_face(canvas, h, w, type):
	#データは行列なので、h、wの順番
	#描画する際の指定順は、w、hの順番
	#混乱するので要注意
	square_size = 30
	w1 = w * square_size * 3
	w1 += (w+1) * 10
	h1 = h * square_size * 3
	h1 += (h+1) * 10

	w2 = w1 + square_size * 3
	h2 = h1 + square_size * 3
	if type == "background":
		canvas.create_rectangle(w1, h1, w2, h2, fill="lightblue")
	elif type == "alpha":
		n = math.floor(matrix_relation[h][w]/100)
		color = getLightColor(n)
		print("color="+color)
		canvas.create_rectangle(w1, h1, w2, h2, fill=color)#, alpha=0.5) #, alpha=0.2)
	else:
		canvas.create_rectangle(w1, h1, w2, h2, fill=type)

def draw_blank():
	draw_face(child_canvas2, blank1[0], blank1[1], "black")
	draw_face(child_canvas2, blank2[0], blank2[1], "black")

def get3x3(x,y):
	array = [
		[matrix[3*x][3*y],matrix[3*x][3*y+1],matrix[3*x][3*y+2]],
		[matrix[3*x+1][3*y],matrix[3*x+1][3*y+1],matrix[3*x+1][3*y+2]],
		[matrix[3*x+2][3*y],matrix[3*x+2][3*y+1],matrix[3*x+2][3*y+2]],
	]
	return array

def put3x3(x,y,array):
	for i in range(3):
		for j in range(3):
			matrix[3*x+i][3*y+j] = array[i][j]
	

#基本形の展開図における座標（1,1）の面を正面に置いたときの回転に特化した処理をしている。汎用性は無いので注意が必要
#キューブの1行または1列を回転させたときの処理関数
#direction: 回転の方向（X+,X-,Y-,Y+)  //旧バージョンEAST,WEST,SOUTH,NORTH）
#index: 各面におて回転させた行または列の場所（0,1,2）
#margin: 4x4の展開図において回転する面の位置（0,1,2,3）2次元配列で考える際に必要
#X+とX-の場合、indexはrow  //EASTとWESTの場合、indexはrow
#Y-とY+の場合、indexはcolumn //SOUTHとNORTHの場合、indexはcolumn
#手順
#１．ボタンに応じた行または列の回転
#２．同じキューブ面の整合性
def rotate(direction, index, geometry_net_x, geometry_net_y):
	#margin = 3*index_geometry_net
#	print("rotateボタン("+direction+","+str(index)+","+str(margin)+")")
	#１．ボタンに応じた行または列の回転
	if direction == "X+":
		margin = 3*geometry_net_x
		print("X+")
		#回転のターゲットとしている4x4の全体展開図の軸(geometry_net_x)に対して、並んでいる4面を回転させる
		temp = [matrix[margin+index][9],matrix[margin+index][10],matrix[margin+index][11]]
		for j in range(11,2,-3):
			matrix[margin+index][j] = matrix[margin+index][j-3]
			matrix[margin+index][j-1] = matrix[margin+index][j-4]
			matrix[margin+index][j-2] = matrix[margin+index][j-5]
		matrix[margin+index][2] = temp[2]
		matrix[margin+index][1] = temp[1]
		matrix[margin+index][0] = temp[0]
		#立体にした場合、端（indexが0か2）の回転は、側面の回転
		if index == 0:
			temp0 = get3x3(0,1)
			temp1 = rotate_counterclockwise(temp0)
			put3x3(0,1,temp1)
		elif index == 2:
			temp0 = get3x3(2,1)
			temp1 = rotate_clockwise(temp0)
			put3x3(2,1,temp1)
			

	elif direction == "X-":
		margin = 3*geometry_net_x
		print("X-")
		#回転のターゲットとしているに4x4の全体展開図の軸(geometry_net_x)に対して、並んでいる4面を回転させる
		temp = [matrix[margin+index][0],matrix[margin+index][1],matrix[margin+index][2]]
		for j in range(0,9,3):
			matrix[margin+index][j] = matrix[margin+index][j+3]
			matrix[margin+index][j+1] = matrix[margin+index][j+4]
			matrix[margin+index][j+2] = matrix[margin+index][j+5]
		matrix[margin+index][9] = temp[0]
		matrix[margin+index][10] = temp[1]
		matrix[margin+index][11] = temp[2]
		#立体にした場合、端（indexが0か2）の回転は、側面の回転
		if index == 0:
			temp0 = get3x3(0,1)
			temp1 = rotate_clockwise(temp0)
			put3x3(0,1,temp1)
		elif index == 2:
			temp0 = get3x3(2,1)
			temp1 = rotate_counterclockwise(temp0)
			put3x3(2,1,temp1)

	elif direction == "Y-":
		margin = 3*geometry_net_y
		print("Y-")
		#回転のターゲットとしている4x4の全体展開図の軸(geometry_net_y)に対して、並んでいる4面を回転させる
		temp = [matrix[9][margin+index],matrix[10][margin+index],matrix[11][margin+index]]
		for i in range(11,2,-3):
			print("x="+str(i))
			matrix[i][margin+index] = matrix[i-3][margin+index]
			matrix[i-1][margin+index] = matrix[i-4][margin+index]
			matrix[i-2][margin+index] = matrix[i-5][margin+index]
		matrix[2][margin+index] = temp[2]
		matrix[1][margin+index] = temp[1]
		matrix[0][margin+index] = temp[0]
		#立体にした場合、端（indexが0か2）の回転は、側面の回転
		if index == 0:
			temp0 = get3x3(1,0)
			temp1 = rotate_clockwise(temp0)
			put3x3(1,0,temp1)
		elif index == 2:
			temp0 = get3x3(1,2)
			temp1 = rotate_counterclockwise(temp0)
			put3x3(1,2,temp1)


	elif direction == "Y+":
		margin = 3*geometry_net_y
		print("Y+")
		temp = [matrix[0][margin+index],matrix[1][margin+index],matrix[2][margin+index]]
		for i in range(0,9,3):
			matrix[i][margin+index] = matrix[i+3][margin+index]
			matrix[i+1][margin+index] = matrix[i+4][margin+index]
			matrix[i+2][margin+index] = matrix[i+5][margin+index]
		matrix[9][margin+index] = temp[0]
		matrix[10][margin+index] = temp[1]
		matrix[11][margin+index] = temp[2]
		#立体にした場合、端（indexが0か2）の回転は、側面の回転
		if index == 0:
			temp0 = get3x3(1,0)
			temp1 = rotate_counterclockwise(temp0)
			put3x3(1,0,temp1)
		elif index == 2:
			temp0 = get3x3(1,2)
			temp1 = rotate_clockwise(temp0)
			put3x3(1,2,temp1)

	elif direction == "Z+":
		print("Z+")
		##展開図(行,列)(0,1)のデータを退避
		temp = [matrix[index][3],matrix[index][4],matrix[index][5]]
		##展開図(行,列)(0,1)が更新先 <- 展開図(1,0)が更新元
		matrix[index][3] = matrix[5][index]
		matrix[index][4] = matrix[4][index]
		matrix[index][5] = matrix[3][index]
			
		##展開図(行,列)(1,0) <- (2,1)
		matrix[3][index] = matrix[8-index][3]
		matrix[4][index] = matrix[8-index][4]
		matrix[5][index] = matrix[8-index][5]
			
		##展開図(行,列)(2,1) <- (1,2)
		matrix[8-index][3] = matrix[5][8-index]
		matrix[8-index][4] = matrix[4][8-index]
		matrix[8-index][5] = matrix[3][8-index]
			
		##展開図(行,列)(1,2) <- (0,1)
		matrix[3][8-index] = temp[0]
		matrix[4][8-index] = temp[1]
		matrix[5][8-index] = temp[2]

		#立体にした場合、端（indexが0か2）の回転は、側面の回転
		if index == 0:
			temp0 = get3x3(1,3)
			temp1 = rotate_counterclockwise(temp0)
			put3x3(1,3,temp1)
		elif index == 2:
			temp0 = get3x3(1,1)
			temp1 = rotate_clockwise(temp0)
			put3x3(1,1,temp1)

	elif direction == "Z-":
		print("Z-")
		##展開図(行,列)(0,1)のデータを退避
		temp = [matrix[index][3],matrix[index][4],matrix[index][5]]
		##展開図(行,列)(0,1)が更新先 <- 展開図(1,2)が更新元
		matrix[index][3] = matrix[3][8-index] 
		matrix[index][4] = matrix[4][8-index] 
		matrix[index][5] = matrix[5][8-index] 
			
		##展開図(行,列)(1,2) <- (2,1)
		matrix[3][8-index] = matrix[8-index][5] 
		matrix[4][8-index] = matrix[8-index][4] 
		matrix[5][8-index] = matrix[8-index][3] 

		##展開図(行,列)(2,1) <- (1,0)
		matrix[8-index][3] = matrix[3][index]
		matrix[8-index][4] = matrix[4][index]
		matrix[8-index][5] = matrix[5][index]
			
		##展開図(行,列)(1,0) <- (0,1)
		matrix[3][index] = temp[2]
		matrix[4][index] = temp[1]
		matrix[5][index] = temp[0]
			
		#立体にした場合、端（indexが0か2）の回転は、側面の回転
		if index == 0:
			temp0 = get3x3(1,3)
			temp1 = rotate_clockwise(temp0)
			put3x3(1,3,temp1)
		elif index == 2:
			temp0 = get3x3(1,1)
			temp1 = rotate_counterclockwise(temp0)
			put3x3(1,1,temp1)

	else:
		print("ERROR")

	#２．同じキューブ面の整合性
	if direction == "X+" or direction == "X-":
		for j in range(4):
			print("consistency1")
			consistency1(geometry_net_x, j)
	elif direction == "Y-" or direction == "Y+":
		for i in range(4):
			consistency1(i, geometry_net_y)
	elif direction == "Z+" or direction == "Z-":
		for i in range(4):
			print("consistency in rotate z")
			consistency1(0,1)
			consistency1(1,0)
			consistency1(2,1)
			consistency1(1,2)
			consistency1(1,3)
			consistency1(1,1)
		
	
	draw_grid(child_canvas, geometric_net_pattern[geometric_net_std_index], "lightblue", "lightblue")
	draw_grid(child_canvas2, geometric_net_pattern[geometric_net_quiz_index], "lightgreen", "lightgreen")
	draw_blank()
#	draw_face(child_canvas2, blank1[0], blank1[1], "black")
#	draw_face(child_canvas2, blank2[0], blank2[1], "black")


	root.update()

#def rotate_vertical(direction, column_index):
#	print("ボタン("+direction+","+str(column_index)+")")

#配列の値と色との関係
def getColor(n):
	if n == 1:
		return "white"
	elif n == 2:
		return "orange"
	elif n == 3:
		return "green"
	elif n == 4:
		return "blue"
	elif n == 5:
		return "red"
	elif n == 6:
		return "yellow"
	else:
		return "lightgray"

def getLightColor(n):
	if n == 1:
		return "#EEEEEE"
	elif n == 2:
		return "#FFE4C4"
	elif n == 3:
		return "#CCFFCC"
	elif n == 4:
		return "#FFFFCC"
	elif n == 5:
		return "#FFAAFF"
	elif n == 6:
		return "#8EB8FF"
	else:
		return "lightgray"

#展開図において、キューブの同じ面だが回転している箇所の辻褄を合わせる（回転させる）関数
def consistency0():
	print("consistency0")
	for i in range(4):
		for j in range(4):
			if geometric_net_std[i][j] > 0:
				consistency1(i,j)

#展開図において、キューブの同じ面だが回転している箇所の辻褄を合わせる（回転させる）関数
#x,y: 展開図上で、基準となる面。この面と整合性が合うように他の面を変更させる
def consistency1(x,y):
	k = matrix_relation[x][y]
	for i in range(4):
		for j in range(4):
			#100の位の値が一致した==同じ面
#			print("("+str(x)+","+str(y)+")->"+str(k)+"    ("+str(i)+","+str(j)+")->"+str(matrix_relation[i][j]))
			if math.floor(k/100) == math.floor(matrix_relation[i][j]/100):
				consistency2(x,y,i,j,matrix_relation[i][j]-k)

#右回転させる関数
def rotate_clockwise(array):
	rotated_array = [[0] * 3 for _ in range(3)]  # 3x3の新しい配列を生成

	for i in range(3):
		for j in range(3):
			rotated_array[j][2-i] = array[i][j]  # 右回転するためにインデックスを調整

	return rotated_array

#左回転させる関数
def rotate_counterclockwise(array):
	rotated_array = [[0] * 3 for _ in range(3)]  # 3x3の新しい配列を生成

	for i in range(3):
		for j in range(3):
			rotated_array[2-j][i] = array[i][j]  # 左回転するためにインデックスを調整

	return rotated_array
	

#面(x1,y1)を回転させて、その結果を面(x2,y2)に反映させる命令
def consistency2(x1,y1,x2,y2,rotate):
#	base_array = get3x3(x1,y1)
	base_array = [
		[matrix[3*x1][3*y1],matrix[3*x1][3*y1+1],matrix[3*x1][3*y1+2]],
		[matrix[3*x1+1][3*y1],matrix[3*x1+1][3*y1+1],matrix[3*x1+1][3*y1+2]],
		[matrix[3*x1+2][3*y1],matrix[3*x1+2][3*y1+1],matrix[3*x1+2][3*y1+2]],
	]
	rotated_array = [[0] * 3 for _ in range(3)]  # 3x3の新しい配列を生成
	
	#rotateが負は、左回転。右回転に変換する。
	if rotate < 0:
		rotate = 4 + rotate

	if rotate == 0:
		for i in range(3):
			for j in range(3):
				matrix[3*x2+i][3*y2+j] = base_array[i][j]
	else:
		#面の回転後の値を計算。全て右回転
		if rotate == 1:
			rotated_array = rotate_clockwise(base_array)
		elif rotate == 2:
			rotated_array = rotate_clockwise(rotate_clockwise(base_array))
		elif rotate == 3:
			rotated_array = rotate_clockwise(rotate_clockwise(rotate_clockwise(base_array)))
		
		#展開図の値に反映させる
		for i in range(3):
			for j in range(3):
				matrix[3*x2+i][3*y2+j] = rotated_array[i][j]
	


def reset_matrix(geometric_net):
	for h in range(4):
		for w in range(4):
			k = geometric_net[h][w]
			for i in range(3):
				for j in range(3):
					matrix[3*h+i][3*w+j] = k
	consistency0()
	draw_grid(child_canvas, geometric_net_pattern[geometric_net_std_index], "lightblue", "lightblue")
	draw_grid(child_canvas2, geometric_net_pattern[geometric_net_quiz_index], "lightgreen", "lightgreen")
	draw_blank()
#	draw_face(child_canvas2, blank1[0], blank1[1], "black")
#	draw_face(child_canvas2, blank2[0], blank2[1], "black")




#展開図のパターン
#0 S3を上下反転、右1回転
geometric_net0_a = [
	[1,0,0,0],
	[2,3,5,0],
	[0,6,0,0],
	[0,4,0,0],
]
#1 S1を上下反転、右1回転
geometric_net0_b = [
	[1,0,0,0],
	[2,3,0,0],
	[0,6,0,0],
	[0,4,5,0],
]
#2 標準状態を右3回転
geometric_net1_a = [
	[0,1,0,0],
	[2,3,5,0],
	[0,6,0,0],
	[0,4,0,0],
]
#3 S6を右1回転
geometric_net1_b = [
	[0,1,0,0],
	[0,3,5,0],
	[0,6,0,0],
	[2,4,0,0],
]
#4 S6を左右反転の右1回転
geometric_net1_c = [
	[0,1,0,0],
	[2,3,0,0],
	[0,6,0,0],
	[0,4,5,0],
]
#5 S8を右2回転
geometric_net1_d = [
	[0,1,0,0],
	[0,3,0,0],
	[0,6,0,0],
	[2,4,5,0],
]
#6 S3を右1回転
geometric_net2_a = [
	[0,0,1,0],
	[2,3,5,0],
	[0,6,0,0],
	[0,4,0,0],
]
#7 S1を右3回転
geometric_net2_b = [
	[0,0,1,0],
	[0,3,5,0],
	[0,6,0,0],
	[2,4,0,0],
]
#8 S8を右1回転
geometric_net0_0 = [
	[1,0,0,0],
	[2,3,5,4],
	[6,0,0,0],
	[0,0,0,0],
]
#9 S7と同じ
geometric_net0_1 = [
	[1,0,0,0],
	[2,3,5,4],
	[0,6,0,0],
	[0,0,0,0],
]
#10 S6と同じ
geometric_net0_2= [
	[1,0,0,0],
	[2,3,5,4],
	[0,0,6,0],
	[0,0,0,0],
]
#11 S5と同じ
geometric_net0_3 = [
	[1,0,0,0],
	[2,3,5,4],
	[0,0,0,6],
	[0,0,0,0],
]
#12 S7を上下反転
geometric_net1_0 = [
	[0,1,0,0],
	[2,3,5,4],
	[6,0,0,0],
	[0,0,0,0],
]
#13 標準状態と同じ
geometric_net1_1 = [
	[0,1,0,0],
	[2,3,5,4],
	[0,6,0,0],
	[0,0,0,0],
]
#14 S4と同じ
geometric_net1_2 = [
	[0,1,0,0],
	[2,3,5,4],
	[0,0,6,0],
	[0,0,0,0],
]
#15 S6を右2回転
geometric_net1_3 = [
	[0,1,0,0],
	[2,3,5,4],
	[0,0,0,6],
	[0,0,0,0],
]
#16 S6を上下反転
geometric_net2_0 = [
	[0,0,1,0],
	[2,3,5,4],
	[6,0,0,0],
	[0,0,0,0],
]
#17 S4を上下反転
geometric_net2_1 = [
	[0,0,1,0],
	[2,3,5,4],
	[0,6,0,0],
	[0,0,0,0],
]
#18 標準状態を右2回転
geometric_net2_2 = [
	[0,0,1,0],
	[2,3,5,4],
	[0,0,6,0],
	[0,0,0,0],
]
#19 S7を右2回転
geometric_net2_3 = [
	[0,0,1,0],
	[2,3,5,4],
	[0,0,0,6],
	[0,0,0,0],
]
#20 S5を上下反転
geometric_net3_0 = [
	[0,0,0,1],
	[2,3,5,4],
	[6,0,0,0],
	[0,0,0,0],
]
#21 S6を左右反転
geometric_net3_1 = [
	[0,0,0,1],
	[2,3,5,4],
	[0,6,0,0],
	[0,0,0,0],
]
#22 S7を左右反転
geometric_net3_2 = [
	[0,0,0,1],
	[2,3,5,4],
	[0,0,6,0],
	[0,0,0,0],
]
#23 S8を左右反転
geometric_net3_3 = [
	[0,0,0,1],
	[2,3,5,4],
	[0,0,0,6],
	[0,0,0,0],
]

#1 S1を上下反転、右1回転
#2 標準状態を右3回転
#3 S6を右1回転
#4 S6を左右反転の右1回転
#5 S8を右2回転
#6 S3を右1回転
#7 S1を右3回転
#8 S8を右1回転
#9 S7と同じ
#10 S6と同じ
#11 S5と同じ
#12 S7を上下反転
#13 標準状態と同じ
#14 S4と同じ
#15 S6を右2回転
#16 S6を上下反転
#17 S4を上下反転
#18 標準状態を右2回転
#19 S7を右2回転
#20 S5を上下反転
#21 S6を左右反転
#22 S7を左右反転
#23 S8を左右反転
geometric_net_pattern = [
	geometric_net0_a,
	geometric_net0_b,
	geometric_net1_a,
	geometric_net1_b,
	geometric_net1_c,
	geometric_net1_d,
	geometric_net2_a,
	geometric_net2_b,
	geometric_net0_0,
	geometric_net0_1,
	geometric_net0_2,
	geometric_net0_3,
	geometric_net1_0,
	geometric_net1_1,
	geometric_net1_2,
	geometric_net1_3,
	geometric_net2_0,
	geometric_net2_1,
	geometric_net2_2,
	geometric_net2_3,
	geometric_net3_0,
	geometric_net3_1,
	geometric_net3_2,
	geometric_net3_3,
]

#展開図として有効とする箇所


geometric_net_std_index = 13
geometric_net_quiz_index = 3
geometric_net_std = geometric_net_pattern[geometric_net_std_index]
geometric_net_quiz = geometric_net_pattern[geometric_net_quiz_index]

#geometric_net_std = [
#	[0,1,0,0],
#	[2,3,5,4],
#	[0,6,0,0],
#	[0,0,0,0],
#]


#展開図の各値（１面が3x3、それが、4x4の展開図）
matrix = [
    [0,0,0,   1,1,1,   0,0,0,   0,0,0],
    [0,0,0,   1,1,1,   0,0,0,   0,0,0],
    [0,0,0,   1,1,1,   0,0,0,   0,0,0],

    [2,2,2,   3,3,3,   5,5,5,   4,4,4],
    [2,2,2,   3,3,3,   5,5,5,   4,4,4],
    [2,2,2,   3,3,3,   5,5,5,   4,4,4],

    [0,0,0,   6,6,6,   0,0,0,   0,0,0],
    [0,0,0,   6,6,6,   0,0,0,   0,0,0],
    [0,0,0,   6,6,6,   0,0,0,   0,0,0],

    [0,0,0,   0,0,0,   0,0,0,   0,0,0],
    [0,0,0,   0,0,0,   0,0,0,   0,0,0],
    [0,0,0,   0,0,0,   0,0,0,   0,0,0],
]

#展開図の面同士の関係
matrix_relation = [
	[103,100,101,102],
	[200,300,500,400],
	[601,600,603,602],
	[202,402,502,302],
]


# ウィンドウを作成
root = tk.Tk()
root.title("ルービックキューブの展開図上での回転シミュレーション")

# 親キャンバスを作成
parent_canvas = tk.Canvas(root, width=1200, height=700, bg="white")
parent_canvas.pack()

# 子キャンバスを作成して親キャンバスに配置
child_canvas = tk.Canvas(parent_canvas, width=410, height=410, bg="lightblue")
parent_canvas.create_window(75, 75, window=child_canvas)
child_canvas.place(x=100, y=150)

# 子キャンバスを作成して親キャンバスに配置
child_canvas2 = tk.Canvas(parent_canvas, width=410, height=410, bg="lightgreen")
parent_canvas.create_window(75, 75, window=child_canvas2)
child_canvas2.place(x=650, y=150)

#ボタンの配置
#index_geometry_net_*はボタンごとに設定する。そのボタンが展開図の縦横のどの位置に影響するかを示す。
#index_geometry_net_h: 4x4の展開図の縦の位置
#index_geometry_net_w: 4x4の展開図の横の位置

geometry_net_x = 1
geometry_net_y = 1

buttonE0 = tk.Button(parent_canvas, text="X0+", command=lambda: rotate("X+", 0, 1, 1))
buttonE1 = tk.Button(parent_canvas, text="X1+", command=lambda: rotate("X+", 1, 1, 1))
buttonE2 = tk.Button(parent_canvas, text="X2+", command=lambda: rotate("X+", 2, 1, 1))
buttonE0.place(x=530, y=250)
buttonE1.place(x=530, y=290)
buttonE2.place(x=530, y=330)

buttonW0 = tk.Button(parent_canvas, text="X0-", command=lambda: rotate("X-", 0, 1, 1))
buttonW1 = tk.Button(parent_canvas, text="X1-", command=lambda: rotate("X-", 1, 1, 1))
buttonW2 = tk.Button(parent_canvas, text="X2-", command=lambda: rotate("X-", 2, 1, 1))
buttonW0.place(x=25, y=250)
buttonW1.place(x=25, y=290)
buttonW2.place(x=25, y=330)

buttonS0 = tk.Button(parent_canvas, text="Y0-", command=lambda: rotate("Y-", 0, 1, 1))
buttonS1 = tk.Button(parent_canvas, text="Y1-", command=lambda: rotate("Y-", 1, 1, 1))
buttonS2 = tk.Button(parent_canvas, text="Y2-", command=lambda: rotate("Y-", 2, 1, 1))
buttonS0.place(x=190, y=570)
buttonS1.place(x=235, y=570)
buttonS2.place(x=280, y=570)

buttonN0 = tk.Button(parent_canvas, text="Y0+", command=lambda: rotate("Y+", 0, 1, 1))
buttonN1 = tk.Button(parent_canvas, text="Y1+", command=lambda: rotate("Y+", 1, 1, 1))
buttonN2 = tk.Button(parent_canvas, text="Y2+", command=lambda: rotate("Y+", 2, 1, 1))
buttonN0.place(x=190, y=110)
buttonN1.place(x=235, y=110)
buttonN2.place(x=280, y=110)


buttonZplus0 = tk.Button(parent_canvas, text="Z0-", command=lambda: rotate("Z-", 0, 0, 1))
buttonZplus1 = tk.Button(parent_canvas, text="Z1-", command=lambda: rotate("Z-", 1, 0, 1))
buttonZplus2 = tk.Button(parent_canvas, text="Z2-", command=lambda: rotate("Z-", 2, 0, 1))
buttonZplus0.place(x=25, y=145)
buttonZplus1.place(x=25, y=180)
buttonZplus2.place(x=25, y=215)

buttonZminus0 = tk.Button(parent_canvas, text="Z0+", command=lambda: rotate("Z+", 0, 0, 1))
buttonZminus1 = tk.Button(parent_canvas, text="Z1+", command=lambda: rotate("Z+", 1, 0, 1))
buttonZminus2 = tk.Button(parent_canvas, text="Z2+", command=lambda: rotate("Z+", 2, 0, 1))
buttonZminus0.place(x=530, y=145)
buttonZminus1.place(x=530, y=180)
buttonZminus2.place(x=530, y=215)




# その他のボタンを作成
button1 = tk.Button(parent_canvas, text="リセット", command=lambda: reset_matrix(geometric_net_pattern[geometric_net_std_index])).place(x=150,y=630)
button2 = tk.Button(parent_canvas, text="閉じる", command=close_window).place(x=250,y=630)
button3 = tk.Button(parent_canvas, text="答え", command=lambda: draw_grid(child_canvas2, geometric_net_pattern[geometric_net_quiz_index], "lightgreen", "lightgreen")).place(x=750,y=630)
button4 = tk.Button(parent_canvas, text="変更", command=lambda: change_grid(child_canvas2, "lightgreen", "lightgreen")).place(x=850,y=630)

# 展開図（格子状の正方形）を描画
consistency0()
draw_grid(child_canvas, geometric_net_pattern[geometric_net_std_index], "lightblue", "lightblue")
draw_grid(child_canvas2, geometric_net_pattern[geometric_net_quiz_index], "lightgreen", "lightgreen")

#空欄の設定
blank1 = [3,1]
blank2 = [3,0]
draw_blank()
#draw_face(child_canvas2, blank1[0], blank1[1], "black")
#draw_face(child_canvas2, blank2[0], blank2[1], "black")
#draw_mask(child_canvas, geometric_net_std, "alpha")


# ウィンドウを表示
root.mainloop()
