
# Workflow

![workflow](../images/workflow.jpg)

## Branches
The project follows a specific branching model to maintain a clean and organized repository:

1. `main` or `master`: The main branch represents the stable, production-ready version of the application. **Direct commits to this branch are not allowed.**
2. `develop`: The develop branch is used for make develop commits. It used to integrate features and bugfixes before they are merged into the main branch. It is checked out from main branch, and **it will not be merged into any other branch.**
3. `test`: The test branch is used by the tester to do testing which is checked out from the `develop` branch by the end of a sprint. After the testing is done, the tester give the feedback wheather it pass the tests, then the team decide to create a release branch. **Note that `test` branch will not be merged into other branch.**
4. `feature/<feature name>`: Feature branches are created for each new feature or enhancement. They should be named `feature/login` for login feature. It is checked out from the `develop` branch.
5. `fix/<bug name>`: Bug branches are created for fixing bugs and issues. It is followed by the bug name or issue id, for example: `fix/issue202`. They should based on the `develope` branch, and sometimes it is checked out from main branch for emergency hotfix.
6. `release/<version number>`: Release branches are created for preparing new releases which follow by version number, such as `release/v1.0.0`. They are checked out from the `develop` branch. After the release is complete, developer make a pull request to the QA which will be merged into `main` branch with tag, and then be deleted.

## Naming Conventions
1. Branch names: Use lowercase letters and separate words with hyphens (e.g., feature/new-feature).
2. Commit messages: Write concise and descriptive commit messages, starting with a capital letter and using the imperative mood (e.g., 'Add new feature' or 'Fix bug in feature').
3. Style guid: 
    - Python: [Google python style guide](https://google.github.io/styleguide/pyguide.html)
    - Javascript: [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html
)

## Pull Requests and Code Review
When a feature or bugfix is complete, submit a pull request to the develop branch.
Request a code review from a team member.
Address any comments or requested changes.
After approval, merge the pull request into the develop branch and delete the feature or bugfix branch.
