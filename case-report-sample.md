# 사건 조사 보고서

## 1. 현재 위치

명령어:

```bash
pwd
```

결과:

```text
/Users/student/campus-detective-case
```

## 2. 사건 자료 목록

명령어:

```bash
ls -al
ls case
ls evidence
ls project
```

결과:

```text
case
docs
evidence
project
case-report.md
check_report.py

briefing.md
suspects.md
timeline.md

access.log
chat.log
file-events.log

draft_report.md
final_report.md
src
```

## 3. 사건 개요

캠퍼스 해커톤 마감 직전 `project/final_report.md`가 사라진 사건이다.
사건 자료는 `case`, `evidence`, `project` 폴더에 나뉘어 있고,
로그에서 `final_report`의 업로드, 삭제 또는 누락, 복구 흐름을 확인해야 한다.

## 4. 로그 증거

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
evidence/file-events.log:24:2026-05-20 08:56:01 FILE_EVENT target=project/final_report.md user=minho action=cleanup result=removed
evidence/file-events.log:25:2026-05-20 08:56:18 CHECK project/final_report.md user=sora status=missing
evidence/file-events.log:26:2026-05-20 08:57:02 CHECK project/final_report.md user=jimin status=missing
evidence/file-events.log:29:2026-05-20 08:58:20 RESTORE project/final_report.md user=admin source=backup
```

## 5. 용의자별 단서

명령어:

```bash
grep -rn "jimin" .
grep -rn "sora" .
grep -rn "minho" .
grep -rn "final_report" . | grep "minho"
grep -rni "removed" . | grep "minho"
```

검색 결과:

```text
evidence/chat.log:14:2026-05-20 08:55 minho: 제출 전에 파일 이름 정리할게.
evidence/chat.log:18:2026-05-20 08:59 minho: 미안, 정리하다가 잘못 눌렀을 수도 있어.
evidence/access.log:30:2026-05-20 08:56:01 INFO POST /file/action 200 user=minho target=final_report.md result=removed
evidence/file-events.log:24:2026-05-20 08:56:01 FILE_EVENT target=project/final_report.md user=minho action=cleanup result=removed
```

## 6. 결론

가장 중요한 증거:

`evidence/file-events.log:24`에서 `minho`가 `project/final_report.md`에 대해
`action=cleanup result=removed`를 만든 기록이 있다.

가장 의심되는 상황:

`minho`가 제출 전 파일 이름을 정리하던 중 `final_report.md`를 잘못 정리해서 사라진 것으로 보인다.
고의로 지웠다는 증거보다는 실수로 정리하다가 제거한 정황이 더 강하다.

아직 확실하지 않은 점:

실제 화면에서 어떤 버튼을 눌렀는지는 로그만으로는 알 수 없다.
하지만 `removed`, `missing`, `RESTORE` 흐름은 사라짐과 복구가 있었음을 보여준다.

## 7. Git 저장 결과

브랜치:

```text
investigation/report
```

커밋:

```text
abc1234 Complete case report
```

사용한 명령어:

```bash
git diff case-report.md
git status
git add case-report.md
git commit -m "Complete case report"
git log --oneline -3
```

## 8. 오늘 사용한 명령어

- `pwd`
- `ls -al`
- `cat`
- `grep -n`
- `grep -r`
- `code case-report.md`
- `git diff`
- `git status`
- `git add`
- `git commit`

## Appendix. 추가 분석

### 사용자별 활동량

```text
   3 user=admin
  23 user=jimin
  18 user=minho
  20 user=sora
   4 user=system
```

### final_report 사건 흐름

명령어:

```bash
find . -type f | sort
wc -l evidence/*.log
grep -rho "user=[a-z]*" evidence/*.log | sort | uniq -c
grep -En "UPLOAD|RESTORE|removed|missing" evidence/*.log
```
