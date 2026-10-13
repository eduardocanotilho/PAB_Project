# PAB_Project
Advanced Programming for Biology Project

### GitHub Workflow ###

# Create a new branch
" " doesnt count
git checkout -b "nome do branch"

# Check whats changed
git status
git diff

# Add new files and modifications (stage)
git add "file name" "file name 2" "file name 3"
git add . - adds everything

# Add comment to what was done
git commit -m "Comentario para saber o que foi alterado"

# Sync with main before pushing
git fetch origin
git merge origin/main

# Push the branch (what you did) to the main (cloud)
git push -u origin "name of branch"

# Open a Pull Request

# Review, then merge

# Clean up
git checkout main
git pull origin main
git branch -d "name of branch"
