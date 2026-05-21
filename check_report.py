#!/usr/bin/env python3
"""Check whether case-report.md contains the required investigation notes."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    description: str
    required: bool
    passed: bool
    hint: str


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def git_has_commit(root: Path) -> bool:
    try:
        top_level = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        if top_level.returncode != 0:
            return False
        if Path(top_level.stdout.strip()).resolve() != root.resolve():
            return False

        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0


def run_checks(report_path: Path, strict_git: bool) -> list[Check]:
    text = report_path.read_text(encoding="utf-8")
    root = report_path.parent

    checks = [
        Check(
            "보고서 파일",
            "`case-report.md` 파일이 있다.",
            True,
            report_path.is_file(),
            "`case-report.md` 파일을 만들었는지 확인한다.",
        ),
        Check(
            "기본 섹션",
            "현재 위치, 자료 목록, 사건 개요, 로그 증거, 용의자 단서, 결론 섹션이 있다.",
            True,
            all(
                keyword in text
                for keyword in ["현재 위치", "사건 자료", "사건 개요", "로그 증거", "용의자", "결론"]
            ),
            "보고서 템플릿의 주요 제목을 지우지 않았는지 확인한다.",
        ),
        Check(
            "시작 위치",
            "`pwd` 실행 결과나 현재 폴더 확인 내용이 있다.",
            True,
            has_any(text, [r"\bpwd\b", r"campus-detective-case", r"현재 위치"]),
            "`pwd` 결과를 보고서에 남긴다.",
        ),
        Check(
            "자료 목록",
            "`case`, `evidence`, `project` 폴더 확인 내용이 있다.",
            True,
            all(keyword in text for keyword in ["case", "evidence", "project"]),
            "`ls -al`, `ls case`, `ls evidence`, `ls project` 결과를 남긴다.",
        ),
        Check(
            "사건 대상",
            "`final_report` 관련 내용이 있다.",
            True,
            has_any(text, [r"final_report", r"final-report"]),
            "`final_report`를 검색한 결과를 보고서에 남긴다.",
        ),
        Check(
            "로그 상태",
            "`removed`와 `missing` 기록이 모두 있다.",
            True,
            has_any(text, [r"removed"]) and has_any(text, [r"missing"]),
            "`grep -ni \"removed\" evidence/*.log`, `grep -ni \"missing\" evidence/*.log` 결과를 남긴다.",
        ),
        Check(
            "줄 번호 근거",
            "로그 파일명과 줄 번호가 함께 들어 있다.",
            True,
            has_any(text, [r"evidence/[a-z-]+\.log:\d+", r"[a-z-]+\.log:\d+"]),
            "`grep -n` 결과처럼 `파일명:줄번호:` 형태의 근거를 남긴다.",
        ),
        Check(
            "인물 단서",
            "`minho` 관련 단서가 있다.",
            True,
            has_any(text, [r"minho"]),
            "`grep -rn \"minho\" .` 또는 조합 검색 결과를 남긴다.",
        ),
        Check(
            "결론 문장",
            "가장 의심되는 상황이나 핵심 증거를 자기 문장으로 정리했다.",
            True,
            has_any(text, [r"가장 중요한 증거", r"가장 의심", r"결론"])
            and has_any(text, [r"minho", r"removed", r"cleanup", r"정리"]),
            "편집기로 결론 섹션에 핵심 증거와 판단을 직접 적는다.",
        ),
        Check(
            "명령어 기록",
            "오늘 사용한 명령어가 여러 개 들어 있다.",
            True,
            sum(1 for cmd in ["pwd", "ls", "cat", "grep", "git"] if has_any(text, [rf"\b{cmd}\b"])) >= 4,
            "`history | tail` 또는 직접 정리한 명령어 목록을 남긴다.",
        ),
        Check(
            "Git 저장 결과",
            "보고서 안에 Git 저장 결과가 있다.",
            True,
            has_any(text, [r"git", r"commit", r"branch", r"커밋", r"브랜치"]),
            "`git diff`, `git status`, `git log --oneline` 결과를 보고서에 적는다.",
        ),
        Check(
            "Appendix 보너스",
            "추가 분석 결과가 있다.",
            False,
            has_any(text, [r"Appendix", r"사용자별 활동량", r"uniq -c", r"grep -E", r"wc -l"]),
            "시간이 남으면 Appendix 미션을 진행하고 추가 분석을 남긴다.",
        ),
    ]
    if strict_git:
        checks.append(
            Check(
                "실제 Git 커밋",
                "현재 저장소에 커밋 기록이 있다.",
                True,
                git_has_commit(root),
                "`git add case-report.md` 후 `git commit -m \"Complete case report\"`를 실행한다.",
            )
        )
    return checks


def print_result(checks: list[Check]) -> int:
    required = [check for check in checks if check.required]
    passed_required = [check for check in required if check.passed]
    bonus = [check for check in checks if not check.required and check.passed]

    print("# case-report.md 자동 점검 결과")
    print()
    print(f"필수 항목: {len(passed_required)}/{len(required)}")
    print(f"보너스 항목: {len(bonus)}/{len(checks) - len(required)}")
    print()

    for check in checks:
        mark = "PASS" if check.passed else "MISS"
        label = "필수" if check.required else "보너스"
        print(f"[{mark}] ({label}) {check.name}: {check.description}")
        if not check.passed:
            print(f"       힌트: {check.hint}")

    print()
    if len(passed_required) == len(required):
        print("결과: 통과")
        return 0

    print("결과: 보완 필요")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="case-report.md 필수 내용 점검")
    parser.add_argument(
        "report",
        nargs="?",
        default="case-report.md",
        type=Path,
        help="점검할 보고서 파일 경로",
    )
    parser.add_argument(
        "--strict-git",
        action="store_true",
        help="실제 Git 커밋 존재 여부도 필수 항목으로 검사",
    )
    args = parser.parse_args(argv)

    report_path = args.report.resolve()
    if not report_path.is_file():
        print(f"보고서 파일을 찾을 수 없습니다: {report_path}", file=sys.stderr)
        return 2

    return print_result(run_checks(report_path, args.strict_git))


if __name__ == "__main__":
    raise SystemExit(main())
