# Git Branch Recovery Steps

This document outlines the step-by-step process used to recover the deleted local Git branch named `update`.

---

## Step 1: Search the Git Reflog
The reflog keeps track of every time the tip of any branch is updated in the local repository (e.g., checkouts, commits, merges, rebases). Even if a branch is deleted, the commits it pointed to remain in the reflog for a period of time.

To search for references to `update`, the following command was run:
```powershell
git reflog | Select-String "update"
```

### Key Reflog Entries Found:
```text
334e369 HEAD@{25}: checkout: moving from update to suraj
ff45a0d HEAD@{26}: commit: new update
ee88e0a HEAD@{27}: checkout: moving from suraj to update
```
- Entry `HEAD@{25}` shows a checkout moving from `update` to `suraj` when the HEAD was at commit `334e369`.
- Entry `HEAD@{26}` shows that the last commit made on the `update` branch before checking out of it was `ff45a0d` (with the commit message `new update`).

---

## Step 2: Verify the Identified Commit
Before recreating the branch, the details of the identified commit `ff45a0d` were inspected to ensure it was the correct head of the branch:
```powershell
git log ff45a0d -n 3
```

### Commit Details:
```text
commit ff45a0d47f9a2bcd67607ca3ccbccbaa69405561
Author: Accolade-Qa <suraj.bhalerao@accoladeelctronics.com>
Date:   Wed Jun 17 18:14:25 2026 +0530

    new update
```
This confirmed that `ff45a0d47f9a2bcd67607ca3ccbccbaa69405561` was indeed the correct commit.

---

## Step 3: Recreate the Branch
With the target commit hash identified, the `update` branch was recreated at that commit using:
```powershell
git branch update ff45a0d47f9a2bcd67607ca3ccbccbaa69405561
```

---

## Step 4: Verify Restoration
Finally, local branch listings and the commit logs were checked to ensure the branch was successfully restored:
```powershell
# List local branches
git branch

# Verify the log history of the restored branch
git log update -n 3
```
Both commands confirmed that the branch `update` was successfully recreated and pointed to the correct history.
