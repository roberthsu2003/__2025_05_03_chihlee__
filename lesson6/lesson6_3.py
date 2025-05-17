import random

def play_game():
    min = 1
    max = 100
    count = 0
    target = random.randint(1, 100)
    print(target)
    print("===============猜數字遊戲=================:\n")
    while(True):
        count += 1
        keyin = int(input("猜數字範圍{0}~{1}:".format(min, max)))
        if(keyin >=min and keyin <= max):
            if(keyin == target):
                print("賓果!猜對了, 答案是:", target)
                print("您猜了",count,"次")
                break
            elif (keyin > target):
                max = keyin
                print("再小一點")
            elif (keyin < target):
                min = keyin
                print("再大一點")
            print("您猜了",count,"次\n")
        else:
            print("請輸入提示範圍內的數字")

play_game()
print("遊戲結束")