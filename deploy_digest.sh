#!/bin/bash
# deploy_digest.sh

set -e # 오류 발생 시 즉시 스크립트 중단
set -x # 스크립트 실행 중에 모든 명령어 출력

# --- 기본 변수 설정 ---
BRANCH=arxiv-digest
MAIN_BRANCH=main
DATE=$(date +%Y-%m-%d)
FILENAME="$DATE.md"
DIGEST_DIR="./digest"
LLM_DIGEST_DIR="$DIGEST_DIR/LLM"
ALL_DIGEST_DIR="$DIGEST_DIR/ALL"

# --- Git 사용자 정보 설정 (스크립트 내에서 명시적 지정) ---
# 중요: 아래 이메일을 실제 GitHub 이메일로 수정해주세요!
git config user.name "2shin0"
git config user.email "02.shin.00@gmail.com" 

# 현재 브랜치 이름 저장
CUR_BRANCH=$(git branch --show-current)

# 로컬 변경사항이 있는 경우 임시 저장 (stash)
STASHED=false
if ! git diff-index --quiet HEAD --; then
    echo "로컬 변경사항을 임시 저장합니다..."
    git stash
    STASHED=true
fi

# === arxiv-digest 브랜치에 배포 ===
echo "'$BRANCH' 브랜치로 전환합니다..."
git checkout $BRANCH
echo "원격 저장소의 최신 변경사항을 가져옵니다..."
git pull origin $BRANCH

# 다이제스트 파일 복사
echo "다이제스트 파일을 복사합니다..."
mkdir -p LLM
mkdir -p ALL

# 파일이 존재할 때만 복사하도록 수정
if [ -f "$LLM_DIGEST_DIR/$FILENAME" ]; then
    cp "$LLM_DIGEST_DIR/$FILENAME" "./LLM/"
else
    echo "경고: LLM 다이제스트 파일($LLM_DIGEST_DIR/$FILENAME)이 없습니다."
fi
if [ -f "$ALL_DIGEST_DIR/$FILENAME" ]; then
    cp "$ALL_DIGEST_DIR/$FILENAME" "./ALL/"
else
    echo "경고: 전체 다이제스트 파일($ALL_DIGEST_DIR/$FILENAME)이 없습니다."
fi

# 커밋 & 푸시
echo "변경사항을 커밋하고 푸시합니다..."
git add LLM/"$FILENAME" ALL/"$FILENAME"

if ! git diff-index --quiet --cached HEAD --; then
    git commit -m "Add digest for $DATE"
    git push origin $BRANCH
else
    echo "커밋할 새로운 다이제스트 파일이 없습니다."
fi

# === main 브랜치에도 배포 (GitHub Pages용) ===
echo "'$MAIN_BRANCH' 브랜치로 전환합니다..."
git checkout $MAIN_BRANCH
echo "원격 저장소의 최신 변경사항을 가져옵니다..."
git pull origin $MAIN_BRANCH

# LLM, ALL 폴더 전체를 main 브랜치에 복사
echo "GitHub Pages용으로 LLM, ALL 폴더를 복사합니다..."
git checkout $BRANCH -- LLM/ ALL/

# main 브랜치에 커밋 & 푸시
echo "main 브랜치에 변경사항을 커밋하고 푸시합니다..."
git add LLM/ ALL/

if ! git diff-index --quiet --cached HEAD --; then
    git commit -m "Update digest folders for GitHub Pages ($DATE)"
    git push origin $MAIN_BRANCH
else
    echo "main 브랜치에 커밋할 변경사항이 없습니다."
fi

# 원래 브랜치로 돌아가기
echo "원래 브랜치('$CUR_BRANCH')로 돌아갑니다..."
git checkout $CUR_BRANCH

# 임시 저장했던 변경사항 복원
if [ "$STASHED" = true ]; then
    echo "임시 저장했던 변경사항을 복원합니다..."
    git stash pop
fi

echo "배포 스크립트가 성공적으로 완료되었습니다."
exit 0