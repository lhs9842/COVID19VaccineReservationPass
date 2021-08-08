import json, requests, webbrowser, warnings
from urllib import parse
warnings.filterwarnings("ignore")
print("===COVID-19 예방접종 사전예약 시스템===")
print("안내에 따라 20시 이전에 NetFunnel Key를 준비해주세요. 준비되지 않은 상태에서 잘못 실행할 경우 예약이 불가능함은 물론 10분 간 동일 명의로 정상적인 접속에서도 접속이 불가합니다.")
head = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
name = input("접종자 성명 : ")
name = parse.quote(name)
birthday = input("접종자 생년월일(yyyymmdd 형태로 작성해주세요) : ")
ntv = int(input("접종자 내외국민 구분을 입력해주세요.\n1. 내국인 2. 외국인\n선택 : "))
ntvFrnrCd = ''
if ntv == 1:
    ntvFrnrCd = 'L'
elif ntv == 2:
    ntvFrnrCd = 'F'
sex = int(input("성별을 선택해주세요.\n1. 남자, 2. 여자\n선택 : "))
sexCd = ''
if sex == 1:
    sexCd = 'M'
elif sex == 2:
    sexCd = 'F'
print("이동통신사를 선택해주세요. \n1. SKT 2. KT 3. LG U+ 4. 알뜰폰(SK망) 5. 알뜰폰(KT망) 6. 알뜰폰(U+망)")
telecom = int(input("선택 : "))
telComCd = "0" + str(telecom)
telNo = input("본인인증할 휴대전화번호를 입력해주세요. : ")
data = "svcGb=P&name=" + name + "&birthday=" + birthday + "&sexCd=" + sexCd + "&ntvFrnrCd=" + ntvFrnrCd + "&telComCd=" + telComCd + "&telNo=" + telNo + "&agree1=Y&agree2=Y&agree3=Y&agree4=Y"
if telecom > 4:
    data = data + "&agree5=Y"
res = requests.post("https://ncvr2.kdca.go.kr/svc/kcb/callKcb", data=data, headers=head, verify = False)
res.request
se = res.json()
if se['rsltCd'] != "B000":
    print("본인인증 실패")
    print("실패 내용" + se['rsltMsg'])
    exit()
txSeqNo = se['txSeqNo']
print("입력하신 휴대전화번호로 인증번호가 발송되었습니다.")
otpNo = input("받으신 인증번호 6자리를 입력해주세요 : ")
data = "svcGb=R&txSeqNo=" + txSeqNo + "&telNo=" + telNo + "&otpNo=" + otpNo
res = requests.post("https://ncvr2.kdca.go.kr/svc/kcb/callKcb", data=data, headers=head, verify = False)
res.request
se = res.json()
if se['rsltCd'] == "CONFLICT":
    print("중복 접속 차단")
    print("동일인은 한번 접속된 후 10분 이후에 접속이 가능합니다.")
    exit()
if se['rsltCd'] != "B000":
    print("본인인증 실패")
    print("실패 내용" + se['rsltMsg'])
    exit()
reqId = se['reqId']
print("본인인증이 완료되었습니다.")
print("별도로 안내해드린 방법으로 준비해둔 NetFunnel Key가 필요합니다.")
nfKey = input("NetFunnel Key : ")
webbrowser.open("https://ncvr2.kdca.go.kr/svc/complete?reqId=" + reqId + "&nfKey=" + nfKey)
