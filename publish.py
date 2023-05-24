import time
import base64
import paho.mqtt.client as mqtt
import json
import camera
import os
from config import Config # 구성값 설정파일

flag = False

# 연결이 되면 바로 'command' 토픽으로 subscribe
def on_connect(client, userdata, flag, rc):
        print("connectedd")
        client.subscribe("action", qos = 0)

# 'command'라는 토픽으로 데이터가 오면 호출
def on_message(client, userdata, msg) :
        global flag

        command = msg.payload.decode("utf-8")
        if command == "goStop" :
                flag = True if(flag == False) else False

# 브로커 IP
broker_ip = Config.BROKER_ADDRESS

# mqtt 객체 생성
client = mqtt.Client()
client.on_connect = on_connect	
client.on_message = on_message

# 브로커 연결
client.connect(broker_ip, 1883)	
client.loop_start()

# 카메라 객체 생성
camera.init(width=640, height=480, fps=3)

# 청크 사이즈
chunk_size = 512 * 1024

# video_boundary 신호
video_boundary = b'--video-boundary--'
base64_video_boundary = base64.b64encode(video_boundary)
video_boundary_ascii = base64_video_boundary.decode('ascii')

# complete 신호
complete = b'complete'
base64_complete = base64.b64encode(complete)
complete_ascii = base64_complete.decode('ascii')

start_time = time.time()

# video parameters
video_duration = 120 #2min
video_output = 'output.mp4'

try:
	while True :
		# 영상 촬영
		camera.record_video(duration=video_duration, output_filename="output.mp4")

		# 촬영한 영상 파일을 청크로 전송
		with open(video_output, 'rb') as video_file:
			while True:
            			chunk = video_file.read(chunk_size)
            			if not chunk:
                			break

            			# MQTT를 통해 청크 전송
            			base64_chunk = base64.b64encode(chunk)
            			ascii_chunk = base64_chunk.decode('ascii')
            			client.publish("cctv_1", ascii_chunk, qos=0)

		# boundary 신호 보내기
		client.publish("cctv_1", video_boundary_ascii, qos=0)
		client.publish("cctv_1", complete_ascii, qos=0)

    # 촬영한 영상 지움
		os.remove(video_output)

except KeyboardInterrupt:
	print("Interrupted by user. Cleaning up")
except Exception as e:
  print("An error occurred: ", e)
finally:
	camera.final()
	client.loop_stop()
	client.disconnect()
