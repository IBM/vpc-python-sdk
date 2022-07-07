Please follow below steps to release a new Go Python on public repository.

Create a branch name release-YYYY-MM-DD with the date as API version date, from the below repository:
https://github.com/IBM/vpc-python-sdk

Update the generated code from the API spec https://pages.github.ibm.com/riaas/api-spec/spec_genesis_production_redirect. Verify the generator version and core-sdk compatibility and update the go.mod file accordingly. Compatibility Chart - https://github.ibm.com/CloudEngineering/openapi-sdkgen/wiki/Compatibility-Chart

Must verify the integration test and examples has been added for the new feature going in the api version.

Update the README.md file with next release version. Commit the code (Semantic versionoing is diabled as of now)

  --------------------------------------------------------------------   -------------------------------------
| Commit message	                                                   | Release type
  --------------------------------------------------------------------   -------------------------------------
| fix(pencil): stop graphite breaking when too much pressure applied   | Patch Fix Release
  --------------------------------------------------------------------   -------------------------------------
| feat(pencil): add 'graphiteWidth' option	                           | Minor Feature Release
  --------------------------------------------------------------------   -------------------------------------
| perf(pencil): remove graphiteWidth option                            | Major Breaking Release
| BREAKING CHANGE: The graphiteWidth option has been removed.          | (Note that the {{BREAKING CHANGE: }}token 
| The default graphite width of 10mm is always                         | must be in the footer of the commit)
| used for performance reasons.                                        |
|                                                                      |
  ---------------------------------------------------------------------  ----------------------------------------                                    
                                      

push the branch and cretae a PR https://github.com/IBM/vpc-python-sdk to master branch

Post the new PR link to slack channel #vpc-client-sdk-terraform-internal

Once the PR will approved and merge, semantic release bot will be triggered and a new release will be created.

Verifiy the release from the releases page. And add release notes in the following order
  a. Breaking changes
  b. new features
  c. changes
  d. bug fixes