# How to Push to GitHub

Since this is a local repository, you need to connect it to your GitHub account to share it.

## Step 1: Create a New Repository on GitHub
1.  Log in to [GitHub.com](https://github.com).
2.  Click the **+** icon in the top right and select **New repository**.
3.  Name the repository: `dlp-portfolio` (or similar).
4.  **Do not** initialize with a README, .gitignore, or License (we already have files).
5.  Click **Create repository**.

## Step 2: Link Your Local Repo
Open your terminal (or use the command line in VS Code) and run the following commands. Replace `YOUR_USERNAME` with your actual GitHub username.

```bash
# 1. Add the remote origin
git remote add origin https://github.com/YOUR_USERNAME/dlp-portfolio.git

# 2. Rename the branch to main (standard practice)
git branch -M main

# 3. Push your files
git push -u origin main
```

## Step 3: Verify
Refresh your GitHub page. You should see all your folders (`docs`, `playbooks`, `scripts`) and the `README.md` displayed beautifully.

## Optional: GitHub Pages
If you want to host this as a website:
1.  Go to repository **Settings**.
2.  Click **Pages** on the left sidebar.
3.  Under "Branch", select `main` and click **Save**.
