# SecurityCCTV

# 2023-10-19
정원진 : 라즈베리파이4를 활용하여 실시간 영상감치 시스템을 구축할려고함.
라즈베리파이4에 os를 설치하는데 raspberry pi imager v1.7.5를 사용하였고, 운영체제를 bookworm을 사용하였는데 vnc가 자꾸 안붙어서 stackoverflow와 github에서 확인해보니 호환성 문제가 3,4일전부터 확인되었다는 게시글이 확인되었다.(https://github.com/raspberrypi/bookworm-feedback/issues/41) 따라서 그전 버전인 bullseye로 64-bit os를 다운받아서 설치하였더니 vnc가 붙어서 ssh 방식으로 원격을 활용 중 이다.
현재 목표는 라즈베리파이에 yolo v8를 넣어서 그 안에서 객체를 인식하는 비디오를 뽑아내고 서버로 TCP 스트림식으로 보내는걸 목표로 가지고있다.

# 2023-10-23
정원진 : 라즈베리파이4에 openCV를 활용하여 웹 스트리밍 방식을 활용하기위하여 설치중인데, 통상적으로 사용하는 방법으로 jpg이미지를 가져오고 저장하는 패키지 중에 이름이 바뀌거나 사라진 패키지가 많아서 에러가 많이 발생하여 4일정도 서칭한결과 github에 올라가져있는 opencv 패키지를 다이랙트로 긁어와서 설치하는 방식을 활용하기로했다.( 다운로드만 1시간 정도 걸림 ) (참고 : https://velog.io/@kaiseong/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4-OpenCV%EC%84%A4%EC%B9%98 )
그리고 라즈베리파이4에서 thonny라는 PYTHON IDE 툴에서 YOLO를 활용하여 영상을 서버로 옮겨주는 방식을 생각했다가, 우선 가장 기본 로직으로 가져가고 추후에 활용하는 방식으로 가져가기위하여 라즈베리파이에서 영상을 웹 스트리밍 방식으로 제공하고 서버에서 해당 영상을 가져와서 YOLO 모델을 거쳐서 YOLO 모델 영상을 FLUTTER ( 클라이언트 )에  뿌려주는 로직으로 가져가는걸 구상하고있다.

라즈베리파이4에서 test.py에 opencv를 활용하여 비디오가 정상실행을 확인하고, 웹스트리밍을 활용하기위해 mjpg_streamer을 활용하하여 아이피:8090 port로 정상 구현 확인하였다. ( 참고 : https://jow1025.tistory.com/295 )
![image](https://github.com/wonjin0307/SecurityCCTV/assets/87004845/21cfcb8a-23d8-474a-9c7c-9da5c38f3f8d)

터미널에서 웹스트리밍을 실행시키고, 종료를 시켰을때 프로세스자체를 종료하지않으면 좀비프로세스로 떠돌고있으므로, kill -9 PID번호 를 활용하여 완전히 종료 시켜준다.

# 2023-11-05
정원진  : 라즈베리파이4에서 mjpg-streamer를 활용하여 웹 스트리밍 서버를 열어서 실시간 영상을 송출하였고, flutter 라이브러리 중 mjpg-stream을 다이랙트로 받는 라이브러리가 pubget에 있어서 활용하였더니 해당 영상을 가져오는것을 성공. 그러나 yolo v8 를 욜로에 설치해서 detection된 영상을 다시 웹 서버로 송출하는게 딜레이는 적을꺼같은데 라즈베리파이4가 버텨줄지 의문이다.. 따라서 보다 안전하게 차라리 웹 스트리밍 서버로부터 영상을 외부 컴퓨터에서 받고 받은 서버에서 YOLO DETECTION 작업을 시키고 작업이 된 영상을 서버에 송출하고 FLUTTER에서 해당 비디오를 가져오는 방식으로 진행할 예정이다.

# 2023-11-08
정원진 : flask를 설치하고, mjpg-streamer에서 실시간 스트리밍 영상을 opencv를 활용하여 서버로 가져오고 , 가져온 영상을 yolo model에 입혀서 디택션되는 영상을 flask 서버에 스트리밍하는 방식으로 진행했고, opencv에서 VideoCapture를 통해 영상을 가져오고 해당 영상에서 다시 스트리밍 하는 방식에서 많이 해맸는데, 구글링을 통해 프레임 자체를 바이트로 변환이 필요하다는 사실을 알게되었고, 스트리밍된 프레임을 반환하는 코드에 주석처리를하며 공부하면서 진행하느냐 시간이 많이 걸렸다. ( 참고 : https://colinch4.github.io/2023-09-06/09-24-30-287952/ )
