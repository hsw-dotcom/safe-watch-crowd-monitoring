# 과거 원본 코드 보존 안내

`main` 브랜치에는 현재 기준 코드만 놓았습니다. 삭제한 코드가 사라진 것은 아닙니다. 정리 직전 모든 원본 및 재구성본은 GitHub의 **`archive/pre-dedup-20261031` 브랜치**로 보존하며, Git 이력에서도 같은 내용을 추적할 수 있습니다.

- 2023년 실제 보존 Python/HTML/PHP: 보관 브랜치의 `src/python/`, `src/web/`, `database/schema_legacy_percent.sql`
- 이전 재구성 ZIP 기반 코드: 보관 브랜치의 `reconstructed/`
- 현재 단일 기준: `main`의 `src/python/`, `src/web/`, `database/schema.sql`

## 정리 이유
기존 저장소는 **역사적 원본**과 **대화 기반 재구성본**을 같은 저장소 루트에 병렬로 보관하여, 어느 파일이 최신인지 혼동될 수 있었습니다. 기능별 실행 파일을 하나만 남기고 원본은 참조용 브랜치로 분리했습니다.
