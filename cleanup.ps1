# Script to clean up deployment and unnecessary files
Write-Host "🧹 Cleaning up unnecessary files for local development..." -ForegroundColor Cyan

# Files to remove
$filesToRemove = @(
    ".env.example",
    ".env.production",
    ".gitattributes",
    ".render-buildpacks.json",
    ".vercelignore",
    "analytics_dashboard_fix.md",
    "AUTHENTICATION_DIAGNOSIS.md",
    "AUTHENTICATION_FIXED_FINAL.md",
    "DEPLOYMENT.md",
    "Dockerfile",
    "FEEDBACK_ALERTS_IMPLEMENTATION_COMPLETE.md",
    "LOGIN_FIX_COMPLETE.md",
    "Procfile",
    "RAILWAY_DEPLOYMENT.md",
    "Spacefile",
    "TEMPLATES_FIXED_COMPLETE.md",
    "TROUBLESHOOTING.md",
    "TROUBLESHOOTING_GUIDE.md",
    "cloudbuild.yaml",
    "deploy.bat",
    "deploy.sh",
    "fly.toml",
    "netlify.toml",
    "oracle_cloud_setup.sh",
    "pythonanywhere_wsgi.py",
    "railway.json",
    "render.yaml",
    "runtime.txt",
    "vercel.json",
    "vercel_app.py",
    "vercel_requirements.txt"
)

# Remove files
foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Removed: $file" -ForegroundColor Green
    }
}

# Remove directories if they exist
$dirsToRemove = @(
    ".github"
)

foreach ($dir in $dirsToRemove) {
    if (Test-Path $dir -PathType Container) {
        Remove-Item $dir -Recurse -Force
        Write-Host "  ✓ Removed directory: $dir" -ForegroundColor Green
    }
}

Write-Host "`n✅ Cleanup complete! Your project now only contains files needed for local development." -ForegroundColor Green
Write-Host "`nTo run your application locally, use:" -ForegroundColor Yellow
Write-Host "  - Windows CMD: start_server.bat" -ForegroundColor Yellow
Write-Host "  - PowerShell: ./start_server.ps1" -ForegroundColor Yellow
