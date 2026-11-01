# Portfolio Architecture & Maintenance Guide

This guide explains how your GitHub Profile README and companion interactive portfolio website are structured, how to publish them, and how to maintain them in the future.

---

## 1. How the GitHub Profile README Works

GitHub has a feature called **Profile Readme**:
* When you have a **public** repository matching your exact username (`Barun-Chhetri/Barun-Chhetri`), GitHub renders its `README.md` at the very top of your public profile page: `https://github.com/Barun-Chhetri`.
* Your assets (SVG graphics, diagrams) live inside the `./assets` directory in that repository and render via GitHub's CDN (`githubusercontent.com`).

---

## 2. Directory Structure in Workspace

```text
/Users/barunchhetri/profile-portfolio-workspace/
├── README.md                      # The production GitHub Profile README
├── preview.html                   # Rendered HTML preview with GitHub Dark styling
├── assets/
│   ├── hero-banner.svg            # Custom SVG header banner with glowing terminal
│   ├── project-resume-analyzer.svg # Architectural pipeline card for Resume Analyzer
│   ├── project-interview-tracker.svg # Architectural dashboard card for Interview Prep Tracker
│   └── github-metrics-dashboard.svg # Standalone offline-safe GitHub & LeetCode analytics card
├── portfolio-web/                 # Full companion Next.js 14 interactive website
│   ├── app/
│   ├── components/
│   ├── package.json
│   └── README.md
└── MAINTENANCE.md                 # This maintenance guide
```

---

## 3. How to Publish to GitHub (Upon Your Approval)

To push the profile portfolio to your GitHub account:

```bash
# 1. Create the special public repository matching your username
gh repo create Barun-Chhetri/Barun-Chhetri --public --description "Barun Chhetri - Special GitHub Profile Repository"

# 2. Initialize git in the workspace and link origin
cd /Users/barunchhetri/profile-portfolio-workspace
git init
git branch -M main
git remote add origin https://github.com/Barun-Chhetri/Barun-Chhetri.git

# 3. Commit only the profile files and assets
git add README.md assets/
git commit -m "feat: initial release of interactive developer portfolio"
git push -u origin main
```

*(Note: The companion `portfolio-web/` directory can either remain local or be pushed to a separate repository like `Barun-Chhetri/developer-portfolio` for deployment to Vercel/Netlify/Dockyard).*

---

## 4. How to Update Specific Content

### Adding Your Official Resume PDF Link
In `README.md`, find the line:
```markdown
<a href="#-resume">
  <img src="https://img.shields.io/badge/Resume-4F46E5?style=for-the-badge&logo=googledocs&logoColor=white" alt="Resume" />
</a>
```
Replace `#-resume` with a direct link to your PDF (e.g., hosted on Google Drive, GitHub releases, or your personal domain: `https://barunchamlagain.me/resume.pdf`).

### Adding Future Projects
To add a new project card, follow the template used in `README.md`:
```markdown
#### 3. New Project Title
> **Brief description of the problem solved and core value.**

* **Live Platform:** [your-domain.com](https://...)
* **Repository:** [Barun-Chhetri/repo-name](https://github.com/Barun-Chhetri/repo-name)
* **Core Technologies:** ...
* **Key Architecture & Features:**
  * Bullet 1
  * Bullet 2
```

### Refreshing LeetCode or GitHub Stats
* The LeetCode card (`leetcard.jacoblin.cool`) and GitHub streak card (`streak-stats.demolab.com`) are dynamic and automatically update as you solve problems and make commits.
* The static KPI card (`assets/github-metrics-dashboard.svg`) is completely self-hosted inside `./assets`, ensuring zero downtime even if third-party APIs have hiccups. You can update numbers directly inside the SVG text elements whenever you hit milestones.
