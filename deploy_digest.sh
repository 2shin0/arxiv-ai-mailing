#!/bin/bash
# deploy_digest.sh

BRANCH=arxiv-digest
DATE=$(date +%Y-%m-%d)
FILENAME="$DATE.md"
DIGEST_DIR="./digest"
LLM_DIGEST_DIR="$DIGEST_DIR/LLM"
ALL_DIGEST_DIR="$DIGEST_DIR/ALL"

# 현재 브랜치 이름 저장
CUR_BRANCH=$(git branch --show-current)

# 결과물이 있어야 할 디렉토리 확인
mkdir -p $LLM_DIGEST_DIR
mkdir -p $ALL_DIGEST_DIR

# 예: Python 코드로 digest markdown 생성
# python generate_digest.py 

# 브랜치 전환
git checkout $BRANCH

# 최신화
git pull origin $BRANCH

# 폴더 생성 및 파일 복사
mkdir -p LLM
mkdir -p ALL
cp "$LLM_DIGEST_DIR/$FILENAME" "./LLM/"
cp "$ALL_DIGEST_DIR/$FILENAME" "./ALL/"

# 커밋 & 푸시
git add LLM/"$FILENAME" ALL/"$FILENAME"
git commit -m "Add digest for $DATE"
git push origin $BRANCH

# 원래 브랜치로 돌아가기
git checkout $CUR_BRANCH
