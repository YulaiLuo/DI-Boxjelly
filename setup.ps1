# Check if Docker is installed
if (-Not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Output "Docker is not installed. Please install it and run this script again."
    Exit
}

# Check if Docker Compose is installed
if (-Not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Output "Docker Compose is not installed. Please install it and run this script again."
    Exit
}

# Check if Yarn is installed
if (-Not (Get-Command yarn -ErrorAction SilentlyContinue)) {
    Write-Output "Yarn is not installed. Please install it and run this script again."
    Exit
}

# Navigate to the di-web directory
if(Test-Path -Path .\src\di-web) {
    Set-Location -Path .\src\di-web
} else {
    Write-Output "di-web directory not found"
    Exit
}

# Run the yarn commands
yarn install
yarn build

# Check if the build directory exists
if(-Not (Test-Path -Path .\build)) {
    Write-Output "Build directory does not exist. Please check if the build command succeeded."
    Exit
}

# Create the necessary directories
$directories = @(
    "~\data\nginx\conf",
    "~\data\nginx\html",
    "~\data\nginx\ssl",
    "~\data\nginx\logs",
    "~\data\di-data\di-auth\avatars"
)
foreach($directory in $directories) {
    if(-Not (Test-Path -Path $directory)) {
        New-Item -ItemType directory -Path $directory
    }
}

# Copy nginx configuration file in the di-web directory to the desired location
Copy-Item -Path .\nginx.conf -Destination ~\data\nginx\conf\ -ErrorAction Stop -Force

# Copy all files in the build directory to the desired location
Copy-Item -Path .\build\* -Destination ~\data\nginx\html\ -ErrorAction Stop -Force

# Navigate back to the root directory
Set-Location -Path ..\..

# Copy the default avatar
Copy-Item -Path .\src\di-auth\default.jpg -Destination ~\data\di-data\di-auth\avatars\ -ErrorAction Stop -Force

# Run the Docker Compose command
docker-compose up -d
