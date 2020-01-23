# Definition-Of-Done (DOD):
For most User Stories for development tasks, to a large extent, the *DOD* can be standardized.

'paste' these as is in GitLab (or any other where markdown is allowed)
```
- [ ] Code builds with 0 errors and 0 warnings
- [ ] Sufficient automated tests are written for each aspect of requirement
- [ ] Code checked-in to a distinctly named branch
- [ ] Automated Unit test cases are added, and passed
- [ ] Code linter is run and passed
- [ ] Static Code Analyzer is run and its values are within limits
- [ ] (if any) Automation is added and made reusable
- [ ] (if any) peculiar observations are noted in JIRA/GitHub/Confluence
- [ ] (wherever necessary) User-Documentation is updated
- [ ] Basic validation is documented and added to input controllers
- [ ] Standardized logging is added (with timestamp, with log-levels and optimum amount of)
- [ ] Generated logs are verified and attached to Ticket
- [ ] For UI, is responsive on all agreed platforms
- [ ] For backend, is tested for all agreed platforms and environments
```

Certain steps could be verified/automated with every check-in:
- linting
- automatic document generation (e.g. Doxygen)
- static-code-analyzer
- check-in comments
- code coverage


-------


# User story (US):

## Following template could be used:
* For a given < role >
* Under certain < situation >
* An < action > is taken
* with an < expectation > of certain < result >


-------


# Acceptance Criteria (AC)

## Characteristics of AC
- is specific for every task
- should be written very thoughtfully
- should be clearly stated (no gray)
- include functional as well as non-functional criteria

## Possible format:
- have < when > this then < that > should take place

## Guidelines
- Possibly for a US, AC could express < situation > more clearly
- When certain action is taken, then express < result > more clearly
- When certain action is NOT taken, then express < result > clearly
