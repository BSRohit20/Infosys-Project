# Install Render CLI for Windows
Write-Host "🚀 Installing Render CLI for Windows..." -ForegroundColor Cyan

# Create temp directory
$tempDir = New-Item -ItemType Directory -Path "$env:TEMP\render-cli" -Force
Write-Host "📁 Created temp directory: $tempDir" -ForegroundColor Gray

try {
    # Download Render CLI
    Write-Host "⬇️ Downloading Render CLI..." -ForegroundColor Yellow
    $downloadUrl = "https://github.com/render-oss/cli/releases/latest/download/cli_windows_amd64.zip"
    $zipFile = Join-Path $tempDir "render-cli.zip"
    
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile
    Write-Host "✓ Downloaded successfully" -ForegroundColor Green
    
    # Extract CLI
    Write-Host "📦 Extracting CLI..." -ForegroundColor Yellow
    Expand-Archive $zipFile -DestinationPath $tempDir -Force
    
    # Find the CLI executable
    $cliExecutable = Get-ChildItem -Path $tempDir -Recurse -Name "*.exe" | Select-Object -First 1
    if ($cliExecutable) {
        $sourcePath = Join-Path $tempDir $cliExecutable
        $destinationPath = Join-Path $PWD "render.exe"
        
        # Copy to current directory
        Copy-Item $sourcePath $destinationPath
        Write-Host "✓ Render CLI installed to: $destinationPath" -ForegroundColor Green
        
        # Test installation
        Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
        & $destinationPath --version
        
        Write-Host ""
        Write-Host "🎉 Render CLI successfully installed!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Run: .\render.exe login" -ForegroundColor White
        Write-Host "2. Run: .\render.exe services" -ForegroundColor White
        Write-Host "3. Select your service to deploy" -ForegroundColor White
        
    } else {
        Write-Host "❌ Could not find CLI executable in download" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Error installing Render CLI: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    # Cleanup
    Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "🧹 Cleaned up temp files" -ForegroundColor Gray
}
