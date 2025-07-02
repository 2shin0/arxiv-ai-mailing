#!/bin/bash
# deploy_digest.sh

BRANCH=arxiv-digest
DATE=$(date +%Y-%m-%d)
FILENAME="$DATE.md"
DIGEST_DIR="./digest"

# 현재 브랜치 이름 저장
CUR_BRANCH=$(git branch --show-current)

# 결과물이 있어야 할 디렉토리 확인
mkdir -p $DIGEST_DIR

# 예: Python 코드로 digest markdown 생성
# python generate_digest.py → ./digest/2025-07-02.md

# 브랜치 전환
git checkout $BRANCH

# 최신화
git pull origin $BRANCH

# 파일 복사
cp "$DIGEST_DIR/$FILENAME" ./

# 커밋 & 푸시
git add "$FILENAME"
git commit -m "Add digest for $DATE"
git push origin $BRANCH

# 원래 브랜치로 돌아가기
git checkout $CUR_BRANCH
