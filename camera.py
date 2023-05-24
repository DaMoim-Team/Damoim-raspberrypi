import cv2
import time
import os

# 카메라 객체
camera = None
fps = 3

# 카메라 초기화
def init(camera_id=0, width=640, height=480, buffer_size=1, fps=fps):
	global camera
	# 카메라 설정
	camera = cv2.VideoCapture(camera_id)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
	camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
	camera.set(cv2.CAP_PROP_FPS, fps)

	if not camera.isOpened():
		print("Camera could not be opened.")

# 특정 시간 동안 비디오를 녹화하고 파일에 저장
def record_video(duration, output_filename="output.mp4"):
	global camera

	start_time = time.time()
	frame_count = 0

	#지정된 시간동안 촬영할 프레임 수  
	target_frame_count = int(duration * fps)

	# 현재 카메라의 프레임 너비와 높이를 가져옴
	frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

  # 비디오 저장을 위한 VideoWriter 객체를 초기화
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
	
	while True:
		success, frame = camera.read()
		if success:
			# 프레임을 디스크에 저장
			out.write(frame)
			frame_count += 1
            
      # 경과 시간 확인
			elapsed_time = time.time() - start_time
			# 경과 시간이 녹화 시간을 초과하면 녹화 중지
			if elapsed_time > duration:
				break
		else:
			break

	# 녹화가 끝나면 객체 종료
	out.release()

# 카메라 해제
def final():
	global camera
	if camera != None:
		camera.release()
	camera = None
