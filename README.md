# SecurityCCTV

# 2023-10-19
정원진 : 라즈베리파이4를 활용하여 실시간 영상감치 시스템을 구축할려고함.
라즈베리파이4에 os를 설치하는데 raspberry pi imager v1.7.5를 사용하였고, 운영체제를 bookworm을 사용하였는데 vnc가 자꾸 안붙어서 stackoverflow와 github에서 확인해보니 호환성 문제가 3,4일전부터 확인되었다는 게시글이 확인되었다.(https://github.com/raspberrypi/bookworm-feedback/issues/41) 따라서 그전 버전인 bullseye로 64-bit os를 다운받아서 설치하였더니 vnc가 붙어서 ssh 방식으로 원격을 활용 중 이다.
현재 목표는 라즈베리파이에 yolo v8를 넣어서 그 안에서 객체를 인식하는 비디오를 뽑아내고 서버로 TCP 스트림식으로 보내는걸 목표로 가지고있다.

# 2023-10-23
정원진 : 라즈베리파이4에 openCV를 활용하여 웹 스트리밍 방식을 활용하기위하여 설치중인데, 통상적으로 사용하는 방법으로 jpg이미지를 가져오고 저장하는 패키지 중에 이름이 바뀌거나 사라진 패키지가 많아서 에러가 많이 발생하여 4일정도 서칭한결과 github에 올라가져있는 opencv 패키지를 다이랙트로 긁어와서 설치하는 방식을 활용하기로했다.( 다운로드만 1시간 정도 걸림 ) (참고 : https://velog.io/@kaiseong/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4-OpenCV%EC%84%A4%EC%B9%98 )
그리고 라즈베리파이4에서 thonny라는 PYTHON IDE 툴에서 YOLO를 활용하여 영상을 서버로 옮겨주는 방식을 생각했다가, 우선 가장 기본 로직으로 가져가고 추후에 활용하는 방식으로 가져가기위하여 라즈베리파이에서 영상을 웹 스트리밍 방식으로 제공하고 서버에서 해당 영상을 가져와서 YOLO 모델을 거쳐서 YOLO 모델 영상을 FLUTTER ( 클라이언트 )에  뿌려주는 로직으로 가져가는걸 구상하고있다.

라즈베리파이4에서 test.py에 opencv를 활용하여 비디오가 정상실행을 확인하고, 웹스트리밍을 활용하기위해 mjpg_streamer을 활용하하여 아이피:8090 port로 정상 구현 확인하였다. ( 참고 : https://jow1025.tistory.com/295 )


터미널에서 웹스트리밍을 실행시키고, 종료를 시켰을때 프로세스자체를 종료하지않으면 좀비프로세스로 떠돌고있으므로, kill -9 PID번호 를 활용하여 완전히 종료 시켜준다.

# 2023-11-05
정원진  : 라즈베리파이4에서 mjpg-streamer를 활용하여 웹 스트리밍 서버를 열어서 실시간 영상을 송출하였고, flutter 라이브러리 중 mjpg-stream을 다이랙트로 받는 라이브러리가 pubget에 있어서 활용하였더니 해당 영상을 가져오는것을 성공. 그러나 yolo v8 를 욜로에 설치해서 detection된 영상을 다시 웹 서버로 송출하는게 딜레이는 적을꺼같은데 라즈베리파이4가 버텨줄지 의문이다.. 따라서 보다 안전하게 차라리 웹 스트리밍 서버로부터 영상을 외부 컴퓨터에서 받고 받은 서버에서 YOLO DETECTION 작업을 시키고 작업이 된 영상을 서버에 송출하고 FLUTTER에서 해당 비디오를 가져오는 방식으로 진행할 예정이다.

# 2023-11-08
정원진 : flask를 설치하고, mjpg-streamer에서 실시간 스트리밍 영상을 opencv를 활용하여 서버로 가져오고 , 가져온 영상을 yolo model에 입혀서 디택션되는 영상을 flask 서버에 스트리밍하는 방식으로 진행했고, opencv에서 VideoCapture를 통해 영상을 가져오고 해당 영상에서 다시 스트리밍 하는 방식에서 많이 해맸는데, 구글링을 통해 프레임 자체를 바이트로 변환이 필요하다는 사실을 알게되었고, 스트리밍된 프레임을 반환하는 코드에 주석처리를하며 공부하면서 진행하느냐 시간이 많이 걸렸다. ( 참고 : https://colinch4.github.io/2023-09-06/09-24-30-287952/ )
또한 yolo v8x 모델을 입혔었는데 , 딜레이가 아주 심하게 걸려서 왜 그러나 했는데 cuda를 사용하는데 cpu 전용을 사용하고있다, gpu가 없기때문에 이 때문에 연산처리과정이 느려서 아무래도 딜레이가 걸린다고 예상된다. 따라서 현재는 cpu-cuda 를 사용중이지만 안양 연구실에서 2080ti GPU 를 가져와서 장착후 , GPU-CUDA 를 활용하여 딜레이를 줄일 생각이다.

# 2023-11-13
정원진 : 저번주에 backend 에 가상환경을 설정하고 flask, opencv-python, yolo 를 설치하고 라즈베리파이에서 mjpg-streamer서버로 실시간 영상을 송출하고 opencv 를 통하여 서버에서 영상을 가져오고, 가져온 영상을 yolov8n 모델을 적용하여 flask 서버로 송출하는 방식을 사용하여 github에 push를 했는데 push하는 과정에서 venv(가상환경)에 있는 라이브러리 용량이 1.5기가바이트나 차지한다고 에러가 발생하여 왜 그러나 확인해봤더니 github limit 용량이 2G 라서 venv를 포함한 project 폴더가 2.5G 가 넘어가서 에러가 나는 상황이였다. 따라서 git 활용을 할때의 유의사항과 자세하게 공부하기위해 (DO IT GIT ) 책을 통하여 공부를 진행하게되었고, 결과적으로 원격 레파지토리를 CCTV_BACKEND/CCTV_FRONTEND로 나눴고, VENV와 같은 가상환경은 제외하고 .py 파일만 업로드하여 정리하기 위하여 lib 폴더를 따로 생성하여 index.html/app.py/main.py/dectection.py 와 같은 파일만 업로드하여 버전관리를 진행하기로 하였다. 추가적으로 git 공부한 내용을 정리하여 올려두도록 하겠다.
![image](https://github.com/wonjin0307/Security_CCTV_backend/assets/87004845/42041e88-2ecc-4836-9912-52de32524250)
추가적으로 venv는 업로드를 안한 상태이니, 다른 개발환경에서는 가상환경을 설치해야되고, 가상환경에서 flask,opencv,yolo(ultralytics) 설치해야한다.

# 2023-11-16
정원진 : 서버에서 opencv 를 활용하여 인코딩을할때 jpg 확장자로 인코딩 처리를 하고 인코딩된 이미지를 바이트로 변환하여 frame 변수에 저장하고, 저장한 프레임을 yield를 활용하여 웹서버에 전송하는 형태로 MJPEG 스트리밍으로 구현하고있었는데, 이 기본 원리를 아예 생각하지않고 그저 FLASK 서버에서 FLUTTER 클라이언트로 실시간영상을 가져오는 방법을 구글링하여 찾을 생각만 해서 이틀을 날렸었다.. 처음에는 video_player라는 라이브러리를 pub get에서 가져와서 쓸려고했는데, ios/androi 에서만 활용이 가능하다는 사실을 늦게 알게되어 1시간동안 삽질을 진행하였고, 구글에 stream video 라는 용어를 사용하여 막 구글링을 뒤지다가 webRTC라는 API를 알게되었는데, 실시간 영상통화와같은 플랫폼인 ZOOM에서 활용되는 기능으로 클라이언트-클라이언트의 1대1방식에서 실시간으로 비디오 및 음성 및 데이터를 p2p 방식으로 전송되도록 지원하는 기능이며, 말 그대로 실시간으로 활용되는 개념이다 이걸 공부를하다가, 문득 나는 그저 라즈베리파이캠에서 스트리밍을 시키고 그 스크리밍된 영상을 opencv로 flask서버에 끌고와서 yolo 모델을 입히고 다시 스트리밍을 시키고있는거를 flutter에서 끌고오기만하는 형태인데 클라이언트-서버라서 이 방식을 사용하는게 맞는건가 ? 싶어서 다른 방식을 검색해야지 하다가 결국에는 video_player에서 windows app 을 지원하는 라이브러리를 찾아서 바로 적용을 해봤다 그러나 예외처리에 있어서 삽질을 또 진행하게되었고, try catch 구문을 활용하여 예외처리를 진행해줬는데, video의 형식이 자꾸 호환이 안된다고 떠서 검색을 해봤는데 아무리 검색을 해도 나오지않았다.. 다음날에 다시 처음부터 천천히 생각했는데 맨 처음 말했던 mjpeg 스트리밍 방식을 사용했었다 라는 말이 생각났고, mjpeg 스트리밍 을 가져오는 방식을 구글에 검색을했는데 pub get에 지원하는 라이브러리가있었다 .. 이번 일을 계기로 직관적으로 보이는 오류에 대해 너무 깊게 생각했다라는 생각이 들었고 오히려 오류가 뜬 부분의 원리를 생각하여 처음부터 지금까지 진행해온 로직을 차근차근 밟아가면서 생각해서 다가가야된다는걸 배웠다.
아무튼, 현재 flutter에서 flask mjpeg스트리밍 영상을 잘 가져왔고, 그전에는 영상이 640x640사이즈였는데 (32size단위로만 호환가능) 좀 더 가시성이 좋게 사이즈를 960 x 640 으로 변경하여 적용시켰다.[참조:https://pub.dev/packages/flutter_mjpeg]

# 2023-11-27
정원진 : flask 서버에서 디택션된 class_id를 딕셔너리형태로 바꿔서 해당 정보를 realtime firebase에 연동하여 실시간으로 감지가 되면 DB에 저장되는 형식으로 코드를 진행하였다. 그러나 비디오 FPS를 따지지않고 매 프레임마다 결과값을 DB에 반영하는 코드와 프레임을 스트리밍Video형태로 서버로 전송하는 코드가 while문에서 같이 돌다보니깐 딜레이가 걸리는걸 확인할 수 있었는데, 다시 생각해보면 매 프래임 마다의 정보를 가지고 오게된다면, 육안으로 cctv를 봤을때 깜빡의 정도에서도 감지리스트에는 디택션이 됐다고 올라올 수준으로 민감도가 매우 높아서 정확성이 떨어질 수 있다는 생각이들었다. 따라서 비디오의 프레임마다가 아니라 1초를 기준으로 두고 1초정도 디택션이 유지가 되었을때, 리스트에 반영할 수 있도록 감지 정보를 DB에 전송하는 형태로 진행하였다.

# 2023-11-27
정원진 : flask 서버에서 realtime batabase를 활용하여 데이터를 보내고 flutter에서 데이터를 받는 형식으로 진행할려고 그랬는데, realtime batabase가 windows app을 지원을 안해서 flutter-firebase가 붙지 못하는 상황이 와버렸다. 그래서 해결 방법을 고안했는데, firebase에 있는 데이터를 http 와 streambuilder라는 라이브러리를 활용하여 해당 DB에서 실시간으로 추가되는 데이터를 감지하여 추가되면 가져오는 방식으로 사용하기로 했다.
_________________________________________________________________
위 방식으로 진행할려고 그랬는데 jsondecoding에서 firebaseDB에서 URL이 자꾸 다른 형식으로 가져와서 print()를 찍어봤는데 그냥 html그래로 통으로 긁어오는거같아서 실패하였다. 그래서 그냥 flutter-flask 방식으로 연동하는 방식으로 진행하기로하였다.

# 2023-11-28
정원진 : flutter에서 socket_io_client 라이브러리를 활용하여 flask 서버에 접속하여, flask에서 디택션되는 정보를 딕셔너리형태로 변환하여 해당 데이터를 socket을 통하여 flutter로 다이렉트로 딕셔너리가 변하면 보내주는 형태로 코드를 작성하였고, flutter에서는 바뀐 데이터를 받는것 까지 성공하였다. 처음에는 연결이 안돼서 머가 문제인지 확인해봤는데, flutter와 flask에서의 socket 라이브러리의 버전이 서로 안맞아서 일어나는 오류였고, 버전을 맞춰서 활용했더니 성공적으로 붙었다.
DB를 따로 사용하지않고 다이렉트로 데이터를 보내는 형식이여서 보낸 딕셔너리 데이터를 FLUTTER에서 따로 만든 list에 차곡차곡 쌓는 형태로 진행하였으며, listview로 목록을 보여주는 형태로 진행하였다.

# 2023-12-07
정원진 : 실시간 cctv 부분에서는 flask 서버에서 영상을 가져와서 그대로 스트리밍 하는 형식에서 flask가 video프레임만 던져주는 형식이 아니라 class_id도 같이 던져 주는 형태로 진행하여 listview로 보여주는 방식이 가능했는데, 비디오를 첨부하는 페이지에서는 어떻게 로직을 구현해야될지 고민이 많이 되었다. 해당 페이지를 열게되면, 버튼이 총 3개가 생기는데 비디오를 골라서 올릴 수 있는 uploading 버튼과 ai detecion을 적용하는 버튼, 그리고 적용시킨 동영상을 play 시키는 버튼으로 구상을 하였고, 첫번째 비디오를 골라서 올릴 수 있는 uploading 버튼은 file_picker 패키지를 활용하여 클라이언트 컴퓨터 폴더에서 원하는 비디오를 고를 수 있게해주는 패키지를 활용하였고, 비디오를 골라서 버튼을 누르면 http post를 통하여 flask 서버에 동영상을 보내고 try catch를 활용하여 예외처리를 진행하여 디버깅을 체킹하였고, if 문으로 response의 값으로 성공 , 실패를 확인 하도록 진행하였다. 그리고 flask에 도착하면 해당 비디오를 yolo ai model에 바로 적용시키는 process_video() 함수를 만들어서 프레임마다 ai를 입혀서 새로운 비디오를 flask 서버 폴더에 저장하도록 하였다.(원래는 firebase를 활용하여 넘어온 데이터들을 DB에 저장하여 꺼내쓰도록 할려했으나, WINDOWS APP 은 지원을 안해서 DB 없이 클라이언튼 저장공간과, 서버 저장공간을 활용하여 진행하였다. 일반적인 데이터였으면 local storage를 활용하면 됐으나 video 타입을 활용하다 보니, 저장공간을 활용.)그래서 flask 서버 폴더에 저장된 detection 데이터를 flutter에서 2번째 버튼인 ai detction을 누르면 http get 를 활용하여 데이터를 가져오게되고, 클라이언트 고정 앱 폴더 path를 활용하여, 해당 경로로 저장되고,3번째 play 버튼을 누르면 똑같이 file_picker 패키지를 활용하여 비디오를 선택하게되고, 선택한 비디오를 video_player 패키지를 활용하여 실행시킬려고했으나, windows app에서 원래는 video_player가 지원이 안됐는데, pub get 문서를 찾아 보니 video_player_win 이라는 패키지가 video_player와 같이 사용하게되면 windows app에서도 비디오 플레이가 가능하다고 하여 패키지를 활용하여 비디오 플레이를 성공적으로 구현하였다.

# 2023-12-13
정원진 : flask 서버에서 video 영상과 디택션된 점보를 넘겨주고 받을때 flutter 리스트뷰에서 디택션 되지도 않았는데 time 만 넘어오는 현상이 발견되어 왜 그러나 확인해봤더니 flask 에서 1 frame당 class_id 와 time 을 넘겨받아 딕셔너리에 담아서 json 파일로 변환하여 넘겨주는 방식을 활용했었는데 , 기존에 확인했던 test 데이터 들이 다 사람이 처음부터 나오는 상황이라 계속 디택션되는 구조라서 디택션이 되지않았을때의 경우를 확인하지 못해서 해당 로직이 빠져있는 상황이였다. 따라서 if 문을 활용하여 딕셔너리가 비어있지 않다면 json 파일을 넘겨주는 방식으로 로직을 짰더니 문제 사항을 해결할 수 있었고, UI부분을 수정했는데, 가시성이 떨어진다는 평을 받았어서 아이콘만 넣는게 아니라 아이콘 밑에 Text를 넣어서 가시성을 높이고, flutter container의 위젯 배치를 통하여 조금 더 통일성 있게 디자인 하였다.
추가로 ? 라는 아이콘을 넣어서 해당 버튼을 눌렀을때 사용자가 어떻게 사용해야되는지에 대한 간단한 안내문을 팝업형식으로 만들었다.



Git Information
---
전반적으로 원래 VSCODE과 같은 에디터를 활용하여 git을 활용했었는데 이러면 다른 에디터를 사용할때마다 공부를 해야될꺼같아서 가장 베이직하게 git bash에서 활용하는 방법을 간략하게 정리해두겠다. 내가 다시 봤을때 이해하기 쉽게 정리한다.
[참조 : https://wordbe.tistory.com/entry/Git-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95-%EC%A0%95%EB%A6%ACcommit-push-pull-request-merge-%EB%93%B1 ]

**Git 의 대략적인 구조**

**Working Directory(Local)** : 로컬 저장소

**Staging** : add를 통해서 수정된 코드를 임시적으로 올려놓는 영역 

**Repository** : 원격 저장소 (git commit을 통해서 수정본을 올려주는 느낌 )

**Git 용어정리**

**pull ->** 원격 저장소에서 로컬 저장소로 데이터를 최신화 하는것. ( 가져오는 느낌 )

**push ->** 로컬 저장소에서 원격 저장소로 데이터를 최신화 하는것. ( 밀어내는 느낌 )

**add ->** 바뀐 내역을 추가하는 것. 즉 commit을 진행하기전에 바뀐 내역들을 리스트로 보여주고 이게 맞으면 commit해 라는 느낌 ( 임시 저장된 상태 )

**commit ->** 로컬 저장소에 이게이게 바꼈으니깐 업데이트를 하라고 알려주것. ( 로컬 저장소 업데이트 느낌 )

**branch ->** 말그대로 가지라는 느낌인데 기존 branch 를 master 라고 생각한다 즉 나무의 기둥이라고 생각하고, 그 주위에 branch(가지)를 달면서 코드를 추가해 나가는 방식을 말한다.

**pull request ->**코드 수정을 했으니깐 master 에게 코드를 master branch에 올려도 되는지 검수 해달라는 행위라고 생각하면 편하다.

**merge ->** master가 pull request을 보고 master branch에 올려도 된다고 생각하면 합병시키는 행위.


