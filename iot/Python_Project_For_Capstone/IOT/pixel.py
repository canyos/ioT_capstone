import cv2


#x는 왼쪽위로부터 아래로 몇 떨어져있는지
#y는 왼쪽위로부터 오른쪽으로 몇 떨어져있는지
#fire 이상은 확실한 빨간색 2반환
#maybe 이상은 온도확인 1반환
#이하는 유의미한 차이 0반환
#sample_size는 짜를 크기
fire = 100
maybe = 30
def check_red(x,y,size,index):
    image_path = '/home/pc/Desktop/'+index+'.jpg'
    image = cv2.imread(image_path)
    height, width, channels = image.shape
    
    outer_sum=0
    inner_sum=0
    for i in range(max(0,x-2* size),min(height,x+2* size)) :
        for j in range(max(0,y-2* size),min(width,y+2* size)):
            (b, g, r) = image[i, j]
            outer_sum+=r-min(b,g,r)
            if i>=max(0,x- size) and i<min(height,x+ size) and j>=max(0,y- size) and j<min(width,y+ size):
                inner_sum += r-min(b,g,r)
    
    outer_avg = outer_sum/ (2*size)**2
    inner_avg = inner_sum/  size**2
    if inner_avg-outer_avg>=fire:return 2
    elif inner_avg-outer_avg>=maybe:return 1
    return 0
