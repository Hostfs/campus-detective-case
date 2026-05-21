# Campus Detective Case

Git Bash 기본 명령어 실습을 위한 가벼운 사건 조사 샘플입니다.

캠퍼스 해커톤 마감 직전 `project/final_report.md`가 사라졌습니다.

목표는 로그와 사건 자료를 조사해서 `case-report.md`를 완성하고 Git 커밋을 만드는 것입니다.

확인할 것:

- `case/briefing.md`의 사건 개요
- `case/suspects.md`의 용의자 목록
- `evidence/*.log`의 UPLOAD, RESTORE, missing, removed 기록
- `project/` 폴더의 제출 파일 상태
- 편집기로 정리한 조사 보고서

## 보고서 자동 점검

보고서 작성이 끝나면 아래 명령으로 필수 정보가 들어갔는지 확인합니다.

```bash
python3 check_report.py
```

실제 Git 커밋까지 필수로 검사하려면 아래처럼 실행합니다.

```bash
python3 check_report.py --strict-git
```

점검 기준:

- `case-report.md` 파일 존재
- 주요 보고서 섹션 존재
- `pwd`, `ls`, `grep`, `git` 등 명령 결과 기록
- `final_report`, `removed`, `missing` 관련 로그 근거
- `파일명:줄번호` 형태의 줄 번호 근거
- `minho` 관련 단서와 결론 문장
- Git 저장 결과
- Appendix 추가 분석은 보너스 항목
