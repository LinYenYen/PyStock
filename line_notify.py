import requests


####################################################################################################
#                                             Setting                                              #
####################################################################################################



####################################################################################################
#                                             Variable                                             #
####################################################################################################



####################################################################################################
#                                             Function                                             #
####################################################################################################
def sendline(line: str, message: str):
    headers = {
        'Authorization': f'Bearer {line}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {'message': message}
    
    r = requests.post(url='https://notify-api.line.me/api/notify', headers=headers, params=params)

    # print(r.status_code)  #200



####################################################################################################
#                                               Test                                               #
####################################################################################################
if __name__ == '__main__':
    line = 'uv1r310Fa14UOhWq9IMXTiCt03OTtqj6rkROUnvx5pq'
    message = 'test'

    headers = {
        'Authorization': f'Bearer {line}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {'message': message, 'imageFile': 'D:\Project\PyStock\stock.png'}
    r = requests.post(url='https://notify-api.line.me/api/notify', headers=headers, params=params)

    # 上傳圖片無法成功......
    # params = {'message': message, 'imageFile': open('D:\Project\PyStock\stock.png', 'rb')}
    # r = requests.post(url='https://notify-api.line.me/api/notify', headers=headers, params=params)

    print(r.status_code)  #200