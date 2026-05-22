# 사건 조사 보고서

## 1. 현재 위치

pwd 명령어로 일단 내 현재 위치부터 확인했음.

명령어:
```bash
pwd
```

결과:
```text
C:\Users\root\Desktop\새 폴더 (9)\campus-detective-case
```

## 2. 사건 자료 목록

사건 분석을 위해 폴더들 ls로 돌려서 자료 목록을 확인했음. case, evidence, project 폴더를 다 체크했음.

명령어:
```bash
ls -al
ls case
ls evidence
ls project
```

결과:
```text
case/
  briefing.md
  suspects.md
  timeline.md

evidence/
  access.log
  chat.log
  file-events.log

project/
  draft_report.md
  final_report.md
  src/
```

## 3. 사건 개요

캠퍼스 해커톤 마감을 고작 10분 앞두고 `project/final_report.md` 파일이 제출 폴더에서 흔적도 없이 사라지는 당황스러운 상황이 발생함.
이 파일이 왜 증발했는지 주범이랑 원인을 밝혀내기 위해 로그 파일과 채팅방 내역을 싹 다 긁어서 조사하기 시작했음.

## 4. 로그 증거

final_report 파일에 무슨 일이 일어났었는지 removed랑 missing 등의 흔적 위주로 로그를 뒤져서 증거를 확보함.

명령어:
```bash
grep -n "final_report" evidence/*.log
grep -ni "removed" evidence/*.log
grep -ni "missing" evidence/*.log
```

발견한 줄:
```text
evidence/access.log:30:2026-05-20 08:56:01 INFO POST /file/action 200 user=minho target=final_report.md result=removed
evidence/file-events.log:14:2026-05-20 08:51:02 UPLOAD project/final_report.md user=sora
evidence/file-events.log:23:2026-05-20 08:55:50 RENAME project/final-report.md project/final_report.md user=minho status=failed
evidence/file-events.log:24:2026-05-20 08:56:01 FILE_EVENT target=project/final_report.md user=minho action=cleanup result=removed
evidence/file-events.log:25:2026-05-20 08:56:18 CHECK project/final_report.md user=sora status=missing
evidence/file-events.log:26:2026-05-20 08:57:02 CHECK project/final_report.md user=jimin status=missing
evidence/file-events.log:29:2026-05-20 08:58:20 RESTORE project/final_report.md user=admin source=backup
```

## 5. 용의자별 단서

채팅 기록이랑 로그를 종합적으로 뒤져보니까 minho의 행적이 가장 유력한 단서로 지목되어 관련 기록을 모았음.

명령어:
```bash
grep -rn "minho" .
```

검색 결과:
- `evidence/chat.log:14:2026-05-20 08:55 minho: 제출 전에 파일 이름 정리할게.`
- `evidence/chat.log:18:2026-05-20 08:59 minho: 미안, 정리하다가 잘못 눌렀을 수도 있어.`
- `evidence/file-events.log:23:2026-05-20 08:55:50 RENAME project/final-report.md project/final_report.md user=minho status=failed`
- `evidence/file-events.log:24:2026-05-20 08:56:01 FILE_EVENT target=project/final_report.md user=minho action=cleanup result=removed`

## 6. 결론

**가장 중요한 증거**:
`evidence/file-events.log:24`랑 `evidence/access.log:30`을 보면, `minho`가 `project/final_report.md` 파일에 대해 `cleanup` 액션을 취해서 결국 파일이 `removed` 되었음이 명확하게 기록되어 있음.

**가장 의심**되는 상황:
`minho`가 마감 직전에 의욕이 앞서서 파일 이름을 깔끔하게 **정리**하려고 파일명을 바꾸려다 실패했고, 이어진 정리 과정에서 실수로 파일을 지워버린 것으로 보임.
본인도 채팅방에서 정리하다가 잘못 눌렀을 수도 있다고 시인한 것을 보아, 악의적인 행동이라기보단 마감 직전 긴박한 상황에서 발생한 단순 실수가 유력함. 다행히 이후 어드민이 백업본으로 RESTORE 해주었음.

## 7. Git 저장 결과

조사를 모두 마무리하고 보고서를 커밋하였음. 브랜치와 커밋 결과임.

브랜치:
```text
main
```

测 커밋:
```text
[main 0993f28] Complete case report
```

사용한 명령어:
```bash
git status
git add case-report.md
git commit -m "Complete case report"
git log --oneline -3
```

## 8. 오늘 사용한 명령어

오늘 주요 분석에 쓴 명령어 목록임.
- `pwd`
- `ls`
- `cat`
- `grep`
- `git`

## Appendix. 추가 분석

로그 기반으로 사용자 활동 내역을 조금 더 분석해 둔 자료임.

### 사용자별 활동량
file-events.log에서 각 사용자별 활동 기록 빈도를 uniq -c와 sort로 추출함.

명령어:
```bash
grep -rho "user=[a-z]*" evidence/*.log | sort | uniq -c
```

라인 수 확인:
```bash
wc -l evidence/*.log
```

끝!
