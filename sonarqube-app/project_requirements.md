Tasks
Task 1: Setup SonarQube Server (15 points)
1. Start SonarQube using Docker:
docker run -d --name sonarqube \
-p 9000:9000 \
-v sonarqube_data:/opt/sonarqube/data \
sonarqube:2026.1-community
2. Access SonarQube at http://localhost:9000:
• Login with default credentials (admin/admin)
• Change the admin password
3. Create a new project manually:
• Set project key and display name
• Generate an authentication token
• Document the token securely
4. Screenshot the SonarQube dashboard after setup
Task 2: Configure Project Analysis (20 points)
1. Create sonar-project.properties in your repository:
sonar.projectKey=your-project-key
sonar.projectName=Your Project Name
sonar.sources=src
sonar.tests=tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
2. Generate test coverage report:
pytest --cov=src --cov-report=xml
3. Run local SonarQube analysis:
docker run --rm \
-e SONAR_HOST_URL="http://host.docker.internal:9000" \
-e SONAR_TOKEN="your-token" \
-v "$(pwd):/usr/src" \
sonarsource/sonar-scanner-cli
4. Review the analysis results in SonarQube dashboard
2
Task 3: Integrate with GitHub Actions (25 points)
1. Create a SonarQube workflow (.github/workflows/sonarqube.yml):
• Trigger on push to main and pull requests
• Run tests with coverage first
• Execute SonarQube scan
• Wait for quality gate result
2. Configure secrets in GitHub repository:
• SONAR_TOKEN: Authentication token
• SONAR_HOST_URL: SonarQube server URL
3. Implement quality gate check:
- name: SonarQube Quality Gate
uses: SonarSource/sonarqube-quality-gate-action@v1
timeout-minutes: 5
env:
SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
4. Configure the workflow to fail if quality gate fails
Task 4: Analyze and Fix Code Issues (25 points)
1. Identify issues reported by SonarQube:
• Bugs
• Vulnerabilities
• Code Smells
• Security Hotspots
2. Create a code sample with intentional issues:
# Example: Code with issues to fix
def process_data(data):
# Bug: Possible NoneType error
result = data.split(",")
# Security: Hardcoded credentials
password = "admin123"
# Code Smell: Bare except
try:
risky_operation()
except:
pass
3. Fix at least 5 issues identified by SonarQube
4. Document the fixes with before/after comparison: | Issue Type | Before | After | Severity | |———
–|——–|——-|———-| | Bug | … | … | … |
5. Re-run analysis and verify issues are resolved
Task 5: Configure Quality Gate (15 points)
1. Review the default “Sonar Way” quality gate
2. Create a custom quality gate with conditions:
3
• New bugs = 0
• New vulnerabilities = 0
• New code coverage >= 80%
• New duplicated lines <= 3%
3. Apply the quality gate to your project
4. Test the quality gate by:
• Submitting code that passes
• Submitting code that fails (intentionally)
5. Screenshot both passing and failing quality gate results
Submission Requirements
Required Deliverables
□ Source code with sonar-project.properties
□ .github/workflows/sonarqube.yml
□ Screenshots of SonarQube dashboard
□ Screenshots of quality gate results (pass and fail)
□ Documentation of fixed issues (before/after)
□ README.md with setup instructions
Submission Checklist
□ SonarQube server running locally
□ Project analyzed successfully
□ GitHub Actions workflow working
□ Quality gate configured and enforced
□ At least 5 code issues fixed
□ SonarLint connected to SonarQube (bonus)
Evaluation Criteria
Criteria Points
SonarQube server setup 15
Project configuration 20
CI/CD integration 25
Code issue analysis and fixes 25
Quality gate configuration 15
Total 100
Bonus: SonarLint IDE integration +10
Hints
[TIP] - Use docker logs sonarqube to troubleshoot startup issues - SonarQube takes
1-2 minutes to fully start up - For public repositories, consider using SonarCloud (free
tier) - Focus on new code metrics to avoid being overwhelmed by legacy issues - Use
4
sonar.qualitygate.wait=true to block pipeline on failure - Install SonarLint in your IDE for
real-time feedback while coding