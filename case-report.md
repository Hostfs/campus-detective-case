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

### 용의자별 상세 분석 및 알리바이 검증

#### 1) minho (민호) - 파일 실종 사건의 직접적인 행위자
- **명백한 물리적 증거**:
  - `evidence/file-events.log:24` (08:56:01): `FILE_EVENT target=project/final_report.md user=minho action=cleanup result=removed`
  - `evidence/access.log:30` (08:56:01): `POST /file/action 200 user=minho target=final_report.md result=removed`
  - 위 두 로그가 동일한 시각(08:56:01)에 민호가 직접 파일 정리(cleanup) 액션을 실행해 최종 보고서 파일을 날렸음을 완벽하게 증명함.
- **실수 정황**:
  - 파일 삭제 직전인 08:55:50에 파일 이름을 변경하려다 실패한 기록(`RENAME project/final-report.md ... status=failed`)이 존재함.
  - 마감 직전 긴박한 상황에서 파일 이름을 예쁘게 정리하려다 조작 실수를 범했음을 자백한 채팅 기록(`08:59 minho: 미안, 정리하다가 잘못 눌렀을 수도 있어.`)과 완벽히 일치함.

#### 2) sora (소라) - 무죄 (피해자 및 최초 발견자)
- **파일의 최초 생성자**:
  - `evidence/file-events.log:14` (08:51:02)에 `UPLOAD project/final_report.md user=sora`를 수행한 장본인임. 본인이 직접 완성해서 업로드한 파일을 고의로 삭제할 동기가 전혀 없음.
- **사건 시점의 알리바이**:
  - 사건이 발생한 08:56:01 직전(08:55:03)까지 해당 파일을 열어두고 확인하고 있었으며, 삭제 직후(08:56:18) 바로 파일이 사라진 것(`status=missing`)을 발견하고 팀원들에게 경고함 (`08:56 sora: 잠깐, final_report가 안 보여.`).

#### 3) jimin (지민) - 무죄 (다른 작업 수행 및 알리바이 성립)
- **전혀 다른 파일 작업 중**:
  - 사건 전후로 지민이의 모든 활동은 초안인 `draft_report.md` 수정에만 쏠려 있음 (`08:41:01` OPEN, `08:43:03` SAVE, `08:47:18` SAVE, `08:49:07` SAVE, `08:54:06` OPEN, `08:54:39` SAVE 등).
- **최종 보고서 수정 권한 및 접근 흔적 없음**:
  - 사건 발생 시각인 08:56:01 전후로 최종 보고서에 어떤 삭제나 수정 액션을 취한 기록이 전무함. 08:57:02에 소라의 말을 듣고 뒤늦게 최종 보고서를 열어보려다 에러 페이지(`status=missing` / 404)를 확인하고 당황해함 (`08:57 jimin: 나도 404가 떠.`).


## 7. Git 저장 결과

조사를 모두 마무리하고 보고서를 커밋하였음. 브랜치와 커밋 결과임.

브랜치:
```text
gyseongpark
```

첫 커밋:
```text
[gyseongpark 45318a2] Complete case report
```

사용한 명령어:
```bash
git status
git switch -c gyseongpark
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

결과:
```text
      3 user=admin
     23 user=jimin
     18 user=minho
     20 user=sora
      4 user=system
```

라인 수 확인:
```bash
wc -l evidence/*.log
```

결과:
```text
      38 evidence/access.log
      20 evidence/chat.log
      32 evidence/file-events.log
      90 total
```

### final_report 사건 흐름

명령어:
```bash
grep -En "UPLOAD|RESTORE|removed|missing" evidence/*.log
```

결과:
```text
evidence/access.log:11:2026-05-20 08:45:31 INFO POST /upload 201 user=sora file=screen-main.png
evidence/access.log:19:2026-05-20 08:50:07 INFO POST /upload 201 user=sora file=team-photo.png
evidence/access.log:21:2026-05-20 08:51:02 INFO POST /upload 201 user=sora file=final_report.md
evidence/access.log:30:2026-05-20 08:56:01 INFO POST /file/action 200 user=minho target=final_report.md result=removed
evidence/file-events.log:6:2026-05-20 08:44:12 UPLOAD project/assets/screen-main.png user=sora
evidence/file-events.log:12:2026-05-20 08:50:07 UPLOAD project/assets/team-photo.png user=sora
evidence/file-events.log:14:2026-05-20 08:51:02 UPLOAD project/final_report.md user=sora
evidence/file-events.log:24:2026-05-20 08:56:01 FILE_EVENT target=project/final_report.md user=minho action=cleanup result=removed
evidence/file-events.log:25:2026-05-20 08:56:18 CHECK project/final_report.md user=sora status=missing
evidence/file-events.log:26:2026-05-20 08:57:02 CHECK project/final_report.md user=jimin status=missing
evidence/file-events.log:28:2026-05-20 08:58:03 CHECK submit/status user=sora status=missing_final_report
evidence/file-events.log:29:2026-05-20 08:58:20 RESTORE project/final_report.md user=admin source=backup
```

끝!
