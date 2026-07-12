# Function to check and return the available Python command
function Get-PythonCommand {
    $commands = @('python3', 'python')
    foreach ($cmd in $commands) {
        $commandInfo = Get-Command $cmd -ErrorAction SilentlyContinue
        if ($null -eq $commandInfo) {
            continue
        }

        $version = & $commandInfo.Source --version 2>&1
        if ($version -match "Python 3\.") {
            return $commandInfo.Source
        }
    }

    Write-Host "Python 3 is not installed or not available on PATH."
    exit 1
}


# Check if npm is available
$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if ($null -ne $npmCmd) {
    $NPM_CMD = "npm"
} else {
    Write-Host "Node is not installed."
    Exit 1
}

# Install dependencies and build the project
cd ".\frontend\palworld-pal-editor-webui"
& $NPM_CMD install
& $NPM_CMD run build

cd "..\..\"
# Move the build directory
if (Test-Path ".\src\palworld_pal_editor\webui") {
    Remove-Item ".\src\palworld_pal_editor\webui" -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -Path ".\src\palworld_pal_editor\webui" -ItemType "directory" -Force | Out-Null
Move-Item -Path ".\frontend\palworld-pal-editor-webui\dist\*" -Destination ".\src\palworld_pal_editor\webui" -Force


# Determine the appropriate Python command
$PYTHON_CMD = Get-PythonCommand

# Check Python version
$versionOutput = & $PYTHON_CMD --version 2>&1
$versionText = ($versionOutput | Out-String).Trim()
$versionNumbers = $versionText -replace "Python ", "" -split "\."
$majorVersion = [int]$versionNumbers[0]
$minorVersion = [int]$versionNumbers[1]

# Ensure Python version is at least 3.10
if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 10)) {
    Write-Host "Python version 3.10 or newer is required."
    exit 1
}

Write-Host "Using $($PYTHON_CMD) (version $($majorVersion).$($minorVersion))"

& $PYTHON_CMD -m venv venv
. .\venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -m pip install -e .
python -m palworld_pal_editor $args
