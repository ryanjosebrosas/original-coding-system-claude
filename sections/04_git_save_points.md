Before implementation, ALWAYS commit the structured plan:
```
git add requests/{feature}-plan.md
git commit -m "plan: {feature} structured plan"
```

If implementation goes wrong:
```
git stash  # or git checkout .
```
Then tweak the plan and retry.
