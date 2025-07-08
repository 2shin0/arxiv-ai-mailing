#!/bin/bash
# deploy_digest.sh

# .env 로딩
set -o allexport
source .env
set +o allexport

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

# 변경사항 자동 커밋
git add .
git commit -m "Auto-commit before switching to $BRANCH" || echo "No changes to commit"

# 브랜치 전환
git checkout $BRANCH
git pull origin $BRANCH

# 파일 복사
mkdir -p LLM
mkdir -p ALL
cp "$LLM_DIGEST_DIR/$FILENAME" "./LLM/"
cp "$ALL_DIGEST_DIR/$FILENAME" "./ALL/"

# 커밋 & 푸시
git add LLM/"$FILENAME" ALL/"$FILENAME"
git commit -m "Add digest for $DATE"
git push "https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/arxiv-ai-mailing.git" $BRANCH

# 원래 브랜치로 돌아가기
git checkout $CUR_BRANCH
