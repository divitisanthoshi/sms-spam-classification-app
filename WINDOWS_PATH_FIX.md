# Fixing Windows PATH Length Limitation Issue for Heroku CLI Installation

## Background

Windows has a default maximum PATH environment variable length of 2048 characters on some versions, which can cause issues when installing tools like Heroku CLI if the PATH becomes too long.

## Steps to Fix or Work Around

### 1. Enable Long Path Support (Windows 10/11)

- Press `Win + R`, type `gpedit.msc`, and press Enter to open the Local Group Policy Editor.
- Navigate to: `Computer Configuration > Administrative Templates > System > Filesystem`
- Find the policy named **"Enable Win32 long paths"**.
- Double-click it and set it to **Enabled**.
- Click OK and restart your computer.

### 2. Manually Edit PATH to Shorten It

- Open System Properties:
  - Press `Win + R`, type `sysdm.cpl`, and press Enter.
- Go to the **Advanced** tab and click **Environment Variables**.
- Under **System variables**, find and select **Path**, then click **Edit**.
- Review the entries and remove any unnecessary or duplicate paths.
- Click OK to save.

### 3. Use the New Windows Terminal or PowerShell

- Sometimes older terminals have issues with long PATHs.
- Use the latest Windows Terminal or PowerShell to run Heroku CLI commands.

### 4. Reinstall Heroku CLI

- Uninstall any existing Heroku CLI.
- Download the latest installer from https://devcenter.heroku.com/articles/heroku-cli
- Install again after applying the above fixes.

### 5. Alternative: Use Heroku CLI via Windows Subsystem for Linux (WSL)

- If issues persist, consider installing WSL and running Heroku CLI inside the Linux environment.
- Install WSL: https://docs.microsoft.com/en-us/windows/wsl/install
- Install Heroku CLI inside WSL using Linux instructions.

## Additional Resources

- https://devcenter.heroku.com/articles/heroku-cli#windows
- https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation

---

Following these steps should resolve the PATH length issue and allow successful Heroku CLI installation and usage.
