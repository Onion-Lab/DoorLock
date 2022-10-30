from pyfcm import FCMNotification

# Firebase에서 얻은 server key. 알맞게 수정할 것 https://console.firebase.google.com/project/doorlock-a24a7/settings/cloudmessaging/android:com.example.doorlock?hl=ko
APIKEY = "AAAAGvjpuyM:APA91bFGtknraBd855RXsj41nCbznfL2AYodim8_6HhhQhtsLO2q8Y7Bb5NXbvFawIZ1cjXCxKQucRensAVhEzShYDEk6b-C5IUqvTXqBJ3OnZ4tQK1vIBOME5IjunUKrjkn9xh1oFqf"

# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)

def sendMessage(message, title):
    # 메시지 (data 타입)
    data_message = {
        "message": message,
        "title": title
    }
    # topic을 이용해 다수의 구독자에게 푸시알림을 전송함
    result = push_service.notify_topic_subscribers(topic_name="warn", data_message=data_message)

    # 전송 결과 출력
    print(result)


if __name__ == "__main__":
    sendMessage("warn", "미등록 사용자")
