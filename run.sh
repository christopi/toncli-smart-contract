git filter-branch -f --env-filter 'if [ "$GIT_AUTHOR_NAME" = "mercedesbenz00" ]; then
     GIT_AUTHOR_EMAIL=webstar119@gmail.com;
     GIT_AUTHOR_NAME="trueices";
     GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL;
     GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"; fi' --tag-name-filter cat -- --all
